from pyopenagi.agents.agent_process import AgentProcessFactory
from typing import Optional

from hexel.sdk.autogen.agent_adapter import (
    adapter_autogen_agent_init,
    _adapter_print_received_message,
    _adapter_generate_oai_reply_from_client,
    adapter_generate_tool_calls_reply,
    adapter_execute_function,
    _adapter_a_execute_tool_call,
    adapter_update_tool_signature
)

from hexel.sdk.autogen.client_adapter import (
    adapter_autogen_client_init,
    adapter_client_create,
    adapter_client_extract_text_or_completion_object
)

from hexel.utils.logger import AgentLogger

try:
    from autogen import (
        OpenAIWrapper,
        ConversableAgent
    )
except ImportError:
    raise ImportError(
        "Could not import autogen python package. "
        "Please install it with `pip install pyautogen`."
    )

logger = AgentLogger("Adapter")


def prepare_autogen(agent_process_factory: Optional[AgentProcessFactory] = None):
    """adapter autogen for hexel
    """
    # Replace OpenAIWrapper method
    OpenAIWrapper.__init__ = adapter_autogen_client_init
    OpenAIWrapper.create = adapter_client_create
    OpenAIWrapper.extract_text_or_completion_object = adapter_client_extract_text_or_completion_object

    # Replace agent method
    ConversableAgent.agent_process_factory = agent_process_factory
    ConversableAgent._print_received_message = _adapter_print_received_message
    ConversableAgent._generate_oai_reply_from_client = _adapter_generate_oai_reply_from_client
    ConversableAgent.generate_tool_calls_reply = adapter_generate_tool_calls_reply
    ConversableAgent.execute_function = adapter_execute_function
    ConversableAgent._a_execute_tool_call = _adapter_a_execute_tool_call
    ConversableAgent.update_tool_signature = adapter_update_tool_signature
    ConversableAgent.__init__ = adapter_autogen_agent_init

    logger.log("Autogen prepare success", "info")
