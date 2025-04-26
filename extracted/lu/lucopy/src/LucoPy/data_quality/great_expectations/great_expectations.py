import json
from datetime import datetime

from great_expectations.core import ExpectationConfiguration
from great_expectations.expectations.registry import get_renderer_impl
from great_expectations.core.util import convert_to_json_serializable
from ..data_quality import CheckResult, CollectionResult

def process_meta_field(meta, mappings):

    mapped_metadata = {'metadata': {}}

    # Invert keys and values to make mapping easier
    mappings = {v: k for k, v in mappings.items()}

    for k, v in meta.items():
        if k in mappings:
            mapped_metadata[mappings[k]] = v
        elif k in mappings.values():
            mapped_metadata[k] = v
        else:
            mapped_metadata['metadata'][k] = v

    return mapped_metadata

class ExpectationResult:

    def __init__(self, expectation_results, metadata_mappings={}):

        expectation_results = convert_to_json_serializable(expectation_results)
        self.expectation = expectation_results
        self.expectation_config = expectation_results['expectation_config']
        self.result = expectation_results['result']
        self.success = expectation_results['success']
        self.result_format = expectation_results['expectation_config']['kwargs'].get('result_format', 'BASIC')
        self.meta = expectation_results['expectation_config']['meta']
        self.custom_mappings = metadata_mappings

    def __str__(self):
        return json.dumps(self.expectation, indent=2)

    def convert_to_check(self):
        """
        Convert expectation into a Check
        """
        rendered_expectation = {}

        rendered_expectation['success'] = self.success
        rendered_expectation['check'] = self.expectation_config['expectation_type']

        # Render expectation config to templated string with args
        rendered_expectation.update(self.render_expectation_config())

        # Render results based on format
        rendered_expectation.update(self.render_results(self.result, self.result_format))

        # Default metadata mappings for recognised fields
        metadata_mappings = {
            'onFail': 'onFail',
            'referenceUrl': 'referenceUrl',
            'tags': 'tags'
        }

        # Update custom metadata mappings if provided
        for k, v in self.custom_mappings.items():
            if k in metadata_mappings:
                metadata_mappings[k] = v

        # Process meta field
        rendered_expectation.update(process_meta_field(self.meta, metadata_mappings))

        return CheckResult(rendered_expectation)

    def render_expectation_config(self):
        """
        For a single expectation get the unique renderer method and call this
        to generate a rendered, parameterised expectation name with args.
        """
        string_render_method = get_renderer_impl(
            object_name=self.expectation_config['expectation_type'],
            renderer_type='renderer.prescriptive'
        )[1]

        rendered_expectation = string_render_method(
            configuration=ExpectationConfiguration(**self.expectation_config)
        )[0]

        rendered_expectation_str = {'check': rendered_expectation.string_template['template'],
                                    'checkArgs': rendered_expectation.string_template['params']}

        return self.filter_rendered_expectation(rendered_expectation_str)

    def filter_rendered_expectation(self, rendered_expectation):
        """
        Remove unused keys from check_args
        """
        filtered_args = {}

        for k, v in rendered_expectation['checkArgs'].items():
            # TODO: Type checking here might be valid in all cases.
            if k in rendered_expectation['check'] and not isinstance(v, (dict, list)):
                # chechArgs must be strings
                filtered_args[k] = str(v)

        rendered_expectation['checkArgs'] = filtered_args

        return rendered_expectation

    def render_results(self, result, result_format):
        """
        Render the result set of an expectation
        """
        if result_format == 'BOOLEAN_ONLY' or len(result) == 0:
            return {}
        elif result.get('observed_value'):
            # If an observed value is provided then use this
            
            if isinstance(result['observed_value'], list):

                # Filter out errant values. This can be introduced by a bug when using
                # SparkDFDataset or MetaSparkDFDataset which prepend '__eval_col' to column names.
                # TODO: Investigate if still necessary
                observed_value = [v for v in result['observed_value'] if '__eval_col' not in v]

                return {'observed': observed_value}
            else:
                return {'observed': f'{result["observed_value"]}'}

        else:
            # Otherwise, map result stats
            # TODO: Parse the full unexpected lists but with a length cap?
            result_mappings = {
                'element_count': 'elementCount',
                'unexpected_percent_total': 'failedPercentage',
                'partial_unexpected_list': 'partialFailedRecordsList',
                'partial_unexpected_index_list': 'partialFailedRecordsIndexList',
                'partial_unexpected_counts': 'partialUnexpectedCounts'
            }

            mapped_result = {}
            for k, v in result.items():
                if k in result_mappings:

                    if 'percent' in k:
                        mapped_result[result_mappings[k]] = self.percentage_as_string(v)
                    else:
                        mapped_result[result_mappings[k]] = v

            return {'observed': mapped_result}

    def percentage_as_string(self, value):
        return f'{round(value, 2)}%'

class ExpectationSuiteResult:

    def __init__(self, suite_results, suite_mappings={}, expectation_mappings={}):

        suite_results = convert_to_json_serializable(suite_results)
        self.expectation_suite = suite_results
        self.meta = suite_results['meta']
        self.suite_mappings = suite_mappings
        self.expectation_mappings = expectation_mappings

    def __str__(self):
        return json.dumps(self.expectation_suite, indent=2)

    def convert_to_collection(self):
        """
        Construct JSON dictionary of collection from expectation suite results.
        """
        # Initialise object with required keys
        collection = {'checks': []}

        # Convert each expectation result to a check
        for expectation in self.expectation_suite['results']:
            collection['checks'].append(
                ExpectationResult(expectation, self.expectation_mappings).convert_to_check().to_json_dict()
                )

        collection['tool'] = 'Great Expectations'

        metadata_mappings = {
            'toolVersion': 'great_expectations_version',
            'name': 'expectation_suite_name',
            'start': 'validation_time',
            'referenceUrl': 'referenceUrl',
            'tags': 'tags',
            'dataSet': 'dataSet'
        }

        # Update metadata mappings if provided
        for k, v in self.suite_mappings.items():
            if k in metadata_mappings:
                metadata_mappings[k] = v

        collection.update(process_meta_field(self.meta, metadata_mappings))

        collection['start'] = self.validate_start_time(collection['start'])

        # GE sets the suite name to 'default' in some cases. Remove if so.
        if collection['name'] == 'default':
            del collection['name']

        return CollectionResult(collection)

    def validate_start_time(self, ts):
        # Converts timestamps to ISO
        dt = datetime.strptime(ts, '%Y%m%dT%H%M%S.%fZ')
        return dt.isoformat()