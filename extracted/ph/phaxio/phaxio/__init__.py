from phaxio.api import PhaxioApi
from phaxio import swagger_client
# import all api return types and exception types
# can generate this from the models directory thusly:
# egrep '^class' ./*.py | sed 's/\.\//from phaxio.swagger_client.models./g' | sed 's/\.py:class/ import/g' | sed 's/(object)://g'
from phaxio.swagger_client.models.account_status_data import AccountStatusData
from phaxio.swagger_client.models.account_status import AccountStatus
from phaxio.swagger_client.models.area_code import AreaCode
from phaxio.swagger_client.models.country import Country
from phaxio.swagger_client.models.error import Error
from phaxio.swagger_client.models.fax_info import FaxInfo
from phaxio.swagger_client.models.generate_phax_code_json_response_data import GeneratePhaxCodeJsonResponseData
from phaxio.swagger_client.models.generate_phax_code_json_response import GeneratePhaxCodeJsonResponse
from phaxio.swagger_client.models.get_area_codes_response import GetAreaCodesResponse
from phaxio.swagger_client.models.get_countries_response import GetCountriesResponse
from phaxio.swagger_client.models.get_faxes_response import GetFaxesResponse
from phaxio.swagger_client.models.get_fax_info_response import GetFaxInfoResponse
from phaxio.swagger_client.models.list_phone_numbers_response import ListPhoneNumbersResponse
from phaxio.swagger_client.models.operation_status import OperationStatus
from phaxio.swagger_client.models.paging import Paging
from phaxio.swagger_client.models.phax_code_data import PhaxCodeData
from phaxio.swagger_client.models.phax_code import PhaxCode
from phaxio.swagger_client.models.phone_number import PhoneNumber
from phaxio.swagger_client.models.phone_number_response import PhoneNumberResponse
from phaxio.swagger_client.models.recipient import Recipient
from phaxio.swagger_client.models.send_fax_response_data import SendFaxResponseData
from phaxio.swagger_client.models.send_fax_response import SendFaxResponse
from phaxio.swagger_client.models.status import Status


from phaxio.swagger_client.rest import ApiException

