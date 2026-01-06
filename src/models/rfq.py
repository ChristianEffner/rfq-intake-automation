from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

UNKNOWN = "unknown"

class RFQ(BaseModel):
    """
    RFQ data model for Project A (MVP).

    Notes:
    - Dates are stored as ISO strings "YYYY-MM-DD" or the literal "unknown".
    - extra='forbid' ensures we don't accidentally accept unexpected fields.
    """

    model_config = ConfigDict(extra="forbid")

    # Identification / Contact
    request_id: str = Field(..., min_length=1, description="Unique RFQ identifier")
    customer_name: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None

    # Request content
    product_or_service: str = Field(..., min_length=1)
    specification: str = Field(..., min_length=1)

    quantity: Optional[float] = Field(default=None, ge=0)
    quantity_unit: Optional[str] = None

    # Delivery & terms
    requested_delivery_date: str = Field(default=UNKNOWN)
    delivery_location: Optional[str] = None
    incoterms: Optional[str] = None

    # Timing
    response_due_date: str = Field(default=UNKNOWN)

    # Review / workflow
    needs_review: bool
    missing_fields: List[str] = Field(default_factory=list)
    clarification_questions: List[str] = Field(default_factory=list)
    tasks: List[str] = Field(default_factory=list)

    # ---- Validators ----

    @field_validator("requested_delivery_date", "response_due_date")
    @classmethod
    def validate_date_or_unknown(cls, v: str) -> str:
        if v is None:
            return UNKNOWN
        v = v.strip()
        if v.lower() == UNKNOWN:
            return UNKNOWN
        # Accept only ISO date format
        try:
            date.fromisoformat(v)
        except ValueError as e:
            raise ValueError(f"Invalid date '{v}'. Use YYYY-MM-DD or 'unknown'.") from e
        return v

    @field_validator("contact_email")
    @classmethod
    def validate_email_basic(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if v == "":
            return None
        # Minimal sanity check (keeps dependencies minimal)
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("contact_email does not look like an email address.")
        return v

    @model_validator(mode="after")
    def validate_quantity_pair(self) -> "RFQ":
        # If unit exists, quantity should exist too (common sense pairing)
        if self.quantity_unit and self.quantity is None:
            raise ValueError("quantity_unit is set but quantity is missing.")
        return self
