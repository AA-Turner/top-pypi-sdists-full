from typing import Any

from pydantic import BaseModel, Field, RootModel


class Span(BaseModel):
    start: int = Field(..., description="Start index of the span in the text", json_schema_extra={"example": 5})
    end: int = Field(..., description="End index of the span in the text", json_schema_extra={"example": 15})


class Boundary(Span):
    name: str = Field(None, description="Name of the boundary", json_schema_extra={"example": "body"})


class Term(BaseModel):
    identifier: str = Field(
        ...,
        description="Unique identifier of the term",
        json_schema_extra={"example": "http://www.example.com/rocks"},
    )
    lexicon: str = Field(None, description="Lexicon of the term", json_schema_extra={"example": "MeSH"})
    preferredForm: str | None = Field(
        None, description="The preferred label of the term", json_schema_extra={"example": "rocks"}
    )
    score: float | None = Field(None, description="Confidence score of the term", json_schema_extra={"example": 0.87})
    properties: dict[str, Any] | None = Field(
        None,
        description="Additional properties of the term",
        json_schema_extra={"example": {"altForms": ["basalt", "granite", "slate"], "wikidataId": "Q8063"}},
    )

    def __eq__(self, other):
        return other and self.lexicon == other.lexicon and self.identifier == other.identifier

    def __hash__(self):
        return hash((self.identifier, self.lexicon))


class AltText(BaseModel):
    name: str = Field(None, description="Name of the alternative text", json_schema_extra={"example": "fingerprint"})
    text: str = Field(None, description="Alternative text")
    properties: dict[str, Any] | None = Field(None, description="Properties of the alternative text")


class Annotation(Span):
    labelName: str = Field(None, description="Label name of the annotation", json_schema_extra={"example": "org"})
    label: str | None = Field(None, description="Label of the annotation", json_schema_extra={"example": "ORG"})
    text: str | None = Field(
        None, description="Covering text of the annotation", json_schema_extra={"example": "Kairntech"}
    )
    score: float | None = Field(
        None, description="Confidence score of the annotation", json_schema_extra={"example": 0.87}
    )
    properties: dict[str, Any] | None = Field(None, description="Properties of annotation")
    terms: list[Term] | None = Field(None, description="Properties of annotation")
    createdBy: str | None = Field(None, description="Name of the user or the process that created the annotation")
    createdDate: str | None = Field(None, description="Creation date")
    modifiedBy: str | None = Field(None, description="Name of the user or the process that modified the annotation")
    modifiedDate: str | None = Field(None, description="Last modification date")
    status: str | None = Field(None, description="Status of the annotation")


class Category(BaseModel):
    labelName: str = Field(None, description="Label name of the category", json_schema_extra={"example": "org"})
    label: str | None = Field(None, description="Label of the category", json_schema_extra={"example": "ORG"})
    score: float | None = Field(
        None, description="Confidence score of the category", json_schema_extra={"example": 0.87}
    )
    properties: dict[str, Any] | None = Field(None, description="Properties of category")
    createdBy: str | None = Field(None, description="Name of the user or the process that created the category")
    createdDate: str | None = Field(None, description="Creation date")
    modifiedDate: str | None = Field(None, description="Last modification date")
    modifiedBy: str | None = Field(None, description="Name of the user or the process that modified the category")
    status: str | None = Field(None, description="Status of the category")


class Sentence(Span):
    metadata: dict[str, Any] | None = Field(None, description="Sentence metadata")
    categories: list[Category] | None = Field(None, description="Sentence categories")


class Document(BaseModel):
    text: str = Field(None, description="Plain text of the converted document")
    identifier: str | None = Field(None, description="Identifier of the document")
    title: str | None = Field(None, description="Title of the document")
    sourceText: str | None = Field(None, description="Source text of the converted document")
    boundaries: dict[str | None, list[Boundary]] | None = Field(None, description="List of boundaries by type")
    metadata: dict[str, Any] | None = Field(None, description="Document metadata")
    altTexts: list[AltText] | None = Field(None, description="Document alternative texts")
    properties: dict[str, Any] | None = Field(None, description="Document properties")
    sentences: list[Sentence] | None = Field(None, description="Document sentences")
    annotations: list[Annotation] | None = Field(None, description="Document annotations")
    categories: list[Category] | None = Field(None, description="Document categories")


class SegmenterDocumentExample(BaseModel):
    text: str = Field("Mandatory text")
    identifier: str | None = Field("Optional identifier")
    title: str | None = Field("Optional title")
    metadata: dict[str, Any] | None = Field({})


class AnnotatorDocumentExample(SegmenterDocumentExample):
    sentences: list[Sentence] | None = Field([])


class ProcessorDocumentExample(AnnotatorDocumentExample):
    annotations: list[Annotation] | None = Field([Annotation(start=0, end=10, labelName="Optional annotation")])
    categories: list[Category] | None = Field([Category(labelName="Optional category")])


class FormatterDocumentExample(ProcessorDocumentExample):
    pass


class DocumentList(RootModel[list[Document]]):
    pass
