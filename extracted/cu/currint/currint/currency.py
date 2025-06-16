# encoding: utf8
from __future__ import unicode_literals
import six
from decimal import Decimal


@six.python_2_unicode_compatible
class Currency(object):
    """
    Represents a currency (unit of account).
    """

    def __init__(self, code, numeric_code, exponent=2, name=None, divisor=None, prefix=None, suffix=None):
        self.code = code
        self.numeric_code = numeric_code
        self.name = name
        self.prefix = prefix or ""
        self.suffix = suffix or ""
        # If they supplied no formatting info, use the currency code
        if not (self.prefix or self.suffix):
            self.suffix = " %s" % self.code
        # Either divisor or exponent must be provided, but not both
        if divisor is None:
            if exponent is None:
                raise ValueError("You must provide a value for divisor or exponent")
            else:
                self.exponent = exponent
                self.divisor = 10 ** self.exponent
        else:
            if exponent is None:
                self.exponent = None
                self.divisor = divisor
            else:
                raise ValueError("You cannot provide a value for both divisor and exponent")

    def __eq__(self, other):
        if not isinstance(other, Currency):
            return False
        return self.code == other.code

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<Currency %s (%s)>" % (self.code, self.name or "no name")

    def major_to_minor(self, value, force_round=False):
        """
        Converts an integer/long or Decimal value in major units
        (e.g. dollars not cents) into an integer value in minor units.

        Will error if the amount cannot be represented as an integer
        number of minor units (e.g. $3.453), unless force_round
        is passed, in which case the value will be rounded half-down.
        """
        # Don't allow imprecise types
        if not isinstance(value, six.integer_types + (Decimal, )):
            raise ValueError("The value passed in must be either an integer, a long or a decimal.")
        # Do the maths!
        minor_value = value * self.divisor
        if force_round:
            minor_value = int(round(minor_value))
        if (minor_value != int(minor_value)):
            raise ValueError(
                "Cannot convert major amount %r to minor amount; would result in fractional amount of minor unit"
                % value
            )
        return int(minor_value)

    def minor_to_major(self, value):
        """
        Converts an integer/long number of minor units (e.g. cents not dollars)
        to a Decimal value of major units.

        Note that this should not be used for further calculation (work with
        the Amount class for that), nor for display purposes (use the format functions)
        """

        # Don't allow imprecise types
        if not isinstance(value, six.integer_types):
            raise ValueError("The value passed in must be either an integer or a long")
        # Simple maths really.
        return Decimal(value) / self.divisor

    def format(self, value):
        """
        Formats a value (in the minor unit as an integer) as a string,
        with the local prefix/suffix.
        """
        return "%s%s%s" % (
            self.prefix,
            self.format_decimal(value),
            self.suffix,
        )

    def format_decimal(self, value):
        """
        Formats a value (in the minor unit as an integer) as a string,
        with no local prefix/suffix.  Can be cast into a Decimal value as needed.
        """
        major_value = self.minor_to_major(value)

        if self.exponent is not None:
            format_str = "{:.{precision}f}"
            format_kwargs = dict(precision=self.exponent)
        else:
            # A custom `divisor` can produce arbitrary precision major representations (think divisor=13)
            format_str = "{:f}"
            format_kwargs = {}

        return format_str.format(major_value, **format_kwargs)


currencies = {
    "AED": Currency("AED", "784", 2, 'UAE Dirham'),
    "AFN": Currency("AFN", "971", 2, 'Afghani'),
    "ALL": Currency("ALL", "008", 2, 'Lek'),
    "AMD": Currency("AMD", "051", 2, 'Armenian Dram'),
    "ANG": Currency("ANG", "532", 2, 'Netherlands Antillean Guilder'),
    "AOA": Currency("AOA", "973", 2, 'Kwanza'),
    "ARS": Currency("ARS", "032", 2, 'Argentine Peso'),
    "AUD": Currency("AUD", "036", 2, 'Australian Dollar'),
    "AWG": Currency("AWG", "533", 2, 'Aruban Florin'),
    "AZN": Currency("AZN", "944", 2, 'Azerbaijanian Manat'),
    "BAM": Currency("BAM", "977", 2, 'Convertible Mark'),
    "BBD": Currency("BBD", "052", 2, 'Barbados Dollar'),
    "BDT": Currency("BDT", "050", 2, 'Taka'),
    "BGN": Currency("BGN", "975", 2, 'Bulgarian Lev'),
    "BHD": Currency("BHD", "048", 3, 'Bahraini Dinar'),
    "BIF": Currency("BIF", "108", 0, 'Burundi Franc'),
    "BMD": Currency("BMD", "060", 2, 'Bermudian Dollar'),
    "BND": Currency("BND", "096", 2, 'Brunei Dollar'),
    "BOB": Currency("BOB", "068", 2, 'Boliviano'),
    "BOV": Currency("BOV", "984", 2, 'Mvdol'),
    "BRL": Currency("BRL", "986", 2, 'Brazilian Real'),
    "BSD": Currency("BSD", "044", 2, 'Bahamian Dollar'),
    "BTN": Currency("BTN", "064", 2, 'Ngultrum'),
    "BWP": Currency("BWP", "072", 2, 'Pula'),
    "BYR": Currency("BYR", "974", 0, 'Belarussian Ruble'),
    "BZD": Currency("BZD", "084", 2, 'Belize Dollar'),
    "CAD": Currency("CAD", "124", 2, 'Canadian Dollar'),
    "CDF": Currency("CDF", "976", 2, 'Congolese Franc'),
    "CHE": Currency("CHE", "947", 2, 'WIR Euro'),
    "CHF": Currency("CHF", "756", 2, 'Swiss Franc'),
    "CHW": Currency("CHW", "948", 2, 'WIR Franc'),
    "CLF": Currency("CLF", "990", 0, 'Unidad de Fomento'),
    "CLP": Currency("CLP", "152", 0, 'Chilean Peso'),
    "CNY": Currency("CNY", "156", 2, 'Yuan Renminbi'),
    "COP": Currency("COP", "170", 2, 'Colombian Peso'),
    "COU": Currency("COU", "970", 2, 'Unidad de Valor Real'),
    "CRC": Currency("CRC", "188", 2, 'Costa Rican Colon'),
    "CUC": Currency("CUC", "931", 2, 'Peso Convertible'),
    "CUP": Currency("CUP", "192", 2, 'Cuban Peso'),
    "CVE": Currency("CVE", "132", 2, 'Cape Verde Escudo'),
    "CZK": Currency("CZK", "203", 2, 'Czech Koruna'),
    "DJF": Currency("DJF", "262", 0, 'Djibouti Franc'),
    "DKK": Currency("DKK", "208", 2, 'Danish Krone'),
    "DOP": Currency("DOP", "214", 2, 'Dominican Peso'),
    "DZD": Currency("DZD", "012", 2, 'Algerian Dinar'),
    "EGP": Currency("EGP", "818", 2, 'Egyptian Pound'),
    "ERN": Currency("ERN", "232", 2, 'Nakfa'),
    "ETB": Currency("ETB", "230", 2, 'Ethiopian Birr'),
    "EUR": Currency("EUR", "978", 2, 'Euro'),
    "FJD": Currency("FJD", "242", 2, 'Fiji Dollar'),
    "FKP": Currency("FKP", "238", 2, 'Falkland Islands Pound'),
    "GBP": Currency("GBP", "826", 2, 'Pound Sterling'),
    "GEL": Currency("GEL", "981", 2, 'Lari'),
    "GHS": Currency("GHS", "936", 2, 'Ghana Cedi'),
    "GIP": Currency("GIP", "292", 2, 'Gibraltar Pound'),
    "GMD": Currency("GMD", "270", 2, 'Dalasi'),
    "GNF": Currency("GNF", "324", 0, 'Guinea Franc'),
    "GTQ": Currency("GTQ", "320", 2, 'Quetzal'),
    "GYD": Currency("GYD", "328", 2, 'Guyana Dollar'),
    "HKD": Currency("HKD", "344", 2, 'Hong Kong Dollar'),
    "HNL": Currency("HNL", "340", 2, 'Lempira'),
    "HRK": Currency("HRK", "191", 2, 'Croatian Kuna'),
    "HTG": Currency("HTG", "332", 2, 'Gourde'),
    "HUF": Currency("HUF", "348", 2, 'Forint'),
    "IDR": Currency("IDR", "360", 2, 'Rupiah'),
    "ILS": Currency("ILS", "376", 2, 'New Israeli Sheqel'),
    "INR": Currency("INR", "356", 2, 'Indian Rupee'),
    "IQD": Currency("IQD", "368", 3, 'Iraqi Dinar'),
    "IRR": Currency("IRR", "364", 2, 'Iranian Rial'),
    "ISK": Currency("ISK", "352", 0, 'Iceland Krona'),
    "JMD": Currency("JMD", "388", 2, 'Jamaican Dollar'),
    "JOD": Currency("JOD", "400", 3, 'Jordanian Dinar'),
    "JPY": Currency("JPY", "392", 0, 'Yen'),
    "KES": Currency("KES", "404", 2, 'Kenyan Shilling'),
    "KGS": Currency("KGS", "417", 2, 'Som'),
    "KHR": Currency("KHR", "116", 2, 'Riel'),
    "KMF": Currency("KMF", "174", 0, 'Comoro Franc'),
    "KPW": Currency("KPW", "408", 2, 'North Korean Won'),
    "KRW": Currency("KRW", "410", 0, 'Won'),
    "KWD": Currency("KWD", "414", 3, 'Kuwaiti Dinar'),
    "KYD": Currency("KYD", "136", 2, 'Cayman Islands Dollar'),
    "KZT": Currency("KZT", "398", 2, 'Tenge'),
    "LAK": Currency("LAK", "418", 2, 'Kip'),
    "LBP": Currency("LBP", "422", 2, 'Lebanese Pound'),
    "LKR": Currency("LKR", "144", 2, 'Sri Lanka Rupee'),
    "LRD": Currency("LRD", "430", 2, 'Liberian Dollar'),
    "LSL": Currency("LSL", "426", 2, 'Loti'),
    "LTL": Currency("LTL", "440", 2, 'Lithuanian Litas'),
    "LYD": Currency("LYD", "434", 3, 'Libyan Dinar'),
    "MAD": Currency("MAD", "504", 2, 'Moroccan Dirham'),
    "MDL": Currency("MDL", "498", 2, 'Moldovan Leu'),
    "MGA": Currency("MGA", "969", None, 'Malagasy Ariary', divisor=5),
    "MKD": Currency("MKD", "807", 2, 'Denar'),
    "MMK": Currency("MMK", "104", 2, 'Kyat'),
    "MNT": Currency("MNT", "496", 2, 'Tugrik'),
    "MOP": Currency("MOP", "446", 2, 'Pataca'),
    "MRO": Currency("MRO", "478", None, 'Ouguiya', divisor=5),
    "MUR": Currency("MUR", "480", 2, 'Mauritius Rupee'),
    "MVR": Currency("MVR", "462", 2, 'Rufiyaa'),
    "MWK": Currency("MWK", "454", 2, 'Kwacha'),
    "MXN": Currency("MXN", "484", 2, 'Mexican Peso'),
    "MXV": Currency("MXV", "979", 2, 'Mexican Unidad de Inversion (UDI)'),
    "MYR": Currency("MYR", "458", 2, 'Malaysian Ringgit'),
    "MZN": Currency("MZN", "943", 2, 'Mozambique Metical'),
    "NAD": Currency("NAD", "516", 2, 'Namibia Dollar'),
    "NGN": Currency("NGN", "566", 2, 'Naira'),
    "NIO": Currency("NIO", "558", 2, 'Cordoba Oro'),
    "NOK": Currency("NOK", "578", 2, 'Norwegian Krone'),
    "NPR": Currency("NPR", "524", 2, 'Nepalese Rupee'),
    "NZD": Currency("NZD", "554", 2, 'New Zealand Dollar'),
    "OMR": Currency("OMR", "512", 3, 'Rial Omani'),
    "PAB": Currency("PAB", "590", 2, 'Balboa'),
    "PEN": Currency("PEN", "604", 2, 'Nuevo Sol'),
    "PGK": Currency("PGK", "598", 2, 'Kina'),
    "PHP": Currency("PHP", "608", 2, 'Philippine Peso'),
    "PKR": Currency("PKR", "586", 2, 'Pakistan Rupee'),
    "PLN": Currency("PLN", "985", 2, 'Zloty'),
    "PYG": Currency("PYG", "600", 0, 'Guarani'),
    "QAR": Currency("QAR", "634", 2, 'Qatari Rial'),
    "RON": Currency("RON", "946", 2, 'New Romanian Leu'),
    "RSD": Currency("RSD", "941", 2, 'Serbian Dinar'),
    "RUB": Currency("RUB", "643", 2, 'Russian Ruble'),
    "RWF": Currency("RWF", "646", 0, 'Rwanda Franc'),
    "SAR": Currency("SAR", "682", 2, 'Saudi Riyal'),
    "SBD": Currency("SBD", "090", 2, 'Solomon Islands Dollar'),
    "SCR": Currency("SCR", "690", 2, 'Seychelles Rupee'),
    "SDG": Currency("SDG", "938", 2, 'Sudanese Pound'),
    "SEK": Currency("SEK", "752", 2, 'Swedish Krona'),
    "SGD": Currency("SGD", "702", 2, 'Singapore Dollar'),
    "SHP": Currency("SHP", "654", 2, 'Saint Helena Pound'),
    "SLL": Currency("SLL", "694", 2, 'Leone'),
    "SOS": Currency("SOS", "706", 2, 'Somali Shilling'),
    "SRD": Currency("SRD", "968", 2, 'Surinam Dollar'),
    "SSP": Currency("SSP", "728", 2, 'South Sudanese Pound'),
    "STD": Currency("STD", "678", 2, 'Dobra'),
    "SVC": Currency("SVC", "222", 2, 'El Salvador Colon'),
    "SYP": Currency("SYP", "760", 2, 'Syrian Pound'),
    "SZL": Currency("SZL", "748", 2, 'Lilangeni'),
    "THB": Currency("THB", "764", 2, 'Baht'),
    "TJS": Currency("TJS", "972", 2, 'Somoni'),
    "TMT": Currency("TMT", "934", 2, 'Turkmenistan New Manat'),
    "TND": Currency("TND", "788", 3, 'Tunisian Dinar'),
    "TOP": Currency("TOP", "776", 2, 'Pa\'anga'),
    "TRY": Currency("TRY", "949", 2, 'Turkish Lira'),
    "TTD": Currency("TTD", "780", 2, 'Trinidad and Tobago Dollar'),
    "TWD": Currency("TWD", "901", 2, 'New Taiwan Dollar'),
    "TZS": Currency("TZS", "834", 2, 'Tanzanian Shilling'),
    "UAH": Currency("UAH", "980", 2, 'Hryvnia'),
    "UGX": Currency("UGX", "800", 0, 'Uganda Shilling'),
    "USD": Currency("USD", "840", 2, 'US Dollar'),
    "UYI": Currency("UYI", "940", 0, 'Uruguay Peso en Unidades Indexadas (URUIURUI)'),
    "UYU": Currency("UYU", "858", 2, 'Peso Uruguayo'),
    "UZS": Currency("UZS", "860", 2, 'Uzbekistan Sum'),
    "VEF": Currency("VEF", "937", 2, 'Bolivar'),
    "VND": Currency("VND", "704", 0, 'Dong'),
    "VUV": Currency("VUV", "548", 0, 'Vatu'),
    "WST": Currency("WST", "882", 2, 'Tala'),
    "XAF": Currency("XAF", "950", 0, 'CFA Franc BEAC'),
    "XCD": Currency("XCD", "951", 2, 'East Caribbean Dollar'),
    "XOF": Currency("XOF", "952", 0, 'CFA Franc BCEAO'),
    "XPF": Currency("XPF", "953", 0, 'CFP Franc'),
    "YER": Currency("YER", "886", 2, 'Yemeni Rial'),
    "ZAR": Currency("ZAR", "710", 2, 'Rand'),
    "ZMW": Currency("ZMW", "967", 2, 'Zambian Kwacha'),
    "ZWL": Currency("ZWL", "932", 2, 'Zimbabwe Dollar'),
    # Why not?
    "XBT": Currency("XBT", None, 8, "Bitcoin"),
}
