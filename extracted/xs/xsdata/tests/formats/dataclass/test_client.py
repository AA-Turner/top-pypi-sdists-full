from dataclasses import asdict, replace
from unittest import TestCase, mock

from tests.fixtures.calculator import (
    Add,
    CalculatorSoapAdd,
    CalculatorSoapAddInput,
    CalculatorSoapAddOutput,
)
from tests.fixtures.hello import HelloGetHelloAsString
from xsdata.exceptions import ClientValueError
from xsdata.formats.dataclass.client import Client, Config, TransportTypes
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.transports import DefaultTransport

response = """
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <soap:Body>
        <AddResponse xmlns="http://tempuri.org/">
            <AddResult>7</AddResult>
        </AddResponse>
    </soap:Body>
</soap:Envelope>"""


class ClientTests(TestCase):
    def test__init__(self) -> None:
        config = Config.from_service(CalculatorSoapAdd, transport="foobar")

        client = Client(config)
        self.assertIs(client.parser.context, client.serializer.context)

        client = Client(config, parser=XmlParser())
        self.assertIs(client.parser.context, client.serializer.context)

        client = Client(config, serializer=XmlSerializer())
        self.assertIs(client.parser.context, client.serializer.context)

    def test_from_service(self) -> None:
        client = Client.from_service(CalculatorSoapAdd, location="http://testurl.com")

        actual = asdict(client.config)
        expected = {
            "style": "document",
            "input": CalculatorSoapAddInput,
            "location": "http://testurl.com",
            "soap_action": "http://tempuri.org/Add",
            "output": CalculatorSoapAddOutput,
            "transport": "http://schemas.xmlsoap.org/soap/http",
            "encoding": None,
        }

        self.assertEqual(expected, actual)

    @mock.patch.object(DefaultTransport, "post")
    def test_send_with_dict_params(self, mock_post) -> None:
        mock_post.return_value = response.encode()

        client = Client.from_service(CalculatorSoapAdd)
        params = {"Body": {"Add": {"intA": 3, "intB": 4}}}

        result = client.send(params, headers={"User-Agent": "xsdata"})

        self.assertIsInstance(result, CalculatorSoapAddOutput)
        self.assertEqual(7, result.body.add_response.add_result)

        obj = CalculatorSoapAddInput(body=CalculatorSoapAddInput.Body(add=Add(3, 4)))
        request = client.serializer.render(obj)

        mock_post.assert_called_once_with(
            "http://www.dneonline.com/calculator.asmx",
            data=request,
            headers={
                "User-Agent": "xsdata",
                "content-type": "text/xml",
                "SOAPAction": "http://tempuri.org/Add",
            },
        )

    @mock.patch.object(DefaultTransport, "post")
    def test_send_with_instance_object(self, mock_post) -> None:
        mock_post.return_value = response.encode()

        client = Client.from_service(CalculatorSoapAdd)
        obj = CalculatorSoapAddInput(body=CalculatorSoapAddInput.Body(add=Add(3, 4)))
        result = client.send(obj)

        self.assertIsInstance(result, CalculatorSoapAddOutput)
        self.assertEqual(7, result.body.add_response.add_result)

        request = client.serializer.render(obj)

        mock_post.assert_called_once_with(
            "http://www.dneonline.com/calculator.asmx",
            data=request,
            headers={
                "content-type": "text/xml",
                "SOAPAction": "http://tempuri.org/Add",
            },
        )

    def test_prepare_payload_with_encoding(self) -> None:
        client = Client.from_service(HelloGetHelloAsString, encoding="utf-8")
        result = client.prepare_payload(
            {"Body": {"getHelloAsString": {"arg0": "Χριστόδουλος"}}}
        )
        self.assertIn("Χριστόδουλος".encode(), result)

    def test_prepare_payload_raises_error_with_type_mismatch(self) -> None:
        client = Client.from_service(CalculatorSoapAdd)

        with self.assertRaises(ClientValueError) as cm:
            client.prepare_payload(CalculatorSoapAddOutput())

        self.assertEqual(
            "Invalid input service type, expected "
            "`CalculatorSoapAddInput` got `CalculatorSoapAddOutput`",
            str(cm.exception),
        )

    def test_prepare_headers(self) -> None:
        config = Config(
            style="document",
            location="",
            transport=TransportTypes.SOAP,
            soap_action="",
            input=None,
            output=None,
        )
        client = Client(config=config)

        headers = {"foo": "bar"}
        result = client.prepare_headers(headers)
        self.assertEqual({"content-type": "text/xml", "foo": "bar"}, result)
        self.assertEqual(1, len(headers))

        config = replace(config, soap_action="add")
        client = Client(config=config)
        result = client.prepare_headers({})
        self.assertEqual({"SOAPAction": "add", "content-type": "text/xml"}, result)

    def test_prepare_headers_raises_error_with_unsupported_binding_transport(
        self,
    ) -> None:
        config = Config.from_service(CalculatorSoapAdd, transport="foobar")
        client = Client(config=config)

        with self.assertRaises(ClientValueError) as cm:
            client.prepare_headers({})

        self.assertEqual("Unsupported binding transport: `foobar`", str(cm.exception))
