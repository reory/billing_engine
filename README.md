# 💷 Billing Engine — Backend‑Only Usage‑Based Billing Microservice

![Last Commit](https://img.shields.io/github/last-commit/reory/billing_engine?cacheSeconds=60)
![Repo Size](https://img.shields.io/github/repo-size/reory/billing_engine?cacheSeconds=60)
![License](https://img.shields.io/badge/License-MIT-green)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/uvicorn-2094f3?style=for-the-badge&logo=uvicorn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![RQ](https://img.shields.io/badge/RQ-FF0000?style=for-the-badge&logo=python&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger_UI-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)

A lightweight, modular, backend‑only billing engine built with FastAPI, SQLAlchemy, and a clean service‑layer architecture.
It ingests usage events, aggregates them, prices them, and generates invoices — all without any frontend or dashboard.

This project is ideal for demonstrating backend engineering skills such as:

- API design
- Background job processing
- Database modeling
- Clean architecture
- Usage metering
- Invoice generation
- Scheduling and workers

---

# ✨ Features

Record usage events (e.g., API calls, storage, workflows)

Daily usage aggregation (group + sum raw events)

Pricing engine (simple per‑unit pricing, easily extendable)

Invoice preview (estimate charges before billing period ends)

Invoice generation (creates real invoice records)

Clean service layer (routers → services → models)

Background‑safe aggregation (manual or scheduled)

SQLite for simplicity (swap for Postgres easily)

---

# 📦 Tech Stack

- FastAPI — API framework

- SQLAlchemy — ORM + models

- SQLite — local development DB

- RQ (Redis Queue) — background worker

- Redis — job queue backend

- Uvicorn — ASGI server

---

# 📁 Project Structure

```
billing_engine/
│
├── app/
│   ├── routers/
│   │   ├── usage.py
│   │   ├── invoice.py
│   │   └── aggregator.py
│   ├── services/
│   │   ├── usage_service.py
│   │   ├── invoice_service.py
│   │   └── aggregator_service.py
│   ├── models.py
|   ├── aggregator.py
|   ├── pricing.py
│   ├── schemas.py
│   ├── deps.py
│   └── database.py
│
├── tests.py/
|   ├── conftest.py
|   ├── test_aggregator.py
|   ├── test_api.py
|   ├── test_invoice.py
|   ├── test_usage.py
├── scheduler.py
├── main.py
├── worker.py
└── README.md
└── LICENSE.md
└── CONTRIBUITING.md
```

---

# 🚀 Getting Started
## Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
## Install dependencies
```bash
pip install -r requirements.txt
```
## Start Redis (required for the worker)
On Windows (WSL recommended):

```bash
redis-server
```
Start the FastAPI server
```bash
uvicorn main:app --reload
```
Your API is now live at:
```
http://127.0.0.1:8000
Swagger UI:

http://127.0.0.1:8000/docs
```
## Start the background worker
In a new terminal:

```bash
rq worker
```
## Start the scheduler (optional)
In another terminal:

```bash
python scheduler.py
```
- This triggers daily aggregation automatically.

---

# 🧪 How to Use the API (Step‑by‑Step) Swagger UI
- Record usage
- POST /usage

- Example:
* **json**
{
  "customer_id": "cust_123",
  "metric": "api_calls",
  "units": 500
}
## Run aggregation manually
POST /aggregate/run

- This groups + sums raw usage into daily totals.

## Preview an invoice
GET /invoice/preview/{customer_id}

- Returns estimated charges for the current billing period.

## Generate a real invoice
POST /invoice/{customer_id}

- Creates an invoice record in the database.

---

# 🧠 How It Works (Conceptual Overview)
Usage Ingestion
Raw events are stored exactly as they happen:

- customer

- metric

- units

- timestamp

- This keeps ingestion fast and append‑only.

## Aggregation
A background job periodically:

fetches raw events

groups them by metric + customer

sums units

writes aggregated rows

This reduces billing load and keeps invoices fast.

## Pricing Engine
A simple per‑unit pricing dictionary:

```
PRICING = {
    "api_calls": 0.0005,
    "storage_gb": 0.25,
    "workflows": 0.10,
}
```
You can easily extend this to:

tiered pricing

free allowances

per‑customer overrides

## Invoice Preview
Reads aggregated usage so far and returns:

usage totals

estimated amount

billing window

No DB writes.

## Invoice Generation
Reads aggregated usage, calculates the final amount, and writes an invoice row.

---

## 🧱 Database Models
- UsageEvent
Raw usage events.

- AggregatedUsage
Daily totals per metric.

- Invoice
Final billed amounts.

---

* **Built By Roy Peters** 😁
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Roy%20Peters-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/roy-p-74980b382/)