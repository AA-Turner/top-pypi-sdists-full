from ..data_quality import CheckResult, CollectionResult
from .great_expectations import ExpectationResult, ExpectationSuiteResult

def convert_expectation_to_check(expectation_results: dict, metadata_mappings={}) -> CheckResult:
    '''
    Converts a single expectation result dictionary into a 
    formatted Check object

    Args:
        expectation_results (dict): Raw validation results for a single expectation.
        metadata_mappings (dict): Optionally submit custom mappings for the meta field.
    
    Returns:
        CheckResult: Expectation validation results converted to CheckResult format
    '''
    expectation = ExpectationResult(expectation_results, metadata_mappings)
    
    return expectation.convert_to_check()
    
def convert_suite_to_collection(expectation_suite_results: dict, suite_mappings={}, expectation_mappings={}) -> CollectionResult:
    '''
    Converts a suite of great expectations results as a 
    dictionary into a formatted Collection object
    
    Args:
        expectation_results (dict): Raw validation results for a single expectation.
        suite_mappings (dict): Optionally submit custom mappings for the suite meta field.
        expectation_mappings (dict): Optionally submit custom mappings for the expectation meta fields.
    
    Returns:
        CollectionResult: Suite validation results converted to CollectionResult format
    '''
    suite = ExpectationSuiteResult(expectation_suite_results, suite_mappings, expectation_mappings)

    return suite.convert_to_collection()