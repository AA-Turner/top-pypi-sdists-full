# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Required, TypedDict


class ArtemisSessionsDecideParams(TypedDict, total=False):
  request_id: Required[str]
  """
  A pending request's request_id.
  """
  digest: Required[str]
  """
  The digest the session showed for it.
  """
  approve: Required[bool]
  """
  True runs the write; false rejects it.
  """
