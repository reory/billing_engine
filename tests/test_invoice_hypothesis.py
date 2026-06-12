import math
from datetime import datetime, timedelta

from hypothesis import given, strategies as st

from app.services.invoice_service import InvoiceService
from app.models import AggregatedUsage, Invoice


def make_fake_row(metric: str, units: float, start: datetime, end: datetime):
    """Create a fake AggregatedUsage row without touching the DB."""

    return AggregatedUsage(
        customer_id="cust",
        metric=metric,
        total_units=units,
        period_start=start,
        period_end=end,
    )


metric_strategy = st.text(min_size=1, max_size=10)

units_strategy = st.floats(
    min_value=0,
    max_value=1e9,
    allow_nan=False,
    allow_infinity=False,
)

usage_row_strategy = st.builds(
    lambda metric, units: (metric, units),
    metric_strategy,
    units_strategy,
)

usage_list_strategy = st.lists(
    usage_row_strategy,
    min_size=0,
    max_size=20,
)

# -----------------------------------------------------------------------------
# Tests


@given(usage_list_strategy)
def test_pricing_amount_is_never_negative(usage_list):
    """Invoice amounts must always be >= 0."""

    amount = InvoiceService.pricing.calculate_invoice_amount("cust", usage_list)
    assert amount >= 0


@given(usage_list_strategy)
def test_pricing_is_deterministic(usage_list):
    """Same input → same output."""

    a1 = InvoiceService.pricing.calculate_invoice_amount("cust", usage_list)
    a2 = InvoiceService.pricing.calculate_invoice_amount("cust", usage_list)
    assert a1 == a2


@given(usage_list_strategy)
def test_pricing_is_order_invariant(usage_list):
    """Reordering usage rows must not change the invoice amount."""

    shuffled = usage_list[::-1]
    a1 = InvoiceService.pricing.calculate_invoice_amount("cust", usage_list)
    a2 = InvoiceService.pricing.calculate_invoice_amount("cust", shuffled)
    assert a1 == a2


@given(usage_list_strategy)
def test_preview_invoice_invariants(usage_list):
    """Preview invoice must always return valid structure + invariants."""

    # Fake DB session with controlled query results
    class FakeQuery:
        def __init__(self, rows):
            self.rows = rows

        def filter(self, *args, **kwargs):
            return self

        def all(self):
            return self.rows

    class FakeDB:
        def query(self, model):

            # Convert usage_list → fake AggregatedUsage rows
            now = datetime.utcnow()
            rows = [
                make_fake_row(metric, units, now - timedelta(days=10), now)
                for metric, units in usage_list
            ]
            return FakeQuery(rows)

    db = FakeDB()

    result = InvoiceService.preview_invoice(db, "cust")

    # Structure invariants
    assert "customer_id" in result
    assert "estimated_amount" in result
    assert "period_start" in result
    assert "period_end" in result
    assert "usage" in result

    # Amount invariants
    assert result["estimated_amount"] >= 0
    assert not math.isnan(result["estimated_amount"])

    # Period invariants
    assert result["period_end"] >= result["period_start"]
    assert result["period_end"] <= datetime.utcnow()


@given(usage_list_strategy)
def test_generate_invoice_invariants(usage_list):
    """Generated invoices must always be valid ORM objects."""

    # Fake DB session that captures added invoices
    class FakeDB:
        def __init__(self):
            self.added = []

        def query(self, model):
            now = datetime.utcnow()
            rows = [
                make_fake_row(metric, units, now - timedelta(days=10), now)
                for metric, units in usage_list
            ]

            class FakeQuery:
                def filter(self, *args, **kwargs):
                    return self

                def all(self_inner):
                    return rows

            return FakeQuery()

        def add(self, obj):
            self.added.append(obj)

        def commit(self):
            pass

        def refresh(self, obj):
            obj.id = 1  # simulate DB identity assignment

    db = FakeDB()

    invoice = InvoiceService.generate_invoice(db, "cust")

    # Type invariants
    assert isinstance(invoice, Invoice)

    # Amount invariants
    assert invoice.amount >= 0
    assert not math.isnan(invoice.amount)

    # Period invariants
    assert invoice.period_end >= invoice.period_start
    assert invoice.period_end <= datetime.utcnow()

    # DB invariants
    assert len(db.added) == 1
    assert db.added[0] is invoice
