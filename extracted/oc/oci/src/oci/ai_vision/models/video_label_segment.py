# coding: utf-8
# Copyright (c) 2016, 2025, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

# NOTE: This class is auto generated by OracleSDKGenerator. DO NOT EDIT. API Version: 20220125


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VideoLabelSegment(object):
    """
    A label segment in a video.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VideoLabelSegment object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param video_segment:
            The value to assign to the video_segment property of this VideoLabelSegment.
        :type video_segment: oci.ai_vision.models.VideoSegment

        :param confidence:
            The value to assign to the confidence property of this VideoLabelSegment.
        :type confidence: float

        """
        self.swagger_types = {
            'video_segment': 'VideoSegment',
            'confidence': 'float'
        }
        self.attribute_map = {
            'video_segment': 'videoSegment',
            'confidence': 'confidence'
        }
        self._video_segment = None
        self._confidence = None

    @property
    def video_segment(self):
        """
        **[Required]** Gets the video_segment of this VideoLabelSegment.

        :return: The video_segment of this VideoLabelSegment.
        :rtype: oci.ai_vision.models.VideoSegment
        """
        return self._video_segment

    @video_segment.setter
    def video_segment(self, video_segment):
        """
        Sets the video_segment of this VideoLabelSegment.

        :param video_segment: The video_segment of this VideoLabelSegment.
        :type: oci.ai_vision.models.VideoSegment
        """
        self._video_segment = video_segment

    @property
    def confidence(self):
        """
        **[Required]** Gets the confidence of this VideoLabelSegment.
        The confidence score, between 0 and 1.


        :return: The confidence of this VideoLabelSegment.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """
        Sets the confidence of this VideoLabelSegment.
        The confidence score, between 0 and 1.


        :param confidence: The confidence of this VideoLabelSegment.
        :type: float
        """
        self._confidence = confidence

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
