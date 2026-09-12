import nbformat
from autopep8 import fix_code
from jupyter_client import KernelManager
from nbformat.v4 import new_code_cell, new_output


class KernelEngine:
    def __init__(self, kernel_name: str = "python3", notebook_path: str = "analysis.ipynb"):
        self.km = KernelManager(kernel_name=kernel_name)  # was hardcoded before
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()
        self.notebook_path = notebook_path
        self.notebook = nbformat.v4.new_notebook()

    def execute(self, code: str):
        code = fix_code(code)
        cell = new_code_cell(
            source=code,
        )
        self.notebook.cells.append(cell)
        self.save()

        execute_id = self.kc.execute(code)
        outputs = []
        execution_count = None
        text_output = ""

        while True:
            out = self.kc.get_iopub_msg()

            if out["parent_header"].get("msg_id") != execute_id:
                continue

            msg_type = out["header"]["msg_type"]
            content = out["content"]

            if msg_type == "status":
                if content["execution_state"] == "idle":
                    break

            elif msg_type == "execute_input":
                continue

            elif msg_type == "stream":
                outputs.append(
                    new_output(
                        output_type="stream",
                        name=content["name"],  # "stdout" or "stderr"
                        text=content["text"],
                    )
                )
                text_output += content["text"]

            elif msg_type == "execute_result":
                execution_count = content.get("execution_count")
                outputs.append(
                    new_output(
                        output_type="execute_result",
                        data=content["data"],  # full mimebundle
                        metadata=content.get("metadata", {}),
                        execution_count=execution_count,
                    )
                )
                text_output += content["data"].get("text/plain", "")

            elif msg_type == "display_data":
                outputs.append(
                    new_output(
                        output_type="display_data",
                        data=content["data"],  # e.g. image/png + text/plain
                        metadata=content.get("metadata", {}),
                    )
                )
                text_output += content["data"].get("text/plain", "")

            elif msg_type == "error":
                outputs.append(
                    new_output(
                        output_type="error",
                        ename=content["ename"],
                        evalue=content["evalue"],
                        traceback=content["traceback"],
                    )
                )
                text_output += "\n".join(content["traceback"])

            elif msg_type == "clear_output":
                if content.get("wait"):
                    outputs = []
                    text_output = ""

        cell.outputs = outputs
        cell.execution_count = execution_count
        self.save()

        return cell.outputs

    def save(self):
        nbformat.validate(self.notebook)  # optional but catches schema mistakes early
        nbformat.write(self.notebook, self.notebook_path)
