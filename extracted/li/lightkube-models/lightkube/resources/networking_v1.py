# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import networking_v1 as m_networking_v1


class IngressClass(res.GlobalResource, m_networking_v1.IngressClass):
    """* **Extends**: ``models.networking_v1.IngressClass``
       * **Type**: Global Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list`, `patch`, `create`, `replace`, `watch`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('networking.k8s.io', 'v1', 'IngressClass'),
        plural='ingressclasses',
        verbs=['delete', 'deletecollection', 'get', 'list', 'patch', 'post', 'put', 'watch'],
    )


class IngressStatus(res.NamespacedSubResource, m_networking_v1.Ingress):
    """* **Extends**: ``models.networking_v1.Ingress``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('networking.k8s.io', 'v1', 'Ingress'),
        parent=res.ResourceDef('networking.k8s.io', 'v1', 'Ingress'),
        plural='ingresses',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class Ingress(res.NamespacedResourceG, m_networking_v1.Ingress):
    """* **Extends**: ``models.networking_v1.Ingress``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Status**: ``IngressStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('networking.k8s.io', 'v1', 'Ingress'),
        plural='ingresses',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Status: ClassVar = IngressStatus


class NetworkPolicy(res.NamespacedResourceG, m_networking_v1.NetworkPolicy):
    """* **Extends**: ``models.networking_v1.NetworkPolicy``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('networking.k8s.io', 'v1', 'NetworkPolicy'),
        plural='networkpolicies',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

