def get_provider_info():
    return {
        'package-name': 'airflow-provider-census',
        'name': 'Census Provider',
        'description': 'A Census provider for Apache Ariflow.',
        'hook-class-names': ['airflow_provider_census.hooks.census.CensusHook'],
        'versions': ['2.0.0']
    }
