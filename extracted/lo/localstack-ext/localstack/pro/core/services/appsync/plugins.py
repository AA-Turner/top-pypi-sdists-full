from localstack.packages import Package
from localstack.pro.core.packages.core import pro_package
@pro_package(name='appsync-utils-js')
def appsync_utils_package():from localstack.pro.core.services.appsync.packages import appsync_utils_package as A;return A