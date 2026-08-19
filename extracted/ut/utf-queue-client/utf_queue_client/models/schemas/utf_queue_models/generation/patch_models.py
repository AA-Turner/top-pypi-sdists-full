import re
import pathlib


def patch_pydantic_v1_models():
    """
    Patch generated pydantic v1 models to replace models generated
    with a root model to a regular model that allows extra fields.

    For example, datamodel-codegen 0.26.5 creates the pydantic v1 QueueRecord
     model like this:

    class QueueRecord(BaseModel):
        __root__: Optional[Dict[str, Any]] = None

    But we need it to be a regular model that allows extra fields:

    class QueueRecord(BaseModel):
        class Config:
            extra = Extra.allow

    """
    models_file = (
        pathlib.Path(__file__).parent.parent
        / "models/python/generated_models_pydantic_v1.py"
    )
    with open(models_file, "r") as f:
        content = f.read()

    content = re.sub(
        r"from pydantic import Field, constr",
        r"from pydantic import Extra, Field, constr",
        content,
    )
    content = re.sub(
        r"    __root__: Optional\[Dict\[str, (Any|str)]] = None",
        r"    class Config:\n        extra = Extra.allow",
        content,
    )
    with open(models_file, "w") as f:
        f.write(content)


def patch_pydantic_v2_models():
    """
    Patch generated pydantic v2 models to replace models generated
    with a root model to a regular model that allows extra fields.

    For example, datamodel-codegen 0.26.5 creates the pydantic v2 QueueRecord
     model like this:

    class QueueRecord(RootModel[Optional[Dict[str, Any]]]):
        root: Optional[Dict[str, Any]] = None

    But we need it to be a regular model that allows extra fields:

    class QueueRecord(BaseModel):
        model_config = ConfigDict(extra='allow')

    Also, for QueueMessage and QueueMessageV1, we need to add a validator
     to convert the payload member from a specific payload type (such as TelemetryData)
     to a generic QueueRecord.
    """
    models_file = (
        pathlib.Path(__file__).parent.parent
        / "models/python/generated_models_pydantic_v2.py"
    )
    with open(models_file, "r") as f:
        content = f.read()
    content = re.sub(
        r"from pydantic import Field, RootModel, constr",
        "from pydantic import Field, RootModel, constr, ConfigDict, field_validator",
        content,
    )
    content = re.sub(
        r"RootModel\[Optional\[Dict\[str, (Any|str)]]]", "BaseModel", content
    )
    content = re.sub(
        r"root: Optional\[Dict\[str, (Any|str)]] = None",
        "model_config = ConfigDict(extra='allow')",
        content,
    )
    content = re.sub(
        r"class QueueMessage\(BaseModel\):",
        """class QueueMessage(BaseModel):
    
    @field_validator("payload", mode="before")
    def validate_payload(cls, v):
        if isinstance(v, BaseModel):
            return QueueRecord(v.model_dump())
        return v
""",
        content,
    )
    content = re.sub(
        r"class QueueMessageV1\(BaseModel\):",
        """class QueueMessageV1(BaseModel):
    
    @field_validator("payload", mode="before")
    def validate_payload(cls, v):
        if isinstance(v, BaseModel):
            return QueueRecord(v.model_dump())
        return v
    """,
        content,
    )
    with open(models_file, "w") as f:
        f.write(content)


def patch_java_models():
    """
    Patch generated Java models for SQA result types to extend the QueueRecord class.
    """
    models_files = [
        "models/java/com/silabs/utf/QueueModels/SqaAppBuildResult.java",
        "models/java/com/silabs/utf/QueueModels/SqaTestResult.java",
        "models/java/com/silabs/utf/QueueModels/SqaTestSession.java",
    ]
    for model_file in models_files:
        model_file = pathlib.Path(__file__).parent.parent / model_file
        with open(model_file, "r") as f:
            content = f.read()
        content = re.sub(
            r"public class (Sqa.*) {",
            r"public class \1 extends QueueRecord {",
            content,
        )
        with open(model_file, "w") as f:
            f.write(content)


def main():
    patch_pydantic_v1_models()
    patch_pydantic_v2_models()
    patch_java_models()


if __name__ == "__main__":
    main()
