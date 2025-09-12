from localstack.runtime import hooks
STATE_SERIALIZATION_BACKEND_NAME='avro'
@hooks.on_pro_infra_start()
def register_avro_serialization_backend():from localstack.pro.core.persistence.avro.codec import AvroDecoder as B,AvroEncoder as C;from localstack.state import codecs as A;A.ENCODERS[STATE_SERIALIZATION_BACKEND_NAME]=C;A.DECODERS[STATE_SERIALIZATION_BACKEND_NAME]=B