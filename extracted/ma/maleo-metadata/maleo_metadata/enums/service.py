from enum import StrEnum

class MaleoMetadataServiceEnums:
    class IdentifierType(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class Service(StrEnum):
        MALEO_STUDIO = "maleo-studio"
        MALEO_NEXUS = "maleo-nexus"
        MALEO_METADATA = "maleo-metadata"
        MALEO_IDENTITY = "maleo-identity"
        MALEO_ACCESS = "maleo-access"
        MALEO_MEDIX = "maleo-medix"
        MALEO_FHIR = "maleo-fhir"
        MALEO_DICOM = "maleo-dicom"
        MALEO_SCRIBE = "maleo-scribe"
        MALEO_CDS = "maleo-cds"
        MALEO_IMAGING = "maleo-imaging"
        MALEO_MCU = "maleo-mcu"