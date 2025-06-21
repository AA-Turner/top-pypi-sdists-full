from edgar import *


if __name__ == '__main__':
    c = Company("AAPL")
    f = c.latest("10-K")
    xb : XBRL = f.xbrl()

    print(f'There are {len(xb)} facts in this XBRL document.')

    query = xb.query()
    df = query.to_dataframe()

    #print(df)
    # Revenues
    # Find revenue-related facts
    revenue_query = xb.query().by_concept("us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax")
    print(revenue_query)

    # Multiple concepts
    #concepts = ["us-gaap:Revenues", "us-gaap:NetIncomeLoss"]
    #multi_query = xb.query().by_concept(concepts)
