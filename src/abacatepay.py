import os
import httpx
from dotenv import load_dotenv
from typing import Dict, Any
from fastapi import HTTPException

from . import schemas

load_dotenv()

ABACATE_PAY_API_KEY = os.getenv("ABACATE_PAY_API_KEY")
ABACATE_PAY_BASE_URL = os.getenv("ABACATE_PAY_BASE_URL", "https://api.abacatepay.com")

class AbacatePayClient:
    def __init__(self, api_key: str, base_url: str):
        if not api_key or api_key == "your_abacate_pay_api_key_here":
            raise ValueError("AbacatePay API key is required. Please set ABACATE_PAY_API_KEY in your .env file.")
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=self.headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                detail = e.response.text
                try:
                    detail = e.response.json()
                except Exception:
                    pass
                raise HTTPException(status_code=e.response.status_code, detail=detail)
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Service Unavailable: {e}")

    async def create_customer(self, customer_data: schemas.CustomerCreate) -> Dict[str, Any]:
        return await self._request(
            "POST",
            "/v1/customer/create",
            json=customer_data.model_dump(by_alias=True)
        )

    async def list_customers(self) -> Dict[str, Any]:
        return await self._request("GET", "/v1/customer/list")

    async def create_billing(self, billing_data: schemas.BillingCreate) -> Dict[str, Any]:
        return await self._request(
            "POST",
            "/v1/billing/create",
            json=billing_data.model_dump(by_alias=True, exclude_none=True)
        )

    async def list_billings(self) -> Dict[str, Any]:
        return await self._request("GET", "/v1/billing/list")

    async def create_pix_qr_code(self, pix_data: schemas.PixQrCodeCreate) -> Dict[str, Any]:
        return await self._request(
            "POST",
            "/v1/pixQrCode/create",
            json=pix_data.model_dump(by_alias=True, exclude_none=True)
        )

    async def check_pix_qr_code_status(self, pix_id: str) -> Dict[str, Any]:
        return await self._request("GET", f"/v1/pixQrCode/check?id={pix_id}")

    async def simulate_pix_qr_code_payment(self, pix_id: str, payment_data: schemas.PixQrCodeSimulatePayment) -> Dict[str, Any]:
        return await self._request(
            "POST",
            f"/v1/pixQrCode/simulate-payment?id={pix_id}",
            json=payment_data.model_dump(by_alias=True)
        )

abacate_pay_client = AbacatePayClient(api_key=ABACATE_PAY_API_KEY, base_url=ABACATE_PAY_BASE_URL)

def get_abacate_pay_client() -> AbacatePayClient:
    return abacate_pay_client
