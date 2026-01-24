from localstack.packages import Package
from localstack.pro.core.packages.core import pro_package
@pro_package(name='kafka')
def kafka_package()->Package:from localstack.pro.core.services.kafka.packages import kafka_package as A;return A
@pro_package(name='kafka_legacy')
def kafka_package_legacy()->Package:from localstack.pro.core.services.kafka.legacy.packages import kafka_package as A;return A