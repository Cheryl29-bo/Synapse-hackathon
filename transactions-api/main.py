from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Transactions API")


class Account(BaseModel):
    account_id: str
    name: str
    balance: int
    currency: str
    balance_formatted: str


class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    account_name: str
    amount: int
    currency: str
    occurred_at: datetime
    transaction_type: str
    status: str
    flag_reason: str
    counterparty: str


class AccountHistory(BaseModel):
    account: Account
    transactions: list[Transaction]


ACCOUNTS = {
    "ACC-104": Account(
        account_id="ACC-104",
        name="Chinedu Okafor",
        balance=1_850_000,
        currency="NGN",
        balance_formatted="₦1,850,000",
    )
}

TRANSACTIONS = [
    Transaction(
        transaction_id="TXN-9021",
        account_id="ACC-104",
        account_name="Chinedu Okafor",
        amount=1_200_000,
        currency="NGN",
        occurred_at=datetime(2026, 11, 22, 14, 35, tzinfo=timezone.utc),
        transaction_type="transfer",
        status="flagged",
        flag_reason="Unusually large transfer to a new beneficiary",
        counterparty="ACC-992 (New beneficiary)",
    ),
    Transaction(
        transaction_id="TXN-9014",
        account_id="ACC-104",
        account_name="Chinedu Okafor",
        amount=450_000,
        currency="NGN",
        occurred_at=datetime(2026, 11, 21, 9, 10, tzinfo=timezone.utc),
        transaction_type="cash_withdrawal",
        status="flagged",
        flag_reason="Multiple high-value withdrawals within 24 hours",
        counterparty="Lagos Island ATM",
    ),
]


@app.get("/transactions/flagged", response_model=list[Transaction])
def get_flagged_transactions() -> list[Transaction]:
    return [transaction for transaction in TRANSACTIONS if transaction.status == "flagged"]


@app.get("/accounts/{account_id}/history", response_model=AccountHistory)
def get_account_history(account_id: str) -> AccountHistory:
    account = ACCOUNTS.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    transactions = [
        transaction for transaction in TRANSACTIONS if transaction.account_id == account_id
    ]
    return AccountHistory(account=account, transactions=transactions)

@app.post("/accounts/{account_id}/freeze")
def freeze_account(account_id: str, reason: str = "Suspected confirmed fraud"):
  """Immediately freeze a bank account suspected of confirmed fraud."""
  return {"account_id": account_id, "status": "FROZEN", "reason": reason}
