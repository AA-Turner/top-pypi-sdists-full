"""Exceptions for the project."""


class BusinessException(Exception):
    """Business Exception."""

    pass


class ProcessException(BusinessException):
    """Process Exception."""

    pass


class WrongDatabaseSelectedError(ProcessException):
    """Wrong Database selected."""

    pass


class MultipleSessionsError(BusinessException):
    """Maximum Session for current user."""

    pass


class NextGenEdiNotFoundException(Exception):
    """EDI Not Found in Import Window."""

    pass


class NextGenDuplicateImportException(BusinessException):
    """NextGen Duplicate Import Exception."""

    pass


class PayFieldNotFoundException(ProcessException):
    """Pay Field Not Found Exception."""

    pass


class FieldNotFoundException(ProcessException):
    """Field Not Found Exception."""

    pass


class NextGenControlLostException(Exception):
    """Raised when pwywinauto loses control of NextGen App."""

    pass


class NoMatchingBatchDescriptionException(BusinessException):
    """No matching batch description found."""

    pass


class ServiceLineMissingRequiredFieldError(BusinessException):
    """Service Line Missing Required Field Error."""

    pass


class BatchFromBarNotFound(Exception):
    """Batch From Bar Not Found."""

    pass


class AdjFieldNotFoundException(ProcessException):
    """Adj Field Not Found Exception."""

    pass


class NextGenPatientPayException(Exception):
    """Raised when there is an issue during the import process."""

    pass


class Ins1FieldNotFoundException(ProcessException):
    """Ins1 Field Not Found Exception."""

    pass


class Ins2FieldNotFoundException(ProcessException):
    """Ins2 Field Not Found Exception."""

    pass


class Ins3FieldNotFoundException(ProcessException):
    """Ins3 Field Not Found Exception."""

    pass


class NextGenImportTimeoutException(Exception):
    """Raised when the EDI import process exceeds the allowed time limit."""

    pass


class BalanceFieldNotFoundException(ProcessException):
    """Balance Field Not Found Exception."""

    pass


class PostingSheetTimeOutException(Exception):
    """Raised when the posting sheet process times out while exporting files."""

    pass


class TransactionNumberNotFoundError(ProcessException):
    """Transaction Number Not Found Exception."""

    pass


class SearchEncounterNotFoundException(ProcessException):
    """Exception raised when the search encounter was not found."""

    pass


class LockedBatchError(Exception):
    """Locked Batch Error."""

    pass


class HeaderButtonNotFoundException(Exception):
    """Header Button Not Found Exception."""

    pass


class DeductFieldNotFoundException(ProcessException):
    """Balance field not found."""

    pass


class LoginPracticeSelectionException(ProcessException):
    """Login Practice Selection Exception."""

    pass


class LnItemRsnsNotUpdatedException(ProcessException):
    """LnItemRsns Not Updated Exception."""

    pass


class StatusNotUpdatedException(ProcessException):
    """Status Not Updated Exception."""

    pass
