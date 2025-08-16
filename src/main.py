from fastapi import FastAPI, Depends
from typing import Any

from . import models, schemas
from .database import engine
from .auth import get_current_user
from .abacatepay import AbacatePayClient, get_abacate_pay_client

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AbacatePay Integration API",
    description="An example API integrating with AbacatePay.",
    version="1.0.0",
)

@app.get("/check-authentication")
async def check_authentication(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authenticated!"}

# --- AbacatePay Endpoints ---

@app.post("/v1/customer/create", tags=["AbacatePay - Customers"], summary="Create a new customer")
async def create_customer(
    customer_data: schemas.CustomerCreate,
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Creates a new customer in AbacatePay.
    """
    return await client.create_customer(customer_data)

@app.get("/v1/customer/list", tags=["AbacatePay - Customers"], summary="List all customers")
async def list_customers(
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Retrieves a list of all customers from AbacatePay.
    """
    return await client.list_customers()

@app.post("/v1/billing/create", tags=["AbacatePay - Billings"], summary="Create a new billing")
async def create_billing(
    billing_data: schemas.BillingCreate,
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Creates a new billing (charge) in AbacatePay.
    """
    return await client.create_billing(billing_data)

@app.get("/v1/billing/list", tags=["AbacatePay - Billings"], summary="List all billings")
async def list_billings(
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Retrieves a list of all billings from AbacatePay.
    """
    return await client.list_billings()

# --- AbacatePay PIX QR Code Endpoints ---

@app.post("/v1/pixQrCode/create", tags=["AbacatePay - PIX QR Code"], summary="Create a new PIX QR Code")
async def create_pix_qr_code(
    pix_data: schemas.PixQrCodeCreate,
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Creates a new PIX QR Code in AbacatePay.
    """
    return await client.create_pix_qr_code(pix_data)

@app.get("/v1/pixQrCode/check/{pix_id}", tags=["AbacatePay - PIX QR Code"], summary="Check PIX QR Code status")
async def check_pix_qr_code_status(
    pix_id: str,
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Checks the payment status of a PIX QR Code.
    """
    return await client.check_pix_qr_code_status(pix_id)

@app.post("/v1/pixQrCode/simulate-payment/{pix_id}", tags=["AbacatePay - PIX QR Code"], summary="Simulate PIX QR Code payment")
async def simulate_pix_qr_code_payment(
    pix_id: str,
    payment_data: schemas.PixQrCodeSimulatePayment,
    current_user: models.User = Depends(get_current_user),
    client: AbacatePayClient = Depends(get_abacate_pay_client)
) -> Any:
    """
    Simulates the payment of a PIX QR Code created in development mode.
    """
    return await client.simulate_pix_qr_code_payment(pix_id, payment_data)
