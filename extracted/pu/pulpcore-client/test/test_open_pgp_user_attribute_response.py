# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from pulpcore.client.pulpcore.models.open_pgp_user_attribute_response import OpenPGPUserAttributeResponse

class TestOpenPGPUserAttributeResponse(unittest.TestCase):
    """OpenPGPUserAttributeResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OpenPGPUserAttributeResponse:
        """Test OpenPGPUserAttributeResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OpenPGPUserAttributeResponse`
        """
        model = OpenPGPUserAttributeResponse()
        if include_optional:
            return OpenPGPUserAttributeResponse(
                pulp_href = '',
                prn = '',
                pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                pulp_last_updated = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                pulp_labels = {
                    'key' : ''
                    },
                sha256 = '',
                signatures = [
                    pulpcore.client.pulpcore.models.nested_open_pgp_signature_response.NestedOpenPGPSignatureResponse(
                        issuer = '', 
                        created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        expiration_time = '', 
                        signers_user_id = '', 
                        key_expiration_time = '', 
                        expired = True, 
                        key_expired = '', )
                    ],
                public_key = ''
            )
        else:
            return OpenPGPUserAttributeResponse(
                sha256 = '',
        )
        """

    def testOpenPGPUserAttributeResponse(self):
        """Test OpenPGPUserAttributeResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
