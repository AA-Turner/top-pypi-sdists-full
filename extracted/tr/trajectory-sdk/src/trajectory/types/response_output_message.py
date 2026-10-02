# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal

from trajectory._models import BaseModel


class ResponseContainerFileCitation(BaseModel):
  container_id: str

  end_index: int

  file_id: str

  filename: str

  start_index: int

  type: Literal["container_file_citation"]


class ResponseFileCitation(BaseModel):
  file_id: str

  filename: str

  index: int

  type: Literal["file_citation"]


class ResponseFilePath(BaseModel):
  file_id: str

  index: int

  type: Literal["file_path"]


class ResponseOutputLogprobTopLogprob(BaseModel):
  token: str

  bytes: list[int]

  logprob: float


class ResponseOutputRefusal(BaseModel):
  refusal: str

  type: Literal["refusal"]


class ResponseUrlCitation(BaseModel):
  end_index: int

  start_index: int

  title: str

  type: Literal["url_citation"]

  url: str


class ResponseOutputLogprob(BaseModel):
  token: str

  bytes: list[int]

  logprob: float

  top_logprobs: list[ResponseOutputLogprobTopLogprob]


class ResponseOutputText(BaseModel):
  annotations: list[
    ResponseFileCitation | ResponseUrlCitation | ResponseContainerFileCitation | ResponseFilePath
  ]

  text: str

  type: Literal["output_text"]

  logprobs: list[ResponseOutputLogprob] | None = None


class ResponseOutputMessage(BaseModel):
  id: str

  content: list[ResponseOutputText | ResponseOutputRefusal]

  role: Literal["assistant"]

  status: Literal["in_progress", "completed", "incomplete"]

  type: Literal["message"]

  phase: Literal["commentary", "final_answer"] | None = None
