# This is a main script that tests the functionality of specific agents.
# It requires no user input.

from hexel.utils.utils import (
    parse_global_args,
)
import os
import warnings

from hexel.hooks.llm import useFactory, useKernel, useFIFOScheduler

from hexel.utils.utils import delete_directories
from dotenv import load_dotenv


def clean_cache(root_directory):
    targets = {
        ".ipynb_checkpoints",
        "__pycache__",
        ".pytest_cache",
        "context_restoration",
    }
    delete_directories(root_directory, targets)


def main():
    # parse arguments and set configuration for this run accordingly
    main_id = os.getpid()
    print(f"Main ID is: {main_id}")
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
    use_backend = args.use_backend
    load_dotenv()

    llm = useKernel(
        llm_name=llm_name,
        max_gpu_memory=max_gpu_memory,
        eval_device=eval_device,
        max_new_tokens=max_new_tokens,
        log_mode=llm_kernel_log_mode,
        use_backend=use_backend
    )

    # run agents concurrently for maximum efficiency using a scheduler

    startScheduler, stopScheduler = useFIFOScheduler(
        llm=llm,
        log_mode=scheduler_log_mode,
        get_queue_message=None
    )

    submitAgent, awaitAgentExecution = useFactory(
        log_mode=agent_log_mode,
        max_workers=64
    )

    startScheduler()

    # register your agents and submit agent tasks
    """ submitAgent(
        agent_name="example/academic_agent",
        task_input="Find recent papers on the impact of social media on mental health in adolescents."
    )
    """

    """
    submitAgent(
        agent_name="om-raheja/transcribe_agent",
        task_input="listen to my yap for 5 seconds and write a response to it"
    )
    """
    
    """
    submitAgent(
        agent_name="example/cocktail_mixlogist",
        task_input="Create a cocktail for a summer garden party. Guests enjoy refreshing, citrusy flavors. Available ingredients include vodka, gin, lime, lemon, mint, and various fruit juices."
    )
    """
    
    """
    submitAgent(
        agent_name="example/cook_therapist",
        task_input="Develop a low-carb, keto-friendly dinner that is flavorful and satisfying."
    )
    """
    
    agent_tasks = [
        ["example/academic_agent", "Tell me what is the prollm paper mainly about"]
        # ["example/cocktail_mixlogist", "Create a cocktail for a summer garden party. Guests enjoy refreshing, citrusy flavors. Available ingredients include vodka, gin, lime, lemon, mint, and various fruit juices."]
    ]
    
    agent_ids = []
    for agent_name, task_input in agent_tasks:
        agent_id = submitAgent(
            agent_name=agent_name,
            task_input=task_input
        )
        agent_ids.append(agent_id)
    
    for agent_id in agent_ids:
        awaitAgentExecution(agent_id)

    stopScheduler()

    clean_cache(root_directory="./")


if __name__ == "__main__":
    main()
