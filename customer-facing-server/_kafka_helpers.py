import os
import logging
import sys
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient

from utils import serializer


KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class KafkaProducerWrapper:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=serializer
        )
        self.topic = KAFKA_TOPIC


    def get_producer(self) -> KafkaProducer:
        return self.producer


    def send_purchase_data(self, purchase_data: dict) -> bool:
        """Send purchase data to Kafka topic."""

        logging.info(f"Sending purchase data to Kafka: {purchase_data}")

        try:
            self.get_producer().send(topic=self.topic, value=purchase_data)
            self.producer.flush()
            self.producer.close()
            return True

        except Exception as e:
            logging.error(f"Error sending message to Kafka: {str(e)}")
            return False


class KafkaAdminWrapper:
    def __init__(self):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=os.getenv("KAFKA_BROKER"),
            client_id='admin-client'
        )


    def check_if_broker_is_up(self) -> bool:
        """Check if the Kafka broker is up and reachable."""
        try:
            # Attempt to retrieve cluster metadata
            self.admin_client.list_topics()
            logging.info("Kafka broker is up and reachable.")
            return True
        except Exception as e:
            logging.error(f"Failed to connect to Kafka broker: {str(e)}")
            return False
