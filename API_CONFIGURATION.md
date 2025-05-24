# API Configuration Guide

ZTimeHelp requires authentication tokens for GitHub, Zoom, and Slack to fetch your activity data. This guide explains how to obtain and configure these tokens.

## Configuration Methods

ZTimeHelp looks for configuration in two places:
1. Environment variables (prefixed with ``)
2. Configuration file (`~/.ztimehelp/config.env`)

Environment variables take precedence over values in the configuration file.

## GitHub Configuration

### Required Values
- `GITHUB_TOKEN`: A personal access token for GitHub API
- `GITHUB_USERNAME`: Your GitHub username
- `GITHUB_ORGANIZATION`: (Optional) Name of the GitHub organization to focus on

### How to Get a GitHub Personal Access Token

1. Go to [GitHub Settings > Developer Settings > Personal Access Tokens > Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token" and select "Generate new token (classic)"
3. Give your token a descriptive name
4. Select the following scopes:
   - `repo` - Full control of private repositories
   - `user` - Read all user profile data
5. Click "Generate token"
6. Copy the token (it will only be shown once!)

### Setting GitHub Configuration

Using environment variables:
```bash
export GITHUB_TOKEN="your_token_here"
export GITHUB_USERNAME="your_username"
export GITHUB_ORGANIZATION="your_organization" # Optional
```

Using configuration file:
```
# In ~/.ztimehelp/config.env
GITHUB_TOKEN=your_token_here
GITHUB_USERNAME=your_username
GITHUB_ORGANIZATION=your_organization
```