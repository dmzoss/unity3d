from datetime import datetime
import os
import logging
import sys

from fastapi import HTTPException
from fastapi.responses import JSONResponse
import requests
from pydantic import BaseModel, Field, constr

from _kafka_helpers import KafkaProducerWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class PurchaseData(BaseModel):
    username: constr(pattern="^[a-zA-Z0-9]+$")
    userid: constr(pattern="^[a-zA-Z0-9]+$")
    price: float = Field(gt=0)
    #! As I can see, the timestamp is automatically created on the Kafka,\
        # !need to consider removing it from the request body.
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())



def get_all_users_purchase_data() -> JSONResponse | None:
    try:
        users_purchase_service_endpoint = os.getenv("DATA_MANAGER_SERVICE")
        response = requests.get(users_purchase_service_endpoint)
        if response.status_code == 200:
            return JSONResponse(status_code=200, content=response.json())
    except Exception:
        err = {"status": "error", "message": "Failed to fetch data"}
        raise HTTPException(status_code=400, detail=err)



def handle_user_purchase_request(purchase: PurchaseData) -> JSONResponse | None:
    try:  # If Kafka is not available, we will failed to create the Producer
        kafka_producer = KafkaProducerWrapper()
        if kafka_producer.send_purchase_data(purchase.model_dump()):
            return JSONResponse(status_code=202, content={"status": "success", "data": purchase.model_dump()})

    except Exception as e:
        logging.error("Failed to send data to Kafka.")
        raise HTTPException(status_code=400, detail="Failed to send data to Kafka")
