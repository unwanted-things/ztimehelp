# Time Entry Helper

A Python application to help with time entry management.

## Installation

### Development Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the package in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

### Production Installation

```bash
pip install .
```

## Usage

```bash
ztimehelp --help
```

## Development

- Run tests: `pytest`
- Format code: `black src tests`
- Sort imports: `isort src tests`
- Lint code: `flake8 src tests`
