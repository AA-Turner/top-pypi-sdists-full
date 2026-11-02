from __future__ import annotations


from pointblank.actions import send_slack_notification


def test_send_slack_notification_dry_run(capsys):
    send_slack_notification(
        step_msg="""🚨 *Validation Step Alert*
• Step Number: {step}
• Column: {column}
• Test Type: {type}
• Value Tested: {value}
• Severity: {level} (level {level_num})
• Brief: {autobrief}
• Details: {failure_text}
• Time: {time}""",
        summary_msg="""📊 *Validation Summary Report*
*Overview*
• Status: {highest_severity}
• All Passed: {all_passed}
• Total Steps: {n_steps}

*Step Results*
• Passing Steps: {n_passing_steps}
• Failing Steps: {n_failing_steps}
• Warning Level: {n_warning_steps}
• Error Level: {n_error_steps}
• Critical Level: {n_critical_steps}

*Table Info*
• Table Name: {tbl_name}
• Row Count: {tbl_row_count}
• Column Count: {tbl_column_count}

*Timing*
• Duration: {validation_duration}s
• Completed: {time}""",
        debug=True,
    )

    # Capture the output and verify that "notification" was printed to the console
    captured = capsys.readouterr()
    assert "=== Step Notification Preview ===" in captured.out
    assert "• Step Number: 1" in captured.out
    assert "• Column: column_name" in captured.out
    assert "• Test Type: col_vals_gt" in captured.out
    assert "• Value Tested: 100" in captured.out
    assert "• Severity: critical (level 50)" in captured.out
    assert "• Brief: Values in column_name must be greater than 100" in captured.out
    assert "• Details: 25% of values failed this test" in captured.out
    assert "• Time: " in captured.out
    assert "=== Summary Notification Preview ===" in captured.out
    assert "• Status: critical" in captured.out
    assert "• All Passed: False" in captured.out
    assert "• Total Steps: 5" in captured.out
    assert "• Passing Steps: 3" in captured.out
    assert "• Failing Steps: 2" in captured.out
    assert "• Warning Level: 1" in captured.out
    assert "• Error Level: 0" in captured.out
    assert "• Critical Level: 1" in captured.out
    assert "• Table Name: example_table" in captured.out
    assert "• Row Count: 1000" in captured.out
    assert "• Column Count: 8" in captured.out
    assert "• Duration: 1.23s" in captured.out
    assert "• Completed: " in captured.out
