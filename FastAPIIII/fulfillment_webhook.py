from fastapi import FastAPI, Header, Request, Response, Query, status, HTTPException, Path, Form, File, UploadFile, BackgroundTasks
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Added BackgroundTasks to the import list above ^

app = FastAPI(title='Logistics Fulfillment Webhook API', description='This is a Logistics Fulfillment Webhook API', version='1.0.0')

# --- Nested Pydantic Models for request and response validation

class ShippedItem(BaseModel):
    sku: str = Field(..., examples=["TECH-MK-001"])
    quantity: int = Field(..., examples=[1], gt=0)

class DeliveryManifest(BaseModel):
    order_id: str = Field(..., examples=["ORD-99281"])
    tracking_number: str = Field(..., examples=["TRK-XYZ-12345"])
    carrier: str = Field(..., examples=["DHL Express"])  # Fixed: changed '=' to ':'
    shipped_at: datetime = Field(default_factory=datetime.utcnow)
    items: List[ShippedItem]

# Asynchronous Background Task

def send_shipping_email_to_customer(payload: DeliveryManifest):
    # Webhooks must respond quickly. Heavy operations run in the background.
    print(f"\n[BACKGROUND PROCESSING] Initialising workflow for Order {payload.order_id}")
    print(f"[EMAIL SERVICE] Sent tracking link ({payload.tracking_number}) via {payload.carrier} to Customer")
    print(f"[INVENTORY UPDATE] Deducting {len(payload.items)} unique SKUs from stock records.\n")

# Webhook Endpoint
@app.post("/webhooks/shipping-update", status_code=status.HTTP_202_ACCEPTED)
async def receive_shipping_update(
    payload: DeliveryManifest,
    background_tasks: BackgroundTasks,
    x_secure_token: str = Header(..., description="Security key to verify the sender")
):
    SECRET_WEBHOOK_KEY = "SUPER_SECRET_STORE_KEY_abc123"

    if x_secure_token != SECRET_WEBHOOK_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Security verification failed. Invalid webhook token."
        )
    
    # Hand off the heavy lifting to our background worker task.
    background_tasks.add_task(send_shipping_email_to_customer, payload)
    
    return {
        "status": "Success",
        "message": "Webhook payload received safely. Background parsing initiated."
    }
