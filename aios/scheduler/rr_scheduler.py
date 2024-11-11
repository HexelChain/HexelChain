# Implementing a round robin scheduler using threads
# Allows multiple agents to run at the same time, with each getting a fixed
# chunk of processor time

from .base import BaseScheduler


# allows for memory to be shared safely between threads
from queue import Queue, Empty


from ..context.simple_context import SimpleContextManager

from hexel.hooks.types.llm import LLMRequestQueueGetMessage
from hexel.hooks.types.memory import MemoryRequestQueueGetMessage
from hexel.hooks.types.tool import ToolRequestQueueGetMessage
from hexel.hooks.types.storage import StorageRequestQueueGetMessage

from queue import Queue, Empty

import traceback
import time
from hexel.utils.logger import SchedulerLogger

from threading import Thread


class RRScheduler:
    def __init__(
        self,
        llm,
        # memory_manager,
        log_mode,
        get_llm_request: LLMRequestQueueGetMessage,
        get_memory_request: MemoryRequestQueueGetMessage,
        get_storage_request: StorageRequestQueueGetMessage,
        get_tool_request: ToolRequestQueueGetMessage,
    ):
        self.agent_process_queue = Queue()
        self.get_llm_request = get_llm_request
        self.get_memory_request = get_memory_request
        self.get_storage_request = get_storage_request
        self.get_tool_request = get_tool_request
        self.active = False  # start/stop the scheduler
        self.log_mode = log_mode
        self.logger = self.setup_logger()
        # self.thread = Thread(target=self.run)
        self.request_processors = {
            "llm_syscall_processor": Thread(target=self.run_llm_request),
            "mem_syscall_processor": Thread(target=self.run_memory_request),
            "sto_syscall_processor": Thread(target=self.run_storage_request),
            "tool_syscall_processor": Thread(target=self.run_tool_request)
            # "memory_request_processor": Thread(self.run_memory_request)
        }
        self.llm = llm
        self.time_limit = 5
        self.simple_context_manager = SimpleContextManager()
        # self.memory_manager = memory_manager

    def start(self):
        """start the scheduler"""
        self.active = True
        for name, thread_value in self.request_processors.items():
            thread_value.start()

    def stop(self):
        """stop the scheduler"""
        self.active = False
        for name, thread_value in self.request_processors.items():
            thread_value.join()

    def setup_logger(self):
        logger = SchedulerLogger("Scheduler", self.log_mode)
        return logger

    def run_llm_request(self):
        while self.active:
            try:
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty
                agent_request = self.get_llm_request()

                agent_request.set_status("executing")
                self.logger.log(
                    f"{agent_request.agent_name} is executing. \n", "execute"
                )
                agent_request.set_start_time(time.time())

                response = self.llm.address_request(agent_request)
                agent_request.set_response(response)

                # self.llm.address_request(agent_request)

                agent_request.event.set()
                agent_request.set_status("done")
                agent_request.set_end_time(time.time())

                self.logger.log(
                    f"Current request of {agent_request.agent_name} is done. Thread ID is {agent_request.get_pid()}\n",
                    "done",
                )
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty

            except Empty:
                pass

            except Exception:
                traceback.print_exc()

    def run_memory_request(self):
        while self.active:
            try:
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty
                agent_request = self.get_memory_request()

                agent_request.set_status("executing")
                self.logger.log(
                    f"{agent_request.agent_name} is executing. \n", "execute"
                )
                agent_request.set_start_time(time.time())

                response = self.memory_manager.address_request(agent_request)
                agent_request.set_response(response)

                # self.llm.address_request(agent_request)

                agent_request.event.set()
                agent_request.set_status("done")
                agent_request.set_end_time(time.time())

                self.logger.log(
                    f"Current request of {agent_request.agent_name} is done. Thread ID is {agent_request.get_pid()}\n",
                    "done",
                )
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty

            except Empty:
                pass

            except Exception:
                traceback.print_exc()
    
    def run_storage_request(self):
        while self.active:
            try:
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty
                agent_request = self.get_memory_request()

                agent_request.set_status("executing")
                self.logger.log(
                    f"{agent_request.agent_name} is executing. \n", "execute"
                )
                agent_request.set_start_time(time.time())

                response = self.storage_manager.address_request(agent_request)
                agent_request.set_response(response)

                # self.llm.address_request(agent_request)

                agent_request.event.set()
                agent_request.set_status("done")
                agent_request.set_end_time(time.time())

                self.logger.log(
                    f"Current request of {agent_request.agent_name} is done. Thread ID is {agent_request.get_pid()}\n",
                    "done",
                )
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty

            except Empty:
                pass

            except Exception:
                traceback.print_exc()
    
    def run_tool_request(self):
        while self.active:
            try:
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty
                agent_request = self.get_memory_request()

                agent_request.set_status("executing")
                self.logger.log(
                    f"{agent_request.agent_name} is executing. \n", "execute"
                )
                agent_request.set_start_time(time.time())

                response = self.tool_manager.address_request(agent_request)
                agent_request.set_response(response)

                # self.llm.address_request(agent_request)

                agent_request.event.set()
                agent_request.set_status("done")
                agent_request.set_end_time(time.time())

                self.logger.log(
                    f"Current request of {agent_request.agent_name} is done. Thread ID is {agent_request.get_pid()}\n",
                    "done",
                )
                # wait at a fixed time interval, if there is nothing received in the time interval, it will raise Empty

            except Empty:
                pass

            except Exception:
                traceback.print_exc()

