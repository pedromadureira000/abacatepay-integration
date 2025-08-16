# Production Deployment Guide

This guide outlines the steps to deploy the AbacatePay Integration API in a production environment using Docker, Docker Compose, PostgreSQL, Gunicorn, and Nginx.

## Prerequisites

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

## 1. Configure Environment Variables

1.  Copy the sample environment file:
    ```bash
    cp contrib/env-sample .env
    ```

2.  Edit the `.env` file and fill in the required values. For a Docker Compose deployment, your `DATABASE_URL` should point to the database service name (`db`):

    ```.env
    # PostgreSQL Database Configuration
    DATABASE_URL="postgresql://abacatepay_user:abacatepay_password@db:5432/abacatepay_db"

    # AbacatePay API Configuration
    ABACATE_PAY_API_KEY="your_production_abacate_pay_api_key"
    ABACATE_PAY_BASE_URL="https://api.abacatepay.com"

    # Webhook Configuration
    WEBHOOK_SECRET="your_strong_production_webhook_secret"
    ```
    **Note:** The database credentials in `.env` must match the `POSTGRES_USER` and `POSTGRES_PASSWORD` values in `docker-compose.yml`.

## 2. Build and Run the Services

From the root of the project, run the following command to build the images and start the containers in detached mode:

```bash
sudo docker compose up -d --build
```

This will start three services:
-   `db`: The PostgreSQL database.
-   `api`: The FastAPI application served by Gunicorn.
-   `nginx`: The Nginx reverse proxy, which exposes the API on port 80.

## 3. Create an API User

To interact with the protected API endpoints, you need to create an initial user. Run the `make create-user` command inside the running `api` container:

```bash
docker compose exec api make create-user
```

You will be prompted to enter a username and password.

## 4. Verify the Deployment

You can check if the API is running by sending a request to the `/check-authentication` endpoint through the Nginx proxy on port 80.

```bash
curl -u your_username:your_password http://localhost/check-authentication
```

You should receive a success message. Your API is now deployed and accessible on `http://localhost`.

## Managing the Database

The `docker-compose.yml` configuration automatically creates the `abacatepay_db` database. If you need to connect to it manually, you can use the following command:

```bash
docker compose exec -it db psql -U abacatepay_user -d abacatepay_db
```
You will be prompted for the password (`abacatepay_password` from your configuration).
```
