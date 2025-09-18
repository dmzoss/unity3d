# from flask import Flask, request, jsonify
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import logging
import sys
import uvicorn

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


@app.get('/getAllUserBuys')
def home():
    # ! need to return the all data from the kafka topic + mongo db
    # ! the data should arrived by the Customers management API
    return get_all_users_purchase_data()
    pass



@app.post('/buy')
def buy(purchase: PurchaseData):
    try:
        logging.info(f"Received purchase data: {purchase}")
        handle_user_purchase_request(purchase)
        return JSONResponse(status_code=201, content={"status": "success", "data": purchase.model_dump()})
    except Exception as e:
        logging.error(f"Error processing purchase request: {e}")
        err = "Cannot process the request, please try again later"
        raise HTTPException(status_code=400, detail=err)
    

if __name__ == '__main__':
    prepare_system()
    uvicorn.run(app, host='0.0.0.0', port=8002)