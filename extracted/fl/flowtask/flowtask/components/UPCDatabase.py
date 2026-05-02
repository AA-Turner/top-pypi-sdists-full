from datetime import date
from .RESTClient import AbstractREST


class UPCDatabase(AbstractREST):
    """
    UPCDatabase.

    Querying UPC Database for Product information.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UPCDatabase:
          method: currency
          base: USD
          credentials:
          apikey: UPC_API_KEY
        ```
    """
    _version = "1.0.0"

    base_url: str = "https://api.upcdatabase.org/"
    _default_method: str = "currency"

    async def start(self, **kwargs):
        if not self.credentials:
            # obtengo las credenciales
            self.credentials["apikey"] = self._environment.get("UPC_API_KEY")
            if not self.credentials["apikey"]:
                raise ValueError("UPC Database: Missing Credentials")
        # calling method for this element:
        await super(UPCDatabase, self).start(**kwargs)

    async def currency(self):
        """currency.

        Currency information and exchange rates supported by UPC
        """
        self.method = "get"
        self.url = self.base_url + "currency/latest/"
        try:
            self.parameters["base"] = self.base
        except (ValueError, TypeError):
            self.parameters["base"] = "USD"

    async def currency_history(self):
        """currency.

        Retrieves the currency conversion rates for a specific date.
        """
        self.method = "get"
        self.url = self.base_url + "currency/history"
        try:
            self.parameters["base"] = self.base
        except (ValueError, TypeError):
            self.parameters["base"] = "USD"
        try:
            self.parameters["date"] = self.date
        except (ValueError, AttributeError):
            today = date.today()
            self.parameters["date"] = today.strftime("%Y-%m-%d")

    async def product(self):
        """product.

        Product information based on UPC barcode
        """
        self.method = "get"
        if not "barcode" in self._args:
            raise ValueError("UPC Database: Missing Barcode")
        self.url = self.base_url + "product/{barcode}"

    async def search(self):
        """product.

        Search for a product based on item parameters.
        """
        self.method = "get"
        self.url = self.base_url + "search/"
        self.parameters["page"] = 1
        try:
            self.parameters["query"] = self.query
        except (ValueError, TypeError) as e:
            raise ValueError("UPC Database: Missing or wrong *query* Search.") from e
