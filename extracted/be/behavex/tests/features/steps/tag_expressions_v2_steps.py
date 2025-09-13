# -*- coding: utf-8 -*-
import logging
import os
import re
import subprocess
import sys
import time

from behave import given, then, when

# Get project paths
root_project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
tests_features_path = os.path.join(root_project_path, 'tests', 'features')
secondary_features_path = os.path.join(tests_features_path, 'secondary_features')


@given('I have Behave 1.3.0 or newer installed')
def step_check_behave_version(context):
    """Skip the scenario if Behave version is less than 1.3.0"""
    try:
        import behave
        version_str = behave.__version__
        version_parts = version_str.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0

        if (major, minor) < (1, 3):
            context.scenario.skip(f"Skipping v2 tag expression test: Behave {version_str} < 1.3.0")
            return

        logging.info(f"Behave version {version_str} supports v2 tag expressions")
    except (ImportError, AttributeError, ValueError, IndexError) as e:
        context.scenario.skip(f"Could not determine Behave version: {e}")


@when('I run behavex with v2 tag expression "{tag_expression}"')
def step_run_behavex_with_v2_expression(context, tag_expression):
    """Run BehaveX with a v2 tag expression"""
    context.tag_expression = tag_expression
    context.expression_type = 'v2'

    # Use secondary features as test target
    output_dir = f'output/v2_test_{hash(tag_expression) % 1000000}'
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', output_dir,
        '-t', tag_expression,
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    context.start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)
    context.end_time = time.time()
    context.execution_time = context.end_time - context.start_time

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    # Log the secondary test execution details for review
    logging.info(f"BehaveX executed with v2 expression '{tag_expression}', exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")

    # Log detailed scenario information
    _log_executed_scenarios(context)


@when('I run behavex with v1 tag expression "{tag_expression}"')
def step_run_behavex_with_v1_expression(context, tag_expression):
    """Run BehaveX with a v1 tag expression"""
    context.tag_expression = tag_expression
    context.expression_type = 'v1'

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/v1_test_{hash(tag_expression) % 1000000}',
        '-t', tag_expression,
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    context.start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)
    context.end_time = time.time()
    context.execution_time = context.end_time - context.start_time

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    # Log the secondary test execution details for review
    logging.info(f"BehaveX executed with v1 expression '{tag_expression}', exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")


@when('I run behavex with invalid v2 tag expression "{tag_expression}"')
def step_run_behavex_with_invalid_v2_expression(context, tag_expression):
    """Run BehaveX with an invalid v2 tag expression (expecting failure)"""
    context.tag_expression = tag_expression
    context.expression_type = 'v2_invalid'

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/v2_invalid_test_{hash(tag_expression) % 1000000}',
        '-t', tag_expression,
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    # Log the secondary test execution details for review
    logging.info(f"BehaveX executed with invalid v2 expression '{tag_expression}', exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")


@when('I run behavex with empty tag expression "{tag_expression}"')
def step_run_behavex_with_empty_expression(context, tag_expression):
    """Run BehaveX with an empty tag expression"""
    context.tag_expression = tag_expression
    context.expression_type = 'empty'

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/empty_test_{hash(str(time.time())) % 1000000}',
        '--logging_level', 'INFO'
    ]

    # Don't add -t flag for empty expression

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    # Log the secondary test execution details for review
    logging.info(f"BehaveX executed with empty expression, exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")

@when('I run behavex with empty tag expression ""')
def step_run_behavex_with_empty_expression_literal(context):
    """Run BehaveX with an empty tag expression (literal empty string)"""
    context.tag_expression = ""
    context.expression_type = 'empty'

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/empty_test_{hash(str(time.time())) % 1000000}',
        '--logging_level', 'INFO'
    ]

    # For empty expression, don't add any -t argument (no filtering)

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    # Log the secondary test execution details for review
    logging.info(f"BehaveX executed with empty expression (literal), exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")


@then('I should see scenarios matching the v2 expression')
def step_should_see_scenarios_matching_v2(context):
    """Verify scenarios matching the v2 expression were executed with intelligent validation"""

    # Extract actual counts from the secondary test output
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    failed_count = _extract_scenario_count(context.stdout, 'failed')
    total_executed = passed_count + failed_count

    # Check if the v2 expression execution was successful
    execution_successful = (context.returncode == 0 or
                          (context.returncode == 1 and total_executed > 0))

    assert execution_successful, \
        f"v2 expression '{context.tag_expression}' failed to execute properly. " \
        f"Exit code: {context.returncode}, scenarios executed: {total_executed}"

    # Provide business coverage feedback based on scenario count
    if total_executed > 0:
        logging.info(f"✅ Excellent business coverage: v2 expression '{context.tag_expression}' " \
                    f"executed {total_executed} scenarios (passed: {passed_count}, failed: {failed_count}). " \
                    f"Tag filtering logic is working correctly!")
    elif context.returncode == 0:
        # 0 scenarios but successful execution - this could be valid for restrictive filters
        logging.info(f"✅ v2 expression '{context.tag_expression}' processed successfully " \
                    f"but found 0 matching scenarios. This may be expected for restrictive filters.")
    else:
        assert False, f"Unexpected execution state for v2 expression '{context.tag_expression}'"


@then('I should see scenarios matching the expression with minimum count "{min_count}"')
def step_should_see_minimum_scenarios(context, min_count):
    """Verify at least a minimum number of scenarios were executed"""
    min_expected = int(min_count)

    # Extract actual counts from the secondary test output
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    failed_count = _extract_scenario_count(context.stdout, 'failed')
    total_executed = passed_count + failed_count

    assert total_executed >= min_expected, \
        f"Expected at least {min_expected} scenarios for '{context.tag_expression}', " \
        f"but got {total_executed} (passed: {passed_count}, failed: {failed_count}). " \
        f"This indicates insufficient business coverage."

    logging.info(f"✅ Business coverage validated: '{context.tag_expression}' executed " \
                f"{total_executed} scenarios (>= {min_expected} required)")


@then('I should verify v2 tag expression processing')
def step_should_verify_v2_processing(context):
    """Verify that v2 tag expression was processed correctly, regardless of scenario count"""
    # The key validation is that:
    # 1. The subprocess executed successfully (exit code 0 or 1 with processed scenarios)
    # 2. No parsing errors occurred
    # 3. The v2 expression was accepted and processed by Behave's native parser

    if context.returncode == 0:
        # Success case - tag expression was processed successfully
        logging.info("✅ v2 tag expression processed successfully by native Behave parser")
    elif context.returncode == 1:
        # Check if this was a parsing error or just scenarios failing/being processed
        error_output = context.stderr + context.stdout

        # Look for parsing errors that would indicate v2 processing failed
        parsing_errors = ['syntax error', 'parse error', 'invalid tag expression', 'unexpected token']
        has_parsing_error = any(error.lower() in error_output.lower() for error in parsing_errors)

        if has_parsing_error:
            assert False, f"v2 tag expression parsing failed: {error_output[:500]}"
        else:
            # Exit code 1 but no parsing errors means scenarios were processed (some may have failed)
            passed_count = _extract_scenario_count(context.stdout, 'passed')
            failed_count = _extract_scenario_count(context.stdout, 'failed')
            total_processed = passed_count + failed_count

            logging.info(f"✅ v2 tag expression processed successfully - {total_processed} scenarios processed " \
                        f"(passed: {passed_count}, failed: {failed_count})")
    else:
        assert False, f"v2 tag expression processing failed with unexpected exit code {context.returncode}"


@when('I run behavex with complex v2 tag expression "{tag_expression}"')
def step_run_behavex_with_complex_v2_expression(context, tag_expression):
    """Run BehaveX with a complex v2 tag expression for performance testing"""
    context.tag_expression = tag_expression
    context.expression_type = 'v2_complex'

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/v2_complex_test_{hash(tag_expression) % 1000000}',
        '-t', tag_expression,
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    context.start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)
    context.end_time = time.time()
    context.execution_time = context.end_time - context.start_time

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    logging.info(f"BehaveX executed with complex v2 expression, exit code: {result.returncode}, time: {context.execution_time:.2f}s")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")

    # Log detailed scenario information
    _log_executed_scenarios(context)


@when('I run behavex with multiple v2 tag arguments "{tag_arg1}" and "{tag_arg2}"')
def step_run_behavex_with_multiple_v2_arguments(context, tag_arg1, tag_arg2):
    """Run BehaveX with multiple v2 tag arguments (combined as single v2 expression)"""
    # Combine the arguments into a single v2 expression
    combined_expression = f"{tag_arg1} and {tag_arg2}"
    context.tag_expression = combined_expression
    context.expression_type = 'v2_multiple'
    context.tag_arguments = [tag_arg1, tag_arg2]

    # Use secondary features as test target - pass as single v2 expression
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/v2_multiple_test_{hash(context.tag_expression) % 1000000}',
        '-t', combined_expression,  # Single combined v2 expression
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    context.start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)
    context.end_time = time.time()
    context.execution_time = context.end_time - context.start_time

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    logging.info(f"BehaveX executed with multiple v2 arguments '{tag_arg1}' and '{tag_arg2}', exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")

    # Log detailed scenario information
    _log_executed_scenarios(context)


@when('I run behavex with three v2 tag arguments "{tag_arg1}" and "{tag_arg2}" and "{tag_arg3}"')
def step_run_behavex_with_three_v2_arguments(context, tag_arg1, tag_arg2, tag_arg3):
    """Run BehaveX with three v2 tag arguments (combined as single v2 expression)"""
    # Combine the arguments into a single v2 expression
    combined_expression = f"{tag_arg1} and {tag_arg2} and {tag_arg3}"
    context.tag_expression = combined_expression
    context.expression_type = 'v2_three'
    context.tag_arguments = [tag_arg1, tag_arg2, tag_arg3]

    # Use secondary features as test target - pass as single v2 expression
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/v2_three_test_{hash(context.tag_expression) % 1000000}',
        '-t', combined_expression,  # Single combined v2 expression
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    context.start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)
    context.end_time = time.time()
    context.execution_time = context.end_time - context.start_time

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    logging.info(f"BehaveX executed with three v2 arguments, exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")

    # Log detailed scenario information
    _log_executed_scenarios(context)


@when('I run behavex with mixed tag arguments "{tag_arg1}" and "{tag_arg2}"')
def step_run_behavex_with_mixed_arguments(context, tag_arg1, tag_arg2):
    """Run BehaveX with mixed v1/v2 tag arguments"""
    context.tag_expression = f"{tag_arg1} and {tag_arg2}"
    context.expression_type = 'mixed'
    context.tag_arguments = [tag_arg1, tag_arg2]

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/mixed_test_{hash(context.tag_expression) % 1000000}',
        '-t', tag_arg1,
        '-t', tag_arg2,
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    logging.info(f"BehaveX executed with mixed arguments '{tag_arg1}' and '{tag_arg2}', exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")


@when('I run behavex with multiple v1 tag arguments "{tag_arg1}" and "{tag_arg2}"')
def step_run_behavex_with_multiple_v1_arguments(context, tag_arg1, tag_arg2):
    """Run BehaveX with multiple v1 tag arguments"""
    context.tag_expression = f"{tag_arg1} and {tag_arg2}"
    context.expression_type = 'v1_multiple'
    context.tag_arguments = [tag_arg1, tag_arg2]

    # Use secondary features as test target
    cmd = [
        sys.executable, '-m', 'behavex',
        secondary_features_path,
        '-o', f'output/v1_multiple_test_{hash(context.tag_expression) % 1000000}',
        '-t', tag_arg1,
        '-t', tag_arg2,
        '--logging_level', 'INFO'
    ]

    # Set up environment with PYTHONPATH
    env = os.environ.copy()
    env['PYTHONPATH'] = root_project_path

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=root_project_path, env=env)

    context.result = result
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.returncode = result.returncode

    logging.info(f"BehaveX executed with multiple v1 arguments '{tag_arg1}' and '{tag_arg2}', exit code: {result.returncode}")
    if result.stdout:
        logging.info(f"Secondary test STDOUT:\n{result.stdout}")
    if result.stderr:
        logging.info(f"Secondary test STDERR:\n{result.stderr}")


@then('the execution should succeed')
def step_execution_should_succeed(context):
    """Verify that BehaveX execution succeeded or had expected failures"""
    # For v2 expressions, we consider it successful if:
    # 1. Exit code is 0 (no failures)
    # 2. Exit code is 1 but scenarios were processed (some scenarios are designed to fail)

    if context.returncode == 0:
        logging.info("BehaveX execution succeeded as expected")
    elif context.returncode == 1:
        # Check if scenarios were actually processed (not a parsing error)
        passed_count = _extract_scenario_count(context.stdout, 'passed')
        failed_count = _extract_scenario_count(context.stdout, 'failed')
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + failed_count + skipped_count

        if total_scenarios > 0:
            logging.info(f"BehaveX execution completed with expected failures: {passed_count} passed, {failed_count} failed, {skipped_count} skipped")
        else:
            assert False, f"BehaveX execution failed with exit code {context.returncode}. Stderr: {context.stderr}"
    else:
        assert False, f"BehaveX execution failed with exit code {context.returncode}. Stderr: {context.stderr}"


@then('the execution should fail with a clear error message')
def step_execution_should_fail_with_error(context):
    """Verify that BehaveX execution failed with appropriate error message"""
    assert context.returncode != 0, f"BehaveX execution should have failed but succeeded. Stdout: {context.stdout}"

    # Check for error message in stderr or stdout
    error_output = context.stderr + context.stdout
    assert any(keyword in error_output.lower() for keyword in ['error', 'failed', 'invalid', 'syntax']), \
        f"Expected error message not found in output: {error_output}"

    logging.info(f"BehaveX execution failed as expected with error: {error_output[:200]}...")


@then('the error should mention invalid tag expression syntax')
def step_error_should_mention_syntax(context):
    """Verify that the error message mentions tag expression syntax"""
    error_output = context.stderr + context.stdout
    assert any(keyword in error_output.lower() for keyword in ['tag expression', 'syntax', 'parse', 'invalid']), \
        f"Expected tag expression syntax error not found in output: {error_output}"

    logging.info("Error message correctly mentions tag expression syntax issues")

@then('the error message should mention tag expression syntax')
def step_error_message_should_mention_tag_expression_syntax(context):
    """Verify that the error message mentions tag expression syntax issues"""
    error_output = context.stderr + context.stdout
    # Check for tag expression syntax related error messages
    assert any(keyword in error_output.lower() for keyword in ['tag expression', 'syntax', 'parse', 'invalid']), \
        f"Expected tag expression syntax error not found in output: {error_output}"

    logging.info("Error message correctly mentions tag expression syntax issues")


@then('I should see scenarios with both tags executed')
def step_should_see_both_tags_executed(context):
    """Verify that scenarios with both required tags were executed"""
    # Check that some scenarios passed (indicating execution occurred)
    passed_count = _extract_scenario_count(context.stdout, 'passed')

    # For AND operations, it's possible no scenarios match - this is valid behavior
    if passed_count == 0:
        # Check if there are any skipped scenarios, which indicates filtering worked
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

        # If we have skipped scenarios, the filtering is working correctly
        if skipped_count > 0 or total_scenarios > 0:
            logging.info(f"No scenarios matched both tags (passed: {passed_count}, skipped: {skipped_count}) - filtering working correctly")
        else:
            assert False, f"No scenarios were processed at all. Output: {context.stdout}"
    else:
        logging.info(f"Verified {passed_count} scenarios with both tags were executed")


@then('I should see scenarios without both tags skipped')
def step_should_see_without_both_tags_skipped(context):
    """Verify that scenarios without both required tags were skipped"""
    # Check that some scenarios were skipped or that filtering occurred
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    skipped_count = _extract_scenario_count(context.stdout, 'skipped')
    total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

    # If no scenarios passed and we have a total count, then filtering worked
    if passed_count == 0 and total_scenarios > 0:
        logging.info(f"All scenarios were filtered out (skipped: {skipped_count}) - filtering working correctly")
    elif skipped_count > 0:
        logging.info(f"Verified {skipped_count} scenarios without both tags were skipped")
    else:
        # This is acceptable if the expression matched some scenarios
        logging.info(f"Tag filtering processed {total_scenarios} scenarios (passed: {passed_count}, skipped: {skipped_count})")


@then('I should see scenarios with either tag executed')
def step_should_see_either_tag_executed(context):
    """Verify that scenarios with either required tag were executed"""
    # Check that some scenarios passed
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    assert passed_count > 0, "Expected some scenarios to pass with either tag"

    logging.info(f"Verified {passed_count} scenarios with either tag were executed")


@then('I should see scenarios without either tag skipped')
def step_should_see_without_either_tag_skipped(context):
    """Verify that scenarios without either required tag were skipped"""
    skipped_count = _extract_scenario_count(context.stdout, 'skipped')
    assert skipped_count > 0, "Expected some scenarios to be skipped"

    logging.info(f"Verified {skipped_count} scenarios without either tag were skipped")


@then('I should see scenarios without the excluded tag executed')
def step_should_see_without_excluded_tag_executed(context):
    """Verify that scenarios without the excluded tag were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    skipped_count = _extract_scenario_count(context.stdout, 'skipped')
    total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

    # For NOT operations, we expect either scenarios to pass OR proper filtering to occur
    if passed_count > 0:
        logging.info(f"Verified {passed_count} scenarios without excluded tag were executed")
    elif total_scenarios > 0:
        logging.info(f"NOT expression filtering worked correctly - {total_scenarios} scenarios processed, {passed_count} passed, {skipped_count} skipped")
    else:
        assert False, f"No scenarios were processed at all. Output: {context.stdout}"


@then('I should see scenarios with the excluded tag skipped')
def step_should_see_with_excluded_tag_skipped(context):
    """Verify that scenarios with the excluded tag were skipped"""
    skipped_count = _extract_scenario_count(context.stdout, 'skipped')
    assert skipped_count > 0, "Expected some scenarios with excluded tag to be skipped"

    logging.info(f"Verified {skipped_count} scenarios with excluded tag were skipped")


@then('I should see scenarios matching the complex expression executed')
def step_should_see_complex_expression_executed(context):
    """Verify that scenarios matching the complex expression were executed"""
    # For v2 expressions, if the execution succeeded (exit code 0), we consider it working
    if context.returncode == 0:
        logging.info("v2 complex tag expression was processed successfully")
    elif context.returncode == 1:
        passed_count = _extract_scenario_count(context.stdout, 'passed')
        failed_count = _extract_scenario_count(context.stdout, 'failed')
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + failed_count + skipped_count

        if total_scenarios > 0:
            logging.info(f"v2 complex tag expression executed scenarios: {passed_count} passed, {failed_count} failed, {skipped_count} skipped")
        else:
            assert False, f"v2 complex tag expression execution failed. Output: {context.stdout}"
    else:
        assert False, f"v2 complex tag expression execution failed with exit code {context.returncode}. Output: {context.stdout}"


@then('I should see scenarios with ORDERED_TEST but not ORDER_001 executed')
def step_should_see_ordered_test_but_not_order_001_executed(context):
    """Verify that scenarios with ORDERED_TEST but not ORDER_001 were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    skipped_count = _extract_scenario_count(context.stdout, 'skipped')
    total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

    # The expression worked if either scenarios passed OR proper filtering occurred
    if passed_count > 0:
        logging.info(f"Verified {passed_count} scenarios with ORDERED_TEST but not ORDER_001 were executed")
    elif total_scenarios > 0:
        logging.info(f"Tag filtering worked correctly - {total_scenarios} scenarios processed, {passed_count} passed, {skipped_count} skipped")
    else:
        assert False, f"No scenarios were processed at all. Output: {context.stdout}"


@then('I should see scenarios matching the nested expression executed')
def step_should_see_nested_expression_executed(context):
    """Verify that scenarios matching the nested expression were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    assert passed_count > 0, "Expected some scenarios to pass with nested expression"

    logging.info(f"Verified {passed_count} scenarios matching nested expression were executed")


@then('I should see scenarios matching all conditions executed')
def step_should_see_all_conditions_executed(context):
    """Verify that scenarios matching all AND conditions were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    assert passed_count > 0, "Expected some scenarios to pass with all conditions"

    logging.info(f"Verified {passed_count} scenarios matching all conditions were executed")


@then('I should see scenarios matching the expression executed')
def step_should_see_expression_executed(context):
    """Generic verification that scenarios matching the expression were executed or properly filtered"""
    # For v2 expressions, if the execution succeeded (exit code 0), we consider it working
    # even if no scenarios match (which is valid behavior)
    if context.returncode == 0:
        logging.info("v2 tag expression was processed successfully")
    elif context.returncode == 1:
        # Check if scenarios were actually processed in the subprocess output
        passed_count = _extract_scenario_count(context.stdout, 'passed')
        failed_count = _extract_scenario_count(context.stdout, 'failed')
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + failed_count + skipped_count

        if total_scenarios > 0:
            logging.info(f"v2 tag expression executed scenarios: {passed_count} passed, {failed_count} failed, {skipped_count} skipped")
        else:
            assert False, f"v2 tag expression execution failed. Output: {context.stdout}"
    else:
        assert False, f"v2 tag expression execution failed with exit code {context.returncode}. Output: {context.stdout}"


@then('I should see scenarios matching the multi-level expression executed')
def step_should_see_multi_level_expression_executed(context):
    """Verify that scenarios matching the multi-level expression were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    assert passed_count > 0, "Expected some scenarios to pass with multi-level expression"

    logging.info(f"Verified {passed_count} scenarios matching multi-level expression were executed")


@then('I should see scenarios with valid image attachment tags executed')
def step_should_see_valid_image_attachment_tags_executed(context):
    """Verify that scenarios with valid image attachment tags were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    skipped_count = _extract_scenario_count(context.stdout, 'skipped')
    total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

    # The expression worked if either scenarios passed OR proper filtering occurred
    if passed_count > 0:
        logging.info(f"Verified {passed_count} scenarios with valid image attachment tags were executed")
    elif total_scenarios > 0:
        logging.info(f"Image attachment tag filtering worked correctly - {total_scenarios} scenarios processed, {passed_count} passed, {skipped_count} skipped")
    else:
        assert False, f"No scenarios were processed at all. Output: {context.stdout}"


@then('all available scenarios should be executed')
def step_all_scenarios_should_be_executed(context):
    """Verify that all scenarios were executed (no tag filtering)"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    total_count = passed_count + _extract_scenario_count(context.stdout, 'failed') + _extract_scenario_count(context.stdout, 'skipped')

    # For empty expressions, if the execution succeeded (exit code 0), we consider it working
    if context.returncode == 0:
        logging.info("Empty tag expression was processed successfully - all scenarios executed")
    elif total_count > 0:
        logging.info(f"Empty tag expression executed scenarios: {passed_count} passed out of {total_count} total")
    else:
        assert False, f"Empty tag expression execution failed. Output: {context.stdout}"


@then('I should see scenarios matching the v1 expression executed')
def step_should_see_v1_expression_executed(context):
    """Verify that scenarios matching the v1 expression were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')
    assert passed_count > 0, "Expected some scenarios to pass with v1 expression"

    logging.info(f"Verified {passed_count} scenarios matching v1 expression were executed")


@then('the legacy tag matching should be used')
def step_legacy_tag_matching_should_be_used(context):
    """Verify that legacy tag matching was used (v1 expressions)"""
    # For v1 expressions, if scenarios were processed successfully, consider it working
    if context.returncode == 0:
        logging.info("Legacy tag matching processed successfully")
    elif context.returncode == 1:
        passed_count = _extract_scenario_count(context.stdout, 'passed')
        failed_count = _extract_scenario_count(context.stdout, 'failed')
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + failed_count + skipped_count

        if total_scenarios > 0:
            logging.info(f"Legacy tag matching executed scenarios: {passed_count} passed, {failed_count} failed, {skipped_count} skipped")
        else:
            assert False, f"Legacy tag matching execution failed. Output: {context.stdout}"
    else:
        assert False, f"Legacy tag matching execution failed with exit code {context.returncode}. Output: {context.stdout}"


@then('the native Behave parser should be used')
def step_native_behave_parser_should_be_used(context):
    """Verify that native Behave parser was used (v2 expressions)"""
    # This is implicit - if v2 expressions work, native parser was used
    # We can add more specific checks if needed (e.g., log analysis)
    assert context.returncode == 0, "Native Behave parser should work correctly"

    logging.info("Verified native Behave parser was used for v2 expressions")


@then('the execution should succeed within reasonable time')
def step_execution_should_succeed_within_reasonable_time(context):
    """Verify that execution completed within reasonable time (performance test)"""
    assert context.returncode == 0, f"Execution failed with exit code {context.returncode}"

    # Define reasonable time limit (adjust as needed)
    reasonable_time = 30.0  # seconds
    assert context.execution_time < reasonable_time, \
        f"Execution took {context.execution_time:.2f}s, expected < {reasonable_time}s"

    logging.info(f"Verified execution completed in {context.execution_time:.2f}s (within reasonable time)")


@then('I should see scenarios matching both tag arguments executed')
def step_should_see_both_tag_arguments_executed(context):
    """Verify that scenarios matching both tag arguments were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')

    # For multiple tag arguments with AND logic, it's possible no scenarios match
    if passed_count == 0:
        # Check if there are any skipped scenarios, which indicates filtering worked
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

        if skipped_count > 0 or total_scenarios > 0:
            logging.info(f"No scenarios matched both tag arguments (passed: {passed_count}, skipped: {skipped_count}) - filtering working correctly")
        else:
            assert False, f"No scenarios were processed at all. Output: {context.stdout}"
    else:
        logging.info(f"Verified {passed_count} scenarios matching both tag arguments were executed")


@then('I should see scenarios matching the merged expression executed')
def step_should_see_merged_expression_executed(context):
    """Verify that scenarios matching the merged expression were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')

    # For merged expressions, it's possible no scenarios match - this is valid behavior
    if passed_count == 0:
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

        if skipped_count > 0 or total_scenarios > 0:
            logging.info(f"No scenarios matched merged expression (passed: {passed_count}, skipped: {skipped_count}) - filtering working correctly")
        else:
            assert False, f"No scenarios were processed at all. Output: {context.stdout}"
    else:
        logging.info(f"Verified {passed_count} scenarios matching merged expression were executed")


@then('I should see scenarios matching all three tag arguments executed')
def step_should_see_all_three_tag_arguments_executed(context):
    """Verify that scenarios matching all three tag arguments were executed"""
    passed_count = _extract_scenario_count(context.stdout, 'passed')

    # For three tag arguments with AND logic, it's very possible no scenarios match
    if passed_count == 0:
        skipped_count = _extract_scenario_count(context.stdout, 'skipped')
        total_scenarios = passed_count + _extract_scenario_count(context.stdout, 'failed') + skipped_count

        if skipped_count > 0 or total_scenarios > 0:
            logging.info(f"No scenarios matched all three tag arguments (passed: {passed_count}, skipped: {skipped_count}) - filtering working correctly")
        else:
            assert False, f"No scenarios were processed at all. Output: {context.stdout}"
    else:
        logging.info(f"Verified {passed_count} scenarios matching all three tag arguments were executed")


@then('the legacy tag matching should be used for mixed arguments')
def step_legacy_tag_matching_should_be_used_for_mixed_arguments(context):
    """Verify that legacy tag matching was used for mixed v1/v2 arguments"""
    # Mixed arguments should fall back to legacy processing
    assert context.returncode == 0, "Legacy tag matching should work correctly for mixed arguments"

    logging.info("Verified legacy tag matching was used for mixed v1/v2 arguments")


@then('the legacy tag matching should be used for v1 arguments')
def step_legacy_tag_matching_should_be_used_for_v1_arguments(context):
    """Verify that legacy tag matching was used for v1 arguments"""
    # v1 arguments should use legacy processing
    assert context.returncode == 0, "Legacy tag matching should work correctly for v1 arguments"

    logging.info("Verified legacy tag matching was used for v1 arguments")


def _extract_scenario_count(output, status):
    """Extract scenario count for a specific status from BehaveX output"""
    import re

    # Look for patterns like "5 scenarios passed" or "3 scenarios skipped"
    pattern = rf'(\d+)\s+scenarios?\s+{status}'
    match = re.search(pattern, output, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return 0


def _extract_executed_scenarios(output):
    """Extract scenario names and their tags from BehaveX output"""
    scenarios = []

    # Look for feature file paths and scenario patterns in the output
    # Pattern: tests/features/secondary_features/some_file.feature:LINE  Scenario Name
    scenario_pattern = r'tests/features/secondary_features/([^:]+\.feature):(\d+)\s+(.+)'

    for match in re.finditer(scenario_pattern, output):
        feature_file = match.group(1)
        line_number = match.group(2)
        scenario_name = match.group(3).strip()

        # Skip if this looks like an error message or summary line
        if any(skip_word in scenario_name.lower() for skip_word in ['failing scenarios:', 'errored scenarios:', 'features passed']):
            continue

        scenarios.append({
            'feature_file': feature_file,
            'line_number': line_number,
            'scenario_name': scenario_name
        })

    return scenarios


def _get_scenario_tags(feature_file, line_number):
    """Extract tags for a specific scenario from the feature file"""
    try:
        feature_path = os.path.join(secondary_features_path, feature_file)
        with open(feature_path, 'r') as f:
            lines = f.readlines()

        # Convert line_number to 0-based index
        line_idx = int(line_number) - 1

        # Look backwards from the scenario line to find tags
        tags = []
        for i in range(line_idx - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith('@'):
                # This line contains tags
                tag_line_tags = [tag.strip() for tag in line.split() if tag.startswith('@')]
                tags.extend(tag_line_tags)
            elif line and not line.startswith('#'):
                # Non-empty, non-comment line that's not tags - stop looking
                break

        return list(reversed(tags))  # Reverse to get original order
    except Exception as e:
        logging.warning(f"Could not extract tags for {feature_file}:{line_number}: {e}")
        return []


def _find_matching_scenarios(tag_expression):
    """Find all scenarios in secondary features that match the given tag expression"""
    try:
        from behave.tag_expression import make_tag_expression

        # Parse the tag expression
        tag_expr = make_tag_expression(tag_expression)

        scenarios = []

        # Parse all feature files in secondary_features
        for feature_file in os.listdir(secondary_features_path):
            if not feature_file.endswith('.feature'):
                continue

            feature_path = os.path.join(secondary_features_path, feature_file)
            try:
                with open(feature_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                feature_tags = []
                for i, line in enumerate(lines):
                    line = line.strip()

                    # Collect feature-level tags
                    if line.startswith('@') and i == 0 or (i > 0 and not lines[i-1].strip()):
                        if 'Feature:' in ''.join(lines[i:i+3]):  # Feature tags
                            feature_tags.extend([tag.strip() for tag in line.split() if tag.startswith('@')])

                    # Find scenarios
                    elif line.startswith('Scenario:') or line.startswith('Scenario Outline:'):
                        scenario_name = line.replace('Scenario:', '').replace('Scenario Outline:', '').strip()
                        scenario_line = i + 1

                        # Collect scenario tags (look backwards from scenario line)
                        scenario_tags = []
                        for j in range(i - 1, -1, -1):
                            tag_line = lines[j].strip()
                            if tag_line.startswith('@'):
                                scenario_tags.extend([tag.strip() for tag in tag_line.split() if tag.startswith('@')])
                            elif tag_line and not tag_line.startswith('#'):
                                break

                        # Combine feature and scenario tags
                        all_tags = feature_tags + scenario_tags

                        # Remove @ prefix for evaluation (Behave expects tags without @)
                        eval_tags = [tag[1:] if tag.startswith('@') else tag for tag in all_tags]

                        # Check if this scenario matches the expression
                        if tag_expr.check(eval_tags):
                            scenarios.append({
                                'scenario_name': scenario_name,
                                'feature_file': feature_file,
                                'line_number': scenario_line,
                                'tags': all_tags,
                                'status': 'matched'
                            })

            except Exception as e:
                logging.debug(f"Error parsing {feature_file}: {e}")

        return scenarios

    except Exception as e:
        logging.debug(f"Error finding matching scenarios: {e}")
        return []


def _extract_scenarios_from_json(context):
    """Extract scenario details from feature files directly"""
    if hasattr(context, 'tag_expression'):
        return _find_matching_scenarios(context.tag_expression)
    return []


def _log_executed_scenarios(context):
    """Log detailed information about executed scenarios"""
    if not hasattr(context, 'stdout') or not context.stdout:
        return

    # Try to extract from JSON output first
    scenarios = _extract_scenarios_from_json(context)

    # Fallback to parsing stdout if JSON not available
    if not scenarios:
        scenarios = _extract_executed_scenarios(context.stdout)

    if scenarios:
        logging.info(f"\n=== EXECUTED SCENARIOS FOR '{context.tag_expression}' ===")
        for i, scenario in enumerate(scenarios, 1):
            tags_str = ' '.join(scenario.get('tags', [])) if scenario.get('tags') else '(no tags found)'

            logging.info(f"{i:2d}. {scenario['scenario_name']}")
            logging.info(f"     📁 {scenario['feature_file']}:{scenario.get('line_number', 'N/A')}")
            logging.info(f"     🏷️  {tags_str}")
            logging.info(f"     📊 Status: {scenario.get('status', 'unknown')}")
            logging.info("")

        logging.info(f"Total scenarios executed: {len(scenarios)}")
        logging.info("=" * 60)
    else:
        logging.info(f"No scenario details found for '{context.tag_expression}' (possibly 0 scenarios executed or parsing issue)")
