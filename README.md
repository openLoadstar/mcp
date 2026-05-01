# loadstar-mcp

LOADSTAR MCP server — exposes LOADSTAR project management tools via the [Model Context Protocol](https://modelcontextprotocol.io).

## Installation

```bash
# Recommended: run directly via uvx (no installation required)
uvx loadstar-mcp

# Or install with pip
pip install loadstar-mcp
```

## Prerequisites

- [loadstar CLI](https://github.com/openLoadstar/cli) must be installed and accessible as `loadstar` in your PATH (or set `LOADSTAR_CLI_PATH`).
- Python 3.10+

## Usage

Every tool (except `loadstar_get_spec`) requires **`project_path`**: the absolute path to a project root that contains a `.loadstar/` directory.

```
# Good
loadstar_show(project_path="/home/user/myproject")

# Bad — relative paths are rejected
loadstar_show(project_path="./myproject")
```

## Environment Variables

| Variable | Required | Purpose |
|:--|:--|:--|
| `LOADSTAR_CLI_PATH` | Optional | Path to `loadstar` binary. Defaults to system PATH. |
| `LOADSTAR_SPEC_PATH` | Optional | Path to the `loadstar_SPEC` directory. Required only for `loadstar_get_spec`. |

## Tools

| Tool | Description |
|:--|:--|
| `loadstar_show` | List all WayPoints with STATUS |
| `loadstar_validate` | Check for broken references |
| `loadstar_todo_list` | Current TODO items |
| `loadstar_todo_history` | Completion history |
| `loadstar_log` | Query activity log |
| `loadstar_log_add` | Add a log entry |
| `loadstar_question` | List open questions |
| `loadstar_get_waypoint` | Read a WayPoint by address |
| `loadstar_get_map` | Read a Map by address |
| `loadstar_get_spec` | Read LOADSTAR SPEC documentation |

## Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "loadstar": {
      "command": "uvx",
      "args": ["loadstar-mcp"],
      "env": {
        "LOADSTAR_CLI_PATH": "/usr/local/bin/loadstar",
        "LOADSTAR_SPEC_PATH": "/path/to/loadstar_SPEC"
      }
    }
  }
}
```

## Claude Code

```bash
claude mcp add loadstar -- uvx loadstar-mcp
```

With environment variables:

```bash
claude mcp add loadstar -e LOADSTAR_CLI_PATH=/usr/local/bin/loadstar \
  -e LOADSTAR_SPEC_PATH=/path/to/loadstar_SPEC -- uvx loadstar-mcp
```

## License

Apache 2.0 — see [LICENSE](LICENSE).
