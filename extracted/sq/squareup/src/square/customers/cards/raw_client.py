# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...requests.address import AddressParams
from ...core.request_options import RequestOptions
from ...core.http_response import HttpResponse
from ...types.create_customer_card_response import CreateCustomerCardResponse
from ...core.jsonable_encoder import jsonable_encoder
from ...core.serialization import convert_and_respect_annotation_metadata
from ...core.unchecked_base_model import construct_type
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...types.delete_customer_card_response import DeleteCustomerCardResponse
from ...core.client_wrapper import AsyncClientWrapper
from ...core.http_response import AsyncHttpResponse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class RawCardsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(
        self,
        customer_id: str,
        *,
        card_nonce: str,
        billing_address: typing.Optional[AddressParams] = OMIT,
        cardholder_name: typing.Optional[str] = OMIT,
        verification_token: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> HttpResponse[CreateCustomerCardResponse]:
        """
        Adds a card on file to an existing customer.

        As with charges, calls to `CreateCustomerCard` are idempotent. Multiple
        calls with the same card nonce return the same card record that was created
        with the provided nonce during the _first_ call.

        Parameters
        ----------
        customer_id : str
            The Square ID of the customer profile the card is linked to.

        card_nonce : str
            A card nonce representing the credit card to link to the customer.

            Card nonces are generated by the Square payment form when customers enter
            their card information. For more information, see
            [Walkthrough: Integrate Square Payments in a Website](https://developer.squareup.com/docs/web-payments/take-card-payment).

            __NOTE:__ Card nonces generated by digital wallets (such as Apple Pay)
            cannot be used to create a customer card.

        billing_address : typing.Optional[AddressParams]
            Address information for the card on file.

            __NOTE:__ If a billing address is provided in the request, the
            `CreateCustomerCardRequest.billing_address.postal_code` must match
            the postal code encoded in the card nonce.

        cardholder_name : typing.Optional[str]
            The full name printed on the credit card.

        verification_token : typing.Optional[str]
            An identifying token generated by [Payments.verifyBuyer()](https://developer.squareup.com/reference/sdks/web/payments/objects/Payments#Payments.verifyBuyer).
            Verification tokens encapsulate customer device information and 3-D Secure
            challenge results to indicate that Square has verified the buyer identity.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[CreateCustomerCardResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/customers/{jsonable_encoder(customer_id)}/cards",
            method="POST",
            json={
                "card_nonce": card_nonce,
                "billing_address": convert_and_respect_annotation_metadata(
                    object_=billing_address, annotation=AddressParams, direction="write"
                ),
                "cardholder_name": cardholder_name,
                "verification_token": verification_token,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    CreateCustomerCardResponse,
                    construct_type(
                        type_=CreateCustomerCardResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, customer_id: str, card_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> HttpResponse[DeleteCustomerCardResponse]:
        """
        Removes a card on file from a customer.

        Parameters
        ----------
        customer_id : str
            The ID of the customer that the card on file belongs to.

        card_id : str
            The ID of the card on file to delete.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        HttpResponse[DeleteCustomerCardResponse]
            Success
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v2/customers/{jsonable_encoder(customer_id)}/cards/{jsonable_encoder(card_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DeleteCustomerCardResponse,
                    construct_type(
                        type_=DeleteCustomerCardResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return HttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncRawCardsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(
        self,
        customer_id: str,
        *,
        card_nonce: str,
        billing_address: typing.Optional[AddressParams] = OMIT,
        cardholder_name: typing.Optional[str] = OMIT,
        verification_token: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AsyncHttpResponse[CreateCustomerCardResponse]:
        """
        Adds a card on file to an existing customer.

        As with charges, calls to `CreateCustomerCard` are idempotent. Multiple
        calls with the same card nonce return the same card record that was created
        with the provided nonce during the _first_ call.

        Parameters
        ----------
        customer_id : str
            The Square ID of the customer profile the card is linked to.

        card_nonce : str
            A card nonce representing the credit card to link to the customer.

            Card nonces are generated by the Square payment form when customers enter
            their card information. For more information, see
            [Walkthrough: Integrate Square Payments in a Website](https://developer.squareup.com/docs/web-payments/take-card-payment).

            __NOTE:__ Card nonces generated by digital wallets (such as Apple Pay)
            cannot be used to create a customer card.

        billing_address : typing.Optional[AddressParams]
            Address information for the card on file.

            __NOTE:__ If a billing address is provided in the request, the
            `CreateCustomerCardRequest.billing_address.postal_code` must match
            the postal code encoded in the card nonce.

        cardholder_name : typing.Optional[str]
            The full name printed on the credit card.

        verification_token : typing.Optional[str]
            An identifying token generated by [Payments.verifyBuyer()](https://developer.squareup.com/reference/sdks/web/payments/objects/Payments#Payments.verifyBuyer).
            Verification tokens encapsulate customer device information and 3-D Secure
            challenge results to indicate that Square has verified the buyer identity.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[CreateCustomerCardResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/customers/{jsonable_encoder(customer_id)}/cards",
            method="POST",
            json={
                "card_nonce": card_nonce,
                "billing_address": convert_and_respect_annotation_metadata(
                    object_=billing_address, annotation=AddressParams, direction="write"
                ),
                "cardholder_name": cardholder_name,
                "verification_token": verification_token,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    CreateCustomerCardResponse,
                    construct_type(
                        type_=CreateCustomerCardResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete(
        self, customer_id: str, card_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AsyncHttpResponse[DeleteCustomerCardResponse]:
        """
        Removes a card on file from a customer.

        Parameters
        ----------
        customer_id : str
            The ID of the customer that the card on file belongs to.

        card_id : str
            The ID of the card on file to delete.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        AsyncHttpResponse[DeleteCustomerCardResponse]
            Success
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v2/customers/{jsonable_encoder(customer_id)}/cards/{jsonable_encoder(card_id)}",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                _data = typing.cast(
                    DeleteCustomerCardResponse,
                    construct_type(
                        type_=DeleteCustomerCardResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
                return AsyncHttpResponse(response=_response, data=_data)
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
