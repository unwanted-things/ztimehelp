"""Tests for the time_entry_helper package."""

from click.testing import CliRunner

from time_entry_helper.cli import main


def test_cli_help():
    """Test the CLI help output."""
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Time Entry Helper" in result.output


def test_entry_command():
    """Test the entry command."""
    runner = CliRunner()
    result = runner.invoke(main, ["entry", "--start", "--message", "Working on project"])
    assert result.exit_code == 0
    assert "Starting a new time entry: Working on project" in result.output
