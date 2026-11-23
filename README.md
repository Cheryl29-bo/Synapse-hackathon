# Synapse-hackathon
Cross-system Fintech &amp; Fraud Operations Copilot built with Synapse CLI and MCP for the 2nd Brain Labs × Geek Room Vibe-a-thon.

## Mock APIs

Install the Python dependencies with `python -m pip install -r requirements.txt`, then run each API in a separate terminal from the repository root:

```bash
uvicorn main:app --app-dir transactions-api --host 0.0.0.0 --port 8001
uvicorn main:app --app-dir compliance-api --host 0.0.0.0 --port 8002
```

The transactions API provides `GET /transactions/flagged` and `GET /accounts/{account_id}/history`. The compliance API provides `GET /alerts/open` and `POST /alerts/{alert_id}/escalate`. Mock data includes account `ACC-104` (Chinedu Okafor, ₦1,850,000) and its open alert `ALT-55`.
