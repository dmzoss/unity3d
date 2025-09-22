from multiprocessing import Process
from logger_config import setup_logger

logger = setup_logger('api')

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

from _mongo_helpers import MongoHelper, MONGODB_COLLECTION
from _purchases_helpers import syncer
from _helpers import prepare_system

api = FastAPI()


@api.get('/')
def home() -> JSONResponse:
    """Get all data from MongoDB."""
    data = MongoHelper().get_collection_data(MONGODB_COLLECTION)
    data_to_return = []
    for document in data:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string for JSON serialization
        data_to_return.append(document)
    return JSONResponse(status_code=200, content=data_to_return)




if __name__ == '__main__':
    prepare_system()


    p = Process(target=syncer)
    p.start()
    uvicorn.run(api, host='0.0.0.0', port=8001)