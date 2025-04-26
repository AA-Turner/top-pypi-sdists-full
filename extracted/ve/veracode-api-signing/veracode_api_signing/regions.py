# MIT License

# Copyright (c) 2020 Veracode, Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from veracode_api_signing.exceptions import VeracodeCredentialsError

REGIONS = {
    'e': 'eu',
    'f': 'fedramp',
    'g': 'global',
}


def get_region_for_api_credential(api_credential):
    if '-' in api_credential:
        prefix = api_credential.split('-')[0]
        if len(prefix) != 8:
            raise VeracodeCredentialsError(
                'Credential {} starts with an invalid prefix'.format(api_credential))
        region_character = prefix[6].lower()
    else:
        region_character = 'g'

    if region_character in REGIONS:
        return REGIONS[region_character]
    else:
        raise VeracodeCredentialsError(
            'Credential {} does not map to a known region'.format(api_credential))


def remove_prefix_from_api_credential(api_credential):
    # Remove region prefix (e.g., 'vera01gs-') if present
    return api_credential.split('-')[-1]
