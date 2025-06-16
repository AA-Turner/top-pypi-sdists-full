from .base import BaseAPIModelStub
from .audit_event import AuditEventStub
from .brief import BriefStub
from .brief_response import BriefResponseStub
from .communication import CommunicationStub, CommunicationMessageStub
from .framework import FrameworkStub
from .framework_agreement import FrameworkAgreementStub
from .lot import LotStub, as_a_service_lots, cloud_lots, dos_lots
from .lot_pricing import LotPricingStub
from .lot_questions_response import LotQuestionsResponseStub
from .services import ArchivedServiceStub, DraftServiceStub, ServiceStub
from .supplier import SupplierStub, CENTRAL_DIGITAL_PLATFORM_DATA
from .supplier_framework import SupplierFrameworkStub
from .technical_ability_certificate import TechnicalAbilityCertificateStub


# TODO: Flesh out the stubs below and move to their own modules


class DirectAwardProjectStub(BaseAPIModelStub):
    resource_name = "project"
    default_data = {}


class DirectAwardSearchStub(BaseAPIModelStub):
    resource_name = "search"
    default_data = {}


class OutcomeStub(BaseAPIModelStub):
    resource_name = "outcome"
    default_data = {}


class UserStub(BaseAPIModelStub):
    resource_name = "users"
    default_data = {}
