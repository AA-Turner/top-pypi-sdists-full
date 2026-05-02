"""
Default runtime parameters:

    - Used for execution outside of AWS lambda
    - Substitue for Lambda environment variables
    - Run spotcli command line utility to create
      configuration file

    .. code: bash

        $ spotcli --configure

"""

defaults = {
    "iam_profile": "default",
    "s3_bucket": "mybucket",
    "duration_days": "1"
}
