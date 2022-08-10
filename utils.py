import subprocess
import shlex
import os


def subprocess_exec_cmd(
    cmd: str,
    working_dir: str = None,
    timeout: int = 30,
):

    cwd = working_dir if working_dir else os.getcwd()

    process = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf8",
        check=False,
        timeout=timeout,
        cwd=cwd,
    )

    return process
