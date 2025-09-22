import logging
import sys
import uvicorn

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from _helpers import prepare_system
from _request_helpers import PurchaseData, get_all_users_purchase_data, handle_user_purchase_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI()


@app.get('/getAllUserBuys', response_model=None)
def home() -> JSONResponse | None:
    """Get all data from Kafka topic + MongoDB via the BE service."""
    return get_all_users_purchase_data()



@app.post('/buy', response_model=None)
def buy(purchase: PurchaseData):
    return handle_user_purchase_request(purchase)



if __name__ == '__main__':
    prepare_system()
    uvicorn.run(app, host='0.0.0.0', port=8002)