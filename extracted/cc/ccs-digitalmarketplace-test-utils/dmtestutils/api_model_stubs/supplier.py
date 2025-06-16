import copy

from .base import BaseAPIModelStub

CENTRAL_DIGITAL_PLATFORM_DATA = {
    "id": "086a91ee-f448-4d7c-8b87-e2178521bc36",
    "name": "My Little Company",
    "associatedPersons": [],
    "additionalParties": [],
    "additionalEntities": [],
    "identifier": {
        "scheme": "GB-COH",
        "id": "12345678",
        "legalName": "My Little Registered Company",
        "uri": None,
    },
    "additionalIdentifiers": [
        {
            "scheme": "Other",
            "id": None,
            "legalName": "My Little Registered Company",
            "uri": None,
        },
        {
            "scheme": "GB-PPON",
            "id": "ELMA-1052-ICAM",
            "legalName": "My Little Registered Company",
            "uri": "https://supplier-information.com/organisations/ELMA-1052-ICAM",
        },
        {
            "scheme": "VAT",
            "id": "111222333",
            "legalName": "My Little Registered Company",
            "uri": None,
        },
    ],
    "address": {
        "streetAddress": "123 Fake Road",
        "locality": "Madeupolis",
        "region": None,
        "postalCode": "A11 1AA",
        "countryName": "United Kingdom",
        "country": "GB",
        "type": "Registered",
    },
    "contactPoint": {
        "name": None,
        "email": "mre@company.com",
        "telephone": None,
        "url": "https://www.mre.company",
    },
    "roles": ["tenderer"],
    "details": {
        "legalForm": {
            "registeredUnderAct2006": True,
            "registeredLegalForm": "LimitedCompany",
            "lawRegistered": "Companies Act 2006",
            "registrationDate": "2025-01-01",
        },
        "scale": "micro",
        "vcse": False,
        "shelteredWorkshop": False,
        "publicServiceMissionOrganization": False,
    },
    "supplierInformationData": {
        "form": {
            "name": "Standard Questions",
            "submissionState": "Submitted",
            "submittedAt": "2025-01-23T13:26:39.338624+00:00",
            "organisationId": "086a91ee-f448-4d7c-8b87-e2178521bc36",
            "formId": "9dfdde74-140e-4ce3-bea1-779be90d8e2a",
            "formVersionId": "1.0",
            "isRequired": True,
            "shareCode": "9LINliKU",
        },
        "answerSets": [
            {
                "id": "ae7fee3d-8a86-49b0-9f35-f082b94d38ea",
                "sectionName": "Qualifications",
                "answers": [],
            },
            {
                "id": "ca2621ef-e47d-4e12-9678-cfaef383d4fc",
                "sectionName": "Trade assurances",
                "answers": [],
            },
            {
                "id": "c0da4071-3d13-44cf-8e7e-6ccea5dda921",
                "sectionName": "Exclusions",
                "answers": [],
            },
            {
                "id": "afd061a6-ba46-45af-ae5e-7dce88994127",
                "sectionName": "Financial information",
                "answers": [
                    {
                        "questionName": "_FinancialInformation03",
                        "boolValue": True,
                        "numericValue": None,
                        "startValue": None,
                        "endValue": None,
                        "dateValue": None,
                        "textValue": None,
                        "optionValue": [],
                        "jsonValue": {},
                        "documentUri": None,
                    },
                    {
                        "questionName": "_FinancialInformation02",
                        "boolValue": None,
                        "numericValue": None,
                        "startValue": None,
                        "endValue": None,
                        "dateValue": None,
                        "textValue": None,
                        "optionValue": [],
                        "jsonValue": {},
                        "documentUri": "https://supplier-information.co/test_pdf_20250123132506219.pdf",
                    },
                    {
                        "questionName": "_FinancialInformation01",
                        "boolValue": None,
                        "numericValue": None,
                        "startValue": None,
                        "endValue": None,
                        "dateValue": "2024-03-31",
                        "textValue": None,
                        "optionValue": [],
                        "jsonValue": {},
                        "documentUri": None,
                    },
                ],
            },
        ],
        "questions": [
            {
                "type": "Text",
                "name": "_Qualifications01",
                "title": "Enter the qualification name",
                "text": '<div class="govuk-hint">Enter one qualification at a time. You can add another at the end if '
                "you need to. For example, ISO 45001 Health and Safety Management.</div>",
                "isRequired": True,
                "sectionName": "Qualifications",
                "options": [],
                "sortOrder": 1,
            },
            {
                "type": "Text",
                "name": "_Qualifications02",
                "title": "Who awarded the qualification?",
                "text": '<div class="govuk-hint">Enter the name of the person or body. For example, ISO, '
                "Constructionline or Red Tractor Assurance.</div>",
                "isRequired": True,
                "sectionName": "Qualifications",
                "options": [],
                "sortOrder": 2,
            },
            {
                "type": "Date",
                "name": "_Qualifications03",
                "title": "What date was the qualification awarded?",
                "text": "",
                "isRequired": True,
                "sectionName": "Qualifications",
                "options": [],
                "sortOrder": 3,
            },
            {
                "type": "Text",
                "name": "_TradeAssurance01",
                "title": "Who awarded the trade assurance?",
                "text": '<div class="govuk-hint">Enter the name of the person or body. You can add another at the end '
                "if you need to. For example, Red Tractor Assurance, QMS Assurance.</div>",
                "isRequired": True,
                "sectionName": "Trade assurances",
                "options": [],
                "sortOrder": 1,
            },
            {
                "type": "Text",
                "name": "_TradeAssurance02",
                "title": "Do you know the reference number?",
                "text": "",
                "isRequired": False,
                "sectionName": "Trade assurances",
                "options": [],
                "sortOrder": 2,
            },
            {
                "type": "Date",
                "name": "_TradeAssurance03",
                "title": "What date was the trade assurance awarded?",
                "text": "",
                "isRequired": True,
                "sectionName": "Trade assurances",
                "options": [],
                "sortOrder": 3,
            },
            {
                "type": "Boolean",
                "name": "_Exclusion07",
                "title": "Did this exclusion happen in the UK?",
                "text": "",
                "isRequired": True,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 1,
            },
            {
                "type": "Option",
                "name": "_Exclusion08",
                "title": "Select which exclusion applies",
                "text": '<div class="govuk-hint"><p>Only select one exclusion. You can add another at the end if you '
                "need to.</p><p>If this exclusion happened outside the UK, select the equivalent offence in "
                "the UK for where it took place.</p></div>",
                "isRequired": True,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 2,
            },
            {
                "type": "OptionJson",
                "name": "_Exclusion09",
                "title": "Select who the exclusion applies to",
                "text": '<div class="govuk-inset-text govuk-!-margin-top-0">If it applies to someone not listed, you '
                "must go back to the ‘Add a connected person’ section and add them.</div>",
                "isRequired": True,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 3,
            },
            {
                "type": "Text",
                "name": "_Exclusion06",
                "title": "Enter an email address",
                "text": '<div class="govuk-hint">Where the contracting authority can contact someone about the '
                "exclusion</div>",
                "isRequired": True,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 4,
            },
            {
                "type": "Text",
                "name": "_Exclusion05",
                "title": "Describe the exclusion in more detail",
                "text": '<div class="govuk-hint">Give us your explanation of the event. For example, any background '
                "information you can give about what happened or what caused the exclusion.</div>",
                "isRequired": True,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 5,
            },
            {
                "type": "Text",
                "name": "_Exclusion04",
                "title": "How the exclusion is being managed",
                "text": '<div class="govuk-hint"><p class="govuk-body">You must tell us what you or the person who was '
                'subject to the event:</p><ul class="govuk-list govuk-list--bullet"><li>have done to prove it '
                "was taken seriously - for example, paid a fine or compensation</li><li>have done to stop the "
                "circumstances that caused it from happening again - for example, taking steps like changing "
                "staff or management or putting procedures or training in place</li><li>are doing to monitor "
                "the steps that were taken - for example, regular meetings</li></ul></div>",
                "isRequired": True,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 6,
            },
            {
                "type": "FileUpload",
                "name": "_Exclusion03",
                "title": "Do you have a supporting document to upload?",
                "text": '<div id="documents-hint" class="govuk-hint">A decision from a public authority that was the '
                "basis for the offence. For example, documentation from the police, HMRC or the court.</div>",
                "isRequired": False,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 7,
            },
            {
                "type": "Url",
                "name": "_Exclusion10",
                "title": "Was the decision recorded on a public authority website?",
                "text": '<div class="govuk-hint">For example, the outcome of a court decision for a conviction or '
                "other event</div>",
                "isRequired": False,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 8,
            },
            {
                "type": "Date",
                "name": "_Exclusion02",
                "title": "Have the circumstances that led to the exclusion ended?",
                "text": '<div id="isEventEnded-hint" class="govuk-hint">For example, a court decision for '
                "environmental misconduct led your organisation or the connected person to stop harming the "
                "environment.</div>",
                "isRequired": False,
                "sectionName": "Exclusions",
                "options": [],
                "sortOrder": 9,
            },
            {
                "type": "Boolean",
                "name": "_FinancialInformation03",
                "title": "Were your accounts audited?",
                "text": "",
                "isRequired": True,
                "sectionName": "Financial information",
                "options": [],
                "sortOrder": 2,
            },
            {
                "type": "FileUpload",
                "name": "_FinancialInformation02",
                "title": "Upload your accounts",
                "text": '<p class="govuk-body">Upload your most recent 2 financial years. If you do not have 2, '
                "upload your most recent financial year.</p>",
                "isRequired": True,
                "sectionName": "Financial information",
                "options": [],
                "sortOrder": 3,
            },
            {
                "type": "Date",
                "name": "_FinancialInformation01",
                "title": "What is the financial year end date for the information you uploaded?",
                "text": "",
                "isRequired": True,
                "sectionName": "Financial information",
                "options": [],
                "sortOrder": 4,
            },
        ],
    },
}


class SupplierStub(BaseAPIModelStub):
    resource_name = "suppliers"
    contact_information = {
        "address1": "123 Fake Road",
        "city": "Madeupolis",
        "contactName": "Mr E Man",
        "email": "mre@company.com",
        "id": 4321,
        "links": {"self": "http://localhost:8000/suppliers/1234/contact-information/4321"},
        "phoneNumber": "01234123123",
        "postcode": "A11 1AA",
    }
    default_data = {
        "companiesHouseNumber": "12345678",
        "companyDetailsConfirmed": True,
        "contactInformation": [contact_information],
        "description": "I'm a supplier.",
        "dunsNumber": "123456789",
        "id": 1234,
        "links": {"self": "http://localhost:8000/suppliers/1234"},
        "name": "My Little Company",
        "organisationSize": "micro",
        "registeredName": "My Little Registered Company",
        "registrationCountry": "country:GB",
        "tradingStatus": "limited company",
        "vatNumber": "111222333",
        "vatCode": "uk_vat_registered",
        "onDebarmentList": False,
        "debarmentDetails": None,
    }
    optional_keys = [
        ("otherCompanyRegistrationNumber", "other_company_registration_number"),
        ("otherTradingStatus", "other_trading_status"),
        ("companyDetailsConfirmed", "company_details_confirmed"),
        ("centralDigitalPlatformOrganisationId", "central_digital_platform_organisation_id"),
        ("centralDigitalPlatformShareCode", "central_digital_platform_share_code"),
        ("centralDigitalPlatformData", "central_digital_platform_data"),
    ]

    def single_result_response(self):
        # Include service_counts in API response only - this key isn't present in Supplier.serialize()
        self.response_data["service_counts"] = {
            "G-Cloud 9": 109,
            "G-Cloud 8": 108,
            "G-Cloud 7": 107,
            "G-Cloud 6": 106,
            "G-Cloud 5": 105,
            "G-Cloud 13": 113,
            "G-Cloud 14": 99,
        }
        return {self.resource_name: self.response_data}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get("id"):
            self.response_data["links"]["self"] = "http://localhost:8000/suppliers/{id}".format(id=kwargs.get("id"))

        if kwargs.get("vat_code"):
            self.response_data["vatCode"] = kwargs.get("vat_code")

        if kwargs.get("contact_id"):
            self.contact_information["id"] = kwargs.get("contact_id")
            self.contact_information["links"]["self"] = (
                "http://localhost:8000/suppliers/{id}/contact-information/{contact_id}".format(
                    id=self.response_data["id"], contact_id=kwargs.get("contact_id")
                )
            )
            self.response_data["contactInformation"] = [self.contact_information]
            # Don't include the kwarg in response
            del self.response_data["contact_id"]

        if kwargs.get("with_cdp_data"):
            cdp_data = copy.deepcopy(CENTRAL_DIGITAL_PLATFORM_DATA)

            self.response_data["centralDigitalPlatformOrganisationId"] = cdp_data["id"]
            self.response_data["centralDigitalPlatformShareCode"] = cdp_data["supplierInformationData"]["form"][
                "shareCode"
            ]
            self.response_data["centralDigitalPlatformData"] = {
                cdp_key: cdp_data[cdp_key]
                for cdp_key in ["identifier", "additionalIdentifiers", "details", "supplierInformationData"]
            }
            self.response_data["registrationCountryName"] = cdp_data["address"]["countryName"]
            self.response_data["contactInformation"][0]["url"] = cdp_data["contactPoint"]["url"]

            del self.response_data["with_cdp_data"]

        if self.response_data.get("otherCompanyRegistrationNumber"):
            # We allow one or other of these registration numbers, but not both
            del self.response_data["companiesHouseNumber"]
            # Companies without a Companies House number aren't necessarily overseas, but they might well be
            self.response_data["registrationCountry"] = "country:NZ"
