# coding: utf-8

"""
    MailSlurp API

    MailSlurp is an API for sending and receiving emails and SMS from dynamically allocated email addresses and phone numbers. It's designed for developers and QA teams to test applications, process inbound emails, send templated notifications, attachments, and more.  ## Resources  - [Homepage](https://www.mailslurp.com) - Get an [API KEY](https://app.mailslurp.com/sign-up/) - Generated [SDK Clients](https://docs.mailslurp.com/) - [Examples](https://github.com/mailslurp/examples) repository  # noqa: E501

    The version of the OpenAPI document: 6.5.2
    Contact: contact@mailslurp.dev
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import mailslurp_client
from mailslurp_client.models.inbox_preview import InboxPreview  # noqa: E501
from mailslurp_client.rest import ApiException

class TestInboxPreview(unittest.TestCase):
    """InboxPreview unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InboxPreview
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = mailslurp_client.models.inbox_preview.InboxPreview()  # noqa: E501
        if include_optional :
            return InboxPreview(
                id = '0', 
                domain_id = '0', 
                email_address = '0', 
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                favourite = True, 
                name = '0', 
                tags = [
                    '0'
                    ], 
                team_access = True, 
                inbox_type = 'HTTP_INBOX', 
                virtual_inbox = True, 
                expires_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                functions_as = 'ALIAS', 
                user_id = '0', 
                description = '0', 
                account_region = 'US_WEST_2'
            )
        else :
            return InboxPreview(
                id = '0',
                email_address = '0',
                created_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                favourite = True,
                team_access = True,
                virtual_inbox = True,
                user_id = '0',
        )

    def testInboxPreview(self):
        """Test InboxPreview"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
