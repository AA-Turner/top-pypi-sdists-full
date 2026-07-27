"""Comprehensive tests for sage/core/security.py - 100% coverage target."""

import json
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sage.core.security import (
    SecurityAuditor,
    SecurityFinding,
    SecuritySeverity,
)

# =============================================================================
# SecuritySeverity Tests
# =============================================================================


class TestSecuritySeverity:
    """Tests for SecuritySeverity constants."""

    def test_severity_values(self):
        """Test severity level values."""
        assert SecuritySeverity.CRITICAL == "CRITICAL"
        assert SecuritySeverity.HIGH == "HIGH"
        assert SecuritySeverity.MEDIUM == "MEDIUM"
        assert SecuritySeverity.LOW == "LOW"
        assert SecuritySeverity.INFO == "INFO"


# =============================================================================
# SecurityFinding Tests
# =============================================================================


class TestSecurityFinding:
    """Tests for SecurityFinding dataclass."""

    def test_basic_finding(self):
        """Test creating a basic finding."""
        finding = SecurityFinding(
            severity=SecuritySeverity.HIGH,
            file="test.py",
            line=10,
            rule="sage/hardcoded_secret",
            message="Hardcoded credential detected",
        )
        assert finding.severity == SecuritySeverity.HIGH
        assert finding.file == "test.py"
        assert finding.line == 10
        assert finding.rule == "sage/hardcoded_secret"
        assert finding.message == "Hardcoded credential detected"
        assert finding.cwe is None
        assert finding.owasp is None

    def test_finding_with_cwe_and_owasp(self):
        """Test finding with CWE and OWASP references."""
        finding = SecurityFinding(
            severity=SecuritySeverity.CRITICAL,
            file="vuln.py",
            line=25,
            rule="sage/sql_injection",
            message="SQL injection vulnerability",
            cwe="CWE-89",
            owasp="A03:2021 Injection",
        )
        assert finding.cwe == "CWE-89"
        assert finding.owasp == "A03:2021 Injection"

    def test_to_dict(self):
        """Test serialization to dict."""
        finding = SecurityFinding(
            severity=SecuritySeverity.MEDIUM,
            file="code.py",
            line=42,
            rule="sage/weak_crypto",
            message="Weak cryptographic algorithm",
            cwe="CWE-327",
            owasp="A02:2021 Cryptographic Failures",
        )
        result = finding.to_dict()

        assert result["severity"] == "MEDIUM"
        assert result["file"] == "code.py"
        assert result["line"] == 42
        assert result["rule"] == "sage/weak_crypto"
        assert result["message"] == "Weak cryptographic algorithm"
        assert result["cwe"] == "CWE-327"
        assert result["owasp"] == "A02:2021 Cryptographic Failures"

    def test_to_dict_without_optional_fields(self):
        """Test serialization without optional fields."""
        finding = SecurityFinding(
            severity=SecuritySeverity.LOW,
            file="test.js",
            line=5,
            rule="test/rule",
            message="Test message",
        )
        result = finding.to_dict()

        assert result["cwe"] is None
        assert result["owasp"] is None


# =============================================================================
# SecurityAuditor Tests
# =============================================================================


class TestSecurityAuditor:
    """Tests for SecurityAuditor class."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_init(self, temp_dir):
        """Test auditor initialization."""
        auditor = SecurityAuditor(temp_dir)
        assert auditor.cwd == temp_dir

    def test_check_tool_not_installed(self, temp_dir):
        """Test checking for a tool that's not installed."""
        auditor = SecurityAuditor(temp_dir)
        result = auditor._check_tool("nonexistent_tool_12345")
        assert result is False

    @patch("subprocess.run")
    def test_check_tool_installed(self, mock_run, temp_dir):
        """Test checking for an installed tool."""
        mock_run.return_value = MagicMock(returncode=0)
        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        result = auditor._check_tool("python")
        assert result is True

    @patch("subprocess.run")
    def test_check_tool_timeout(self, mock_run, temp_dir):
        """Test handling timeout when checking tool."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="test", timeout=5)
        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        result = auditor._check_tool("slow_tool")
        assert result is False

    def test_available_scanners_patterns_only(self, temp_dir):
        """Test available scanners when no tools installed."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            scanners = auditor.available_scanners
            assert scanners == ["patterns"]

    def test_available_scanners_with_bandit(self, temp_dir):
        """Test available scanners with bandit installed."""

        def mock_check(tool):
            return tool == "bandit"

        with patch.object(SecurityAuditor, "_check_tool", side_effect=mock_check):
            auditor = SecurityAuditor(temp_dir)
            scanners = auditor.available_scanners
            assert "patterns" in scanners
            assert "bandit" in scanners

    def test_available_scanners_with_semgrep(self, temp_dir):
        """Test available scanners with semgrep installed."""

        def mock_check(tool):
            return tool == "semgrep"

        with patch.object(SecurityAuditor, "_check_tool", side_effect=mock_check):
            auditor = SecurityAuditor(temp_dir)
            scanners = auditor.available_scanners
            assert "patterns" in scanners
            assert "semgrep" in scanners

    def test_scan_file_nonexistent(self, temp_dir):
        """Test scanning a file that doesn't exist."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("nonexistent.py")
            assert findings == []

    def test_scan_file_with_hardcoded_secret(self, temp_dir):
        """Test detecting hardcoded secrets."""
        test_file = temp_dir / "secrets.py"
        test_file.write_text('password = "supersecretpassword123"\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("secrets.py")

            assert len(findings) >= 1
            secret_finding = next((f for f in findings if "hardcoded" in f.message.lower()), None)
            assert secret_finding is not None
            assert secret_finding.severity == SecuritySeverity.HIGH

    def test_scan_file_with_sql_injection(self, temp_dir):
        """Test detecting SQL injection."""
        test_file = temp_dir / "db.py"
        test_file.write_text('cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("db.py")

            sql_finding = next((f for f in findings if "sql" in f.message.lower()), None)
            assert sql_finding is not None
            assert sql_finding.severity == SecuritySeverity.CRITICAL

    def test_scan_file_with_command_injection(self, temp_dir):
        """Test detecting command injection."""
        test_file = temp_dir / "cmd.py"
        test_file.write_text('os.system("rm -rf " + user_input)\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("cmd.py")

            cmd_finding = next((f for f in findings if "command" in f.message.lower()), None)
            assert cmd_finding is not None
            assert cmd_finding.severity == SecuritySeverity.CRITICAL

    def test_scan_file_with_shell_true(self, temp_dir):
        """Test detecting shell=True."""
        test_file = temp_dir / "shell.py"
        test_file.write_text("subprocess.run(cmd, shell=True)\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("shell.py")

            shell_finding = next((f for f in findings if "shell" in f.message.lower()), None)
            assert shell_finding is not None

    def test_scan_file_with_xss(self, temp_dir):
        """Test detecting XSS vulnerabilities."""
        test_file = temp_dir / "web.js"
        test_file.write_text('element.innerHTML = userInput + "<script>alert(1)</script>";\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("web.js")

            xss_finding = next((f for f in findings if "xss" in f.message.lower()), None)
            assert xss_finding is not None

    def test_scan_file_with_path_traversal(self, temp_dir):
        """Test detecting path traversal."""
        test_file = temp_dir / "files.py"
        test_file.write_text('open("../etc/passwd")\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("files.py")

            path_finding = next((f for f in findings if "path" in f.message.lower()), None)
            assert path_finding is not None

    def test_scan_file_with_weak_crypto(self, temp_dir):
        """Test detecting weak cryptography."""
        test_file = temp_dir / "crypto.py"
        test_file.write_text("hashlib.md5(data)\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("crypto.py")

            crypto_finding = next((f for f in findings if "weak" in f.message.lower()), None)
            assert crypto_finding is not None
            assert crypto_finding.severity == SecuritySeverity.MEDIUM

    def test_scan_file_with_debug_mode(self, temp_dir):
        """Test detecting debug mode enabled."""
        test_file = temp_dir / "config.py"
        test_file.write_text("DEBUG = True\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("config.py")

            debug_finding = next((f for f in findings if "debug" in f.message.lower()), None)
            assert debug_finding is not None
            assert debug_finding.severity == SecuritySeverity.LOW

    def test_scan_file_with_private_key(self, temp_dir):
        """Test detecting private keys."""
        test_file = temp_dir / "keys.pem"
        test_file.write_text("-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("keys.pem")

            key_finding = next((f for f in findings if "private key" in f.message.lower()), None)
            assert key_finding is not None
            assert key_finding.severity == SecuritySeverity.CRITICAL

    def test_scan_file_with_aws_key(self, temp_dir):
        """Test detecting AWS access keys."""
        test_file = temp_dir / "aws.py"
        test_file.write_text('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("aws.py")

            aws_finding = next((f for f in findings if "aws" in f.message.lower()), None)
            assert aws_finding is not None
            assert aws_finding.severity == SecuritySeverity.CRITICAL

    def test_scan_file_with_jwt_secret(self, temp_dir):
        """Test detecting hardcoded JWT secrets."""
        test_file = temp_dir / "jwt.py"
        test_file.write_text('JWT_SECRET = "my-super-secret-jwt-key"\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("jwt.py")

            jwt_finding = next((f for f in findings if "jwt" in f.message.lower()), None)
            assert jwt_finding is not None

    def test_scan_file_with_insecure_random(self, temp_dir):
        """Test detecting insecure random."""
        test_file = temp_dir / "random.py"
        test_file.write_text("token = random.random()\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("random.py")

            random_finding = next((f for f in findings if "random" in f.message.lower()), None)
            assert random_finding is not None

    def test_scan_file_with_ssrf(self, temp_dir):
        """Test detecting potential SSRF."""
        test_file = temp_dir / "http.py"
        test_file.write_text('requests.get("http://example.com/" + user_url)\n')

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("http.py")

            ssrf_finding = next((f for f in findings if "ssrf" in f.message.lower()), None)
            assert ssrf_finding is not None

    def test_scan_file_with_unsafe_yaml(self, temp_dir):
        """Test detecting unsafe YAML load."""
        test_file = temp_dir / "yaml_file.py"
        test_file.write_text("data = yaml.load(user_input)\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("yaml_file.py")

            yaml_finding = next((f for f in findings if "yaml" in f.message.lower()), None)
            assert yaml_finding is not None

    def test_scan_file_with_pickle_load(self, temp_dir):
        """Test detecting unsafe pickle."""
        test_file = temp_dir / "pickle_file.py"
        test_file.write_text("data = pickle.load(file)\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_file("pickle_file.py")

            pickle_finding = next((f for f in findings if "pickle" in f.message.lower()), None)
            assert pickle_finding is not None

    def test_scan_files_multiple(self, temp_dir):
        """Test scanning multiple files."""
        (temp_dir / "file1.py").write_text('password = "secret123456"\n')
        (temp_dir / "file2.py").write_text("DEBUG = True\n")

        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_files(["file1.py", "file2.py"])

            assert len(findings) >= 2
            files_found = {f.file for f in findings}
            assert "file1.py" in files_found
            assert "file2.py" in files_found

    def test_scan_content(self, temp_dir):
        """Test scanning content string."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            content = """
password = "hardcoded123456"
subprocess.run(cmd, shell=True)
"""
            findings = auditor.scan_content(content, "test.py")

            assert len(findings) >= 2

    def test_scan_content_empty(self, temp_dir):
        """Test scanning empty content."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            findings = auditor.scan_content("", "empty.py")
            assert findings == []

    @patch("subprocess.run")
    def test_run_bandit(self, mock_run, temp_dir):
        """Test running bandit scanner."""
        bandit_output = json.dumps(
            {
                "results": [
                    {
                        "issue_severity": "HIGH",
                        "line_number": 10,
                        "test_id": "B105",
                        "issue_text": "Hardcoded password",
                        "issue_cwe": {"id": "CWE-259"},
                    }
                ]
            }
        )
        mock_run.return_value = MagicMock(stdout=bandit_output, returncode=0)

        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        auditor._has_bandit = True
        auditor._has_semgrep = False

        findings = auditor._run_bandit("test.py")
        assert len(findings) == 1
        assert findings[0].severity == "HIGH"
        assert findings[0].line == 10
        assert "bandit" in findings[0].rule

    @patch("subprocess.run")
    def test_run_bandit_no_output(self, mock_run, temp_dir):
        """Test running bandit with no findings."""
        mock_run.return_value = MagicMock(stdout="", returncode=0)

        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        auditor._has_bandit = True

        findings = auditor._run_bandit("clean.py")
        assert findings == []

    @patch("subprocess.run")
    def test_run_bandit_exception(self, mock_run, temp_dir):
        """Test handling bandit exceptions."""
        mock_run.side_effect = Exception("Bandit crashed")

        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        auditor._has_bandit = True

        findings = auditor._run_bandit("test.py")
        assert findings == []

    @patch("subprocess.run")
    def test_run_semgrep(self, mock_run, temp_dir):
        """Test running semgrep scanner."""
        semgrep_output = json.dumps(
            {
                "results": [
                    {
                        "extra": {
                            "severity": "ERROR",
                            "message": "SQL injection detected",
                            "metadata": {
                                "cwe": "CWE-89",
                                "owasp": "A03",
                            },
                        },
                        "check_id": "python.security.sql-injection",
                        "start": {"line": 15},
                    }
                ]
            }
        )
        mock_run.return_value = MagicMock(stdout=semgrep_output, returncode=0)

        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        auditor._has_semgrep = True
        auditor._has_bandit = False

        findings = auditor._run_semgrep("test.py")
        assert len(findings) == 1
        assert findings[0].severity == SecuritySeverity.HIGH
        assert findings[0].line == 15
        assert "semgrep" in findings[0].rule

    @patch("subprocess.run")
    def test_run_semgrep_warning_severity(self, mock_run, temp_dir):
        """Test semgrep WARNING severity mapping."""
        semgrep_output = json.dumps(
            {
                "results": [
                    {
                        "extra": {
                            "severity": "WARNING",
                            "message": "Minor issue",
                        },
                        "check_id": "test-rule",
                        "start": {"line": 1},
                    }
                ]
            }
        )
        mock_run.return_value = MagicMock(stdout=semgrep_output, returncode=0)

        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        auditor._has_semgrep = True

        findings = auditor._run_semgrep("test.py")
        assert findings[0].severity == SecuritySeverity.MEDIUM

    @patch("subprocess.run")
    def test_run_semgrep_exception(self, mock_run, temp_dir):
        """Test handling semgrep exceptions."""
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="semgrep", timeout=60)

        auditor = SecurityAuditor.__new__(SecurityAuditor)
        auditor.cwd = temp_dir
        auditor._has_semgrep = True

        findings = auditor._run_semgrep("test.py")
        assert findings == []

    def test_deduplicate_findings(self, temp_dir):
        """Test finding deduplication."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.HIGH,
                    file="test.py",
                    line=10,
                    rule="sage/test",
                    message="Test",
                ),
                SecurityFinding(
                    severity=SecuritySeverity.HIGH,
                    file="test.py",
                    line=10,
                    rule="sage/test",  # Duplicate
                    message="Test",
                ),
                SecurityFinding(
                    severity=SecuritySeverity.LOW,
                    file="test.py",
                    line=20,
                    rule="sage/test2",
                    message="Test 2",
                ),
            ]

            deduplicated = auditor._deduplicate_findings(findings)
            assert len(deduplicated) == 2

    def test_deduplicate_findings_sorted_by_severity(self, temp_dir):
        """Test that deduplication sorts by severity."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.LOW, file="a.py", line=1, rule="r1", message="m1"
                ),
                SecurityFinding(
                    severity=SecuritySeverity.CRITICAL, file="b.py", line=1, rule="r2", message="m2"
                ),
                SecurityFinding(
                    severity=SecuritySeverity.MEDIUM, file="c.py", line=1, rule="r3", message="m3"
                ),
            ]

            deduplicated = auditor._deduplicate_findings(findings)
            assert deduplicated[0].severity == SecuritySeverity.CRITICAL
            assert deduplicated[1].severity == SecuritySeverity.MEDIUM
            assert deduplicated[2].severity == SecuritySeverity.LOW

    def test_format_findings_empty(self, temp_dir):
        """Test formatting empty findings."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)
            result = auditor.format_findings([])
            assert "No security issues found" in result

    def test_format_findings_with_issues(self, temp_dir):
        """Test formatting findings with issues."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.CRITICAL,
                    file="test.py",
                    line=10,
                    rule="sage/sql_injection",
                    message="SQL injection",
                    cwe="CWE-89",
                ),
                SecurityFinding(
                    severity=SecuritySeverity.LOW,
                    file="config.py",
                    line=5,
                    rule="sage/debug",
                    message="Debug enabled",
                ),
            ]

            result = auditor.format_findings(findings)
            assert "Security Scan Results" in result
            assert "CRITICAL" in result
            assert "SQL injection" in result
            assert "CWE-89" in result
            assert "LOW" in result

    def test_has_critical_findings_true(self, temp_dir):
        """Test detecting critical findings."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.CRITICAL,
                    file="test.py",
                    line=1,
                    rule="r1",
                    message="m1",
                ),
            ]

            assert auditor.has_critical_findings(findings) is True

    def test_has_critical_findings_high(self, temp_dir):
        """Test detecting high severity findings."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.HIGH, file="test.py", line=1, rule="r1", message="m1"
                ),
            ]

            assert auditor.has_critical_findings(findings) is True

    def test_has_critical_findings_false(self, temp_dir):
        """Test no critical findings."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.MEDIUM,
                    file="test.py",
                    line=1,
                    rule="r1",
                    message="m1",
                ),
                SecurityFinding(
                    severity=SecuritySeverity.LOW, file="test.py", line=2, rule="r2", message="m2"
                ),
            ]

            assert auditor.has_critical_findings(findings) is False

    def test_get_summary(self, temp_dir):
        """Test getting findings summary."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            findings = [
                SecurityFinding(
                    severity=SecuritySeverity.CRITICAL, file="a.py", line=1, rule="r1", message="m1"
                ),
                SecurityFinding(
                    severity=SecuritySeverity.HIGH, file="b.py", line=1, rule="r2", message="m2"
                ),
                SecurityFinding(
                    severity=SecuritySeverity.MEDIUM, file="c.py", line=1, rule="r3", message="m3"
                ),
                SecurityFinding(
                    severity=SecuritySeverity.MEDIUM, file="d.py", line=1, rule="r4", message="m4"
                ),
                SecurityFinding(
                    severity=SecuritySeverity.LOW, file="e.py", line=1, rule="r5", message="m5"
                ),
            ]

            summary = auditor.get_summary(findings)
            assert summary["total"] == 5
            assert summary["critical"] == 1
            assert summary["high"] == 1
            assert summary["medium"] == 2
            assert summary["low"] == 1
            assert summary["info"] == 0

    def test_get_summary_empty(self, temp_dir):
        """Test getting summary with no findings."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_dir)

            summary = auditor.get_summary([])
            assert summary["total"] == 0
            assert summary["critical"] == 0


# =============================================================================
# Integration Tests
# =============================================================================


class TestSecurityAuditorIntegration:
    """Integration tests for SecurityAuditor."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)

            # Create Python files
            (project / "app.py").write_text("""
from flask import Flask
app = Flask(__name__)
password = "admin123456789"  # Security issue
""")

            (project / "db.py").write_text("""
import sqlite3
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
""")

            (project / "config.py").write_text("""
DEBUG = True
SECRET_KEY = "not-so-secret-key123"
""")

            (project / "clean.py").write_text("""
import secrets
token = secrets.token_hex(32)
""")

            yield project

    def test_scan_entire_project(self, temp_project):
        """Test scanning an entire project."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_project)

            files = ["app.py", "db.py", "config.py", "clean.py"]
            findings = auditor.scan_files(files)

            # Should find issues in app.py, db.py, config.py
            files_with_issues = {f.file for f in findings}
            assert "app.py" in files_with_issues
            assert "db.py" in files_with_issues
            assert "config.py" in files_with_issues
            # clean.py should not have issues
            assert "clean.py" not in files_with_issues

    def test_complete_workflow(self, temp_project):
        """Test a complete security audit workflow."""
        with patch.object(SecurityAuditor, "_check_tool", return_value=False):
            auditor = SecurityAuditor(temp_project)

            # Scan files
            findings = auditor.scan_files(["app.py", "db.py"])

            # Check for critical issues
            has_critical = auditor.has_critical_findings(findings)

            # Get summary
            summary = auditor.get_summary(findings)

            # Format for display
            formatted = auditor.format_findings(findings)

            assert findings is not None
            assert isinstance(has_critical, bool)
            assert summary["total"] >= 0
            assert len(formatted) > 0
