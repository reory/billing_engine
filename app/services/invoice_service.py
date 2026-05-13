# Business logic layer generates the invoice

from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models import AggregatedUsage, Invoice
from app.pricing import PricingEngine


class InvoiceService:
    pricing = PricingEngine()

    @staticmethod
    def preview_invoice(db: Session, customer_id: str):
        # Billing period: last 30 days (same as real invoice)
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)

        # Fetch aggregated usage for this customer + period
        usage_rows = (
            db.query(AggregatedUsage)
            .filter(AggregatedUsage.customer_id == customer_id)
            .filter(AggregatedUsage.period_start >= period_start)
            .filter(AggregatedUsage.period_end <= period_end)
            .all()
        )

        usage_list = [(row.metric, row.total_units) for row in usage_rows]

        # Calculate estimated amount
        estimated_amount = InvoiceService.pricing.calculate_invoice_amount(
            customer_id, usage_list
        )

        return {
            "customer_id": customer_id,
            "estimated_amount": estimated_amount,
            "period_start": period_start,
            "period_end": period_end,
            "usage": usage_list,
        }

    @staticmethod
    def generate_invoice(db: Session, customer_id: str) -> Invoice:

        # Billing period (simple: last 30 days)
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)

        # Fetch aggregated usage for this customer + period
        usage_rows = (
            db.query(AggregatedUsage)
            .filter(AggregatedUsage.customer_id == customer_id)
            .filter(AggregatedUsage.period_start >= period_start)
            .filter(AggregatedUsage.period_end <= period_end)
            .all()
        )

        # Convert rows → list of (metric, total_units)
        usage_list = [(row.metric, row.total_units) for row in usage_rows]

        # Calculate invoice amount
        amount = InvoiceService.pricing.calculate_invoice_amount(
            customer_id, usage_list
        )

        # Create invoice record
        invoice = Invoice(
            customer_id=customer_id,
            amount=amount,
            period_start=period_start,
            period_end=period_end,
        )

        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        return invoice

