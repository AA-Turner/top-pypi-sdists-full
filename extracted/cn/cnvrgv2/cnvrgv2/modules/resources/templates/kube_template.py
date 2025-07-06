from cnvrgv2.config import routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.casters import safe_cast
from cnvrgv2.utils.validators import attributes_validator, validate_gpu


class KubeTemplate(DynamicAttributes):
    available_attributes = {
        "slug": str,
        "title": str,
        "cpu": float,
        "memory": float,
        "users": list,
        "gpu": dict,
        "mig_device": str,
        "spark_config": str,
        "gaudi": float,
        "is_private": bool,
        "compute_type": str,
        "labels": list,
        "taints": list,
        "worker": dict,
        "cluster_title": str,
        "num_executors": int,
        "templates_ids": list
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = Context(context=context)

        # Set current context scope to current template
        if slug:
            self._context.set_scope(SCOPE.TEMPLATE, slug)

        scope = self._context.get_scope(SCOPE.TEMPLATE)

        self._proxy = Proxy(context=self._context)
        self._route = routes.TEMPLATE_BASE.format(
            scope["organization"],
            'clusters',
            scope['resource'],
            scope["template"]
        )
        self._attributes = attributes or {}
        self.slug = scope["template"]

    def update(self, **kwargs):
        """
        Updates given attributes of a kube compute template

        @param kwargs: A list of optional attributes to update
            title: Name of the kube template
            cpu: CPU cores of the kube template
            memory: RAM memory of the kube template
            users: Users with access to the kube template
            gpu: GPU cores of the kube template
            shm: Shared memory (RAM) count of the kube template
            huge_pages: Gaudi huge pages count of the kube template
            gaudi: Gaudi accelerators num of the kube template
            is_private: is the kube template private or public
            spark_config: A dict of spark executor properties
            mig_device: mig device type for the kube template
            labels: labels of the kube template
            taints: taints of the kube template
            worker_num_executors: num of workers for the kube template
            worker_cpu: worker CPU cores of the kube template
            worker_memory: worker RAM memory of the kube template
            worker_huge_pages: worker Gaudi huge pages count of the kube template
            worker_gpu: worker GPU cores of the kube template
            worker_mig_device: worker mig device type
            worker_labels: worker labels
            worker_taints: worker taints

        """

        updated_attributes = {
            **kwargs,
        }

        parent_attributes = {
            "cpu": float,
            "memory": float,
            "labels": str,
            "taints": str,
            "gaudi": float,
            "shm": float,
            "huge_pages": float
        }

        for key in parent_attributes:
            if key in kwargs:
                updated_attributes['parent_' + key] = safe_cast(kwargs[key], parent_attributes[key], kwargs[key])
                updated_attributes.pop(key, None)

        if kwargs.get("gpu") is not None or kwargs.get("mig_device"):
            updated_attributes["parent_gpu"] = {
                "count": float(kwargs.get("gpu")) if kwargs.get("gpu") is not None
                else self._attributes["gpu"],
                "mig_device": kwargs.get("mig_device") if kwargs.get("mig_device") is not None
                else self._attributes["mig_device"]
            }
            updated_attributes.pop('mig_device', None)
            updated_attributes.pop('gpu', None)
            validate_gpu(updated_attributes["parent_gpu"])

        if kwargs.get("worker_gpu") or kwargs.get("worker_mig_device"):
            updated_attributes["worker_gpu"] = {
                "count": kwargs.get("worker_gpu") if kwargs.get("worker_gpu")
                else self._attributes["worker"]["gpu"],
                "mig_device": kwargs.get("worker_mig_device") if kwargs.get("worker_mig_device")
                else self._attributes["worker"]["mig_device"]
            }
            updated_attributes.pop('worker_gpu', None)
            updated_attributes.pop('worker_mig_device', None)
            validate_gpu(updated_attributes["worker_gpu"])

        if "is_private" in kwargs:
            updated_attributes["is_private"] = kwargs["is_private"]

        attributes_validator(
            {**self.available_attributes,
             "parent_cpu": float,
             "parent_memory": float,
             "parent_labels": str,
             "parent_taints": str,
             "parent_gpu": dict,
             "worker_gpu": dict,
             "worker_num_executors": int,
             "worker_cpu": float,
             "worker_huge_pages": float,
             "worker_memory": float,
             "worker_shm": float,
             "worker_labels": str,
             "worker_taints": str,
             "parent_shm": float,
             "parent_huge_pages": float,
             "parent_gaudi": float,
             }, updated_attributes,
        )

        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.PUT,
            payload={"template_slug": self.slug, **updated_attributes})

        self._attributes = response.attributes

    def save(self):
        """
        In case of any attribute change, saves the changes
        """
        self.update(**self._attributes)

    def delete(self):
        """
        Deletes the current template
        @return: None
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)
