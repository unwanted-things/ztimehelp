# Installation Guide

This guide provides detailed instructions for installing ZTimeHelp on your system.

## Prerequisites

Before installing ZTimeHelp, make sure you have the following:

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

## Installation Methods

### Method 1: Install from PyPI (Not yet available)

```bash
pip install ztimehelp
```

### Method 2: Install from Source

1. Clone the repository (or download the source code):
   ```bash
   git clone https://github.com/yourusername/ztimehelp.git
   cd ztimehelp
   ```

2. Install the package:
   ```bash
   pip install .
   ```

### Method 3: Development Installation

If you plan to modify the code or contribute to the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ztimehelp.git
   cd ztimehelp
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the package in development mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

   This will install the package in "editable" mode, so your changes to the source code will be immediately available without reinstallation.

4. Alternatively, use the provided setup script:
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

## Verifying Installation

After installation, verify that ZTimeHelp is correctly installed by running:

```bash
ztimehelp --help
```

You should see the help message for the ZTimeHelp command-line interface.

## Troubleshooting

### Common Issues

1. **Command not found: ztimehelp**
   - Make sure your Python scripts directory is in your PATH.
   - If you're using a virtual environment, ensure it's activated.

2. **Dependency conflicts**
   - Consider using a virtual environment to avoid conflicts with other packages.

3. **Permission errors during installation**
   - On Unix-like systems, you might need to use `sudo pip install .` or install in user mode with `pip install --user .`.

### Getting Help

If you encounter any issues during installation, please:
- Check the [GitHub issues](https://github.com/yourusername/ztimehelp/issues) to see if your problem has been reported.
- Open a new issue if needed, providing details about your environment and the error messages you're seeing.
