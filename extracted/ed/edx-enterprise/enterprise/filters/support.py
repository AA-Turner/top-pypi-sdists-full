"""
Pipeline steps for the support views filters.
"""
from crum import get_current_request
from openedx_filters.filters import PipelineStep

# This import will be replaced with an internal path in ENT-11576 when
# enterprise_support is migrated into edx-enterprise.
try:
    from openedx.features.enterprise_support.api import enterprise_customer_for_request
except ImportError:
    enterprise_customer_for_request = None


class SupportContactEnterpriseTagStep(PipelineStep):
    """
    Append a support-ticket tag for linked customer-account requests.

    This step is intended to be registered as a pipeline step for the
    ``org.openedx.learning.support.contact.context.requested.v1`` filter.
    """

    def run_filter(self, context):  # pylint: disable=arguments-differ
        """
        Append 'enterprise_learner' to context['tags'] if the requester is linked to a customer account.
        """
        request = get_current_request()
        customer = enterprise_customer_for_request(request)
        tags = context.get('tags', [])
        if customer and 'enterprise_learner' not in tags:
            context = {**context, 'tags': [*tags, 'enterprise_learner']}

        return {'context': context}
