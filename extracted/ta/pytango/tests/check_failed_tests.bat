@echo off
REM Wrapper script to run tests and check for failures

REM Check if any tests failed
if exist ".\tests\failed_tests.txt" (
    echo.
    echo ========================================
    echo FAILED TESTS:
    echo ========================================
    type ".\tests\failed_tests.txt"
    echo ========================================

    exit /b 1
)

echo.
echo ========================================
echo All tests passed!
echo ========================================
exit /b 0
