import subprocess
import shlex


def subprocess_exec_cmd(cmd: str):
    process = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf8",
        check=False,
        timeout=10,
    )
    return process
