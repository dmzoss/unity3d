from multiprocessing import Process
from time import sleep
import logging
import sys

from _kafka_helpers import KafkaAdminWrapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def check_kafka_connection():
    while True:
        try:
            kafka_admin = KafkaAdminWrapper()
            if kafka_admin.check_if_broker_is_up():
                break
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            logging.info("Retrying to connect to Kafka broker in 5 seconds...")
            sleep(5)
            
            
def prepare_system():
    

    check_kafka_process = Process(target=check_kafka_connection)

    check_kafka_process.start()
    check_kafka_process.join()

