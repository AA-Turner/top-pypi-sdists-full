from typing import Optional, List, Any, Dict

from pydantic import BaseModel, Field


class Span(BaseModel):
    start: int = Field(
        ..., description="Start index of the span in the text", example=5
    )
    end: int = Field(..., description="End index of the span in the text", example=15)


class Boundary(Span):
    name: str = Field(None, description="Name of the boundary", example="body")


class Term(BaseModel):
    identifier: str = Field(
        ...,
        description="Unique identifier of the term",
        example="http://www.example.com/rocks",
    )
    lexicon: str = Field(None, description="Lexicon of the term", example="MeSH")
    preferredForm: Optional[str] = Field(
        None, description="The preferred label of the term", example="rocks"
    )
    score: Optional[float] = Field(
        None, description="Confidence score of the term", example=0.87
    )
    properties: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional properties of the term",
        example={"altForms": ["basalt", "granite", "slate"], "wikidataId": "Q8063"},
    )

    def __eq__(self, other):  # noqa: E126
        return (
            other
            and self.lexicon == other.lexicon  # noqa: W503
            and self.identifier == other.identifier  # noqa: W503
        )

    def __hash__(self):
        return hash((self.identifier, self.lexicon))


class AltText(BaseModel):
    name: str = Field(
        None, description="Name of the alternative text", example="fingerprint"
    )
    text: str = Field(None, description="Alternative text")
    properties: Optional[Dict[str, Any]] = Field(
        None, description="Properties of the alternative text"
    )


class Annotation(Span):
    labelName: str = Field(
        None, description="Label name of the annotation", example="org"
    )
    label: Optional[str] = Field(
        None, description="Label of the annotation", example="ORG"
    )
    text: Optional[str] = Field(
        None, description="Covering text of the annotation", example="Kairntech"
    )
    score: Optional[float] = Field(
        None, description="Confidence score of the annotation", example=0.87
    )
    properties: Optional[Dict[str, Any]] = Field(
        None, description="Properties of annotation"
    )
    terms: Optional[List[Term]] = Field(None, description="Properties of annotation")
    createdBy: Optional[str] = Field(
        None, description="Name of the user or the process that created the annotation"
    )
    createdDate: Optional[str] = Field(None, description="Creation date")
    modifiedBy: Optional[str] = Field(
        None, description="Name of the user or the process that modified the annotation"
    )
    modifiedDate: Optional[str] = Field(None, description="Last modification date")
    status: Optional[str] = Field(None, description="Status of the annotation")


class Category(BaseModel):
    labelName: str = Field(
        None, description="Label name of the category", example="org"
    )
    label: Optional[str] = Field(
        None, description="Label of the category", example="ORG"
    )
    score: Optional[float] = Field(
        None, description="Confidence score of the category", example=0.87
    )
    properties: Optional[Dict[str, Any]] = Field(
        None, description="Properties of category"
    )
    createdBy: Optional[str] = Field(
        None, description="Name of the user or the process that created the category"
    )
    createdDate: Optional[str] = Field(None, description="Creation date")
    modifiedDate: Optional[str] = Field(None, description="Last modification date")
    modifiedBy: Optional[str] = Field(
        None, description="Name of the user or the process that modified the category"
    )
    status: Optional[str] = Field(None, description="Status of the category")


class Sentence(Span):
    metadata: Optional[Dict[str, Any]] = Field(None, description="Sentence metadata")
    categories: Optional[List[Category]] = Field(
        None, description="Sentence categories"
    )


class Document(BaseModel):
    text: str = Field(None, description="Plain text of the converted document")
    identifier: Optional[str] = Field(None, description="Identifier of the document")
    title: Optional[str] = Field(None, description="Title of the document")
    sourceText: Optional[str] = Field(
        None, description="Source text of the converted document"
    )
    boundaries: Optional[Dict[Optional[str], List[Boundary]]] = Field(
        None, description="List of boundaries by type"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Document metadata")
    altTexts: Optional[List[AltText]] = Field(
        None, description="Document alternative texts"
    )
    properties: Optional[Dict[str, Any]] = Field(
        None, description="Document properties"
    )
    sentences: Optional[List[Sentence]] = Field(None, description="Document sentences")
    annotations: Optional[List[Annotation]] = Field(
        None, description="Document annotations"
    )
    categories: Optional[List[Category]] = Field(
        None, description="Document categories"
    )


class SegmenterDocumentExample(BaseModel):
    text: str = Field("Mandatory text")
    identifier: Optional[str] = Field("Optional identifier")
    title: Optional[str] = Field("Optional title")
    metadata: Optional[Dict[str, Any]] = Field({})


class AnnotatorDocumentExample(SegmenterDocumentExample):
    sentences: Optional[List[Sentence]] = Field([])


class ProcessorDocumentExample(AnnotatorDocumentExample):
    annotations: Optional[List[Annotation]] = Field(
        [Annotation(start=0, end=10, labelName="Optional annotation")]
    )
    categories: Optional[List[Category]] = Field(
        [Category(labelName="Optional category")]
    )


class FormatterDocumentExample(ProcessorDocumentExample):
    pass


class DocumentList(BaseModel):
    __root__: List[Document]
