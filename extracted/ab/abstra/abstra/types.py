from mailparser import MailParser

from abstra_internals.contracts_generated import (
    CloudApiCliModelsBankStatementResponse as BankStatementResponse,
)
from abstra_internals.contracts_generated import (
    CloudApiCliModelsBoletoResponse as BoletoResponse,
)
from abstra_internals.contracts_generated import (
    CloudApiCliModelsInvoiceResponse as InvoiceResponse,
)
from abstra_internals.contracts_generated import (
    CloudApiCliModelsNfeResponse as NfeResponse,
)
from abstra_internals.contracts_generated import (
    CloudApiCliModelsNfseResponse as NfseResponse,
)
from abstra_internals.contracts_generated import (
    CloudApiCliModelsUsDriverLicenseResponse as UsDriverLicenseResponse,
)
from abstra_internals.contracts_generated import (
    CloudApiCliModelsUsPassportResponse as UsPassportResponse,
)
from abstra_internals.controllers.sdk.sdk_ai import Format, Prompt
from abstra_internals.entities.forms.form_state import State
from abstra_internals.entities.forms.steps import (
    ComputationStep,
    GeneratorStep,
    PageStep,
    Step,
)
from abstra_internals.entities.forms.template import (
    BackButton,
    Button,
    ExitButton,
    NextButton,
    Template,
    TemplateFunction,
    TemplateGenerator,
    TemplateGeneratorFunction,
    TemplateWithButtons,
)
from abstra_internals.entities.forms.widgets.library.CardsInput import CardOption
from abstra_internals.entities.forms.widgets.widget_base import (
    InputWidget,
    LabelValueDict,
    OutputWidget,
    Widget,
)
from abstra_internals.interface.sdk.forms.deprecated.widgets.response_types import (
    AppointmentSlot,
    FileResponse,
    PhoneResponse,
)
from abstra_internals.interface.sdk.forms.deprecated.widgets.widget_base import (
    AbstraOption,
    LabelValueOption,
)
from abstra_internals.interface.sdk.forms.form import Runnable
from abstra_internals.interface.sdk.tables.api import Row as TableRow
from abstra_internals.interface.sdk.tables.comparators import Comparator
from abstra_internals.repositories.connectors import AccessTokenDTO
from abstra_internals.repositories.tasks import TaskDTO, TaskPayload
from abstra_internals.services.jwt import UserClaims

__all__ = [
    # Widget hierarchy (use as type annotations, e.g. `widgets: list[Widget]`)
    "Widget",
    "InputWidget",
    "OutputWidget",
    # Form state
    "State",
    # Widget value / response types (returned by user input)
    "FileResponse",
    "PhoneResponse",
    "AppointmentSlot",
    "CardOption",
    "AbstraOption",
    "LabelValueOption",
    "LabelValueDict",
    # Buttons (also useful as type annotations)
    "Button",
    "NextButton",
    "BackButton",
    "ExitButton",
    # Step / template aliases (for users defining page functions)
    "Step",
    "PageStep",
    "ComputationStep",
    "GeneratorStep",
    "Template",
    "TemplateWithButtons",
    "TemplateFunction",
    "TemplateGenerator",
    "TemplateGeneratorFunction",
    "Runnable",
    # Auth
    "UserClaims",
    # Tasks
    "TaskDTO",
    "TaskPayload",
    # Hooks
    "MailParser",
    # Connectors
    "AccessTokenDTO",
    # Tables
    "TableRow",
    "Comparator",
    # AI
    "Prompt",
    "Format",
    "BankStatementResponse",
    "BoletoResponse",
    "InvoiceResponse",
    "NfeResponse",
    "NfseResponse",
    "UsDriverLicenseResponse",
    "UsPassportResponse",
]
