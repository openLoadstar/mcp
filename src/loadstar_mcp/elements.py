import re
from pathlib import Path


def _resolve_path(project_path: Path, address: str) -> Path:
    """Convert W:// or M:// address to .loadstar file path."""
    if address.startswith("W://"):
        rest = address[4:]
        filename = rest.replace("/", ".") + ".md"
        return project_path / ".loadstar" / "WAYPOINT" / filename
    if address.startswith("M://"):
        rest = address[4:]
        filename = rest.replace("/", ".") + ".md"
        return project_path / ".loadstar" / "MAP" / filename
    raise ValueError(f"Unknown address scheme: {address!r}. Use W:// or M://")


def get_waypoint(project_path: Path, address: str) -> str:
    path = _resolve_path(project_path, address)
    if not path.exists():
        raise FileNotFoundError(f"WayPoint not found: {address!r} → {path}")
    return path.read_text(encoding="utf-8")


def get_map(project_path: Path, address: str) -> str:
    path = _resolve_path(project_path, address)
    if not path.exists():
        raise FileNotFoundError(f"Map not found: {address!r} → {path}")
    return path.read_text(encoding="utf-8")


def extract_code_map_scope(waypoint_content: str) -> list[str]:
    """Return CODE_MAP.scope entries from WayPoint markdown."""
    m = re.search(
        r"### CODE_MAP\s*\n.*?scope:\s*\n((?:[ \t]+-[ \t]+.+\n)*)",
        waypoint_content,
        re.DOTALL,
    )
    if not m:
        return []
    return [item.strip() for item in re.findall(r"[ \t]+-[ \t]+(.+)", m.group(1))]
