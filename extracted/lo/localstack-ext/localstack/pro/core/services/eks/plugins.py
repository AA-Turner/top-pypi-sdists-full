from localstack.packages import Package
from localstack.pro.core.packages.core import pro_package
from localstack.pro.core.services.ssm import hooks as ssm_hooks
@ssm_hooks.register_public_parameters()
def register_eks_ssm_params(custom_resolvers):from localstack.pro.core.services.eks.ssm_params import register_eks_resolvers as A;A(custom_resolvers)
@pro_package(name='k3d')
def k3d_package()->Package:from localstack.pro.core.services.eks.packages import k3d_package as A;return A
@pro_package(name='velero')
def velero_package()->Package:from localstack.pro.core.services.eks.packages import velero_package as A;return A