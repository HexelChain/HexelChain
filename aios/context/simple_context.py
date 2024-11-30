# This manages restoring and snapshotting the context.
# The file is used in the BaseLLM class and the RRScheduler class.

from hexel.context.base import BaseContextManager

class SimpleContextManager(BaseContextManager):
    def __init__(self):
        BaseContextManager.__init__(self)
        self.context_dict = {}

    def start(self):
        pass

    def gen_snapshot(self, pid, context):
        # file_path = os.path.join(self.context_dir, f"process-{pid}.pt")
        # torch.save(context, file_path)
        self.context_dict[str(pid)] = context

    def gen_recover(self, pid):
        # file_path = os.path.join(self.context_dir, f"process-{pid}.pt")
        # return torch.load(file_path)
        return self.context_dict[str(pid)]

    def check_restoration(self, pid):
        # return os.path.exists(os.path.join(self.context_dir, f"process-{pid}.pt"))
        return str(pid) in self.context_dict.keys()

    def clear_restoration(self, pid):
        # print(f"Process {pid} has been deleted.")
        # os.remove(os.path.join(self.context_dir, f"process-{pid}.pt"))
        self.context_dict.pop(pid)
        return

    def stop(self):
        pass
