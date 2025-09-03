"""Top-level package for t-nextgen."""

from t_nextgen.nextgen_window import NextGenWindow
from t_nextgen.ng_pm.windows.batch_maitenance import BatchMaintenanceWindow
from t_nextgen.ng_pm.windows.batch_posting import BatchPostingWindow
from t_nextgen.ng_pm.windows.cob import COBWindow
from t_nextgen.ng_pm.windows.encounter_insurance import EncounterInsuranceWindow
from t_nextgen.ng_pm.windows.import_file import ImportFileWindow
from t_nextgen.ng_pm.windows.payment_entry import PaymentEntryWindow
from t_nextgen.ng_pm.windows.transaction_ledger import TransactionLedgerWindow
from t_nextgen.ng_document_manager.core import NgDocumentManager
from t_nextgen.ng_pm.core import NextGenPMCore


__author__ = """Thoughtful"""
__email__ = "support@thoughtful.ai"
__version__ = "__version__ = '0.4.15'"

__all__ = [
    "NextGenWindow",
    "BatchMaintenanceWindow",
    "BatchPostingWindow",
    "COBWindow",
    "EncounterInsuranceWindow",
    "ImportFileWindow",
    "PaymentEntryWindow",
    "TransactionLedgerWindow",
    "NgDocumentManager",
    "NextGenPMCore",
]
