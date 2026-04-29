import os
from pathlib import Path


def validate_project_path(project_path: str) -> Path:
    p = Path(project_path)
    if not p.is_absolute():
        raise ValueError(f"project_path must be absolute: {project_path!r}")
    if not p.exists():
        raise ValueError(f"project_path does not exist: {project_path!r}")
    if not p.is_dir():
        raise ValueError(f"project_path is not a directory: {project_path!r}")
    if not (p / ".loadstar").is_dir():
        raise ValueError(
            f"project_path has no .loadstar/ directory: {project_path!r}\n"
            "Run 'loadstar init' in the project root first."
        )
    return p


def get_cli_path() -> str:
    return os.environ.get("LOADSTAR_CLI_PATH", "loadstar")


def get_spec_path() -> Path:
    spec = os.environ.get("LOADSTAR_SPEC_PATH")
    if not spec:
        raise ValueError(
            "LOADSTAR_SPEC_PATH environment variable is not set. "
            "Set it to the loadstar_SPEC directory path to use loadstar_get_spec."
        )
    return Path(spec)
