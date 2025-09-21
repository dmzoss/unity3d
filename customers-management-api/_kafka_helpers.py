import os
import json
from kafka import KafkaConsumer, TopicPartition
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError
from logger_config import setup_logger

logger = setup_logger('kafka_helpers')

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

class NonTopicConsumer():
    def __init__(self):
        self.consumer = KafkaConsumer(
            bootstrap_servers=os.getenv("KAFKA_BROKER"),
            enable_auto_commit=False,  # manual control
            auto_offset_reset='earliest'  # fallback if offset not found
        )
    def get_consumer(self):
        return self.consumer
    
class KafkaConsumerWrapper:
    def __init__(self, topic=None):
        self.topic = topic or KAFKA_TOPIC
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=os.getenv("KAFKA_BROKER"),
            auto_offset_reset='earliest',
        )


    def get_consumer(self):
        return self.consumer


    def get_partitions_by_topic(self) -> list:
        """Get the list of partitions for the topic."""
        return list(self.consumer.partitions_for_topic(self.topic))


    def get_partition_offset(self, partition: int) -> int:
        """Get the latest offset for a specific partition of the topic."""
        tp = TopicPartition(self.topic, partition)
        return self.consumer.end_offsets([tp])[tp]


    def get_partitions_offset(self) -> dict:
        """Get the latest offsets for all partitions of the topic."""
        offsets = {}
        partitions = self.consumer.partitions_for_topic(self.topic)
        for p in partitions:
            tp = TopicPartition(self.topic, p)
            # print(self.consumer.beginning_offsets([tp])[tp], self.consumer.end_offsets([tp])[tp])
            offsets[p] = self.consumer.end_offsets([tp])[tp]

        return offsets


    def get_data_from_specific_offset(self, partition: int, offset: int) -> list:
        """Get data from a specific partition and offset."""
        c = NonTopicConsumer().get_consumer()
        tp = TopicPartition(self.topic, partition)
        end_offset = c.end_offsets([tp])[tp]
        c.assign([tp])
        c.seek(tp, offset)

        data = []
        for msg in c:
            msg_dict = json.loads(msg.value.decode())
            msg_dict['_partition'] = msg.partition
            msg_dict['_offset'] = msg.offset
            data.append(msg_dict)
            # if is the last message, break the loop (need +1 because the offset is always +1 for the incoming message)
            if msg.offset + 1 == end_offset:
                break

        c.close()
        return data


class KafkaAdminWrapper:
    def __init__(self):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=os.getenv("KAFKA_BROKER"),
            client_id='admin-client'
        )

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        """Create a Kafka topic."""
        try:
            topic_list = [
                NewTopic(
                    name=topic_name,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor
                )
            ]
            self.admin_client.create_topics(new_topics=topic_list, validate_only=False)
            logger.info(f"Topic '{topic_name}' created successfully.")
        except TopicAlreadyExistsError:
            logger.info(f"Topic '{topic_name}' already exists.")
        finally:
            self.admin_client.close()


    def check_if_broker_is_up(self) -> bool:
        """Check if the Kafka broker is reachable."""
        try:
            # Attempt to list topics to check connectivity
            topics = self.admin_client.list_topics()
            logger.info(f"Connected to Kafka broker. Available topics: {topics}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Kafka broker: {e}")
            return False

# Example usage
if __name__ == '__main__':
    consumer = KafkaConsumerWrapper().get_consumer()
    # print(KafkaConsumerWrapper().get_partitions_offset())
    # # print(KafkaConsumerWrapper().get_partitions_by_topic())
    # print(KafkaConsumerWrapper().get_data_from_specific_offset(0, 74700))  # start_offsets = {0: 74700}  # optional: specify starting offset per partition
    print('DONE')
    consumer.close()
