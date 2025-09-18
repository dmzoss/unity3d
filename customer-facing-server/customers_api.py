import logging
import sys

from fastapi import FastAPI
import uvicorn

from _request_helpers import PurchaseData, get_all_users_purchase_data, handle_user_purchase_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

api = FastAPI()

@api.get('/getAllUserBuys')
def get_all_user_buys():
    """Get all data from Kafka topic + MongoDB via the BE service."""
    logging.info("Fetching all user purchase data.")
    return get_all_users_purchase_data()



@api.post('/buy')
def buy(purchase: PurchaseData):
    logging.info(f"Processing purchase request: {purchase}")
    return handle_user_purchase_request(purchase)


if __name__ == '__main__':
    uvicorn.run(api, host='0.0.0.0', port=8000)
