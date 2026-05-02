from collections.abc import Callable
import asyncio
from typing import Optional, Dict, Any, Literal
import pandas as pd
import json
from urllib.parse import urlencode
from ..exceptions import ComponentError, DataNotFound, NotSupported
from ..interfaces.http import HTTPService
from .flow import FlowComponent
from ..conf import LEADIQ_API_KEY


class LeadIQ(FlowComponent, HTTPService):
    """
    LeadIQ API Component

    Overview:

    This component interacts with the LeadIQ GraphQL API to retrieve company and employee information.
    Supports different types of searches through the 'type' parameter.

       :widths: auto

    | type                  | Yes      | Type of search to perform: 'company', 'employees' or 'flat'                                         |
    | column                | No       | Name of the column containing company names (default: 'company_name')                               |
    | companies             | No       | List of company names to search (alternative to using DataFrame input)                               |

    Returns:
        DataFrame containing the requested information based on the search type

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          LeadIQ:
          # attributes here
        ```
    """
    _version = "1.0.0"

    accept = "application/json"
    base_url = "https://api.leadiq.com"
    download = None

    # GraphQL Queries
    COMPANY_SEARCH_QUERY = """
    query SearchCompany($input: SearchCompanyInput!) {
        searchCompany(input: $input) {
            totalResults
            hasMore
            results {
                source
                name
                alternativeNames
                domain
                description
                emailDomains
                type
                phones
                country
                address
                locationInfo {
                    formattedAddress
                    street1
                    street2
                    city
                    areaLevel1
                    country
                    postalCode
                }
                logoUrl
                linkedinId
                linkedinUrl
                numberOfEmployees
                industry
                specialities
                fundingInfo {
                    fundingRounds
                    fundingTotalUsd
                    lastFundingOn
                    lastFundingType
                    lastFundingUsd
                }
                technologies {
                    name
                    category
                    parentCategory
                }
                revenue
                revenueRange {
                    start
                    end
                    description
                }
                sicCode {
                    code
                    description
                }
                naicsCode {
                    code
                    description
                }
                employeeRange
                foundedYear
            }
        }
    }
    """

    EMPLOYEE_SEARCH_QUERY = """
    query GroupedAdvancedSearch($input: GroupedSearchInput!) {
        groupedAdvancedSearch(input: $input) {
            totalCompanies
            companies {
                company {
                    id
                    name
                    industry
                    companyDescription: description
                    linkedinId
                    domain
                    employeeCount
                    city
                    country
                    state
                    postalCode
                    score
                    companyTechnologies
                    companyTechnologyCategories
                    revenueRange {
                        ...RevenueRangeFragment
                    }
                    fundingInfo {
                        ...FundingInfoFragment
                    }
                    naicsCode {
                        ...NAICSCodeFragment
                    }
                }
                people {
                    id
                    companyId
                    name
                    linkedinId
                    linkedinUrl
                    title
                    role
                    state
                    country
                    seniority
                    workEmails
                    verifiedWorkEmails
                    verifiedLikelyWorkEmails
                    workPhones
                    personalEmails
                    personalPhones
                    score
                    firstName
                    middleName
                    lastName
                    updatedAt
                    currentPositionStartDate
                    company {
                        id
                        name
                        industry
                        companyDescription: description
                        linkedinId
                        domain
                        employeeCount
                        city
                        country
                        state
                        postalCode
                        score
                        companyTechnologies
                        companyTechnologyCategories
                        revenueRange {
                            ...RevenueRangeFragment
                        }
                        fundingInfo {
                            ...FundingInfoFragment
                        }
                        naicsCode {
                            ...NAICSCodeFragment
                        }
                    }
                    picture
                }
                totalContactsInCompany
            }
        }
    }

    fragment RevenueRangeFragment on RevenueRange {
        start
        end
        description
    }

    fragment FundingInfoFragment on FundingInfo {
        fundingRounds
        fundingTotalUsd
        lastFundingOn
        lastFundingType
        lastFundingUsd
    }

    fragment NAICSCodeFragment on NAICSCode {
        code
        naicsDescription: description
    }
    """

    FLAT_SEARCH_QUERY = """
    query FlatAdvancedSearch($input: FlatSearchInput!) {
        flatAdvancedSearch(input: $input) {
            totalPeople
            people {
                id
                companyId
                name
                linkedinId
                linkedinUrl
                title
                role
                state
                country
                seniority
                workEmails
                verifiedWorkEmails
                verifiedLikelyWorkEmails
                workPhones
                personalEmails
                personalPhones
                score
                firstName
                middleName
                lastName
                updatedAt
                currentPositionStartDate
                company {
                    id
                    name
                    industry
                    companyDescription: description
                    linkedinId
                    domain
                    employeeCount
                    city
                    country
                    state
                    postalCode
                    score
                    companyTechnologies
                    companyTechnologyCategories
                    revenueRange {
                        ...RevenueRangeFragment
                    }
                    fundingInfo {
                        ...FundingInfoFragment
                    }
                    naicsCode {
                        ...NAICSCodeFragment
                    }
                }
                picture
            }
        }
    }

    fragment RevenueRangeFragment on RevenueRange {
        start
        end
        description
    }

    fragment FundingInfoFragment on FundingInfo {
        fundingRounds
        fundingTotalUsd
        lastFundingOn
        lastFundingType
        lastFundingUsd
    }

    fragment NAICSCodeFragment on NAICSCode {
        code
        naicsDescription: description
    }
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs
    ):
        self.column = kwargs.get('column', 'company_name')
        self.companies = kwargs.get('companies', [])
        self.search_type = kwargs.get('type', 'company')
        self._counter = 0
        self._debug = kwargs.get('debug', False)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def get_leadiq_url(self, resource: str, args: dict = None) -> str:
        """Construct LeadIQ API URL with optional query parameters."""
        url = f"{self.base_url}/{resource}"
        if args:
            query = urlencode(args)
            url = f"{url}?{query}"
        return url

    async def start(self, **kwargs):
        """Initialize the component and validate inputs."""
        if not LEADIQ_API_KEY:
            raise ComponentError("LEADIQ_API_KEY not configured")

        if self.search_type not in ['company', 'employees', 'flat']:
            raise NotSupported(f"Search type '{self.search_type}' not supported")

        # Set up headers with API key
        self.headers = {
            'Authorization': f'Basic {LEADIQ_API_KEY}',
            'Content-Type': 'application/json',
            'apollo-require-preflight': 'true'
        }

        # Get company names from either input DataFrame or companies parameter
        if self.previous:
            self.data = self.input  # Aquí está el cambio clave

        if hasattr(self, 'data'):
            if self.column not in self.data.columns:
                raise ComponentError(f"Input DataFrame must contain a '{self.column}' column")
            self.companies = self.data[self.column].unique().tolist()
        elif not self.companies:
            raise ComponentError("No company names provided")

        return True

    async def search_company(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Basic company search."""
        try:
            variables = {
                "input": {
                    "name": company_name
                }
            }

            payload = {
                "query": self.COMPANY_SEARCH_QUERY,
                "variables": variables
            }

            result = await self._execute_query(payload, company_name)

            # Añadir logs detallados
            if result and "data" in result:
                if "searchCompany" in result["data"]:
                    search_data = result["data"]["searchCompany"]

                    if search_data.get('results'):
                        self._logger.info(f"First result name: {search_data['results'][0].get('name')}")

            # Procesar el resultado usando _process_company_response
            processed = self._process_response(result, company_name)
            return processed

        except Exception as e:
            self._logger.error(f"Error in company search for {company_name}: {str(e)}")
            return None

    async def search_employees(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Search for employees at a company."""
        try:
            variables = {
                "input": {
                    "companyFilter": {
                        "names": company_name
                    },
                    "limit": 100
                }
            }

            payload = {
                "query": self.EMPLOYEE_SEARCH_QUERY,
                "variables": variables
            }

            result = await self._execute_query(payload, company_name)

            return self._process_response(result, company_name)

        except Exception as e:
            self._logger.error(f"Error in employee search for {company_name}: {str(e)}")
            return None

    async def search_flat(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Flat search for employees at a company."""
        try:
            variables = {
                "input": {
                    "companyFilter": {
                        "names": company_name
                    },
                    "limit": 100
                }
            }

            payload = {
                "query": self.FLAT_SEARCH_QUERY,
                "variables": variables
            }

            result = await self._execute_query(payload, company_name)

            return self._process_response(result, company_name)

        except Exception as e:
            self._logger.error(f"Error in flat search for {company_name}: {str(e)}")
            return None

    async def _execute_query(self, payload: dict, company_name: str) -> Optional[Dict[str, Any]]:
        """Execute GraphQL query and process response."""
        self._logger.info(f"Searching for {self.search_type} in company: {company_name}")

        url = self.get_leadiq_url("graphql")
        args = {
            "method": "post",
            "url": url,
            "data": json.dumps(payload),
            "headers": self.headers
        }

        result, error = await self.session(**args)

        if error:
            self._logger.error(f"Error searching for {company_name}: {error}")
            return None

        # Solo retornar el resultado, no procesarlo aquí
        return result  # Quitar el _process_response

    def _process_response(self, result: dict, company_name: str) -> Optional[Dict[str, Any]]:
        """Process API response based on search type."""
        if self.search_type == 'company':
            return self._process_company_response(result, company_name)
        elif self.search_type == 'flat':
            return self._process_flat_response(result, company_name)
        else:
            return self._process_employee_response(result, company_name)

    def _process_company_response(self, result: dict, company_name: str) -> Optional[Dict[str, Any]]:
        """Process company search response."""
        if "data" in result and "searchCompany" in result["data"]:
            search_data = result["data"]["searchCompany"]

            if search_data["results"]:
                company_data = search_data["results"][0]  # Tomamos el primer resultado

                # Crear un diccionario con los datos procesados
                processed_data = {
                    "search_term": company_name,  # Término de búsqueda original
                    "found": True,
                    "total_results": search_data["totalResults"],
                    "name": company_data["name"],
                    "domain": company_data["domain"],
                    "industry": company_data["industry"],
                    "country": company_data["country"],
                    "address": company_data["address"],
                    "linkedin_id": company_data["linkedinId"],
                    "linkedin_url": company_data["linkedinUrl"],
                    "employee_count": company_data["numberOfEmployees"],
                    "employee_range": company_data["employeeRange"],
                    "founded_year": company_data["foundedYear"],
                }

                # Procesar locationInfo
                if loc := company_data.get("locationInfo"):
                    processed_data.update({
                        "street": loc.get("street1"),
                        "city": loc.get("city"),
                        "state": loc.get("areaLevel1"),
                        "postal_code": loc.get("postalCode")
                    })

                # Procesar NAICS
                if naics := company_data.get("naicsCode"):
                    processed_data.update({
                        "naics_code": naics["code"],
                        "naics_description": naics["description"]
                    })

                # Procesar technologies como listas
                if techs := company_data.get("technologies"):
                    tech_names = []
                    tech_categories = []
                    for tech in techs:
                        if tech.get("name"):
                            tech_names.append(tech["name"])
                        if tech.get("category"):
                            tech_categories.append(tech["category"])

                    processed_data.update({
                        "technologies": tech_names,
                        "tech_categories": list(set(tech_categories))  # Eliminar duplicados
                    })

                # Procesar specialities si existe
                if specs := company_data.get("specialities"):
                    processed_data["specialities"] = specs

                self._counter += 1
                return processed_data
            else:
                # Si no se encontraron resultados
                return {
                    "search_term": company_name,
                    "found": False,
                    "total_results": 0
                }

        self._logger.warning(f"Unexpected response structure for {company_name}")
        return None

    def _process_employee_response(self, result: dict, company_name: str) -> Optional[Dict[str, Any]]:
        """Process employee search response."""
        if "data" in result and "groupedAdvancedSearch" in result["data"]:
            search_data = result["data"]["groupedAdvancedSearch"]

            if search_data["companies"]:
                company_data = search_data["companies"][0]
                company_info = company_data["company"]
                employees = company_data["people"]

                # Extraer solo la información básica de la empresa
                basic_company_info = {
                    "company_id": company_info["id"],
                    "company_name": company_info["name"],
                    "company_industry": company_info["industry"],
                    "company_domain": company_info["domain"],
                    "company_employee_count": company_info["employeeCount"],
                    "company_city": company_info["city"],
                    "company_country": company_info["country"],
                    "company_state": company_info["state"]
                }

                # Crear una fila por cada empleado
                processed_rows = []
                for employee in employees:
                    # Remover la información duplicada de la empresa del empleado
                    employee_copy = employee.copy()
                    employee_copy.pop('company', None)  # Eliminar la información duplicada de la empresa

                    # Combinar información básica de la empresa con datos del empleado
                    row = {
                        **basic_company_info,
                        **employee_copy
                    }
                    processed_rows.append(row)

                self._counter += len(processed_rows)
                return processed_rows

            self._logger.warning(f"No company data found for {company_name}")
        else:
            self._logger.warning(f"Unexpected response structure for {company_name}")

        return None

    def _process_flat_response(self, result: dict, company_name: str) -> Optional[Dict[str, Any]]:
        """Process flat search response."""
        if "data" in result and "flatAdvancedSearch" in result["data"]:
            search_data = result["data"]["flatAdvancedSearch"]

            if search_data["people"]:
                processed_rows = []
                for person in search_data["people"]:
                    # Extraer información básica de la empresa
                    company_info = person.pop('company', {})
                    basic_company_info = {
                        "company_id": company_info.get("id"),
                        "company_name": company_info.get("name"),
                        "company_industry": company_info.get("industry"),
                        "company_domain": company_info.get("domain"),
                        "company_employee_count": company_info.get("employeeCount"),
                        "company_city": company_info.get("city"),
                        "company_country": company_info.get("country"),
                        "company_state": company_info.get("state")
                    }

                    # Combinar información de la empresa con datos del empleado
                    row = {
                        **basic_company_info,
                        **person
                    }
                    processed_rows.append(row)

                self._counter += len(processed_rows)
                return processed_rows

            self._logger.warning(f"No people found for {company_name}")
        else:
            self._logger.warning(f"Unexpected response structure for {company_name}")

        return None

    async def run(self):
        """Execute searches based on the specified type."""
        # search_method = getattr(self, f"search_{self.search_type}", None)
        search_method = {
            'company': self.search_company,
            'employees': self.search_employees,
            'flat': self.search_flat
        }[self.search_type]

        tasks = [search_method(company) for company in self.companies]
        results = await asyncio.gather(*tasks)

        # Filter out None results and flatten the list for employee/flat searches
        if self.search_type in ['employees', 'flat']:
            valid_results = [
                row
                for result in results
                if result is not None
                for row in result
            ]
        else:
            valid_results = [r for r in results if r is not None]

        if not valid_results:
            raise DataNotFound(f"No {self.search_type} data found")

        # Convert to DataFrame
        df = pd.DataFrame(valid_results)

        # Add metrics
        self.add_metric(f"{self.search_type.upper()}_FOUND", self._counter)

        if self._debug:
            print(df)
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])

        self._result = df
        return self._result

    async def close(self):
        """Clean up resources."""
        return True
