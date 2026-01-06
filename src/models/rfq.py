#Imports
from __future__ import annotations #Aktiviert ein Python-Feature: Type Hints werden als “Strings” behandelt
from datetime import date #Importiert den Typ date, um ISO-Datumstrings zu prüfen
from typing import List, Optional #Das sind Typen für Type Hints: Optional[str] bedeutet: entweder str oder None; List[str] bedeutet: Liste von Strings
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator #Das ist alles aus pydantic (v2), um dein Datenmodell zu definieren und zu prüfen

UNKNOWN = "unknown" #konstante um den String nur einmal zu definieren

class RFQ(BaseModel): #eine Klasse RFQ und erbt BaseModel aus import
    """
    RFQ data model for Project A (MVP).

    Notes:
    - Dates are stored as ISO strings "YYYY-MM-DD" or the literal "unknown".
    - extra='forbid' ensures we don't accidentally accept unexpected fields.
    """

    model_config = ConfigDict(extra="forbid") #extra="forbid" bedeutet: Wenn in deinem Input-JSON zusätzliche Felder auftauchen, die du im Modell nicht definiert hast, dann kommt ein Validierungsfehler.

    # Identification / Contact
    request_id: str = Field(..., min_length=1, description="Unique RFQ identifier")   #genereller Aufbau von Daten: field_name: TYPE = DEFAULT
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

    @field_validator("requested_delivery_date", "response_due_date") #ein Validator für die Felder request.../response...
    @classmethod
    def validate_date_or_unknown(cls, v: str) -> str: #Methode zur Überprüfung ob es sich um ein valides Datum handelt, cls da es sich um eine Klassenmethode handelt, ansonsten self. v ist der Wert der vom Feld reinkommt
        if v is None: #wenn v fehlt oder null ist
            return UNKNOWN #wird unkown eingesetzt
        v = v.strip() #alle Leerzeichen entfernen
        if v.lower() == UNKNOWN: #wenn v kleingeschrieben auch unknown ist
            return UNKNOWN #gib unknown zurück
        # Accept only ISO date format
        try: #überprüft ob es sich um ein gültiges ISO Format handelt
            date.fromisoformat(v)
        except ValueError as e:
            raise ValueError(f"Invalid date '{v}'. Use YYYY-MM-DD or 'unknown'.") from e
        return v #wenn alles passt Wert zurückgeben

    @field_validator("contact_email") #Validator für die Felder contact_email
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
