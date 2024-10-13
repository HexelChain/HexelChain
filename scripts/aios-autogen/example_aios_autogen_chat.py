# This is a main script that tests the functionality of specific agents.
# It requires no user input.
import warnings
from dotenv import load_dotenv
from hexel.sdk import prepare_framework, FrameworkType
from hexel.hooks.llm import hexel_starter
from hexel.utils.utils import delete_directories
from hexel.utils.utils import (
    parse_global_args,
)

from autogen import ConversableAgent, UserProxyAgent


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
    warnings.filterwarnings("ignore")
    parser = parse_global_args()
    args = parser.parse_args()
    load_dotenv()

    with hexel_starter(**vars(args)):
        prepare_framework(FrameworkType.AutoGen)

        # Create the agent that uses the LLM.
        assistant = ConversableAgent("agent")

        # Create the agent that represents the user in the conversation.
        user_proxy = UserProxyAgent("user", code_execution_config=False)

        # Let the assistant start the conversation.  It will end when the user types exit.
        assistant.initiate_chat(user_proxy, message="How can I help you today?")

    clean_cache(root_directory="./")


if __name__ == "__main__":
    main()
