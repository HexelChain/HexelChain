# global variables

from hexel.hooks.modules.llm import useLLMRequestQueue

from hexel.hooks.modules.memory import useMemoryRequestQueue

from hexel.hooks.modules.storage import useStorageRequestQueue

from hexel.hooks.modules.tool import useToolRequestQueue

(
    global_llm_req_queue,
    global_llm_req_queue_get_message,
    global_llm_req_queue_add_message,
    global_llm_req_queue_is_empty,
) = useLLMRequestQueue()

(
    global_memory_req_queue,
    global_memory_req_queue_get_message,
    global_memory_req_queue_add_message,
    global_memory_req_queue_is_empty,
) = useMemoryRequestQueue()

(
    global_storage_req_queue,
    global_storage_req_queue_get_message,
    global_storage_req_queue_add_message,
    global_storage_req_queue_is_empty,
) = useStorageRequestQueue()

(
    global_tool_req_queue,
    global_tool_req_queue_get_message,
    global_tool_req_queue_add_message,
    global_tool_req_queue_is_empty
) = useToolRequestQueue()
