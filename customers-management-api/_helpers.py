from multiprocessing import Process
from time import sleep
from logger_config import setup_logger


from _mongo_helpers import MongoManager
from _kafka_helpers import KafkaAdminWrapper, KAFKA_TOPIC

logger = setup_logger('helpers')


def check_kafka_connection() -> None:
    while True:
        try:
            kafka_admin = KafkaAdminWrapper()
            if kafka_admin.check_if_broker_is_up():
                break
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            logger.info("Retrying to connect to Kafka broker in 5 seconds...")
            sleep(5)



def check_mongo_connection() -> None:
    mongo_manager = MongoManager()

    while True:
        if mongo_manager.check_connection():
            logger.info("MongoDB connection successful.")
            break
        else:
            logger.error("MongoDB connection failed.")
            sleep(5)



def prepare_system() -> None:
    
    check_mongo_process = Process(target=check_mongo_connection)
    check_kafka_process = Process(target=check_kafka_connection)

    # Start both processes in parallel
    check_mongo_process.start()
    check_kafka_process.start()

    # Wait for both processes to complete
    check_mongo_process.join()
    check_kafka_process.join()

    kafka_admin = KafkaAdminWrapper()
    kafka_admin.create_topic(KAFKA_TOPIC)
