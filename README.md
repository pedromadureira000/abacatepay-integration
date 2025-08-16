# AbacatePay Integration Project

This project provides a FastAPI backend that integrates with the AbacatePay API, allowing you to manage customers and billings.

## Initial setup

1.  Clone the repository:
    ```bash
    git clone git@github.com:pedromadureira000/abacatepay-integration.git
    cd abacatepay-integration
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up your environment variables. If you don't have a `.env` file, create one and add the following content:
    ```.env
    DATABASE_URL="sqlite:///./app.db"
    ABACATE_PAY_API_KEY="your_abacate_pay_api_key_here"
    ABACATE_PAY_BASE_URL="https://api.abacatepay.com"
    ```
    **Important:** Replace `"your_abacate_pay_api_key_here"` with your actual key from AbacatePay.

5.  Create a local user for API authentication:
    ```bash
    make create-user
    ```
    You will be prompted to enter a username and password.

## Run server locally

```bash
uvicorn src.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can access the interactive documentation at `http://127.0.0.1:8000/docs`.

## Usage example

Replace `your_username` and `your_password` with the credentials you created during setup.

### Check Authentication

```bash
curl -u your_username:your_password http://127.0.0.1:8000/check-authentication
```

### Create a Customer in AbacatePay

```bash
curl -X POST "http://127.0.0.1:8000/v1/customer/create" \
-u your_username:your_password \
-H "Content-Type: application/json" \
-d '{
  "name": "Fulano de tal",
  "cellphone": "(00) 0000-0000",
  "email": "cliente@gmail.com",
  "taxId": "123.456.789-01"
}'
```

### List Customers from AbacatePay

```bash
curl -X GET "http://127.0.0.1:8000/v1/customer/list" \
-u your_username:your_password
```

### Create a Billing in AbacatePay
```bash
curl -X POST "http://127.0.0.1:8000/v1/billing/create" \
-u your_username:your_password \
-H "Content-Type: application/json" \
-d '{
  "customerId": "cust_abcdefghij",
  "methods": ["PIX"],
  "frequency": "ONE_TIME",
  "products": [
    {
      "externalId": "prod-1234",
      "name": "Assinatura de Programa Fitness",
      "description": "Acesso ao programa fitness premium por 1 mês.",
      "quantity": 1,
      "price": 2000
    }
  ],
  "returnUrl": "https://example.com/billing",
  "completionUrl": "https://example.com/completion"
}'
```
You can also send the customer like this instead:
```
  "customer": {
    "name": "Daniel Lima",
    "cellphone": "(11) 4002-8922",
    "email": "daniel_lima@abacatepay.com",
    "taxId": "123.456.789-01"
  },
```

### List Billings from AbacatePay

```bash
curl -X GET "http://127.0.0.1:8000/v1/billing/list" \
-u your_username:your_password
```

### Create a PIX QR Code in AbacatePay

```bash
curl -X POST "http://127.0.0.1:8000/v1/pixQrCode/create" \
-u your_username:your_password \
-H "Content-Type: application/json" \
-d '{
  "amount": 123,
  "expiresIn": 123,
  "description": "Test PIX QR Code",
  "customer": {
    "name": "Daniel Lima",
    "cellphone": "(11) 4002-8922",
    "email": "daniel_lima@abacatepay.com",
    "taxId": "123.456.789-01"
  },
  "metadata": {
    "externalId": "123"
  }
}'
```

### Check PIX QR Code Status from AbacatePay

Replace `{pix_qr_code_id}` with the actual ID from the creation response.

```bash
curl -X GET "http://127.0.0.1:8000/v1/pixQrCode/check/{pix_qr_code_id}" \
-u your_username:your_password
```

### Simulate PIX QR Code Payment in AbacatePay

Replace `{pix_qr_code_id}` with the actual ID from the creation response.

```bash
curl -X POST "http://127.0.0.1:8000/v1/pixQrCode/simulate-payment/{pix_qr_code_id}" \
-u your_username:your_password \
-H "Content-Type: application/json" \
-d '{
  "metadata": {}
}'
```

# Webhook Integration

This project includes an endpoint to receive webhook notifications from AbacatePay.

## Setup

1.  Add the webhook secret to your `.env` file:
    ```.env
    WEBHOOK_SECRET="your_webhook_secret_here"
    ```
    Replace `"your_webhook_secret_here"` with a strong, unique secret string.

2.  Configure the webhook URL in your AbacatePay dashboard. The URL should include the secret as a query parameter.
    Example: `https://your-api-domain.com/webhook/abacatepay?webhookSecret=your_webhook_secret_here`

## Usage Example

You can simulate a webhook call using `curl`.

### Simulate `billing.paid` (PIX QR Code)

```bash
curl -X POST "http://127.0.0.1:8000/webhook/abacatepay?webhookSecret=your_webhook_secret_here" \
-H "Content-Type: application/json" \
-d '{
  "data": {
    "payment": {
      "amount": 1000,
      "fee": 80,
      "method": "PIX"
    },
    "pixQrCode": {
      "amount": 1000,
      "id": "pix_char_mXTWdj6sABWnc4uL2Rh1r6tb",
      "kind": "PIX",
      "status": "PAID"
    }
  },
  "devMode": false,
  "event": "billing.paid"
}'
```

### Simulate `billing.paid` (Billing)

```bash
curl -X POST "http://127.0.0.1:8000/webhook/abacatepay?webhookSecret=your_webhook_secret_here" \
-H "Content-Type: application/json" \
-d '{
  "data": {
    "payment": {
      "amount": 1000,
      "fee": 80,
      "method": "PIX"
    },
    "billing": {
      "amount": 1000,
      "couponsUsed": [],
      "customer": {
        "id": "cust_4hnLDN3YfUWrwQBQKYMwL6Ar",
        "metadata": {
          "cellphone": "11111111111",
          "email": "christopher@abacatepay.com",
          "name": "Christopher Ribeiro",
          "taxId": "12345678901"
        }
      },
      "frequency": "ONE_TIME",
      "id": "bill_QgW1BT3uzaDGR3ANKgmmmabZ",
      "kind": [
        "PIX"
      ],
      "paidAmount": 1000,
      "products": [
        {
          "externalId": "123",
          "id": "prod_RGKGsjBWsJwRn1mHyGMFJNjP",
          "quantity": 1
        }
      ],
      "status": "PAID"
    }
  },
  "devMode": false,
  "event": "billing.paid"
}'
```
