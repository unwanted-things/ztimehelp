"""Tests for the ztimehelp package."""

from click.testing import CliRunner

from ztimehelp.cli import main


def test_cli_help():
    """Test the CLI help output."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ZTimeHelp" in result.output
