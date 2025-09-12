from localstack.packages import Package
from localstack.pro.core.packages.core import pro_package
@pro_package(name='kafka')
def kafka_package():from localstack.pro.core.services.kafka.packages import kafka_package as A;return A
@pro_package(name='kafka_v2')
def kafka_package_v2():from localstack.pro.core.services.kafka.v2.packages import kafka_package as A;return A