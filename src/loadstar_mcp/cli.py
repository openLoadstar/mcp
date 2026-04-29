import subprocess
from pathlib import Path

from .paths import get_cli_path

_TIMEOUT = 30


class CLIError(Exception):
    def __init__(self, returncode: int, stderr: str, command: list[str]):
        self.returncode = returncode
        self.stderr = stderr
        self.command = command
        super().__init__(f"CLI exited {returncode}: {stderr.strip()!r}")


def run_cli(args: list[str], project_path: Path) -> str:
    cli = get_cli_path()
    cmd = [cli, *args]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(project_path),
            capture_output=True,
            text=True,
            timeout=_TIMEOUT,
        )
    except FileNotFoundError:
        raise CLIError(
            -1,
            f"loadstar CLI not found at {cli!r}. Install it or set LOADSTAR_CLI_PATH.",
            cmd,
        )
    except subprocess.TimeoutExpired:
        raise CLIError(-1, f"CLI timed out after {_TIMEOUT}s", cmd)
    if result.returncode != 0:
        raise CLIError(result.returncode, result.stderr or result.stdout, cmd)
    return result.stdout
