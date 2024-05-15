import os
import sys
import json

from src.scheduler.fifo_scheduler import FIFOScheduler

from src.scheduler.rr_scheduler import RRScheduler

from src.utils.utils import (
    parse_global_args,
)

from openagi.src.agents.agent_factory import AgentFactory

from openagi.src.agents.agent_process import AgentProcessFactory

import warnings

from src.llm_kernel import llms

from concurrent.futures import ThreadPoolExecutor, as_completed

from multiprocessing import Process

from src.utils.utils import delete_directories
from dotenv import find_dotenv, load_dotenv

def clean_cache(root_directory):
    targets = {'.ipynb_checkpoints', '__pycache__', ".pytest_cache", "context_restoration"}
    delete_directories(root_directory, targets)

def main():
    warnings.filterwarnings("ignore")
    parser = parse_global_args()
    args = parser.parse_args()

    llm_name = args.llm_name
    max_gpu_memory = args.max_gpu_memory
    eval_device = args.eval_device
    max_new_tokens = args.max_new_tokens
    scheduler_log_mode = args.scheduler_log_mode
    agent_log_mode = args.agent_log_mode
    llm_kernel_log_mode = args.llm_kernel_log_mode
    load_dotenv()

    llm = llms.LLMKernel(
        llm_name = llm_name,
        max_gpu_memory = max_gpu_memory,
        eval_device = eval_device,
        max_new_tokens = max_new_tokens,
        log_mode = llm_kernel_log_mode
    )

    scheduler = RRScheduler(
        llm = llm,
        log_mode = scheduler_log_mode
    )

    agent_process_factory = AgentProcessFactory()

    agent_factory = AgentFactory(
        llm = llm,
        agent_process_queue = scheduler.agent_process_queue,
        agent_process_factory = agent_process_factory,
        agent_log_mode = agent_log_mode
    )

    agent_thread_pool = ThreadPoolExecutor(max_workers=64)

    scheduler.start()

    # construct agents
    math_agent = agent_thread_pool.submit(
        agent_factory.run_agent,
        "MathAgent",
        "A freelance graphic designer in Canada earns CAD 500 per project and is planning to work on projects from clients in both the UK and Canada this month. With an expected 3 projects from Canadian clients and 2 from UK clients (paying GBP 400 each), how much will the designer earn in total in CAD by the end of the month"
    )

    narrative_agent = agent_thread_pool.submit(
        agent_factory.run_agent,
        "NarrativeAgent",
        "Craft a tale about a valiant warrior on a quest to uncover priceless treasures hidden within a mystical island."
    )

    rec_agent = agent_thread_pool.submit(
        agent_factory.run_agent,
        "RecAgent", "I want to take a tour to New York during the spring break, recommend some restaurants around for me."
    )

    travel_agent = agent_thread_pool.submit(
        agent_factory.run_agent,
        "TravelAgent", "I want to take a trip to Paris, France from July 4th to July 10th 2024 and I am traveling from New York City. Help me plan this trip."
    )

    agent_tasks = [math_agent, narrative_agent, rec_agent, travel_agent]

    for r in as_completed(agent_tasks):
        res = r.result()

    scheduler.stop()

    clean_cache(root_directory="./")

if __name__ == "__main__":
    main()
