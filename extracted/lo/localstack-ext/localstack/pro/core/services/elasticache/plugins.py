from localstack.packages import Package
from localstack.pro.core.packages.core import pro_package
@pro_package(name='redis')
def redis_package()->Package:from.packages import redis_package as A;return A