from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union, Any

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

class WebhookPayment(BaseModel):
    amount: int
    fee: int
    method: str

class WebhookPixQrCode(BaseModel):
    amount: int
    id: str
    kind: str
    status: str

class WebhookBillingCustomerMetadata(BaseModel):
    cellphone: str
    email: EmailStr
    name: str
    taxId: str = Field(..., alias="taxId")

class WebhookBillingCustomer(BaseModel):
    id: str
    metadata: WebhookBillingCustomerMetadata

class WebhookBillingProductUsed(BaseModel):
    externalId: str = Field(..., alias="externalId")
    id: str
    quantity: int

class WebhookBilling(BaseModel):
    amount: int
    couponsUsed: List[Any] = Field(..., alias="couponsUsed")
    customer: WebhookBillingCustomer
    frequency: str
    id: str
    kind: List[str]
    paidAmount: int = Field(..., alias="paidAmount")
    products: List[WebhookBillingProductUsed]
    status: str

class WebhookDataPix(BaseModel):
    payment: WebhookPayment
    pixQrCode: WebhookPixQrCode = Field(..., alias="pixQrCode")

class WebhookDataBilling(BaseModel):
    payment: WebhookPayment
    billing: WebhookBilling

class WebhookPayload(BaseModel):
    data: Union[WebhookDataPix, WebhookDataBilling]
    devMode: bool = Field(..., alias="devMode")
    event: str
