import logging
import sys
from _kafka_helpers import KafkaConsumerWrapper
from _mongo_helpers import MongoHelper, MONGODB_COLLECTION

# Configure logging to write to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger('purchases_helper')




def syncer():
    #* Check what is the last message that exists on the MongoDB Documents
    #* Then, check if that message is the last one on the Kafka topic
    #* If not, consume messages from Kafka and store them in MongoDB until the last by offset & seek
    consumer = KafkaConsumerWrapper()
    mongo_helper = MongoHelper()
    logger.info("Starting sync process...")
    while True:
        for partition in consumer.get_partitions_by_topic():

            partition_offset = consumer.get_partition_offset(partition)

            last_purchase = mongo_helper.get_the_last_message(partition)

            if last_purchase:
                last_purchase = last_purchase[0]["_offset"]
            else:
                last_purchase = -1 #empty collection
            logger.info(f"Last purchase after IF {partition=}: {last_purchase=}")

            if last_purchase + 1 == partition_offset:
                break
            else:
                logger.info(f"Syncing data from offset {last_purchase} for partition {partition}")
                data = consumer.get_data_from_specific_offset(partition, last_purchase + 1)
                mongo_helper.insert_multi_documents(MONGODB_COLLECTION, data)
                logger.info(f"Successfully synced {len(data)} records from partition {partition}")
