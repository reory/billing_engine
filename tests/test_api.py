
def test_usage_endpoint(client):
    """
    Ensure the /usage endpoint accepts and stores usage events.
    """
    response = client.post("/usage/", json={
        "customer_id": "cust_123",
        "metric": "api_calls",
        "units": 10
    })

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["customer_id"] == "cust_123"
    assert data["metric"] == "api_calls"
    assert data["units"] == 10


def test_full_billing_pipeline(client):
    """
    End-to-end test:
    1. Record usage
    2. Aggregate usage
    3. Preview invoice
    4. Generate invoice
    """

    # 1. Record usage
    client.post("/usage/", json={
        "customer_id": "cust_123",
        "metric": "api_calls",
        "units": 100
    })

    # 2. Aggregate
    agg = client.post("/aggregate/run")
    assert agg.status_code == 200
    assert agg.json()["aggregated_records"] == 1

    # 3. Preview invoice
    preview = client.get("/invoice/preview/cust_123")
    assert preview.status_code == 200
    assert preview.json()["estimated_amount"] > 0

    # 4. Generate invoice
    invoice = client.post("/invoice/cust_123")
    assert invoice.status_code == 200
    assert invoice.json()["amount"] == preview.json()["estimated_amount"]
