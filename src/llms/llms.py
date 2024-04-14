import torch

import sys

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

model_class = {
    "causal_lm": AutoModelForCausalLM,
}

from openai import OpenAI

from src.utils.utils import get_from_env

import os

import json

import re

import time

class LLMKernel:
    def __init__(self, llm_name: str, max_gpu_memory: dict = None, eval_device: str = None, max_new_tokens: int = 256):
        print("Initialize AIOS powered by LLM: {}".format(llm_name))
        self.config = self.load_config(llm_name)
        self.max_gpu_memory = max_gpu_memory
        self.eval_device = eval_device

        self.load_llm_and_tokenizer()
        self.MAX_NEW_TOKENS = max_new_tokens
        print("AIOS LLM successfully loaded. ")

    def convert_map(self, map: dict) -> dict:
        new_map = {}
        for k,v in map.items():
            new_map[int(k)] = v
        return new_map

    def load_config(self, llm_name):
        # print(os.getcwd())
        config_file = os.path.join(os.getcwd(), "src", "llms", "llm_config/{}.json".format(llm_name))
        with open(config_file, "r") as f:
            config = json.load(f)
            return config

    def load_llm_and_tokenizer(self): # load model from config
        open_sourced = self.config["open_sourced"]
        self.model_type = self.config["model_type"]
        self.model_name = self.config["model_name"]

        if open_sourced:
            self.max_gpu_memory = self.convert_map(self.max_gpu_memory)
            hf_token = self.config["hf_token"] if "hf_token" in self.config.keys() else None
            cache_dir = self.config["cache_dir"] if "cache_dir" in self.config.keys() else None
            self.model = model_class[self.model_type].from_pretrained(
                self.model_name,
                use_auth_token = hf_token,
                cache_dir = cache_dir,
                torch_dtype=torch.float16,
                # load_in_8bit = True,
                device_map="auto",
                max_memory = self.max_gpu_memory
            )
            # self.model = self.model.to(self.eval_device)
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                use_auth_token = hf_token,
                cache_dir = cache_dir
            )
            # print(f"EOS token id: {self.model.config.eos_token_id}")
            self.tokenizer.pad_token_id = self.model.config.eos_token_id

            # print(self.tokenizer.pad_token_id)

        else:
            if re.search(r'gpt', self.model_name, re.IGNORECASE):
                self.model = OpenAI()
                self.tokenizer = None
            if self.model_name == "gemini-pro":
                try:
                    import google.generativeai as genai
                    gemini_api_key = get_from_env("GEMINI_API_KEY")
                    genai.configure(api_key=gemini_api_key)
                    self.model = genai.GenerativeModel(self.model_name)
                    self.tokenizer = None
                except ImportError:
                    raise ImportError(
                        "Could not import google.generativeai python package. "
                        "Please install it with `pip install google-generativeai`."
                    )
            elif self.model_name.startswith("bedrock"):
                try:
                    from langchain_community.chat_models import BedrockChat
                    model_id = self.model_name.split("/")[-1]
                    self.model = BedrockChat(
                        model_id=model_id,
                        model_kwargs={
                            'temperature': 0.0
                        }
                    )
                except ModuleNotFoundError as err:
                    raise err
                except ImportError:
                    raise ImportError(
                        "Could not import langchain_community python package. "
                        "Please install it with `pip install langchain_community`."
                    )
            else:
                return NotImplementedError

    def address_request(self, prompt, temperature=0.0):
        # The pattern looks for 'gpt', 'claude', or 'gemini', ignoring case (re.IGNORECASE)
        closed_model_pattern = r'gpt|claude|gemini'

        if re.search(closed_model_pattern, self.model_name, re.IGNORECASE):
            return self.closed_llm_process(prompt, temperature=temperature)
        else:
            return self.open_llm_process(prompt, temperature=temperature)

    def closed_llm_process(self, prompt, temperature=0.0):
        if re.search(r'gemini', self.model_name, re.IGNORECASE):
            outputs = self.gemini_process(prompt, temperature=temperature)
            return outputs
        elif re.search(r'gpt', self.model_name, re.IGNORECASE):
            return self.gpt_process(prompt, temperature=temperature)
        elif self.model_name.startswith("bedrock") and \
             re.search(r'claude', self.model_name, re.IGNORECASE):
            return self.bedrock_process(prompt, temperature=temperature)
        else:
            return NotImplementedError

    def gemini_process(self, prompt, temperature=0.0):
        outputs = self.model.generate_content(
            prompt
        )
        # print(outputs)
        try:
            return outputs.candidates[0].content.parts[0].text
        except IndexError:
            return f"{self.model_name} can not generate a valid result, please try again"

    def gpt_process(self, prompt, temperature=0.0):
        response = self.model.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        time.sleep(2) # set according to your request per minite
        return response.choices[0].message.content

    def bedrock_process(self, prompt, temperature=0.0):
        from langchain_core.prompts import ChatPromptTemplate
        chat_template = ChatPromptTemplate.from_messages([
            ("user", "{prompt}")
        ])
        messages = chat_template.format_messages(prompt=prompt)
        self.model.model_kwargs['temperature'] = temperature
        response = self.model(messages)
        return response.content

    def open_llm_process(self, prompt, temperature=0.0):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = input_ids != self.tokenizer.pad_token_id
        input_ids = input_ids.to(self.eval_device)
        output_ids = self.model.generate(
            input_ids = input_ids,
            attention_mask = attention_mask,
            max_new_tokens = self.MAX_NEW_TOKENS,
            num_return_sequences=1,
            temperature = temperature
        )
        outputs = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        # print(outputs)
        outputs = outputs[len(prompt)+1: ]
        return outputs

if __name__ == "__main__":
    llm_type = "gemini-pro"
    llm = LLMKernel(llm_type)
    prompt = "Craft a tale about a valiant warrior on a quest to uncover priceless treasures hidden within a mystical island."
    llm.address_request(prompt)
