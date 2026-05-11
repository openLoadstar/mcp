from mcp.server.fastmcp import FastMCP

from .cli import CLIError, run_cli
from .elements import get_map as _get_map
from .elements import get_waypoint as _get_waypoint
from .paths import get_spec_path, validate_project_path

mcp = FastMCP(
    "loadstar",
    instructions=(
        "LOADSTAR MCP server. All tools except loadstar_get_spec require project_path: "
        "absolute path to the project root containing a .loadstar/ directory. "
        "Typical workflow: loadstar_show → loadstar_get_waypoint(address) → "
        "code tools (LSP/grep scoped to CODE_MAP.scope) → loadstar_log_add. "
        "Before starting work: ensure WayPoint STATUS is S_PRG. "
        "After completing all TODO TASK items: set STATUS to S_STB."
    ),
)


def _err(e: Exception) -> str:
    return f"[ERROR] {e}"


# ── CLI-wrapping tools ────────────────────────────────────────────────────────

@mcp.tool(
    description=(
        "Show all WayPoints with STATUS and LAST_MODIFIED. "
        "filter: optional keyword matched case-insensitively against the address only "
        "(e.g. 'cli' matches 'W://root/cli/cmd_show'). "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_show(project_path: str, filter: str | None = None) -> str:
    try:
        p = validate_project_path(project_path)
        args = ["show"]
        if filter:
            args.append(filter)
        return run_cli(args, p)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "Validate WayPoint references and schema. "
        "Reports broken PARENT/CHILDREN/REFERENCE links and missing required fields. "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_validate(project_path: str) -> str:
    try:
        p = validate_project_path(project_path)
        return run_cli(["validate"], p)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "List current TODO items (PENDING / ACTIVE / BLOCKED) from WayPoint STATUS. "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_todo_list(project_path: str) -> str:
    try:
        p = validate_project_path(project_path)
        return run_cli(["todo", "list"], p)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "Show TODO completion history. "
        "map: optional Map address to filter (e.g. 'M://root/cli'). "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_todo_history(project_path: str, map: str | None = None) -> str:
    try:
        p = validate_project_path(project_path)
        args = ["todo", "history"]
        if map:
            args.append(map)
        return run_cli(args, p)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "Query the LOADSTAR activity log. "
        "time_range: 'Nd' for last N days or 'Nh' for last N hours (e.g. '7d', '3h'). "
        "Omit for all entries. "
        "filter: keyword matched against address, KIND, or content (case-insensitive). "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_log(
    project_path: str,
    time_range: str | None = None,
    filter: str | None = None,
) -> str:
    try:
        p = validate_project_path(project_path)
        args = ["log"]
        if time_range:
            args.append(time_range)
        if filter:
            args.append(filter)
        return run_cli(args, p)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "Add a log entry to a WayPoint. "
        "address: WayPoint address (e.g. 'W://root/feature') or short ID (e.g. 'feature'). "
        "kind: entry type, must be one of NOTE, DECISION, ISSUE, RESOLVED, PROGRESS, MODIFIED. "
        "content: log message text. "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_log_add(
    project_path: str, address: str, kind: str, content: str
) -> str:
    try:
        p = validate_project_path(project_path)
        return run_cli(["log", "add", address, kind, content], p)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "List open questions (OPEN_QUESTIONS) across WayPoints. "
        "filter: keyword to narrow results. "
        "with_resolved: include resolved/done questions (default false). "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_question(
    project_path: str,
    filter: str | None = None,
    with_resolved: bool = False,
) -> str:
    try:
        p = validate_project_path(project_path)
        args = ["question"]
        if filter:
            args.append(filter)
        if with_resolved:
            args.append("--with-resolved")
        return run_cli(args, p)
    except Exception as e:
        return _err(e)


# ── Direct file-reading tools ─────────────────────────────────────────────────

@mcp.tool(
    description=(
        "Read a WayPoint by address. Returns full markdown: "
        "IDENTITY, CONNECTIONS, CODE_MAP, TODO (TASK / RECURRING checklist), ISSUE. "
        "Use CODE_MAP.scope directories to limit subsequent code searches (LSP/grep). "
        "WayPoint STATUS rules: set S_IDL→S_PRG before starting; "
        "set S_PRG→S_STB after all TODO TASK [ ] items are [x]. "
        "address: e.g. 'W://root/feature'. "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_get_waypoint(project_path: str, address: str) -> str:
    try:
        p = validate_project_path(project_path)
        return _get_waypoint(p, address)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "Read a Map by address. Returns Map markdown with WAYPOINTS list. "
        "Start here to navigate project structure, then use loadstar_get_waypoint. "
        "address: e.g. 'M://root'. "
        "project_path: absolute path to the project root (must contain .loadstar/)."
    )
)
def loadstar_get_map(project_path: str, address: str) -> str:
    try:
        p = validate_project_path(project_path)
        return _get_map(p, address)
    except Exception as e:
        return _err(e)


@mcp.tool(
    description=(
        "Read LOADSTAR SPEC documentation. Requires LOADSTAR_SPEC_PATH env var. "
        "section: filename or number prefix (e.g. '01', '06', 'README', 'CLI_SPEC'). "
        "Omit section to get the SPEC README/index."
    )
)
def loadstar_get_spec(section: str | None = None) -> str:
    try:
        spec_dir = get_spec_path()
        if not spec_dir.is_dir():
            return _err(FileNotFoundError(f"LOADSTAR_SPEC_PATH does not exist: {spec_dir}"))
        if section is None:
            target = spec_dir / "README.md"
        else:
            candidates = sorted(spec_dir.glob(f"*{section}*"))
            if not candidates:
                return _err(FileNotFoundError(f"No SPEC file matching {section!r} in {spec_dir}"))
            md = [c for c in candidates if c.suffix == ".md"]
            target = md[0] if md else candidates[0]
        return target.read_text(encoding="utf-8")
    except Exception as e:
        return _err(e)


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
