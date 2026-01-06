from src.models.rfq import RFQ

def test_valid_rfq():
    data = {
        "request_id": "RFQ_0001",
        "product_or_service": "Pneumatic valve",
        "specification": "Test spec",
        "requested_delivery_date": "unknown",
        "response_due_date": "2026-01-31",
        "needs_review": True,
        "missing_fields": [],
        "clarification_questions": [],
        "tasks": []
    }
    rfq = RFQ.model_validate(data)
    assert rfq.request_id == "RFQ_0001"
