import logging
from typing import Optional, Literal
import time
from databricks.sdk.runtime import dbutils as db

# Helper for data contract creation: extract DDL components
def extract_ddl(ddl: str) -> str:
    import re

    ddl = re.sub(
        r"\nUSING\s+.*?(?=\nCOMMENT|\nTBLPROPERTIES|$)",
        "",
        ddl,
        flags=re.DOTALL
    )

    ddl = re.sub(
        r"\nTBLPROPERTIES\s*\(.*?\)\s*",
        "",
        ddl,
        flags=re.DOTALL
    )

    ddl = re.sub(
        r"\s+COMMENT\s+'[^']*'",
        "",
        ddl
    )
    ddl = re.sub(
        r"\nCOMMENT\s+'.*?'",
        "",
        ddl,
        flags=re.DOTALL
    )

    ddl = ddl.strip()
    if not ddl.endswith(";"):
        ddl += ";"

    return ddl

# Create DDL from table and generate data contract YAML file
def create_data_contract_yaml(spark, table: str):
    import yaml
    import os
    from datacontract.data_contract import DataContract

    ddl = spark.sql(
        f"SHOW CREATE TABLE {table}"
    ).collect()[0][0]

    clean_ddl = extract_ddl(ddl)

    output_file = f"ddl/{table}.sql"
    os.makedirs("ddl", exist_ok=True)
    with open(output_file, "w") as f:
        f.write(clean_ddl)

    data_contract = DataContract.import_from_source(source=output_file, format="sql").to_yaml()

    yml_file = f"contract/{table}.yml"
    os.makedirs("contract", exist_ok=True)
    with open(yml_file, "w") as f:
        f.write(data_contract)

    print(data_contract)




def run_data_contract_tests(
    data_contract_file: str,
    spark_session=None,
    show_sample_data: bool = True,
    export_results: bool = False,
    output_path: str = None,
    raise_on_failure: bool = False
):
    """
    Run data quality checks using datacontract-cli.
    
    Args:
        data_contract_file: Path to the data contract YAML file
        spark_session: Spark session (defaults to global spark if None)
        show_sample_data: Whether to show sample data from the table
        export_results: Whether to export results to JSON
        output_path: Path for JSON export (defaults to contract name if None)
        raise_on_failure: Whether to raise exception if tests fail
    
    Returns:
        dict: Summary of test results including pass/fail status and counts
    
    Raises:
        ValueError: If tests fail and raise_on_failure is True
    """
    from datacontract.data_contract import DataContract
    import json
    from datetime import datetime
    
    # Use provided spark session or fall back to global
    spark_session = spark_session or spark
    
    # Initialize data contract
    data_contract = DataContract(
        data_contract_file=data_contract_file,
        spark=spark_session
    )
    
    # Run tests
    print(f"🔍 Running data quality checks from: {data_contract_file}")
    print("="*80)
    
    run = data_contract.test()
    
    # Calculate statistics
    total_checks = len(run.checks)
    passed = sum(1 for c in run.checks if c.result == 'passed')
    failed = sum(1 for c in run.checks if c.result == 'failed')
    warnings = sum(1 for c in run.checks if c.result == 'warning')
    skipped = sum(1 for c in run.checks if c.result == 'skipped')
    errors = sum(1 for c in run.checks if c.result == 'error')
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"TEST RESULTS: {'✅ PASSED' if run.has_passed() else '❌ FAILED'}")
    print(f"{'='*80}")
    print(f"Total checks:  {total_checks}")
    print(f"✅ Passed:     {passed} ({passed/total_checks*100:.1f}%)")
    print(f"❌ Failed:     {failed} ({failed/total_checks*100:.1f}%)")
    if warnings > 0:
        print(f"⚠️  Warnings:   {warnings}")
    if errors > 0:
        print(f"🔴 Errors:     {errors}")
    if skipped > 0:
        print(f"⏭️  Skipped:    {skipped}")
    
    # Show detailed results
    print(f"\n{'='*80}")
    print("DETAILED CHECK RESULTS")
    print(f"{'='*80}")
    
    for i, check in enumerate(run.checks, 1):
        status_icons = {
            "passed": "✅",
            "failed": "❌",
            "warning": "⚠️",
            "error": "🔴",
            "skipped": "⏭️"
        }
        status_icon = status_icons.get(check.result, "❓")
        
        print(f"\n{i}. {status_icon} {check.name}")
        print(f"   Result: {check.result.upper()}")
        print(f"   Type: {check.type}")
        
        # Use getattr with defaults for safer attribute access
        field = getattr(check, 'field', None)
        if field:
            print(f"   Field: {field}")
        
        reason = getattr(check, 'reason', None)
        if reason:
            print(f"   Reason: {reason}")
        
        engine = getattr(check, 'engine', None)
        if engine:
            print(f"   Engine: {engine}")
    
    # Show failed checks summary
    failed_checks = [c for c in run.checks if c.result in ["failed", "error"]]
    if failed_checks:
        print(f"\n{'='*80}")
        print(f"FAILED CHECKS SUMMARY ({len(failed_checks)} failures)")
        print(f"{'='*80}")
        for check in failed_checks:
            print(f"\n❌ {check.name}")
            print(f"   Type: {check.type}")
            field = getattr(check, 'field', None)
            if field:
                print(f"   Field: {field}")
            reason = getattr(check, 'reason', None)
            if reason:
                print(f"   Reason: {reason}")
    
   
    # Export results if requested
    if export_results:
        output_file = output_path or f"dq_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        results = {
            "contract_file": data_contract_file,
            "timestamp": datetime.now().isoformat(),
            "passed": run.has_passed(),
            "summary": {
                "total": total_checks,
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "errors": errors,
                "skipped": skipped
            },
            "checks": [
                {
                    "name": c.name,
                    "type": c.type,
                    "result": c.result,
                    "field": getattr(c, 'field', None),
                    "reason": getattr(c, 'reason', None),
                    "engine": getattr(c, 'engine', None)
                }
                for c in run.checks
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results exported to: {output_file}")
    
    # Prepare return summary
    summary = {
        "passed": run.has_passed(),
        "total_checks": total_checks,
        "passed_checks": passed,
        "failed_checks": failed,
        "warning_checks": warnings,
        "error_checks": errors,
        "skipped_checks": skipped,
        "run_object": run
    }
    
    # Raise exception if requested and tests failed
    if raise_on_failure and not run.has_passed():
        raise ValueError(
            f"Data quality checks failed! {failed} out of {total_checks} checks failed."
        )
    
    print(f"\n{'='*80}")
    print("✨ Data quality check complete")
    print(f"{'='*80}\n")
    
    return summary



def html_to_markdown(html_content: str) -> str:
    import html2text

    h = html2text.HTML2Text()
    h.ignore_links = False  # keep links
    h.ignore_images = False # keep images
    h.body_width = 0        # avoid line wrapping
    return h.handle(html_content)


def get_confluence_markdown(page_id: str) -> str:
    import requests
    from requests.auth import HTTPBasicAuth

    CONFLUENCE_USER = db.secrets.get("DATAPLATTFORM_CONFLUENCE", "user")
    CONFLUENCE_API_TOKEN = db.secrets.get("DATAPLATTFORM_CONFLUENCE", "token")
    CONFLUENCE_BASE_URL = db.secrets.get("DATAPLATTFORM_CONFLUENCE", "url")

    try:
        url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
        resp = requests.get(url, auth=HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_API_TOKEN))
        resp.raise_for_status()
        html_content = resp.json()["body"]["storage"]["value"]
        #print(html_content)
        return html_to_markdown(html_content)

    except Exception as e:
        logging.warning(f"Could not fetch Confluence page {page_id}: {e}")
        return ""



def push_data_products_to_datahub_from_yml(
    yml_path: str, 
    env: str = "test"
) -> None:
    import yaml
    import logging
    from datahub.emitter.rest_emitter import DatahubRestEmitter
    from datahub.emitter.mce_builder import make_domain_urn, make_dataset_urn
    from datahub.emitter.mcp import MetadataChangeProposalWrapper
    from datahub.metadata.schema_classes import (
        DataProductPropertiesClass,
        DataProductAssociationClass,
        DomainsClass,
    )

    """
    Create Data Product entities in DataHub from a YAML file.
    """

    DATAHUB_URL = db.secrets.get("DATAPLATTFORM_DATAHUB", "url")
    DATAHUB_TOKEN = db.secrets.get("DATAPLATTFORM_DATAHUB", "token")
    DATAHUB_GMS_URL = f"https://{DATAHUB_URL}/api/gms"
    
    if env == "prod":
        platform = "databricks,PROD"
    elif env == "test":
        platform = "databricks,TEST"
    elif env == "stage":
        platform = "databricks,TEST"


    try:
        emitter = DatahubRestEmitter(gms_server=DATAHUB_GMS_URL, token=DATAHUB_TOKEN)

        # Load YAML file
        with open(yml_path, "r") as f:
            yml_data = yaml.safe_load(f)

        data_products = yml_data.get("data_products", [])
        if not data_products:
            logging.error("YAML contains no data products under 'data_products:'")
            return

        for dp in data_products:
            logging.info(f"Creating Data Product: {dp['label']}")

            # Domain(s)
            domains = []
            if "domain" in dp:
                domains.append(dp["domain"])
            if "domains" in dp:
                domains.extend(dp["domains"])

            if not domains:
                logging.warning(f"No domain specified for '{dp['name']}'.")

            domain_urns = [make_domain_urn(d.lower()) for d in domains]

            # Set data Product URN
            data_product_urn = f"urn:li:dataProduct:{dp['name']}"

            asset_associations = []

            for asset in dp.get("depends_on", []):
                if "." not in asset:
                    logging.warning(
                        f"Invalid asset '{asset}'. Must be 'catalog.schema.table'"
                    )
                    continue
                #dataset_urn = f"urn:li:dataset:(urn:li:dataPlatform:databricks,{asset},PROD)"
                dataset_urn = f"urn:li:dataset:(urn:li:dataPlatform{platform}.{asset},PROD)"
                #dataset_urn = "urn:li:dataset:(urn:li:dataPlatform:databricks,TEST.dataplattform_test.shared.d_calendar,PROD)"

                print(dataset_urn)
                
                asset_associations.append(
                    DataProductAssociationClass(destinationUrn=dataset_urn)
                )
                logging.info(f"  - Asset: {asset}")

            print(asset_associations)

            # Data Product Properties
            properties = DataProductPropertiesClass(
                name=dp["label"],
                description=get_confluence_markdown(dp.get("description", "")),
                assets=asset_associations,
                customProperties={
                    "Produkteier": dp.get("productowner", "")
                },
            )

            emitter.emit(
                MetadataChangeProposalWrapper(
                    entityUrn=data_product_urn,
                    aspect=properties,
                )
            )

            # Domain assignment
            if domain_urns:
                emitter.emit(
                    MetadataChangeProposalWrapper(
                        entityUrn=data_product_urn,
                        aspect=DomainsClass(domains=domain_urns),
                    )
                )

            logging.info(
                f"Data Product '{dp['label']}' created with "
                f"{len(asset_associations)} assets and {len(domain_urns)} domains"
            )

        logging.info("Successfully created Data Products from YAML")

    except Exception as e:
        logging.error(f"Error creating Data Products: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        if "emitter" in locals():
            emitter.close()
            logging.info("DataHub emitter closed")


def report_table_freshness(
    table_name: str,
    gms_url: Optional[str] = None,
    gms_token: Optional[str] = None,
    #platform: str = "databricks,TEST", #Brukes ikke frem til vi fjerner "TEST"
    env : str = "test",
    result: Literal["SUCCESS", "FAILURE"] = "SUCCESS",
    run_id: Optional[str] = None,
    cron_schedule: str = "0 2 * * *",
    timezone: str = "Europe/Oslo",
    description: Optional[str] = None,
) -> str:
    """
    Report table freshness to DataHub.
    
    Args:
        table_name: Full table name (e.g., "catalog.schema.table")
        gms_url: DataHub GMS URL
        gms_token: DataHub authentication token
        platform: Data platform name (default: "databricks")
        result: Test result - "SUCCESS" or "FAILURE"
        run_id: Optional unique run identifier
        cron_schedule: Expected update schedule in cron format
        timezone: Timezone for the schedule
        description: Optional description for the assertion
        
    Returns:
        The assertion URN
    """

    import datahub.emitter.mce_builder as builder
    from datahub.emitter.mcp import MetadataChangeProposalWrapper
    from datahub.emitter.rest_emitter import DatahubRestEmitter
    from datahub.metadata.schema_classes import (
        AssertionInfoClass,
        AssertionResultClass,
        AssertionResultTypeClass,
        AssertionRunEventClass,
        AssertionRunStatusClass,
        AssertionTypeClass,
        FreshnessAssertionInfoClass,
        FreshnessAssertionScheduleClass,
        FreshnessAssertionScheduleTypeClass,
        FreshnessAssertionTypeClass,
        FreshnessCronScheduleClass,
    )

    if env == "prod":
        platform = "databricks,PROD"
    elif env == "test":
        platform = "databricks,TEST"
    elif env == "stage":
        platform = "databricks,TEST"


     # Resolve secrets if not explicitly provided
    if gms_url is None or gms_token is None:
        gms_url = gms_url or f"https://{db.secrets.get('DATAPLATTFORM_DATAHUB', 'url')}/api/gms"
        gms_token = gms_token or db.secrets.get("DATAPLATTFORM_DATAHUB", "token")
    
    emitter = DatahubRestEmitter(gms_server=gms_url, token=gms_token)
    
    #dataset_urn = builder.make_dataset_urn(platform=platform, name=table_name)
    dataset_urn = f"urn:li:dataset:(urn:li:dataPlatform:{platform}.{table_name},PROD)"
    
    assertion_urn = builder.make_assertion_urn(
        builder.datahub_guid({"entity": dataset_urn, "type": "freshness"})
    )
    
    freshness_assertion_info = FreshnessAssertionInfoClass(
        type=FreshnessAssertionTypeClass.DATASET_CHANGE,
        entity=dataset_urn,
        schedule=FreshnessAssertionScheduleClass(
            type=FreshnessAssertionScheduleTypeClass.CRON,
            cron=FreshnessCronScheduleClass(
                cron=cron_schedule,
                timezone=timezone,
                windowStartOffsetMs=None,
            ),
        ),
    )
    
    assertion_info = AssertionInfoClass(
        type=AssertionTypeClass.FRESHNESS,
        freshnessAssertion=freshness_assertion_info,
        description=description or f"Table should be updated according to schedule: {cron_schedule}",
    )
    
    assertion_info_mcp = MetadataChangeProposalWrapper(
        entityUrn=assertion_urn,
        aspect=assertion_info,
    )
    emitter.emit_mcp(assertion_info_mcp)
    
    result_type = AssertionResultTypeClass.SUCCESS if result == "SUCCESS" else AssertionResultTypeClass.FAILURE
    
    assertion_result_mcp = MetadataChangeProposalWrapper(
        entityUrn=assertion_urn,
        aspect=AssertionRunEventClass(
            timestampMillis=int(round(time.time() * 1000)),
            assertionUrn=assertion_urn,
            asserteeUrn=dataset_urn,
            runId=run_id or f"run-{int(time.time())}",
            result=AssertionResultClass(type=result_type),
            status=AssertionRunStatusClass.COMPLETE,
        ),
    )
    emitter.emit_mcp(mcp=assertion_result_mcp)
    
    return assertion_urn