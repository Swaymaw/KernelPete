# %%
import os
import subprocess


class EnvManager:
    def __init__(self, base_path: str):
        self.base_path = base_path

    def create_environment(self, name: str):
        try:
            result = subprocess.run(
                ["uv", "venv", os.path.join(self.base_path, name)], check=True, capture_output=True, text=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(e.stderr)

    def setup_environment(self, name: str, dependencies: list[str]):
        dependencies = list(set(dependencies + ["ipykernel"]))
        try:
            result = subprocess.run(
                ["uv", "pip", "install", "--python", os.path.join(self.base_path, name), *dependencies],
                check=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(e.stderr)

        try:
            result = subprocess.run(
                [
                    os.path.join(self.base_path, name, "bin", "python"),
                    "-m",
                    "ipykernel",
                    "install",
                    "--user",
                    "--name",
                    f"{name}_auto",
                    "--display-name",
                    f"Auto ({name}_auto)",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(e.stderr)
