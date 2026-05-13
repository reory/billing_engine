# Endpoints for generating invoices.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import deps
from app.services.invoice_service import InvoiceService

router = APIRouter()
invoice_service = InvoiceService()

@router.post("/{customer_id}", summary="Generate an invoice for a customer")
def generate_invoice(customer_id: str, db: Session = Depends(deps.get_db),):

    invoice = invoice_service.generate_invoice(db, customer_id)

    # Return the newly created invoice details
    return {
        "invoice_id": invoice.id,
        "customer_id": invoice.customer_id,
        "amount": invoice.amount,
        "period_start": invoice.period_start,
        "period_end": invoice.period_end,
        "created_at": invoice.created_at,
    }

@router.get("/preview/{customer_id}",
            summary="Preview current invoice for a customer")
def preview_invoice(
    customer_id: str,
    db: Session = Depends(deps.get_db),
):
    return invoice_service.preview_invoice(db, customer_id)
