"""All config variables goes here."""


class Config:
    """Static class container for all variables."""

    class DIRECTORIES:
        """Directories to interact with NextGen."""

        BASE_DIR = r"C:/NextGen"
        FILE_MAINTENANCE = r"C:/NextGen/NGFileMaint.exe"
        DOC_MANAGEMENT = r"C:/NextGen/NextGenICS.exe"
        ENTERPRISE_PM = r"C:/NextGen/NextGenEPM.exe"

    class DATABASES:
        """NextGen available databases."""

        TEST = "NGTEST"
        BETA = "NGBETA"
        PROD = "NGPROD"
