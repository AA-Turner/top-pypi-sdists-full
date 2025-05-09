# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations


import proto  # type: ignore

from google.ads.googleads.v18.enums.types import (
    placeholder_type as gage_placeholder_type,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v18.resources",
    marshal="google.ads.googleads.v18",
    manifest={
        "FeedPlaceholderView",
    },
)


class FeedPlaceholderView(proto.Message):
    r"""A feed placeholder view.

    Attributes:
        resource_name (str):
            Output only. The resource name of the feed placeholder view.
            Feed placeholder view resource names have the form:

            ``customers/{customer_id}/feedPlaceholderViews/{placeholder_type}``
        placeholder_type (google.ads.googleads.v18.enums.types.PlaceholderTypeEnum.PlaceholderType):
            Output only. The placeholder type of the feed
            placeholder view.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    placeholder_type: (
        gage_placeholder_type.PlaceholderTypeEnum.PlaceholderType
    ) = proto.Field(
        proto.ENUM,
        number=2,
        enum=gage_placeholder_type.PlaceholderTypeEnum.PlaceholderType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
