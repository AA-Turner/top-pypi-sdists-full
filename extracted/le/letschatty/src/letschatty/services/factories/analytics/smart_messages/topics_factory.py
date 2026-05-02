from letschatty.models.analytics.smart_messages.topic import Topic
from letschatty.models.analytics.smart_messages.topic_message import MessageTopic
import logging
logger = logging.getLogger("logger")
class TopicFactory:
    
    @staticmethod
    def instantiate_topic(topic_data: dict) -> Topic:
        topic_messages = []
        for m in topic_data['messages']:
            logger.debug(f"m: {m}, type: {type(m)}")
            m_ = MessageTopic(**m)
            for topic_message in topic_messages:
                m_.check_message_conflict(topic_message)
            topic_messages.append(m_)
        topic_data['messages'] = topic_messages
        return Topic(**topic_data)
