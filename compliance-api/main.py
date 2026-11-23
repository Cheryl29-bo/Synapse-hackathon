from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Compliance API")


class Alert(BaseModel):
    alert_id: str
    account_id: str
    title: str
    severity: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "escalated", "closed"]
    description: str
    created_at: datetime


ALERTS = {
    "ALT-55": Alert(
        alert_id="ALT-55",
        account_id="ACC-104",
        title="Unusual high-value account activity",
        severity="high",
        status="open",
        description="Review flagged high-value transfers and cash withdrawals.",
        created_at=datetime(2026, 11, 22, 14, 40, tzinfo=timezone.utc),
    )
}


@app.get("/alerts/open", response_model=list[Alert])
def get_open_alerts() -> list[Alert]:
    return [alert for alert in ALERTS.values() if alert.status == "open"]


@app.post("/alerts/{alert_id}/escalate", response_model=Alert)
def escalate_alert(
    alert_id: str, severity: Literal["low", "medium", "high", "critical"] | None = None
) -> Alert:
    alert = ALERTS.get(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    if alert.status == "closed":
        raise HTTPException(status_code=409, detail="Closed alerts cannot be escalated")
    alert.status = "escalated"
    if severity is not None:
        alert.severity = severity
    return alert
