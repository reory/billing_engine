# Unit tests for usage

from app.services.usage_service import UsageService
from app.schemas import UsageEventCreate


def test_record_usage_service(db):
    """
    Ensure UsageService correctly stores a usage event
    and returns a fully populated SQLAlchemy model.
    """
    payload = UsageEventCreate(
        customer_id="cust_123",
        metric="api_calls",
        units=100
    )

    event = UsageService.record_usage(db, payload)

    assert event.id is not None
    assert event.customer_id == "cust_123"
    assert event.metric == "api_calls"
    assert event.units == 100
    assert event.timestamp is not None


def test_record_usage_api(client):
    """
    Ensure the /usage/ endpoint accepts JSON payloads,
    stores the event, and returns a valid response.
    """
    response = client.post("/usage/", json={
        "customer_id": "cust_123",
        "metric": "api_calls",
        "units": 50
    })

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["customer_id"] == "cust_123"
    assert data["metric"] == "api_calls"
    assert data["units"] == 50
    assert data["timestamp"] is not None
