#!/usr/bin/env python3
"""
Agent Runtime Module Test Execution Script

Provides different levels and types of test execution options, supports generating detailed test reports.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class TestRunner:
    """Test executor"""
    
    def __init__(self, test_dir: Path):
        self.test_dir = test_dir
        self.runtime_dir = test_dir / "runtime"
        self.client_dir = test_dir / "client"
        
    def run_command(self, cmd: List[str], description: str) -> bool:
        """Execute command and display results"""
        print(f"\n{'='*60}")
        print(f"🧪 {description}")
        print(f"{'='*60}")
        print(f"Command: {' '.join(cmd)}")
        print("-" * 60)
        
        try:
            # Modify to use poetry run prefix and run directly
            if cmd[0] == "python":
                cmd = ["poetry", "run"] + cmd
            result = subprocess.run(cmd, cwd=self.test_dir.parent.parent)  # Set to project root directory
            
            if result.returncode == 0:
                print(f"✅ {description} - PASSED")
                return True
            else:
                print(f"❌ {description} - FAILED (exit code: {result.returncode})")
                return False
        except Exception as e:
            print(f"❌ {description} - ERROR: {e}")
            return False
    
    def run_unit_tests(self, verbose: bool = False, coverage: bool = False) -> bool:
        """Run unit tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/runtime/", "-m", "unit"]

        if verbose:
            cmd.append("-v")
        
        if coverage:
            cmd.extend([
                "--cov=novita_sandbox.agent_runtime.runtime",
                "--cov-report=html:htmlcov/runtime_unit",
                "--cov-report=term-missing"
            ])
        
        return self.run_command(cmd, "Unit Tests")
    
    def run_integration_tests(self, verbose: bool = False) -> bool:
        """Run integration tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/runtime/", "-m", "integration"]
        
        if verbose:
            cmd.append("-v")
        
        return self.run_command(cmd, "Integration Tests")
    
    
    def run_compatibility_tests(self, verbose: bool = False) -> bool:
        """Run compatibility tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/runtime/", "-m", "compatibility"]
        
        if verbose:
            cmd.append("-v")
        
        return self.run_command(cmd, "Compatibility Tests")
    
    def run_examples_tests(self, verbose: bool = False) -> bool:
        """Run example tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/examples/"]
        
        if verbose:
            cmd.append("-v")
        
        return self.run_command(cmd, "Examples Tests")
    
    def run_all_tests(self, verbose: bool = False, coverage: bool = False, module: str = "all") -> bool:
        """Run all tests
        
        Args:
            module: Test module ("runtime", "client", "all")
        """
        if module == "runtime":
            cmd = ["python", "-m", "pytest", "agent_runtime/tests/runtime/"]
            cov_source = "novita_sandbox.agent_runtime.runtime"
            report_dir = "htmlcov/runtime_full"
        elif module == "client":
            cmd = ["python", "-m", "pytest", "agent_runtime/tests/client/"]
            cov_source = "novita_sandbox.agent_runtime.client"
            report_dir = "htmlcov/client_full"
        else:  # "all"
            cmd = ["python", "-m", "pytest", "agent_runtime/tests/"]
            cov_source = "novita_sandbox.agent_runtime"
            report_dir = "htmlcov/agent_runtime_full"
        
        
        if verbose:
            cmd.append("-v")
        
        if coverage:
            cmd.extend([
                f"--cov={cov_source}",
                f"--cov-report=html:{report_dir}",
                "--cov-report=term-missing",
                "--cov-fail-under=85"
            ])
        
        description = f"All {module.title()} Tests" if module != "all" else "All Agent Runtime Tests"
        return self.run_command(cmd, description)
    
    def run_specific_file(self, file_path: str, verbose: bool = False) -> bool:
        """Run specific test file"""
        cmd = ["python", "-m", "pytest", file_path]
        
        if verbose:
            cmd.append("-v")
        
        return self.run_command(cmd, f"Tests in {file_path}")
    
    # === Client Tests ===
    def run_client_unit_tests(self, verbose: bool = False, coverage: bool = False) -> bool:
        """Run client unit tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/client/"]
        
        if verbose:
            cmd.append("-v")
        
        if coverage:
            cmd.extend([
                "--cov=novita_sandbox.agent_runtime.client",
                "--cov-report=html:htmlcov/client_unit",
                "--cov-report=term-missing"
            ])
        
        return self.run_command(cmd, "Client Unit Tests")
    
    def run_client_integration_tests(self, verbose: bool = False) -> bool:
        """Run client integration tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/client/"]
        
        if verbose:
            cmd.append("-v")
        
        return self.run_command(cmd, "Client Integration Tests")
    
    
    def run_all_client_tests(self, verbose: bool = False, coverage: bool = False) -> bool:
        """Run all client tests"""
        cmd = ["python", "-m", "pytest", "agent_runtime/tests/client/"]
        
        if verbose:
            cmd.append("-v")
        
        if coverage:
            cmd.extend([
                "--cov=novita_sandbox.agent_runtime.client",
                "--cov-report=html:htmlcov/client_full",
                "--cov-report=term-missing",
                "--cov-fail-under=90"
            ])
        
        return self.run_command(cmd, "All Client Tests")
    
    def run_parallel_tests(self, workers: int = 4, verbose: bool = False, module: str = "all") -> bool:
        """Run tests in parallel"""
        if module == "runtime":
            test_path = "agent_runtime/tests/runtime/"
        elif module == "client":
            test_path = "agent_runtime/tests/client/"
        else:  # "all"
            test_path = "agent_runtime/tests/"
        
        cmd = [
            "python", "-m", "pytest", 
            test_path,
            "-n", str(workers),
        ]
        
        if verbose:
            cmd.append("-v")
        
        description = f"Parallel {module.title()} Tests" if module != "all" else "Parallel Agent Runtime Tests"
        return self.run_command(cmd, f"{description} (workers: {workers})")
    
    def generate_test_report(self, module: str = "all") -> bool:
        """Generate detailed test report"""
        if module == "runtime":
            test_path = "agent_runtime/tests/runtime/"
            cov_source = "novita_sandbox.agent_runtime.runtime"
            report_prefix = "runtime"
        elif module == "client":
            test_path = "agent_runtime/tests/client/"
            cov_source = "novita_sandbox.agent_runtime.client"
            report_prefix = "client"
        else:  # "all"
            test_path = "agent_runtime/tests/"
            cov_source = "novita_sandbox.agent_runtime"
            report_prefix = "agent_runtime"
        
        cmd = [
            "python", "-m", "pytest",
            test_path,
            f"--html=reports/{report_prefix}_report.html",
            "--self-contained-html",
            f"--junitxml=reports/{report_prefix}_junit.xml",
            f"--cov={cov_source}",
            f"--cov-report=html:reports/{report_prefix}_coverage_html",
            f"--cov-report=xml:reports/{report_prefix}_coverage.xml"
        ]
        
        # Create reports directory
        reports_dir = self.test_dir.parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        description = f"Generate {module.title()} Test Report" if module != "all" else "Generate Complete Test Report"
        return self.run_command(cmd, description)
    
    def lint_and_format_check(self) -> bool:
        """Code quality check"""
        results = []
        
        # Check code format - Runtime
        results.append(self.run_command(
            ["python", "-m", "ruff", "check", "src/novita_sandbox/agent_runtime/runtime/"],
            "Ruff Code Quality Check (Runtime)"
        ))
        
        # Check code format - Client
        results.append(self.run_command(
            ["python", "-m", "ruff", "check", "src/novita_sandbox/agent_runtime/client/"],
            "Ruff Code Quality Check (Client)"
        ))
        
        # Type check - Runtime
        results.append(self.run_command(
            ["python", "-m", "mypy", "src/novita_sandbox/agent_runtime/runtime/"],
            "MyPy Type Check (Runtime)"
        ))
        
        # Type check - Client
        results.append(self.run_command(
            ["python", "-m", "mypy", "src/novita_sandbox/agent_runtime/client/"],
            "MyPy Type Check (Client)"
        ))
        
        return all(results)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Agent Runtime Module Test Executor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Test Execution Examples:

  # Run all unit tests
  poetry run python run_tests.py --unit

  # Run integration tests (with verbose output)
  poetry run python run_tests.py --integration --verbose

  # Run all tests (with coverage report)
  poetry run python run_tests.py --all --coverage

  # Run tests in parallel
  poetry run python run_tests.py --parallel

  # Generate complete test report
  poetry run python run_tests.py --report

  # Run specific test file
  poetry run python run_tests.py --file agent_runtime/tests/runtime/test_models.py

  # Code quality check
  poetry run python run_tests.py --lint
        """
    )
    
    # Test type options
    test_group = parser.add_mutually_exclusive_group(required=True)
    test_group.add_argument("--unit", action="store_true", help="Run unit tests")
    test_group.add_argument("--integration", action="store_true", help="Run integration tests")
    test_group.add_argument("--compatibility", action="store_true", help="Run compatibility tests")
    test_group.add_argument("--examples", action="store_true", help="Run example tests")
    test_group.add_argument("--all", action="store_true", help="Run all tests")
    test_group.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    test_group.add_argument("--report", action="store_true", help="Generate test report")
    test_group.add_argument("--file", type=str, help="Run specific test file")
    test_group.add_argument("--lint", action="store_true", help="Code quality check")
    
    # Client-specific test options
    test_group.add_argument("--client-unit", action="store_true", help="Run client unit tests")
    test_group.add_argument("--client-integration", action="store_true", help="Run client integration tests")
    test_group.add_argument("--client-all", action="store_true", help="Run all client tests")
    
    # Option arguments
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel test worker processes")
    parser.add_argument("--module", choices=["runtime", "client", "all"], default="runtime", 
                       help="Specify test module (runtime/client/all)")
    parser.add_argument("--network", action="store_true", help="Include tests requiring network")
    
    args = parser.parse_args()
    
    # Determine test directory
    test_dir = Path(__file__).parent
    if not test_dir.exists():
        print(f"❌ Test directory does not exist: {test_dir}")
        sys.exit(1)
    
    # Create test executor
    runner = TestRunner(test_dir)
    
    # Execute corresponding tests
    success = False
    
    if args.unit:
        success = runner.run_unit_tests(verbose=args.verbose, coverage=args.coverage)
    elif args.integration:
        success = runner.run_integration_tests(verbose=args.verbose)
    elif args.compatibility:
        success = runner.run_compatibility_tests(verbose=args.verbose)
    elif args.examples:
        success = runner.run_examples_tests(verbose=args.verbose)
    elif args.all:
        success = runner.run_all_tests(
            verbose=args.verbose, 
            coverage=args.coverage,
            module=args.module
        )
    elif args.parallel:
        success = runner.run_parallel_tests(workers=args.workers, verbose=args.verbose, module=args.module)
    elif args.report:
        success = runner.generate_test_report(module=args.module)
    elif args.file:
        success = runner.run_specific_file(args.file, verbose=args.verbose)
    elif args.lint:
        success = runner.lint_and_format_check()
    # Client-specific tests
    elif args.client_unit:
        success = runner.run_client_unit_tests(verbose=args.verbose, coverage=args.coverage)
    elif args.client_integration:
        success = runner.run_client_integration_tests(verbose=args.verbose)
    elif args.client_all:
        success = runner.run_all_client_tests(
            verbose=args.verbose, 
            coverage=args.coverage
        )
    
    # Output results
    if success:
        print(f"\n🎉 Test execution successful!")
        sys.exit(0)
    else:
        print(f"\n💥 Test execution failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
