import os
import pymongo
from logger_config import setup_logger

logger = setup_logger('mongo_helpers')

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION")


class MongoHelper:
    def __init__(self, uri=MONGODB_URI, db_name=MONGODB_DB):
        self.uri = uri
        self.db_name = db_name
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]


    def get_collection(self, collection_name):
        return self.db[collection_name]

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id

    def insert_multi_documents(self, collection_name: str, documents: list):
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return result.inserted_ids

    def get_collection_data(self, collection_name, query={}):
        collection = self.get_collection(collection_name)
        return list(collection.find(query))



    def save_message(self, message):
        """Save Kafka message to MongoDB."""
        collection = self.get_collection(MONGODB_COLLECTION)
        document = message.value  # Assuming message value is already a dict
        collection.insert_one(document)
        

    def get_the_last_message(self, partition: int) -> list:
        """Get the last message stored in MongoDB by offset."""

        collection = self.get_collection(MONGODB_COLLECTION)
        return list(collection.find({"_partition": partition}).sort("_offset", pymongo.DESCENDING).limit(1))


class MongoManager(MongoHelper):
    def __init__(self, uri=MONGODB_URI, db_name=MONGODB_DB):
        super().__init__(uri, db_name)


    def check_connection(self) -> bool:
        """Check if the connection to MongoDB is successful."""
        try:
            # The ping command is cheap and does not require auth.
            logger.info(f"Checking MongoDB ({self.uri}) connection...")
            self.client.admin.command('ping')
            return True
        except pymongo.errors.ConnectionFailure:
            return False
