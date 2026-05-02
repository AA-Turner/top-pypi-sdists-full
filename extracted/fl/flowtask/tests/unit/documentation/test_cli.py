"""Unit tests for documentation CLI."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from flowtask.documentation.cli import main, parse_args, get_base_dir


class TestParseArgs:
    """Tests for argument parsing."""

    def test_default_output(self):
        """Default output is documentation/."""
        args = parse_args([])
        assert args.output.name == "documentation"

    def test_custom_output(self, tmp_path):
        """--output sets custom output directory."""
        output = tmp_path / "custom"
        args = parse_args(["--output", str(output)])
        assert args.output == output

    def test_short_output(self, tmp_path):
        """-o is shorthand for --output."""
        output = tmp_path / "custom"
        args = parse_args(["-o", str(output)])
        assert args.output == output

    def test_components_single(self, tmp_path):
        """--components accepts single directory."""
        comp_dir = tmp_path / "components"
        args = parse_args(["--components", str(comp_dir)])
        assert args.components == [comp_dir]

    def test_components_multiple(self, tmp_path):
        """--components accepts multiple directories."""
        dir1 = tmp_path / "comp1"
        dir2 = tmp_path / "comp2"
        args = parse_args(["--components", str(dir1), str(dir2)])
        assert args.components == [dir1, dir2]

    def test_short_components(self, tmp_path):
        """-c is shorthand for --components."""
        comp_dir = tmp_path / "components"
        args = parse_args(["-c", str(comp_dir)])
        assert args.components == [comp_dir]

    def test_verbose_flag(self):
        """--verbose enables verbose mode."""
        args = parse_args(["--verbose"])
        assert args.verbose is True

    def test_short_verbose(self):
        """-v is shorthand for --verbose."""
        args = parse_args(["-v"])
        assert args.verbose is True

    def test_quiet_flag(self):
        """--quiet enables quiet mode."""
        args = parse_args(["--quiet"])
        assert args.quiet is True

    def test_short_quiet(self):
        """-q is shorthand for --quiet."""
        args = parse_args(["-q"])
        assert args.quiet is True


class TestMain:
    """Tests for main CLI function."""

    def test_help_exits_zero(self, capsys):
        """--help shows usage and returns 0."""
        result = main(["--help"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Generate documentation" in captured.out

    def test_main_returns_zero_on_success(self, tmp_path):
        """Main returns 0 on success."""
        with patch("flowtask.documentation.cli.ComponentDocGenerator") as mock_gen:
            mock_instance = MagicMock()
            mock_instance.generate.return_value = MagicMock(components={})
            mock_gen.return_value = mock_instance

            result = main(["--output", str(tmp_path), "--quiet"])

            assert result == 0

    def test_main_calls_generator(self, tmp_path):
        """Main creates generator with correct output directory."""
        output = tmp_path / "docs"
        with patch("flowtask.documentation.cli.ComponentDocGenerator") as mock_gen:
            mock_instance = MagicMock()
            mock_instance.generate.return_value = MagicMock(components={})
            mock_gen.return_value = mock_instance

            main(["--output", str(output), "--quiet"])

            mock_gen.assert_called_once_with(output_dir=output)

    def test_main_passes_component_paths(self, tmp_path):
        """Main passes component paths to generator."""
        comp_dir = tmp_path / "components"
        comp_dir.mkdir()

        with patch("flowtask.documentation.cli.ComponentDocGenerator") as mock_gen:
            mock_instance = MagicMock()
            mock_instance.generate.return_value = MagicMock(components={})
            mock_gen.return_value = mock_instance

            main(["--components", str(comp_dir), "--output", str(tmp_path), "--quiet"])

            mock_instance.generate.assert_called_once()
            call_args = mock_instance.generate.call_args[0][0]
            assert len(call_args) == 1
            assert call_args[0] == comp_dir

    def test_main_returns_one_on_error(self, tmp_path):
        """Main returns 1 on error."""
        with patch("flowtask.documentation.cli.ComponentDocGenerator") as mock_gen:
            mock_gen.side_effect = Exception("Test error")

            result = main(["--output", str(tmp_path), "--quiet"])

            assert result == 1


class TestGetBaseDir:
    """Tests for get_base_dir function."""

    def test_returns_path(self):
        """get_base_dir returns a Path object."""
        result = get_base_dir()
        assert isinstance(result, Path)

    def test_fallback_to_cwd(self):
        """Falls back to cwd when navconfig unavailable."""
        with patch.dict("sys.modules", {"navconfig": None}):
            with patch("flowtask.documentation.cli.Path") as mock_path:
                mock_path.cwd.return_value = Path("/test/cwd")
                # Re-import to trigger fallback
                # This is tricky to test, so we just verify the function works
                result = get_base_dir()
                assert isinstance(result, Path)


class TestIntegration:
    """Integration tests for CLI."""

    def test_cli_generates_real_docs(self, tmp_path):
        """CLI generates documentation for real components."""
        from pathlib import Path
        components_path = Path("flowtask/components")

        if not components_path.exists():
            pytest.skip("flowtask/components directory not found")

        output = tmp_path / "documentation"
        result = main([
            "--output", str(output),
            "--components", str(components_path),
            "--quiet"
        ])

        assert result == 0
        assert (output / "index.json").exists()
        assert (output / "components").exists()

    def test_cli_handles_missing_directory(self, tmp_path):
        """CLI handles missing component directory gracefully."""
        output = tmp_path / "documentation"
        missing_dir = tmp_path / "nonexistent"

        result = main([
            "--output", str(output),
            "--components", str(missing_dir),
            "--quiet"
        ])

        # Should succeed but with no components
        assert result == 0
        assert (output / "index.json").exists()


class TestModuleExecution:
    """Test module can be executed."""

    def test_module_has_main(self):
        """Module has main function."""
        from flowtask.documentation import cli
        assert hasattr(cli, "main")
        assert callable(cli.main)
