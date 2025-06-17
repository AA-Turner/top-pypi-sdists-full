######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.860225                                                            #
######################################################################################################

from __future__ import annotations


from .exception import MetaflowTaggingError as MetaflowTaggingError

def is_utf8_encodable(x):
    """
    Returns true if the object can be encoded with UTF-8
    """
    ...

def is_utf8_decodable(x):
    """
    Returns true if the object can be decoded with UTF-8
    """
    ...

MAX_USER_TAG_SET_SIZE: int

MAX_TAG_SIZE: int

def validate_tags(tags, existing_tags = None):
    """
    Raises MetaflowTaggingError if invalid based on these rules:
    
    Tag set size is too large. But it's OK if tag set is not larger
    than an existing tag set (if provided).
    
    Then, we validate each tag.  See validate_tag()
    """
    ...

def validate_tag(tag):
    """
    - Tag must be either of bytes-type or unicode-type.
    - If tag is of bytes-type, it must be UTF-8 decodable
    - If tag is of unicode-type, it must be UTF-8 encodable
    - Tag may not be empty string.
    - Tag cannot be too long (500 chars)
    """
    ...

