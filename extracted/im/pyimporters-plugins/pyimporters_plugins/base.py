import abc
import os
import zipfile
from contextlib import contextmanager
from gzip import GzipFile
from io import TextIOWrapper
from pathlib import Path
from typing import Optional, Dict, Any, Type, Generator, Union, List

from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass


class Term(BaseModel):
    lexicon: Optional[str] = Field(
        None, description="Lexicon of the term", example="MeSH"
    )
    identifier: str = Field(
        ...,
        description="Unique identifier of the term",
        example="http://www.example.com/rocks",
    )
    preferredForm: Optional[str] = Field(
        None, description="The preferred label of the term", example="rocks"
    )
    properties: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional properties of the term",
        example={"altForms": ["basalt", "granite", "slate"], "wikidataId": "Q8063"},
    )


@dataclass
class KnowledgeParserOptions:
    project: str = Query(None, description="Name of the project", extra="internal")
    lexicon: str = Query(
        None, description="Lexicon to inject the terms", extra="internal"
    )
    lang: str = Query("en", description="Language of the project", extra="internal")
    limit: int = Query(
        0, description="Number of terms to import. O means all", extra="advanced", ge=0
    )


KnowledgeParserModel = KnowledgeParserOptions.__pydantic_model__


class KnowledgeParserBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(
        self,
        source: Path,
        options: Union[KnowledgeParserOptions, Dict[str, Any]],
        bar: Bar,
    ) -> Generator[Term, None, None]:
        """Parse the input source file and return a stream of concepts.

        :param source: A file object containing the knowledge.
        :param options: options of the parser.
        :param bar: progress bar
        :returns: Iterable producing the concepts.
        """

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return KnowledgeParserOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return KnowledgeParserModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return []


@contextmanager
def maybe_archive(source: Path, mode="r", encoding="utf-8"):
    try:
        archive = None
        file = None
        guessed = None
        if source.suffix == ".gz":
            guessed = "gzip"
        elif source.suffix == ".zip":
            guessed = "zip"
        else:
            if zipfile.is_zipfile(source):
                guessed = "zip"
            if is_gzipfile(source):
                guessed = "gzip"
        if guessed == "gzip":
            file = GzipFile(str(source), mode=mode)
        elif guessed == "zip":
            archive = zipfile.ZipFile(str(source))
            if "[Content_Types].xml" in archive.NameToInfo:
                # This is not a real zip file but a xlsx file
                archive.close()
                archive = None
                guessed = None
            else:
                if len(archive.filelist) == 1:
                    file = (
                        archive.open(archive.filelist[0])
                        if "b" in mode
                        else TextIOWrapper(
                            archive.open(archive.filelist[0]), encoding=encoding
                        )
                    )
                else:
                    file = archive
        if file is None:
            file = (
                source.open(mode)
                if "b" in mode
                else source.open(mode, encoding=encoding)
            )
        yield file
    finally:
        if file:
            file.close()
        if archive:
            archive.close()


def is_gzipfile(filename):
    """
    This function attempts to ascertain the gzip status of a file based on the "magic signatures" of
    the file. This was taken from the stack overflow
    http://stackoverflow.com/questions/13044562/python-mechanism-to-identify-compressed-file-type\
        -and-uncompress
    """
    assert os.path.exists(filename), (
        "Input {} does not ".format(filename) + "point to a file."
    )
    with open(filename, "rb") as in_f:
        start_of_file = in_f.read(3)
        if start_of_file == b"\x1f\x8b\x08":
            return True
        else:
            return False
