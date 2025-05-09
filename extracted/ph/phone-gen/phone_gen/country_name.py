"""Sources: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes."""

from typing import Dict

COUNTRY_NAME: Dict[str, Dict[str, str]] = {
    "AFGHANISTAN": {"name": "Afghanistan", "code": "AF"},
    "ALANDISLANDS": {"name": "Åland Islands", "code": "AX"},
    "ALBANIA": {"name": "Albania", "code": "AL"},
    "ALGERIA": {"name": "Algeria", "code": "DZ"},
    "AMERICANSAMOA": {"name": "American Samoa", "code": "AS"},
    "ANDORRA": {"name": "Andorra", "code": "AD"},
    "ANGOLA": {"name": "Angola", "code": "AO"},
    "ANGUILLA": {"name": "Anguilla", "code": "AI"},
    "ANTARCTICA": {"name": "Antarctica", "code": "AQ"},
    "ANTIGUAANDBARBUDA": {"name": "Antigua and Barbuda", "code": "AG"},
    "ARGENTINA": {"name": "Argentina", "code": "AR"},
    "ARMENIA": {"name": "Armenia", "code": "AM"},
    "ARUBA": {"name": "Aruba", "code": "AW"},
    "ASCENSIONISLAND": {"name": "Ascension Island", "code": "AC"},
    "AUSTRALIA": {"name": "Australia", "code": "AU"},
    "AUSTRIA": {"name": "Austria", "code": "AT"},
    "AZERBAIJAN": {"name": "Azerbaijan", "code": "AZ"},
    "Bahamas": {"name": "Bahamas", "code": "BS"},
    "BAHRAIN": {"name": "Bahrain", "code": "BH"},
    "BANGLADESH": {"name": "Bangladesh", "code": "BD"},
    "BARBADOS": {"name": "Barbados", "code": "BB"},
    "BELARUS": {"name": "Belarus", "code": "BY"},
    "BELGIUM": {"name": "Belgium", "code": "BE"},
    "BELIZE": {"name": "Belize", "code": "BZ"},
    "BENIN": {"name": "Benin", "code": "BJ"},
    "BERMUDA": {"name": "Bermuda", "code": "BM"},
    "BHUTAN": {"name": "Bhutan", "code": "BT"},
    "BOLIVIA": {"name": "Bolivia", "code": "BO"},
    "BONAIRE": {"name": "Bonaire", "code": "BQ"},
    "BOSNIAANDHERZEGOVINA": {"name": "Bosnia and Herzegovina", "code": "BA"},
    "BOTSWANA": {"name": "Botswana", "code": "BW"},
    "BOUVETISLAND": {"name": "Bouvet Island", "code": "BV"},
    "BRAZIL": {"name": "Brazil", "code": "BR"},
    "BRITISHINDIANOCEANTERRITORY": {"name": "British Indian Ocean Territory", "code": "IO"},
    "BRITISHVIRGINISLANDS": {"name": "British Virgin Islands", "code": "VG"},
    "BRUNEIDARUSSALAM": {"name": "Brunei Darussalam", "code": "BN"},
    "BULGARIA": {"name": "Bulgaria", "code": "BG"},
    "BURKINAFASO": {"name": "Burkina Faso", "code": "BF"},
    "BURMA": {"name": "Myanmar", "code": "MM"},
    "BURUNDI": {"name": "Burundi", "code": "BI"},
    "CABOVERDE": {"name": "Cabo Verde", "code": "CV"},
    "CAMBODIA": {"name": "Cambodia", "code": "KH"},
    "CAMEROON": {"name": "Cameroon", "code": "CM"},
    "CANADA": {"name": "Canada", "code": "CA"},
    "CAPEVERDE": {"name": "Cabo Verde", "code": "CV"},
    "CAYMANISLANDS": {"name": "Cayman Islands", "code": "KY"},
    "CENTRALAFRICANREPUBLIC": {"name": "Central African Republic", "code": "CF"},
    "CHAD": {"name": "Chad", "code": "TD"},
    "CHILE": {"name": "Chile", "code": "CL"},
    "CHINA": {"name": "China", "code": "CN"},
    "CHRISTMASISLAND": {"name": "Christmas Island", "code": "CX"},
    "COCOSISLANDS": {"name": "Cocos (Keeling) Islands", "code": "CC"},
    "COLOMBIA": {"name": "Colombia", "code": "CO"},
    "COMOROS": {"name": "Comoros", "code": "KM"},
    "CONGO": {"name": "Republic of the Congo", "code": "CG"},
    "COOKISLANDS": {"name": "Cook Islands", "code": "CK"},
    "COSTARICA": {"name": "Costa Rica", "code": "CR"},
    "COTEDIVOIRE": {"name": "Côte d'Ivoire", "code": "CI"},
    "CROATIA": {"name": "Croatia", "code": "HR"},
    "CUBA": {"name": "Cuba", "code": "CU"},
    "CURACAO": {"name": "Curaçao", "code": "CW"},
    "CURAÇAO": {"name": "Curaçao", "code": "CW"},
    "CYPRUS": {"name": "Cyprus", "code": "CY"},
    "CZECHIA": {"name": "Czech Republic", "code": "CZ"},
    "CZECHREPUBLIC": {"name": "Czech Republic", "code": "CZ"},
    "CÔTEDIVOIRE": {"name": "Côte d'Ivoire", "code": "CI"},
    "DEMOCRATICPEOPLESREPUBLICOFKOREA": {"name": "Democratic People's Republic of Korea", "code": "KP"},
    "DEMOCRATICREPUBLICOFTHECONGO": {"name": "Democratic Republic of the Congo", "code": "CD"},
    "DENMARK": {"name": "Denmark", "code": "DK"},
    "DJIBOUTI": {"name": "Djibouti", "code": "DJ"},
    "DOMINICA": {"name": "Dominica", "code": "DM"},
    "DOMINICANREPUBLIC": {"name": "Dominican Republic", "code": "DO"},
    "EASTTIMOR": {"name": "Timor-Leste", "code": "TL"},
    "ECUADOR": {"name": "Ecuador", "code": "EC"},
    "EGYPT": {"name": "Egypt", "code": "EG"},
    "ELSALVADOR": {"name": "El Salvador", "code": "SV"},
    "ENGLAND": {"name": "England", "code": "GB"},
    "EQUATORIALGUINEA": {"name": "Equatorial Guinea", "code": "GQ"},
    "ERITREA": {"name": "Eritrea", "code": "ER"},
    "ESTONIA": {"name": "Estonia", "code": "EE"},
    "ESWATINI": {"name": "Eswatini", "code": "SZ"},
    "ETHIOPIA": {"name": "Ethiopia", "code": "ET"},
    "FALKLANDISLANDS": {"name": "Falkland Islands", "code": "FK"},
    "FAROEISLANDS": {"name": "Faroe Islands", "code": "FO"},
    "FIJI": {"name": "Fiji", "code": "FJ"},
    "FINLAND": {"name": "Finland", "code": "FI"},
    "FRANCE": {"name": "France", "code": "FR"},
    "FRENCHGUIANA": {"name": "French Guiana", "code": "GF"},
    "FRENCHPOLYNESIA": {"name": "French Polynesia", "code": "PF"},
    "FRENCHSOUTHERNTERRITORIES": {"name": "French Southern Territories", "code": "TF"},
    "GABON": {"name": "Gabon", "code": "GA"},
    "GAMBIA": {"name": "Gambia", "code": "GM"},
    "GAZASTRIP": {"name": "Gaza Strip", "code": "GS"},
    "GEORGIA": {"name": "Georgia", "code": "GE"},
    "GERMANY": {"name": "Germany", "code": "DE"},
    "GHANA": {"name": "Ghana", "code": "GH"},
    "GIBRALTAR": {"name": "Gibraltar", "code": "GI"},
    "GREATBRITAIN": {"name": "United Kingdom", "code": "GB"},
    "GREECE": {"name": "Greece", "code": "GR"},
    "GREENLAND": {"name": "Greenland", "code": "GL"},
    "GRENADA": {"name": "Grenada", "code": "GD"},
    "GUADELOUPE": {"name": "Guadeloupe", "code": "GP"},
    "GUAM": {"name": "Guam", "code": "GU"},
    "GUATEMALA": {"name": "Guatemala", "code": "GT"},
    "GUERNSEY": {"name": "Guernsey", "code": "GG"},
    "GUINEA": {"name": "Guinea", "code": "GN"},
    "GUINEABISSAU": {"name": "Guinea-Bissau", "code": "GW"},
    "GUYANA": {"name": "Guyana", "code": "GY"},
    "HAITI": {"name": "Haiti", "code": "HT"},
    "HEARDISLANDANDMCDONALDISLANDS": {"name": "Heard Island and McDonald Islands", "code": "HM"},
    "HOLYSEE": {"name": "Holy See", "code": "VA"},
    "HONDURAS": {"name": "Honduras", "code": "HN"},
    "HONGKONG": {"name": "Hong Kong", "code": "HK"},
    "HUNGARY": {"name": "Hungary", "code": "HU"},
    "ICELAND": {"name": "Iceland", "code": "IS"},
    "INDIA": {"name": "India", "code": "IN"},
    "INDONESIA": {"name": "Indonesia", "code": "ID"},
    "IRAN": {"name": "Iran", "code": "IR"},
    "IRAQ": {"name": "Iraq", "code": "IQ"},
    "IRELAND": {"name": "Ireland", "code": "IE"},
    "ISLEOFMAN": {"name": "Isle of Man", "code": "IM"},
    "ISRAEL": {"name": "Israel", "code": "IL"},
    "ITALY": {"name": "Italy", "code": "IT"},
    "JAMAICA": {"name": "Jamaica", "code": "JM"},
    "JANMAYEN": {"name": "Jan Mayen", "code": "SJ"},
    "JAPAN": {"name": "Japan", "code": "JP"},
    "JERSEY": {"name": "Jersey", "code": "JE"},
    "JORDAN": {"name": "Jordan", "code": "JO"},
    "KAZAKHSTAN": {"name": "Kazakhstan", "code": "KZ"},
    "KEELINGISLANDS": {"name": "Cocos (Keeling) Islands", "code": "CC"},
    "KENYA": {"name": "Kenya", "code": "KE"},
    "KIRIBATI": {"name": "Kiribati", "code": "KI"},
    "KOREA": {"name": "Republic of Korea", "code": "KR"},
    "KOSOVO": {"name": "Kosovo", "code": "XK"},
    "KUWAIT": {"name": "Kuwait", "code": "KW"},
    "KYRGYZSTAN": {"name": "Kyrgyzstan", "code": "KG"},
    "LAOPEOPLESDEMOCRATICREPUBLIC": {"name": "Lao People's Democratic Republic", "code": "LA"},
    "LAOS": {"name": "Lao People's Democratic Republic", "code": "LA"},
    "LATVIA": {"name": "Latvia", "code": "LV"},
    "LEBANON": {"name": "Lebanon", "code": "LB"},
    "LESOTHO": {"name": "Lesotho", "code": "LS"},
    "LIBERIA": {"name": "Liberia", "code": "LR"},
    "LIBYA": {"name": "Libya", "code": "LY"},
    "LIECHTENSTEIN": {"name": "Liechtenstein", "code": "LI"},
    "LITHUANIA": {"name": "Lithuania", "code": "LT"},
    "LUXEMBOURG": {"name": "Luxembourg", "code": "LU"},
    "MACAO": {"name": "Macao", "code": "MO"},
    "MACEDONIA": {"name": "North Macedonia", "code": "MK"},
    "MADAGASCAR": {"name": "Madagascar", "code": "MG"},
    "MALAWI": {"name": "Malawi", "code": "MW"},
    "MALAYSIA": {"name": "Malaysia", "code": "MY"},
    "MALDIVES": {"name": "Maldives", "code": "MV"},
    "MALI": {"name": "Mali", "code": "ML"},
    "MALTA": {"name": "Malta", "code": "MT"},
    "MARSHALLISLANDS": {"name": "Marshall Islands", "code": "MH"},
    "MARTINIQUE": {"name": "Martinique", "code": "MQ"},
    "MAURITANIA": {"name": "Mauritania", "code": "MR"},
    "MAURITIUS": {"name": "Mauritius", "code": "MU"},
    "MAYOTTE": {"name": "Mayotte", "code": "YT"},
    "MEXICO": {"name": "Mexico", "code": "MX"},
    "MICRONESIA": {"name": "Micronesia", "code": "FM"},
    "MIDWAYISLANDS": {"name": "Midway Islands", "code": "MI"},
    "MINOROUTLYINGISLANDS": {"name": "United States Minor Outlying Islands", "code": "UM"},
    "MOLDOVA": {"name": "Moldova", "code": "MD"},
    "MONACO": {"name": "Monaco", "code": "MC"},
    "MONGOLIA": {"name": "Mongolia", "code": "MN"},
    "MONTENEGRO": {"name": "Montenegro", "code": "ME"},
    "MONTSERRAT": {"name": "Montserrat", "code": "MS"},
    "MOROCCO": {"name": "Morocco", "code": "MA"},
    "MOZAMBIQUE": {"name": "Mozambique", "code": "MZ"},
    "MYANMAR": {"name": "Myanmar", "code": "MM"},
    "NAMIBIA": {"name": "Namibia", "code": "NA"},
    "NAURU": {"name": "Nauru", "code": "NR"},
    "NEPAL": {"name": "Nepal", "code": "NP"},
    "NETHERLANDS": {"name": "Netherlands", "code": "NL"},
    "NETHERLANDSANTILLES": {"name": "Netherlands Antilles", "code": "AN"},
    "NEWCALEDONIA": {"name": "New Caledonia", "code": "NC"},
    "NEWZEALAND": {"name": "New Zealand", "code": "NZ"},
    "NICARAGUA": {"name": "Nicaragua", "code": "NI"},
    "NIGER": {"name": "Niger", "code": "NE"},
    "NIGERIA": {"name": "Nigeria", "code": "NG"},
    "NIUE": {"name": "Niue", "code": "NU"},
    "NORFOLKISLAND": {"name": "Norfolk Island", "code": "NF"},
    "NORTHERNCYPRUS": {"name": "Northern Cyprus", "code": "NY"},
    "NORTHERNIRELAND": {"name": "Northern Ireland", "code": "GB"},
    "NORTHERNMARIANAISLANDS": {"name": "Northern Mariana Islands", "code": "MP"},
    "NORTHKOREA": {"name": "Democratic People's Republic of Korea", "code": "KP"},
    "NORTHMACEDONIA": {"name": "North Macedonia", "code": "MK"},
    "NORWAY": {"name": "Norway", "code": "NO"},
    "OMAN": {"name": "Oman", "code": "OM"},
    "PAKISTAN": {"name": "Pakistan", "code": "PK"},
    "PALAU": {"name": "Palau", "code": "PW"},
    "PALESTINE": {"name": "Palestine", "code": "PS"},
    "PANAMA": {"name": "Panama", "code": "PA"},
    "PAPUANEWGUINEA": {"name": "Papua New Guinea", "code": "PG"},
    "PARAGUAY": {"name": "Paraguay", "code": "PY"},
    "PERU": {"name": "Peru", "code": "PE"},
    "PHILIPPINES": {"name": "Philippines", "code": "PH"},
    "PITCAIRN": {"name": "Pitcairn", "code": "PN"},
    "POLAND": {"name": "Poland", "code": "PL"},
    "PORTUGAL": {"name": "Portugal", "code": "PT"},
    "PUERTORICO": {"name": "Puerto Rico", "code": "PR"},
    "QATAR": {"name": "Qatar", "code": "QA"},
    "REPUBLICOFKOREA": {"name": "Republic of Korea", "code": "KR"},
    "REPUBLICOFTHECONGO": {"name": "Republic of the Congo", "code": "CG"},
    "REUNION": {"name": "Réunion", "code": "RE"},
    "ROMANIA": {"name": "Romania", "code": "RO"},
    "RUSSIA": {"name": "Russian Federation", "code": "RU"},
    "RUSSIANFEDERATION": {"name": "Russian Federation", "code": "RU"},
    "RWANDA": {"name": "Rwanda", "code": "RW"},
    "RÉUNION": {"name": "Réunion", "code": "RE"},
    "SABA": {"name": "Saba", "code": "BQ"},
    "SAINTBARTHELEMY": {"name": "Saint Barthélemy", "code": "BL"},
    "SAINTBARTHÉLEMY": {"name": "Saint Barthélemy", "code": "BL"},
    "SAINTHELENA": {"name": "Saint Helena", "code": "SH"},
    "SAINTKITTSANDNEVIS": {"name": "Saint Kitts and Nevis", "code": "KN"},
    "SAINTLUCIA": {"name": "Saint Lucia", "code": "LC"},
    "SAINTMARTIN": {"name": "Saint Martin", "code": "MF"},
    "SAINTPIERREANDMIQUELON": {"name": "Saint Pierre and Miquelon", "code": "PM"},
    "SAINTVINCENTANDTHEGRENADINES": {"name": "Saint Vincent and the Grenadines", "code": "VC"},
    "SALVADOR": {"name": "El Salvador", "code": "SV"},
    "SAMOA": {"name": "Samoa", "code": "WS"},
    "SANMARINO": {"name": "San Marino", "code": "SM"},
    "SAOTOMEANDPRINCIPE": {"name": "Sao Tome and Principe", "code": "ST"},
    "SAUDIARABIA": {"name": "Saudi Arabia", "code": "SA"},
    "SENEGAL": {"name": "Senegal", "code": "SN"},
    "SERBIA": {"name": "Serbia", "code": "RS"},
    "SEYCHELLES": {"name": "Seychelles", "code": "SC"},
    "SIERRALEONE": {"name": "Sierra Leone", "code": "SL"},
    "SINGAPORE": {"name": "Singapore", "code": "SG"},
    "SINTEUSTATIUS": {"name": "Sint Eustatius", "code": "BQ"},
    "SINTMAARTEN": {"name": "Sint Maarten", "code": "SX"},
    "SLOVAKIA": {"name": "Slovakia", "code": "SK"},
    "SLOVENIA": {"name": "Slovenia", "code": "SI"},
    "SOLOMONISLANDS": {"name": "Solomon Islands", "code": "SB"},
    "SOMALIA": {"name": "Somalia", "code": "SO"},
    "SOUTHAFRICA": {"name": "South Africa", "code": "ZA"},
    "SOUTHGEORGIAANDTHESOUTHSANDWICHISLANDS": {"name": "South Georgia and the South Sandwich Islands", "code": "GS"},
    "SOUTHKOREA": {"name": "Republic of Korea", "code": "KR"},
    "SOUTHSUDAN": {"name": "South Sudan", "code": "SS"},
    "SPAIN": {"name": "Spain", "code": "ES"},
    "SRILANKA": {"name": "Sri Lanka", "code": "LK"},
    "SUDAN": {"name": "Sudan", "code": "SD"},
    "SURINAME": {"name": "Suriname", "code": "SR"},
    "SVALBARD": {"name": "Svalbard", "code": "SJ"},
    "SWEDEN": {"name": "Sweden", "code": "SE"},
    "SWITZERLAND": {"name": "Switzerland", "code": "CH"},
    "SYRIA": {"name": "Syrian Arab Republic", "code": "SY"},
    "SYRIANARABREPUBLIC": {"name": "Syrian Arab Republic", "code": "SY"},
    "TAIWAN": {"name": "Taiwan", "code": "TW"},
    "TAJIKISTAN": {"name": "Tajikistan", "code": "TJ"},
    "TANZANIA": {"name": "Tanzania", "code": "TZ"},
    "THAILAND": {"name": "Thailand", "code": "TH"},
    "TIMORLESTE": {"name": "Timor-Leste", "code": "TL"},
    "TOGO": {"name": "Togo", "code": "TG"},
    "TOKELAU": {"name": "Tokelau", "code": "TK"},
    "TONGA": {"name": "Tonga", "code": "TO"},
    "TRINIDADANDTOBAGO": {"name": "Trinidad and Tobago", "code": "TT"},
    "TRISTANDACUNHA": {"name": "Tristan da Cunha", "code": "TA"},
    "TUNISIA": {"name": "Tunisia", "code": "TN"},
    "TURKEY": {"name": "Turkey", "code": "TR"},
    "TURKMENISTAN": {"name": "Turkmenistan", "code": "TM"},
    "TURKSANDCAICOSISLANDS": {"name": "Turks and Caicos Islands", "code": "TC"},
    "TUVALU": {"name": "Tuvalu", "code": "TV"},
    "UGANDA": {"name": "Uganda", "code": "UG"},
    "UKRAINE": {"name": "Ukraine", "code": "UA"},
    "UNITEDARABEMIRATES": {"name": "United Arab Emirates", "code": "AE"},
    "UNITEDKINGDOM": {"name": "United Kingdom", "code": "GB"},
    "UNITEDSTATE": {"name": "United States of America", "code": "US"},
    "UNITEDSTATESMINOROUTLYINGISLANDS": {"name": "United States Minor Outlying Islands", "code": "UM"},
    "UNITEDSTATESOFAMERICA": {"name": "United States of America", "code": "US"},
    "UNITEDSTATESVIRGINISLANDS": {"name": "United States Virgin Islands", "code": "VI"},
    "URUGUAY": {"name": "Uruguay", "code": "UY"},
    "USA": {"name": "United States of America", "code": "US"},
    "USVIRGINISLANDS": {"name": "US Virgin Islands", "code": "VI"},
    "UZBEKISTAN": {"name": "Uzbekistan", "code": "UZ"},
    "VANUATU": {"name": "Vanuatu", "code": "VU"},
    "VENEZUELA": {"name": "Venezuela", "code": "VE"},
    "VIETNAM": {"name": "Vietnam", "code": "VN"},
    "WALES": {"name": "Wales", "code": "GB"},
    "WALLISANDFUTUNA": {"name": "Wallis and Futuna", "code": "WF"},
    "WESTBANK": {"name": "West Bank", "code": "WB"},
    "WESTERNSAHARA": {"name": "Western Sahara", "code": "EH"},
    "YEMEN": {"name": "Yemen", "code": "YE"},
    "ZAMBIA": {"name": "Zambia", "code": "ZM"},
    "ZIMBABWE": {"name": "Zimbabwe", "code": "ZW"},
}
