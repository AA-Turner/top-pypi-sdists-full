import json
import os
import requests
import pandas as pd
from datetime import datetime
import warnings
import urllib3
#from ..conf import LEADIQ_API_KEY
# Suprimir advertencias de SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def search_companies(company_names):
    endpoint = 'https://api.leadiq.com/graphql'
    api_key = os.environ.get('LEADIQ_API_KEY')
    #api_key = config.get('LEADIQ_API_KEY')
    
    print(f"\nTesting LeadIQ Company Search")
    print(f"Using API Key: {api_key[:10]}..." if api_key else "No API key found!")
    
    if not api_key:
        print("Error: LEADIQ_API_KEY environment variable not set")
        return
    
    headers = {
        'Authorization': f'Basic {api_key}',
        'Content-Type': 'application/json',
        'apollo-require-preflight': 'true'
    }
    
    # Query para buscar compañías
    query = """
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
                attributes
                categories
            }
            revenue
            revenueRange {
                start
                end
                description
            }
            predictedRevenue {
                start
                end
                description
            }
            sicCode {
                code
                description
            }
            secondarySicCodes {
                code
                description
            }
            naicsCode {
                code
                description
            }
            employeeRange
            crunchbaseUrl
            facebookUrl
            twitterUrl
            foundedYear
            companyHierarchy {
                isUltimate
                parent {
                id
                name
                }
                ultimateParent {
                id
                name
                }
            }
            updatedDate
            }
        }
        }
    """
    
    all_companies = []
    
    for company_name in company_names:
        print(f"\nSearching for: {company_name}")
        
        variables = {
            "input": {
                "name": company_name
            }
        }
        
        body = json.dumps({
            "query": query,
            "variables": variables
        })
        
        try:
            response = requests.post(endpoint, headers=headers, data=body, verify=False)
            print(f"Status Code: {response.status_code}")
            
            if response.ok:
                result = response.json()
                
                if "data" in result and "searchCompany" in result["data"]:
                    search_data = result["data"]["searchCompany"]
                    print(f"Found {search_data['totalResults']} results")
                    
                    for company in search_data['results']:
                        # Agregar el término de búsqueda
                        company['search_term'] = company_name
                        
                        # Aplanar locationInfo si existe y no es None
                        if location_info := company.pop('locationInfo', None):
                            if location_info:  # Verificar que no sea None
                                for key, value in location_info.items():
                                    company[f'location_{key}'] = value
                            else:
                                # Agregar campos vacíos si no hay locationInfo
                                company.update({
                                    'location_formattedAddress': None,
                                    'location_street1': None,
                                    'location_street2': None,
                                    'location_city': None,
                                    'location_areaLevel1': None,
                                    'location_country': None,
                                    'location_postalCode': None
                                })
                        
                        # # También podemos hacer lo mismo con technologies
                        # if techs := company.pop('technologies', None):
                        #     if techs:  # Verificar que no sea None
                        #         company['tech_names'] = ';'.join([t['name'] for t in techs])
                        #         company['tech_categories'] = ';'.join([t['category'] for t in techs])
                        #         company['tech_parent_categories'] = ';'.join([t['parentCategory'] for t in techs])
                        #     else:
                        #         company.update({
                        #             'tech_names': '',
                        #             'tech_categories': '',
                        #             'tech_parent_categories': ''
                        #         })
                        
                        all_companies.append(company)
                else:
                    print("No results found in response")
            else:
                print(f"Error! Response: {response.text}")
                
        except Exception as e:
            print(f"Error searching for {company_name}: {str(e)}")
            continue
    
    if all_companies:
        # Convertir a DataFrame
        df = pd.DataFrame(all_companies)
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'leadiq_companies_{timestamp}.csv'
        
        # Guardar a CSV
        df.to_csv(filename, index=False)
        print(f"\nResults saved to: {filename}")
        print(f"Total companies found: {len(df)}")
        
        # Mostrar las primeras filas
        print("\nFirst few rows:")
        print(df.head())
        
        return df
    else:
        print("\nNo results found for any company")
        return None

if __name__ == "__main__":
    # Lista de compañías para buscar
    companies = [
        "Microsoft",
        "Alphabet",
        "Apple",
        "Amazon",
        "Meta",
        "T-ROC"
    ]
    
    df = search_companies(companies) 