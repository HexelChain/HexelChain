from random import randint

from typing import Tuple

from hexel.llm_core.llms import LLM
from hexel.hooks.types.llm import (
    LLMParams,
    LLMRequestQueue,
    LLMRequestQueueAddMessage,
    LLMRequestQueueGetMessage,
    LLMRequestQueueCheckEmpty
)
from hexel.hooks.utils.validate import validate
from hexel.hooks.stores import queue as QueueStore, processes as ProcessStore
# from hexel.hooks.utils import generate_random_string
# from pyopenagi.agents.agent_factory import AgentFactory

ids = []  # List to store process IDs


@validate(LLMParams)
def useCore(params: LLMParams) -> LLM:
    """
    Initialize and return a Language Learning Model (LLM) instance.

    Args:
        params (LLMParams): Parameters required for LLM initialization.

    Returns:
        LLM: An instance of the initialized LLM.
    """
    return LLM(**params.model_dump())


def useLLMRequestQueue() -> (
    Tuple[LLMRequestQueue, LLMRequestQueueGetMessage, LLMRequestQueueAddMessage, LLMRequestQueueCheckEmpty]
):
    """
    Creates and returns a queue for LLM requests along with helper methods to manage the queue.

    Returns:
        Tuple: A tuple containing the LLM request queue, get message function, add message function, and check queue empty function.
    """
    # r_str = (
    #     generate_random_string()
    # )  # Generate a random string for queue identification
    r_str = "llm"
    _ = LLMRequestQueue()

    # Store the LLM request queue in QueueStore
    QueueStore.REQUEST_QUEUE[r_str] = _

    # Function to get messages from the queue
    def getMessage():
        return QueueStore.getMessage(_)

    # Function to add messages to the queue
    def addMessage(message: str):
        return QueueStore.addMessage(_, message)

    # Function to check if the queue is empty
    def isEmpty():
        return QueueStore.isEmpty(_)

    return _, getMessage, addMessage, isEmpty
