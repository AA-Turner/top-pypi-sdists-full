from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.config import error_messages, routes
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.validators import attributes_validator, validate_gpu, validate_template_type
from cnvrgv2.modules.resources.templates.kube_template import KubeTemplate
from cnvrgv2.utils.casters import safe_cast

required_attributes = [
    'title',
    'parent_cpu',
    'parent_memory',
]


class KubeTemplatesClient:
    def __init__(self, context=None):
        self._context = Context(context=context)
        scope = self._context.get_scope(SCOPE.RESOURCE)
        self._proxy = Proxy(context=self._context)
        self._route = routes.TEMPLATES_BASE.format(scope["organization"], 'clusters', scope['resource'])

    def list(self, sort="-id"):
        """
        List all kube compute templates in a specific resource
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields kube compute templates objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=KubeTemplate,
            sort=sort,
        )

    def get(self, slug):
        """
        Retrieves a kube compute template by the given slug
        @param slug: The slug of the requested kube compute template
        @return: kube compute template object
        """
        if not slug or not isinstance(slug, str):
            raise CnvrgArgumentsError(error_messages.TEMPLATE_GET_FAULTY_SLUG)

        return KubeTemplate(context=self._context, slug=slug)

    def create(
            self,
            title,
            cpu,
            memory,
            **kwargs
    ):
        """

        @param title: Name of the new kube template
        @param cpu: CPU cores of the new kube template
        @param memory: RAM memory of the new kube template
        @param kwargs: A list of optional attributes for creation
            gpu: GPU cores of the new kube template
            gaudi: Gaudi accelerators num of the new kube template
            huge_pages: Gaudi huge pages count of the kube template
            is_private: is the new kube template private or public
            users: Users with access to the new kube template
            mig_device: mig device type for the new kube template
            shm: Shared memory (RAM) count of the kube template
            template_type: template type of the new kube template
            labels: labels of the new kube template
            taints: taints of the new kube template
            worker_num_executors: num of workers for the new kube template
            worker_cpu: worker CPU cores of the new kube template
            worker_memory: worker RAM memory of the new kube template
            worker_gpu: worker GPU cores of the new kube template
            worker_mig_device: worker mig device type
            worker_labels: worker labels
            worker_taints: worker taints

        @return: The newly created kube template
        """

        formatted_attributes = {
            "title": title,
            "type": kwargs.get("template_type") or 'regular',
            "parent_cpu": float(cpu),
            "parent_memory": float(memory),
            "parent_labels": kwargs.get("labels"),
            "parent_taints": kwargs.get("taints"),
            "parent_shm": safe_cast(kwargs.get("shm"), float),
            "parent_gaudi": safe_cast(kwargs.get("gaudi"), float),
            "parent_huge_pages": safe_cast(kwargs.get("huge_pages"), float),
            **kwargs,
            "parent_gpu": {
                "count": safe_cast(kwargs.get("gpu"), float),
                "mig_device": kwargs.get("mig_device")
            },
            "worker_gpu": {
                "count": safe_cast(kwargs.get("worker_gpu"), float),
                "mig_device": kwargs.get("worker_mig_device"),
            }
        }
        # The cnvrg api requires cpu and memory of the parent, For other templates - parent and/or worker.
        # for pytorch template - we need to define only worker, but only worker is not valid.
        # so we convert parent into worker and send it to the api.
        if kwargs.get("type") == "pytorch":
            formatted_attributes["worker_cpu"] = safe_cast(cpu, float)
            formatted_attributes["worker_memory"] = safe_cast(memory, float)
            formatted_attributes["worker_gpu"] = {
                "count": safe_cast(kwargs.get("gpu"), float),
                "mig_device": kwargs.get("mig_device"),
            }

        formatted_attributes.pop('worker_mig_device', None)
        formatted_attributes.pop('mig_device', None)
        formatted_attributes.pop('gpu', None)
        formatted_attributes.pop('labels', None)
        formatted_attributes.pop('taints', None)
        formatted_attributes.pop('shm', None)
        formatted_attributes.pop('huge_pages', None)
        formatted_attributes.pop('gaudi', None)

        attributes_validator(
            {
                **KubeTemplate.available_attributes,
                # These are being saved in server with the parent_ suffix,
                # so they appear without it in available attributes as well.
                "parent_cpu": float,
                "parent_memory": float,
                "parent_labels": str,
                "parent_taints": str,
                "parent_gpu": dict,
                "worker_gpu": dict,
                "type": str,
                "worker_num_executors": int,
                "worker_huge_pages": float,
                "worker_cpu": float,
                "worker_memory": float,
                "worker_labels": str,
                "worker_taints": str,
                "parent_shm": float,
                "worker_shm": float,
                "parent_huge_pages": float,
                "parent_gaudi": float,
            },
            formatted_attributes,
            required_attributes
        )

        # Instance specific validation
        validate_gpu(formatted_attributes["parent_gpu"])
        validate_gpu(formatted_attributes["worker_gpu"])
        validate_template_type(formatted_attributes["type"])

        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type='kube_template', attributes=formatted_attributes)
        )

        slug = response.attributes['slug']
        return KubeTemplate(
            context=self._context,
            slug=slug,
            attributes=response.attributes
        )
