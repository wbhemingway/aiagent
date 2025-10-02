import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'

    if target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            ["python3", target_file].extend(args),
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
        )

        stdout = result.stdout or ""
        stderr = result.stderr or ""

        if not stdout and not stderr:
            return "No output produced."

        parts = []
        parts.append(f"STDOUT: {stdout}")
        parts.append(f"STDERR: {stderr}")
        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")
        return " ".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
