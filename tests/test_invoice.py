# Unit tests for billing logic.

from app.services.usage_service import UsageService
from app.services.aggregator_service import AggregatorService
from app.services.invoice_service import InvoiceService
from app.schemas import UsageEventCreate
from app.models import Invoice


def test_invoice_preview_and_generation(db):
    """
    Ensure invoice preview calculates correctly and invoice generation
    writes a real invoice record.
    """

    # Insert usage
    UsageService.record_usage(db, UsageEventCreate(
        customer_id="cust_123",
        metric="api_calls",
        units=1000
    ))

    # Aggregate usage
    AggregatorService.run_aggregation(db)

    # Preview invoice
    preview = InvoiceService.preview_invoice(db, "cust_123")
    assert preview["estimated_amount"] > 0
    assert preview["period_start"] is not None
    assert preview["period_end"] is not None

    # Generate invoice
    invoice = InvoiceService.generate_invoice(db, "cust_123")

    assert invoice.id is not None
    assert invoice.amount == preview["estimated_amount"]
    assert invoice.customer_id == "cust_123"

    # Confirm invoice exists in DB
    stored = db.query(Invoice).first()
    assert stored.amount == invoice.amount
