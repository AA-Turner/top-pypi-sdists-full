import unittest.mock
from io import BytesIO

from slixmpp.plugins.xep_0363.http_upload import PurposeNotSupported
from slixmpp.test import SlixTest


class TestHTTPUpload(SlixTest):
    def setUp(self) -> None:
        self.stream_start(
            plugins={"xep_0363"},
            plugin_config={"xep_0363": {"upload_service": "upload.test"}},
        )
        self.__put_mock = unittest.mock.AsyncMock()
        self.__response_mock = unittest.mock.AsyncMock()
        self.__response_mock.close = lambda: None
        self.__response_mock.status = 200
        self.__put_mock.return_value = self.__response_mock
        self.__patcher = unittest.mock.patch(
            "aiohttp.ClientSession.put", self.__put_mock
        )
        self.__patcher.start()
        self.__file = BytesIO(b"xxxxx")

    def tearDown(self) -> None:
        self.__patcher.stop()
        super().tearDown()

    def test_no_purpose(self) -> None:
        task = self.xmpp.loop.create_task(
            self.xmpp.plugin["xep_0363"].upload_file("test.jpg", input_file=self.__file)
        )
        self.send("""
        <iq xmlns="jabber:client" id="1" type="get" to="upload.test">
          <request xmlns="urn:xmpp:http:upload:0"
                   filename="test.jpg"
                   size="5"
                   content-type="image/jpeg" />
        </iq>
        """)
        self.__recv_slot()
        self.__assert_put_awaited()
        assert task.result() == "get_url"

    def test_purpose_not_supported(self) -> None:
        task = self.xmpp.loop.create_task(
            self.xmpp.plugin["xep_0363"].upload_file(
                "test.jpg", input_file=self.__file, purpose="profile"
            )
        )
        self.send("""
        <iq xmlns="jabber:client" id="1" to="upload.test" type="get">
          <query xmlns="http://jabber.org/protocol/disco#info" />
        </iq>
        """)
        self.recv("""
        <iq from='upload.test' id='1' type='result'>
          <query xmlns='http://jabber.org/protocol/disco#info'>
            <feature var='urn:xmpp:http:upload:0' />
          </query>
        </iq>
        """)
        self.assertRaises(PurposeNotSupported, task.result)

    def test_purpose_supported(self) -> None:
        task = self.xmpp.loop.create_task(
            self.xmpp.plugin["xep_0363"].upload_file(
                "test.jpg", input_file=self.__file, purpose="profile"
            )
        )
        self.send("""
        <iq xmlns="jabber:client" id="1" to="upload.test" type="get">
          <query xmlns="http://jabber.org/protocol/disco#info" />
        </iq>
        """)
        self.recv("""
        <iq from='upload.test' id='1' type='result'>
          <query xmlns='http://jabber.org/protocol/disco#info'>
            <feature var='urn:xmpp:http:upload:0' />
            <feature var='urn:xmpp:http:upload:purpose:0#profile' />
          </query>
        </iq>
        """)
        self.send("""
        <iq xmlns="jabber:client" id="2" type="get" to="upload.test">
          <request xmlns="urn:xmpp:http:upload:0"
                   filename="test.jpg"
                   size="5"
                   content-type="image/jpeg">
            <profile xmlns="urn:xmpp:http:upload:purpose:0"/>
          </request>
        </iq>
        """)
        self.__recv_slot(2)
        self.__assert_put_awaited()
        assert task.result() == "get_url"

    def __recv_slot(self, id_: int = 1) -> None:
        self.recv(f"""
        <iq xmlns="jabber:client" id="{id_}" type="result" from="upload.test">
          <slot xmlns='urn:xmpp:http:upload:0'>
            <put url='put_url'>
              <header name='some-name'>some-value</header>
            </put>
            <get url='get_url' />
          </slot>
        </iq>
        """)

    def __assert_put_awaited(self) -> None:
        self.__put_mock.assert_awaited_once_with(
            "put_url",
            data=self.__file,
            headers={
                "Content-Length": "5",
                "Content-Type": "image/jpeg",
                "some-name": "some-value",
            },
        )


suite = unittest.TestLoader().loadTestsFromTestCase(TestHTTPUpload)
