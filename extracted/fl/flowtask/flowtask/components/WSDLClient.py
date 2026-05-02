import os
from pathlib import Path

# zeep integration
from zeep import Client, Settings, helpers
from zeep.transports import Transport
from ..exceptions import ComponentError
from .flow import FlowComponent


class WSDLClient(FlowComponent):
    """
    WSDLClient.

        Client for WSDL SOAP Web Services using Zeep

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          WSDLClient:
          # attributes here
        ```
    """
    _version = "1.0.0"

    transport = None
    transport_options = {"timeout": 10}
    method = ""
    settings = None
    settings_options = {"strict": True, "xml_huge_tree": False}
    _wsdl = None
    url: str = ""
    raw_response = False
    _filename: str = ""
    _directory: str = ""
    saving_xml = False

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        # defining methods for WSDL Client
        self.transport = Transport(**self.transport_options)
        self.settings = Settings(**self.settings_options)
        if not hasattr(self, "method"):
            raise ComponentError(
                "WSDL Error: You need to define a Method using *method* attribute"
            )
        if not self.url:
            raise ComponentError(
                "WSDL Error: You need to define a WSDL endpoint using the *url* attribute"
            )
        # creating a client:
        self._wsdl = Client(self.url, settings=self.settings)
        # check if we need to save to an xml file:
        if hasattr(self, "to_file"):
            self.saving_xml = True
            self._directory = Path(self.to_file["directory"])
            if "filename" in self.to_file:
                self._filename = self.to_file["filename"]
            else:
                # using a pattern:
                f = self.to_file["file"]
                file = f["pattern"]
                if hasattr(self, "masks"):
                    for mask, replace in self.masks.items():
                        if isinstance(replace, str):
                            m = mask.translate({ord("{"): None, ord("}"): None})
                            if m in self.params.keys():
                                # using params instead mask value
                                file = file.replace(mask, self.params[m])
                            else:
                                # replace inmediately
                                file = file.replace(mask, replace)
                        # else:
                        #    file = file.replace(mask, convert(replace))
                self._filename = file

    @property
    def client(self):
        return self._wsdl

    async def close(self):
        """Method."""
        self._wsdl = None

    def saving_file(self, content):
        if not self._directory.exists():
            raise ComponentError(
                f"Directory for saving XML file doesn't exists: {self._directory}"
            )
        path = self._directory.joinpath(self._filename)
        if path.exists():
            if "replace" in self.to_file:
                os.remove(path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        if self._debug:
            print(f"Saving XML File on: {path}")
        # self._result = path

    def queryMethod(self, method, **kwargs):
        response = None
        if not method:
            method = self.method
        try:
            fn = getattr(self._wsdl.service, method)
            response = fn(**kwargs)
        except Exception as err:
            raise ComponentError(
                f"Error Calling method {method} over WSDL client, error: {err}"
            ) from err
        finally:
            return response

    async def run(self):
        response = None
        try:
            with self._wsdl.settings(raw_response=self.raw_response):
                obj = self.queryMethod(self.method, **self.params)
                if obj:
                    if hasattr(self, "serialize"):
                        response = helpers.serialize_object(obj, dict)
                    else:
                        response = obj
                    self._result = response
                    return self._result
                else:
                    return False
        except (ComponentError, Exception) as err:
            raise ComponentError(str(err)) from err
