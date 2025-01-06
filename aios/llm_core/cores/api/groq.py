import re
from openai import OpenAI

import openai

import re
import time
import json

from hexel.llm_core.cores.base import BaseLLM

from hexel.utils import get_from_env

from cerebrum.llm.communication import Response

import os

from hexel.config.config_manager import config


class GroqLLM(BaseLLM):
    def __init__(
        self,
        llm_name: str,
        max_gpu_memory: dict = None,
        eval_device: str = None,
        max_new_tokens: int = 1024,
        log_mode: str = "console",
        use_context_manager: bool = False,
        api_key: str = None,
    ):
        # Get API key from config or environment variable
        api_key = api_key or config.get_api_key('groq') or os.getenv("GROQ_API_KEY")
        
        super().__init__(
            llm_name,
            max_gpu_memory,
            eval_device,
            max_new_tokens,
            log_mode,
            use_context_manager,
            api_key
        )

    def load_llm_and_tokenizer(self) -> None:
        if not self.api_key:
            raise ValueError("Groq API key not found in config or parameters")
        self.model = OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
        self.tokenizer = None

    def parse_tool_calls(self, tool_calls):
        if tool_calls:
            parsed_tool_calls = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                parsed_tool_calls.append(
                    {"name": function_name, "parameters": function_args}
                )
            return parsed_tool_calls
        return None

    def address_syscall(self, llm_syscall, temperature=0.0):
        # ensures the model is the current one

        # assert re.search(r'gpt', self.model_name, re.IGNORECASE)

        """wrapper around openai api"""
        llm_syscall.set_status("executing")
        llm_syscall.set_start_time(time.time())
        messages = llm_syscall.query.messages
        # print(messages)
        self.logger.log(
            f"{llm_syscall.agent_name} is switched to executing.\n", level="executing"
        )
        # time.sleep(2)
        try:
            response = self.model.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=llm_syscall.query.tools,
                # tool_choice = "required" if agent_request.query.tools else None,
                max_tokens=self.max_new_tokens,
            )
            response_message = response.choices[0].message.content
            tool_calls = self.parse_tool_calls(response.choices[0].message.tool_calls)

            response = Response(
                response_message=response_message, tool_calls=tool_calls
            )

        except openai.APIConnectionError as e:
            response = Response(
                response_message=f"Server connection error: {e.__cause__}"
            )

        except openai.RateLimitError as e:
            response = Response(
                response_message=f"OpenAI RATE LIMIT error {e.status_code}: (e.response)"
            )

        except openai.APIStatusError as e:
            response = Response(
                response_message=f"OpenAI STATUS error {e.status_code}: (e.response)"
            )

        except openai.BadRequestError as e:
            response = Response(
                response_message=f"OpenAI BAD REQUEST error {e.status_code}: (e.response)"
            )

        except Exception as e:
            response = Response(response_message=f"An unexpected error occurred: {e}")

        return response
