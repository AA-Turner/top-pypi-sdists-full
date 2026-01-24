"""
EMRValidator - Comprehensive Usage Examples
Demonstrates all features of the library
"""

import pandas as pd
import numpy as np
from emr_validator import (
    DataValidator, 
    DataProfiler,
    HTMLReporter,
    JSONReporter,
    ValidationRule,
    RuleSet,
    Expectation,
    ExpectationSuite,
    HealthcareRuleSets
)


def create_sample_healthcare_data():
    """Create sample healthcare dataset for demonstration"""
    np.random.seed(42)
    n_records = 1000
    
    data = {
        'mrn': [f"MRN{str(i).zfill(8)}" for i in range(n_records)],
        'patient_id': range(1, n_records + 1),
        'age': np.random.randint(18, 90, n_records),
        'gender': np.random.choice(['M', 'F', 'Other'], n_records, p=[0.48, 0.48, 0.04]),
        'admission_date': pd.date_range('2023-01-01', periods=n_records, freq='8H'),
        'discharge_date': pd.date_range('2023-01-02', periods=n_records, freq='8H'),
        'icd10_code': np.random.choice(['I10', 'E11.9', 'J44.0', 'N18.3', 'I50.9'], n_records),
        'charge_amount': np.random.uniform(1000, 50000, n_records),
        'payment_amount': np.random.uniform(800, 45000, n_records),
        'provider_id': np.random.choice(['PROV001', 'PROV002', 'PROV003', 'PROV004'], n_records),
        'department': np.random.choice(['Cardiology', 'Emergency', 'Surgery', 'ICU'], n_records),
        'insurance_type': np.random.choice(['Medicare', 'Medicaid', 'Commercial', 'Self-Pay'], n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Introduce some data quality issues for demonstration
    df.loc[np.random.choice(df.index, 20), 'age'] = np.nan  # Missing ages
    df.loc[np.random.choice(df.index, 10), 'age'] = -5  # Invalid ages
    df.loc[np.random.choice(df.index, 5), 'icd10_code'] = 'INVALID'  # Invalid ICD codes
    df.loc[np.random.choice(df.index, 15), 'charge_amount'] = -100  # Negative charges
    
    return df


def example_1_basic_validation():
    """Example 1: Basic validation with fluent API"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Validation")
    print("="*60)
    
    # Create sample data
    df = create_sample_healthcare_data()
    
    # Initialize validator and run validations
    validator = DataValidator("Healthcare Data Quality Check")
    validator.load_data(df)
    
    # Chain validation rules
    (validator
        .expect_column_exists('mrn')
        .expect_column_exists('patient_id')
        .expect_column_not_null('mrn', threshold=0.99)
        .expect_column_not_null('age', threshold=0.95)
        .expect_column_values_between('age', 0, 120, threshold=0.98)
        .expect_column_values_in_set('gender', {'M', 'F', 'Other'}, threshold=1.0)
        .expect_column_values_unique('patient_id', threshold=1.0)
        .expect_mrn_format('mrn', threshold=0.99)
        .expect_icd_format('icd10_code', version=10, threshold=0.98)
    )
    
    # Get results
    results = validator.get_results()
    print(f"\nValidation completed!")
    print(f"Total validations: {results['summary']['total']}")
    print(f"Passed: {results['summary']['passed']}")
    print(f"Failed: {results['summary']['failed']}")
    print(f"Success rate: {results['summary']['success_rate']}%")
    
    # Show failed validations
    print("\nFailed Validations:")
    for fail in validator.get_failed_validations():
        print(f"  - {fail['rule']}: {fail['message']}")
    
    return validator


def example_2_data_profiling():
    """Example 2: Automated data profiling"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Data Profiling")
    print("="*60)
    
    df = create_sample_healthcare_data()
    
    # Create profiler and generate profile
    profiler = DataProfiler(df, "Healthcare Dataset Profile")
    profile = profiler.generate_profile()
    
    # Print summary
    profiler.print_summary()
    
    # Get column profiles as DataFrame
    column_df = profiler.to_dataframe()
    print("\nColumn Statistics:")
    print(column_df[['dtype', 'missing', 'unique_values']].head(10))
    
    return profiler


def example_3_custom_validations():
    """Example 3: Custom validation functions"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Validations")
    print("="*60)
    
    df = create_sample_healthcare_data()
    
    # Custom validation: charges > payments
    def validate_charge_payment_relationship(df, **kwargs):
        valid_mask = df['charge_amount'] >= df['payment_amount']
        valid_pct = valid_mask.sum() / len(df)
        
        passed = valid_pct > 0.95
        message = f"{valid_pct*100:.2f}% of records have charges >= payments"
        details = {
            "valid_percentage": round(valid_pct * 100, 2),
            "invalid_count": int((~valid_mask).sum())
        }
        
        return passed, message, details
    
    # Custom validation: date ranges
    def validate_date_sequence(df, **kwargs):
        valid_mask = df['discharge_date'] >= df['admission_date']
        valid_pct = valid_mask.sum() / len(df)
        
        passed = valid_pct == 1.0
        message = f"{valid_pct*100:.2f}% have valid date sequences"
        details = {"valid_percentage": round(valid_pct * 100, 2)}
        
        return passed, message, details
    
    # Apply custom validations
    validator = DataValidator("Custom Validations")
    validator.load_data(df)
    
    (validator
        .expect_custom("charge_payment_logic", validate_charge_payment_relationship)
        .expect_custom("date_sequence", validate_date_sequence)
    )
    
    results = validator.get_results()
    print(f"\nCustom validations completed!")
    print(f"Results: {results['summary']['passed']} passed, {results['summary']['failed']} failed")
    
    return validator


def example_4_rule_sets():
    """Example 4: Using reusable rule sets"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Reusable Rule Sets")
    print("="*60)
    
    df = create_sample_healthcare_data()
    
    # Create custom rule set
    financial_rules = RuleSet("Financial Validations", "Rules for financial data quality")
    
    def validate_positive_charges(df, **kwargs):
        valid = (df['charge_amount'] > 0).sum() / len(df)
        return valid > 0.98, f"Positive charges: {valid*100:.1f}%", {"valid_pct": round(valid*100, 2)}
    
    def validate_payment_range(df, **kwargs):
        valid = ((df['payment_amount'] >= 0) & (df['payment_amount'] <= df['charge_amount'])).sum() / len(df)
        return valid > 0.95, f"Valid payment range: {valid*100:.1f}%", {"valid_pct": round(valid*100, 2)}
    
    financial_rules.create_rule("positive_charges", "Charges must be positive", validate_positive_charges)
    financial_rules.create_rule("payment_range", "Payments within valid range", validate_payment_range)
    
    # Execute rule set
    results = financial_rules.execute_all(df)
    
    print(f"\nExecuted {len(financial_rules)} rules:")
    for result in results:
        status = "✓" if result['passed'] else "✗"
        print(f"  {status} {result['rule']}: {result['message']}")
    
    # Use pre-built healthcare rule sets
    demo_rules = HealthcareRuleSets.patient_demographics()
    demo_results = demo_rules.execute_all(df)
    
    print(f"\nPre-built healthcare rules:")
    for result in demo_results:
        status = "✓" if result['passed'] else "✗"
        print(f"  {status} {result['rule']}: {result['message']}")
    
    return financial_rules


def example_5_expectations():
    """Example 5: Great Expectations-style API"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Expectations API")
    print("="*60)
    
    df = create_sample_healthcare_data()
    
    # Create expectation suite
    suite = ExpectationSuite("Healthcare Data Expectations")
    
    # Add expectations
    (suite
        .expect("mrn_exists", Expectation.column_to_exist('mrn'))
        .expect("mrn_not_null", Expectation.column_values_to_not_be_null('mrn', mostly=0.99))
        .expect("valid_gender", Expectation.column_values_to_be_in_set('gender', {'M', 'F', 'Other'}))
        .expect("unique_patients", Expectation.column_values_to_be_unique('patient_id'))
        .expect("valid_age_range", Expectation.column_values_to_be_between('age', 0, 120, mostly=0.98))
        .expect("expected_rows", Expectation.table_row_count_to_be_between(500, 2000))
        .expect("expected_columns", Expectation.table_column_count_to_equal(12))
    )
    
    # Validate
    results = suite.validate(df)
    
    print(f"\nExecuted {len(suite)} expectations:")
    for result in results:
        status = "✓" if result['passed'] else "✗"
        print(f"  {status} {result['expectation']}: {result['message']}")
    
    return suite


def example_6_report_generation():
    """Example 6: Generate HTML and JSON reports"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Report Generation")
    print("="*60)
    
    df = create_sample_healthcare_data()
    
    # Run comprehensive validation
    validator = DataValidator("Comprehensive Healthcare Validation")
    validator.load_data(df)
    
    (validator
        .expect_column_exists('mrn')
        .expect_column_exists('patient_id')
        .expect_column_not_null('age', threshold=0.95)
        .expect_column_values_between('age', 0, 120, threshold=0.98)
        .expect_column_values_in_set('gender', {'M', 'F', 'Other'})
        .expect_column_values_unique('patient_id')
        .expect_mrn_format('mrn', threshold=0.99)
        .expect_icd_format('icd10_code', version=10, threshold=0.98)
    )
    
    results = validator.get_results()
    
    # Generate HTML report
    html_reporter = HTMLReporter(results)
    html_reporter.generate(
        filepath='/mnt/user-data/outputs/validation_report.html',
        title='Healthcare Data Quality Report'
    )
    print("✓ HTML report generated: validation_report.html")
    
    # Generate JSON report
    json_reporter = JSONReporter(results)
    json_reporter.generate(
        filepath='/mnt/user-data/outputs/validation_report.json',
        pretty=True
    )
    print("✓ JSON report generated: validation_report.json")
    
    # Export to DataFrame for further analysis
    results_df = validator.to_dataframe()
    results_df.to_csv('/mnt/user-data/outputs/validation_results.csv', index=False)
    print("✓ CSV export generated: validation_results.csv")
    
    return validator


def example_7_complete_workflow():
    """Example 7: Complete data quality workflow"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Complete Workflow")
    print("="*60)
    
    # Step 1: Load and profile data
    print("\n1. Loading and profiling data...")
    df = create_sample_healthcare_data()
    profiler = DataProfiler(df, "Initial Data Profile")
    profile = profiler.generate_profile()
    print(f"   Quality Score: {profile['quality_summary']['quality_score']}/100")
    
    # Step 2: Run validations
    print("\n2. Running comprehensive validations...")
    validator = DataValidator("Complete Quality Check")
    validator.load_data(df)
    
    (validator
        .expect_column_exists('mrn')
        .expect_column_exists('patient_id')
        .expect_column_not_null('mrn', threshold=0.99)
        .expect_column_not_null('age', threshold=0.95)
        .expect_column_values_between('age', 0, 120, threshold=0.98)
        .expect_column_values_in_set('gender', {'M', 'F', 'Other'})
        .expect_column_values_unique('patient_id')
        .expect_mrn_format('mrn')
        .expect_icd_format('icd10_code', version=10, threshold=0.98)
    )
    
    results = validator.get_results()
    print(f"   Success Rate: {results['summary']['success_rate']}%")
    
    # Step 3: Generate reports
    print("\n3. Generating reports...")
    html_reporter = HTMLReporter(results)
    html_reporter.generate(filepath='/mnt/user-data/outputs/complete_report.html')
    print("   ✓ HTML report generated")
    
    # Step 4: Identify and log issues
    print("\n4. Data quality issues identified:")
    failed = validator.get_failed_validations()
    for i, fail in enumerate(failed[:5], 1):
        print(f"   {i}. {fail['rule']}: {fail['message']}")
    
    # Step 5: Validation status
    print("\n5. Final status:")
    if validator.is_valid():
        print("   ✓ All validations passed!")
    else:
        print(f"   ✗ {len(failed)} validations failed")
        print("   → Review reports for detailed analysis")
    
    return validator, profiler


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("EMRValidator - Healthcare Data Quality & Validation Library")
    print("Comprehensive Examples and Use Cases")
    print("="*70)
    
    # Run all examples
    example_1_basic_validation()
    example_2_data_profiling()
    example_3_custom_validations()
    example_4_rule_sets()
    example_5_expectations()
    example_6_report_generation()
    example_7_complete_workflow()
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("Check /mnt/user-data/outputs/ for generated reports")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
