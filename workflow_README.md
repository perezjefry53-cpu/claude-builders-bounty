# 🔄 n8n Workflow: Weekly Dev Summary

This n8n workflow automatically generates a weekly narrative summary of your GitHub repository's activity using the Claude API.

## Features

- ⏰ **Scheduled**: Runs every Friday at 5 PM (configurable)
- 📊 **Data sources**: Git commits, closed issues, merged PRs
- 🤖 **AI-powered**: Generates narrative via Claude Sonnet 4
- 📬 **Delivery**: Slack OR Discord/email webhook
- 🌐 **Multi-language**: English or French output
- ⚙️ **Configurable**: All variables in one place

## Import

1. Open your n8n instance
2. Go to **Workflows** → **Import from File**
3. Select `workflows/weekly-dev-summary.json`
4. Configure the credentials:
   - GitHub API token (read-only access)
   - Anthropic/Claude API key
   - Slack bot token / webhook URL

## Configuration

Set these environment variables or n8n credentials:

| Variable | Description | Default |
|----------|-------------|---------|
| `owner` | GitHub owner | (set per repo) |
| `repo` | GitHub repo name | (set per repo) |
| `githubToken` | GitHub PAT with `repo` scope | - |
| `claudeApiKey` | Anthropic API key | - |
| `channel` | Slack channel | #dev-updates |
| `webhookUrl` | Fallback webhook URL | - |
| `language` | `EN` or `FR` | `EN` |

## Output sample

> **Weekly Dev Summary — myorg/myrepo**
> 
> This week saw significant progress on the authentication rewrite (PR #127, #129), with 23 commits from 4 contributors. The team focused on migrating from JWT to session-based auth, resolving 5 security-related issues. Key highlights include a 40% reduction in login latency and the introduction of rate limiting middleware. Next week's focus: database migration tooling and API v2 documentation.

## Requirements

- n8n v1.0+
- Claude API key (Anthropic)
- GitHub token with `repo` scope
- Slack webhook or Discord webhook
