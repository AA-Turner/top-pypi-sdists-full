"""
Created December 2016

@author Ari Polsky
"""

from phaxio import swagger_client
import os
from six import string_types
from phaxio.swagger_client.apis.default_api import DefaultApi


def _opt_args_to_dict(**kwargs):
    # return kwargs as a dictionary that excludes parameters that are set to None. It's handy because some APIs don't
    # like having optional params set to null when None was passed in, so we return the kwargs without the nulls
    ret = {}
    for k, v in kwargs.items():
        if v is not None:
            ret[k] = v
    return ret


def _add_tags_dict(tags_dict, opt_args):
    # because tags don't have a defined key name, there is no way to represent them in swagger. So I added support
    # for an _extra_args parameter to the client, which will just pass though anything you put in there. If there are
    # other form fields it'll put them there, else it'll put them into the query string
    if tags_dict:
        extra_args = {}
        for k, v in tags_dict.items():
            key = 'tag[{}]'.format(k)
            extra_args[key] = v
        opt_args['_extra_args'] = extra_args



class PhaxioApi(object):
    """
    :param api_key: Your API key
    :param api_secret: Your API secret
    :param file_download_path: Destination directory for downloaded files

    :ivar _Fax Fax: Object for all fax-related functionality
    :ivar _PhaxCode PhaxCode: Object for creating and retrieving PhaxCodes
    :ivar _PhoneNumber PhoneNumber: Object for provisioning and querying phone numbers
    :ivar _Countries Countries: Object for querying countries
    :ivar _Account Account: Object for querying account info
    """
    def __init__(self, api_key, api_secret, file_download_path=None):
        """
        Initialize a Phaxio Api client

        :param api_key: Your API key
        :param api_secret: Your API secret
        :param file_download_path: Destination directory for downloaded files
        """

        swagger_client.configuration.username = api_key
        swagger_client.configuration.password = api_secret
        if file_download_path:
            swagger_client.configuration.temp_folder_path = file_download_path
        self._client = DefaultApi()

        # create objects to group related functions together
        self.Fax = _Fax(self._client)
        self.Account = _Account(self._client)
        self.PhoneNumber = _PhoneNumber(self._client)
        self.PhaxCode = _PhaxCode(self._client)
        self.Countries = _Countries(self._client)


class _Fax(object):
    """
    class for all APIs related to faxes. Don't instantiate directly - use the Fax instance in the PhaxioApi object.
    """

    def __init__(self, client):
        self._client = client

    def send(self, to, files=None, content_urls=None, header_text=None, batch_delay=None, batch_collision_avoidance=None,
             callback_url=None, cancel_timeout=None, tags_dict=None, caller_id=None, test_fail=None):
        """
        Send a fax

        :param to: A phone number or list of phone numbers in E.164 format
        :param files: The file or list of files you wish to fax. A least one file or content_url parameter is required.
        :param content_urls: A URL or list of URLs to be rendered and sent as the fax content. A least one file or content_url parameter is required.
        :param header_text: Text that will be displayed at the top of each page of the fax. 50 characters maximum.
        :param batch_delay: Enables batching and specifies the amount of time, in seconds, before the batch is fired. Maximum delay is 3600 (1 hour).
        :param batch_collision_avoidance: When batch_delay is set, fax will be blocked until the receiving machine is no longer busy.
        :param callback_url: Callback url that will override the one you have defined globally for your account.
        :param cancel_timeout: A number of minutes after which the fax will be canceled if it hasn't yet completed. Must be between 3 and 60.
        :param tags_dict: A dictionary of metadata that is relevant to your application.
        :param caller_id: A Phaxio phone number you would like to use for the caller id.
        :param test_fail: When using a test API key, this will simulate a sending failure at Phaxio. The contents of this parameter should be one of the Phaxio error types which will dictate how the fax will "fail".
        :rtype: SendFaxResponse
        """
        # make sure array parameters are lists if only one instance was passed in
        if isinstance(files, string_types):
            files = [files]
        if isinstance(content_urls, string_types):
            content_urls = [content_urls]
        if isinstance(to, string_types):
            to = [to]


        opt_args = _opt_args_to_dict(file=files, content_url=content_urls, header_text=header_text,
                                     batch_delay=batch_delay, batch_collision_avoidance=batch_collision_avoidance,
                                     callback_url=callback_url, cancel_timeout=cancel_timeout,
                                     caller_id=caller_id, test_fail=test_fail)
        _add_tags_dict(tags_dict, opt_args)

        return self._client.send_fax(to=to, **opt_args)

    def status(self, fax_id):
        """
        Get the status of a fax by ID

        :param fax_id: Fax ID
        :rtype: FaxInfo
        """
        return self._client.get_fax(fax_id)

    def cancel(self, fax_id):
        """
        Cancel sending a fax

        :param fax_id: Fax ID
        :rtype: SendFaxResponse
        """
        return self._client.cancel_fax(fax_id)

    def get_file(self, fax_id, thumbnail=None):
        """
        Get fax content file or thumbnail

        :param fax_id: Fax ID
        :param thumbnail: Either 's' (small) or 'l' (large). If specified, a thumbnail of the requested size will be returned
        :return: Filename of downloaded fax file
        """
        opt_args = _opt_args_to_dict(thumbnail=thumbnail)
        return self._client.get_fax_file(fax_id, **opt_args)

    def delete(self, fax_id):
        """
        Delete a fax. May only be used with test API credentials.

        :param fax_id: Fax ID
        :rtype: OperationStatus
        """
        return self._client.delete_fax(fax_id)

    def delete_file(self, fax_id):
        """
        Delete fax document files

        :param fax_id: Fax ID
        :rtype: OperationStatus
        """
        return self._client.delete_fax_file(fax_id)

    def resend(self, fax_id):
        """
        Resend a fax

        :param fax_id: Fax ID
        :rtype: SendFaxResponse
        """
        return self._client.resend_fax(fax_id)

    def query_faxes(self, created_before=None, created_after=None, direction=None, status=None, phone_number=None,
                    tags_dict=None, per_page=None, page=None):
        """
        List faxes in date range

        :param created_before: timestamp string in ISO-3339 format or datetime object
        :param created_after: timestamp string in ISO-3339 format or datetime object
        :param direction: Either '`sent`' or '`received`'. Limits results to faxes with the specified direction.
        :param status: Limits results to faxes with the specified status.
        :param phone_number: A phone number in E.164 format that you want to use to filter results. The phone number must be an exact match, not a number fragment
        :param tags_dict: A tag name and value that you want to use to filter results.
        :param per_page: The maximum number of results to return per call or "page" (1000 max).
        :param page: The page number to return for the request. 1-based.
        :rtype: GetFaxesResponse
        """

        opt_args = _opt_args_to_dict(created_before=created_before, created_after=created_after, direction=direction,
                                     status=status, phone_number=phone_number, per_page=per_page, page=page)
        _add_tags_dict(tags_dict, opt_args)
        return self._client.query_faxes(**opt_args)


class _Account(object):
    """
    class for retrieving account information. Don't instantiate directly - use the Account instance in the PhaxioApi object.
    """
    def __init__(self, client):
        self._client = client

    def get_status(self):
        """
        Get Account Status

        :rtype: AccountStatus
        """
        return self._client.get_account_status()


class _PhoneNumber(object):
    """
    class for all APIs related to phone numbers. Don't instantiate directly - use the PhoneNumber instance in the PhaxioApi object.
    """
    def __init__(self, client):
        self._client = client

    def get_area_codes(self, page=None, per_page=None):
        """
        List area codes available for purchasing numbers

        :param page: The maximum number of results to return per call or "page" (1000 max).
        :param per_page: The page number to return for the request. 1-based.
        :rtype: GetAreaCodesResponse
        """
        opt_args = _opt_args_to_dict(page=page, per_page=per_page)
        return self._client.get_area_codes(**opt_args)

    def get_phone_number_info(self, number):
        """
        Get number info

        :param number: A phone number in E.164 format
        :rtype: PhoneNumberResponse
        """
        return self._client.get_phone_number(number)

    def release_phone_number(self, number):
        """
        Release a phone number you no longer need

        :param number: A phone number in E.164 format
        :rtype: OperationStatus
        """
        return self._client.release_phone_number(number)

    def provision_phone_number(self, country_code, area_code, callback_url=None):
        """
        Provision a phone number that you can use to receive faxes in your Phaxio account.

        :param country_code: The country code (E.164) of the number you'd like to provision.
        :param area_code: The area code of the number you'd like to provision.
        :param callback_url: A callback URL that we'll post to when a fax is received by this number.
        :rtype: PhoneNumberResponse
        """
        opt_args = _opt_args_to_dict(callback_url=callback_url)
        return self._client.provision_phone_number(country_code, area_code, **opt_args)

    def query_phone_numbers(self, country_code=None, area_code=None, page=None, per_page=None):
        """
        Get a detailed list of the phone numbers that you currently own on Phaxio.

        :param country_code: A country code (E.164) you'd like to filter by.
        :param area_code: An area code you'd like to filter by.
        :param page: The maximum number of results to return per call or "page" (1000 max).
        :param per_page: The page number to return for the request. 1-based.
        :rtype: ListPhoneNumbersResponse
        """
        opt_args = _opt_args_to_dict(country_code=country_code, area_code=area_code, page=page, per_page=per_page)
        return self._client.query_phone_numbers(**opt_args)


class _PhaxCode(object):
    """
    class for all APIs related to PhaxCodes. Don't instantiate directly - use the PhaxCode instance in the PhaxioApi object.
    """
    def __init__(self, client):
        self._client = client

    def get_phax_code_json_response(self, phax_code_id=None):
        """
        Retrieve a PhaxCode. Response is JSON.

        :param phax_code_id: PhaxCode ID to retrieve. If omitted, gets the default PhaxCode.
        :rtype: PhaxCode
        """
        if not phax_code_id:
            return self._client.get_default_phax_code()

        return self._client.get_phax_code(phax_code_id)

    def get_phax_code_png_response(self, phax_code_id=None):
        """
        Retrieve a PhaxCode. Response is filename of downloaded png file.

        :param phax_code_id: PhaxCode ID to retrieve. If omitted, gets the default PhaxCode.
        :return: Filename of downloaded png file.
        """
        if phax_code_id:
            full_path = self._client.get_phax_code_png(phax_code_id)
        else:
            full_path = self._client.get_default_phax_code_png()

        if full_path:
            new_dir = swagger_client.configuration.temp_folder_path
            new_full_path = os.path.join(new_dir, '{}.png'.format(phax_code_id or 'phaxcode'))
            os.rename(full_path, new_full_path)
            return new_full_path

    def create_phax_code_json_response(self, metadata):
        """
        Create a custom PhaxCode. Response is JSON.

        :param metadata: Custom metadata to be associated with this barcode.
        :rtype: GeneratePhaxCodeJsonResponse
        """
        return self._client.create_phax_code_json(metadata=metadata)

    def create_phax_code_png_response(self, metadata):
        """
        Create a custom PhaxCode. Response is filename of downloaded png file.

        :param metadata: Custom metadata to be associated with this barcode.
        :return: Filename of downloaded png file.
        """
        full_path = self._client.create_phax_code_png(metadata=metadata)

        new_dir = swagger_client.configuration.temp_folder_path
        new_full_path = os.path.join(new_dir, 'phaxcode-new.png')
        os.rename(full_path, new_full_path)
        return new_full_path


class _Countries(object):
    """
    class for retrieving a list of countries Phaxio supports. Don't instantiate directly - use the Countries instance in the PhaxioApi object.
    """
    def __init__(self, client):
        self._client = client

    def get_countries(self, page=None, per_page=None):
        """
        Get a list of supported countries for sending faxes

        :param page: The maximum number of results to return per call or "page" (1000 max).
        :param per_page: The page number to return for the request. 1-based.
        :rtype: GetCountriesResponse
        """
        opt_args = _opt_args_to_dict(page=page, per_page=per_page)

        return self._client.get_countries(**opt_args)



