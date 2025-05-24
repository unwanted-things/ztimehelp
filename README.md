# ZTimeHelp

ZTimeHelp is a Python CLI application that helps you track and summarize your daily activities by fetching data from multiple platforms such as GitHub, Slack, and Zoom. It generates comprehensive time entry reports to help you document your work activities.

## Features

- **GitHub Activity Tracking**
  - Track issues created
  - Track issue comments
  - Track pull requests created
  - Track commits made


- **Report Generation**
  - Generate daily reports in Markdown format
  - Organize activities by platform and type
  - Include links to relevant resources

## Quick Start

```bash
# Install the package
pip install .

# Generate a time entry report for today
ztimehelp make-entry --date 2023-08-01 --output-dir ./reports
```

## Development

- Run tests: `pytest`
- Format code: `black src tests`
- Sort imports: `isort src tests`
- Lint code: `flake8 src tests`

## Requirements

- Python 3.8 or higher
- GitHub Personal Access Token

## License

This project is licensed under the MIT License - see the LICENSE file for details.
