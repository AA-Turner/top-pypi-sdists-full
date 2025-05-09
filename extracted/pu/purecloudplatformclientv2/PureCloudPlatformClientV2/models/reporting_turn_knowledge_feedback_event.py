# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from datetime import datetime
from datetime import date
from pprint import pformat
import re
import json

from ..utils import sanitize_for_serialization

# type hinting support
from typing import TYPE_CHECKING
from typing import List
from typing import Dict

if TYPE_CHECKING:
    from . import ReportingTurnKnowledgeDocument

class ReportingTurnKnowledgeFeedbackEvent(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self) -> None:
        """
        ReportingTurnKnowledgeFeedbackEvent - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'search_id': 'str',
            'knowledge_base_id': 'str',
            'documents': 'list[ReportingTurnKnowledgeDocument]',
            'feedback_rating': 'int',
            'document_variation_id': 'str',
            'document_version_id': 'str'
        }

        self.attribute_map = {
            'search_id': 'searchId',
            'knowledge_base_id': 'knowledgeBaseId',
            'documents': 'documents',
            'feedback_rating': 'feedbackRating',
            'document_variation_id': 'documentVariationId',
            'document_version_id': 'documentVersionId'
        }

        self._search_id = None
        self._knowledge_base_id = None
        self._documents = None
        self._feedback_rating = None
        self._document_variation_id = None
        self._document_version_id = None

    @property
    def search_id(self) -> str:
        """
        Gets the search_id of this ReportingTurnKnowledgeFeedbackEvent.
        The ID of this knowledge search.

        :return: The search_id of this ReportingTurnKnowledgeFeedbackEvent.
        :rtype: str
        """
        return self._search_id

    @search_id.setter
    def search_id(self, search_id: str) -> None:
        """
        Sets the search_id of this ReportingTurnKnowledgeFeedbackEvent.
        The ID of this knowledge search.

        :param search_id: The search_id of this ReportingTurnKnowledgeFeedbackEvent.
        :type: str
        """
        

        self._search_id = search_id

    @property
    def knowledge_base_id(self) -> str:
        """
        Gets the knowledge_base_id of this ReportingTurnKnowledgeFeedbackEvent.
        The Knowledge Base ID that the captured knowledge data relates to.

        :return: The knowledge_base_id of this ReportingTurnKnowledgeFeedbackEvent.
        :rtype: str
        """
        return self._knowledge_base_id

    @knowledge_base_id.setter
    def knowledge_base_id(self, knowledge_base_id: str) -> None:
        """
        Sets the knowledge_base_id of this ReportingTurnKnowledgeFeedbackEvent.
        The Knowledge Base ID that the captured knowledge data relates to.

        :param knowledge_base_id: The knowledge_base_id of this ReportingTurnKnowledgeFeedbackEvent.
        :type: str
        """
        

        self._knowledge_base_id = knowledge_base_id

    @property
    def documents(self) -> List['ReportingTurnKnowledgeDocument']:
        """
        Gets the documents of this ReportingTurnKnowledgeFeedbackEvent.
        The list of search documents that the feedback applies to.

        :return: The documents of this ReportingTurnKnowledgeFeedbackEvent.
        :rtype: list[ReportingTurnKnowledgeDocument]
        """
        return self._documents

    @documents.setter
    def documents(self, documents: List['ReportingTurnKnowledgeDocument']) -> None:
        """
        Sets the documents of this ReportingTurnKnowledgeFeedbackEvent.
        The list of search documents that the feedback applies to.

        :param documents: The documents of this ReportingTurnKnowledgeFeedbackEvent.
        :type: list[ReportingTurnKnowledgeDocument]
        """
        

        self._documents = documents

    @property
    def feedback_rating(self) -> int:
        """
        Gets the feedback_rating of this ReportingTurnKnowledgeFeedbackEvent.
        The feedback rating for the search (1.0 - 5.0). 1 = Negative, 5 = Positive.

        :return: The feedback_rating of this ReportingTurnKnowledgeFeedbackEvent.
        :rtype: int
        """
        return self._feedback_rating

    @feedback_rating.setter
    def feedback_rating(self, feedback_rating: int) -> None:
        """
        Sets the feedback_rating of this ReportingTurnKnowledgeFeedbackEvent.
        The feedback rating for the search (1.0 - 5.0). 1 = Negative, 5 = Positive.

        :param feedback_rating: The feedback_rating of this ReportingTurnKnowledgeFeedbackEvent.
        :type: int
        """
        

        self._feedback_rating = feedback_rating

    @property
    def document_variation_id(self) -> str:
        """
        Gets the document_variation_id of this ReportingTurnKnowledgeFeedbackEvent.
        The variation of the document.

        :return: The document_variation_id of this ReportingTurnKnowledgeFeedbackEvent.
        :rtype: str
        """
        return self._document_variation_id

    @document_variation_id.setter
    def document_variation_id(self, document_variation_id: str) -> None:
        """
        Sets the document_variation_id of this ReportingTurnKnowledgeFeedbackEvent.
        The variation of the document.

        :param document_variation_id: The document_variation_id of this ReportingTurnKnowledgeFeedbackEvent.
        :type: str
        """
        

        self._document_variation_id = document_variation_id

    @property
    def document_version_id(self) -> str:
        """
        Gets the document_version_id of this ReportingTurnKnowledgeFeedbackEvent.
        The version of the document.

        :return: The document_version_id of this ReportingTurnKnowledgeFeedbackEvent.
        :rtype: str
        """
        return self._document_version_id

    @document_version_id.setter
    def document_version_id(self, document_version_id: str) -> None:
        """
        Sets the document_version_id of this ReportingTurnKnowledgeFeedbackEvent.
        The version of the document.

        :param document_version_id: The document_version_id of this ReportingTurnKnowledgeFeedbackEvent.
        :type: str
        """
        

        self._document_version_id = document_version_id

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in self.swagger_types.items():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_json(self):
        """
        Returns the model as raw JSON
        """
        return json.dumps(sanitize_for_serialization(self.to_dict()))

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

