from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class CustomerCreate(BaseModel):
    name: str
    cellphone: str
    email: EmailStr
    taxId: str = Field(..., alias="taxId")

class PixQrCodeCustomer(BaseModel):
    name: str
    cellphone: str
    email: EmailStr
    taxId: str = Field(..., alias="taxId")

class PixQrCodeMetadata(BaseModel):
    externalId: Optional[str] = Field(None, alias="externalId")

class PixQrCodeCreate(BaseModel):
    amount: int = Field(..., gt=0)
    expiresIn: Optional[int] = Field(None, alias="expiresIn")
    description: Optional[str] = None
    customer: Optional[PixQrCodeCustomer] = None
    metadata: Optional[PixQrCodeMetadata] = None

class PixQrCodeSimulatePayment(BaseModel):
    metadata: Optional[dict] = {}

class BillingProduct(BaseModel):
    externalId: str = Field(..., alias="externalId")
    name: str
    description: Optional[str] = None
    quantity: int = Field(..., ge=1)
    price: int = Field(..., ge=100)

class BillingCreate(BaseModel):
    frequency: str = "ONE_TIME"
    methods: List[str] = ["PIX"]
    products: List[BillingProduct]
    returnUrl: str = Field(..., alias="returnUrl")
    completionUrl: str = Field(..., alias="completionUrl")
    customerId: Optional[str] = Field(None, alias="customerId")
    customer: Optional[CustomerCreate] = None
