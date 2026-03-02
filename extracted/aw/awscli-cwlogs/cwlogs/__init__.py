#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Amazon Software License (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/asl/
#
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.

__version__ = '1.4.6'

def awscli_initialize(cli):
    """
    The entry point for Cloudwatch logs high level commands.
    """
    # The setup.py imports this module to get __version__, but cwlogs.pull
    # and push depend on awscli which is not available because awscli is
    # configured as dependency of cwlogs plugin and installed later
    # by setup.py. Moving import within this method avoid the problem.
    from cwlogs.pull import initialize as logs_pull_init
    from cwlogs.push import initialize as logs_push_init
    from cwlogs.filter import initialize as logs_filter_init
    logs_pull_init(cli)
    logs_filter_init(cli)
    logs_push_init(cli)
