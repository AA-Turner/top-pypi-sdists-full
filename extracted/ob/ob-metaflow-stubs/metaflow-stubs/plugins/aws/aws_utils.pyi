######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.923413                                                            #
######################################################################################################

from __future__ import annotations


from ...exception import MetaflowException as MetaflowException

MAX_MEMORY_PER_TASK: None

MAX_CPU_PER_TASK: None

def parse_s3_full_path(s3_uri):
    ...

def get_ec2_instance_metadata():
    """
    Fetches the EC2 instance metadata through AWS instance metadata service
    
    Returns either an empty dictionary, or one with the keys
        - ec2-instance-id
        - ec2-instance-type
        - ec2-region
        - ec2-availability-zone
    """
    ...

def get_docker_registry(image_uri):
    """
    Explanation:
        (.+?(?:[:.].+?)\/)? - [GROUP 0] REGISTRY
            .+?                  - A registry must start with at least one character
            (?:[:.].+?)\/       - A registry must have ":" or "." and end with "/"
            ?                    - Make a registry optional
        (.*?)                - [GROUP 1] REPOSITORY
            .*?                  - Get repository name until separator
        (?:[@:])?            - SEPARATOR
            ?:                   - Don't capture separator
            [@:]                 - The separator must be either "@" or ":"
            ?                    - The separator is optional
        ((?<=[@:]).*)?       - [GROUP 2] TAG / DIGEST
            (?<=[@:])            - A tag / digest must be preceded by "@" or ":"
            .*                   - Capture rest of tag / digest
            ?                    - A tag / digest is optional
    Examples:
        image
            - None
            - image
            - None
        example/image
            - None
            - example/image
            - None
        example/image:tag
            - None
            - example/image
            - tag
        example.domain.com/example/image:tag
            - example.domain.com/
            - example/image
            - tag
        123.123.123.123:123/example/image:tag
            - 123.123.123.123:123/
            - example/image
            - tag
        example.domain.com/example/image@sha256:45b23dee0
            - example.domain.com/
            - example/image
            - sha256:45b23dee0
    """
    ...

def compute_resource_attributes(decos, compute_deco, step_name, resource_defaults):
    """
    Compute resource values taking into account defaults, the values specified
    in the compute decorator (like @batch or @kubernetes) directly, and
    resources specified via @resources decorator.
    
    Returns a dictionary of resource attr -> value (str).
    """
    ...

def sanitize_batch_tag(key, value):
    """
    Sanitize a key and value for use as a Batch tag.
    """
    ...

