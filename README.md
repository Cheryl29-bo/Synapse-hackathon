# Synapse-hackathon

Cross-system fintech and fraud operations copilot built with Synapse CLI and MCP for the 2nd Brain Labs × Geek Room Vibe-a-thon.

## Local demo

This demo connects two stdio MCP servers to local FastAPI mock services:

| VS Code MCP server | Python entry point | API |
| --- | --- | --- |
| `transactions-mcp` | `transactions-api/synapse_auto_server_2.py` | `http://127.0.0.1:8001` |
| `compliance-mcp` | `compliance-api/synapse_auto_server.py` | `http://127.0.0.1:8002` |

The MCP server definitions are in `.vscode/mcp.json`. Update each `command` to the Python interpreter where the dependencies are installed if `/home/codespace/.python/current/bin/python3` is not available in your environment. The `ENDPOINT_BASE_URL` values should match the API addresses above.

### Start the APIs

From the repository root, install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Run each mock API in its own terminal:

```bash
python -m uvicorn main:app --app-dir transactions-api --host 127.0.0.1 --port 8001
```

```bash
python -m uvicorn main:app --app-dir compliance-api --host 127.0.0.1 --port 8002
```

Once both APIs are running, open the repository in VS Code and enable/restart the MCP servers from `.vscode/mcp.json`. The available tools are:

- `transactions-mcp`: `get_flagged_transactions`, `get_account_history`, and `freeze_account`.
- `compliance-mcp`: `get_open_alerts` and `escalate_alert`. Escalation optionally accepts a severity of `low`, `medium`, `high`, or `critical`.

### Demo workflow

1. Call `get_flagged_transactions` and `get_open_alerts` to review both systems.
2. Match records by `account_id`. For example, the mock data has flagged transaction `TXN-9021` for `ACC-104` in the amount of ₦1,200,000 and open alert `ALT-55` for that same account.
3. If the review warrants escalation, call `escalate_alert` with the alert ID and desired severity (for example, `ALT-55` and `critical`).
4. Freeze an account only when the transaction and compliance review support that action. Call `freeze_account` with the matching account ID; the mock endpoint supplies a default reason if one is not provided.

These are mock services: their records are held in memory and reset when their API process restarts. The freeze endpoint returns a simulated `FROZEN` result; it does not affect a real financial account.
