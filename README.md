# Copilot Demo

This repository demonstrates the use of GitHub Copilot in VS Code and on GitHub.com. It focuses on the setup and use of tools rather than the details of code created with them.

## Features

- Model Context Protocol (MCP) servers
- Copilot for code review on PRs
- Custom [prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)

## Prerequisites

- [git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/)
- [uv](https://docs.astral.sh/uv/) to manage python environments
- [Docker](https://www.docker.com/) (optional) to run the local version of the GitHub MCP server

## MCP servers

- [GitHub](https://github.com/github/github-mcp-server)
- [Context7](https://github.com/upstash/context7)
- [DuckDB (MotherDuck MCP server)](https://github.com/motherduckdb/mcp-server-motherduck)

## Setup

1. Clone the repository

   ```bash
   git clone https://github.com/damonmcc/copilot-demo.git
   cd copilot-demo
   ```

2. Configure environment
   - Copy `.env.example` to `.env`
   - Configure required environment variables

3. Start the MCP servers configured in `.vscode/mcp.json`

### Environment Variables

| Variable                     | Description                                                                                                                                                                                     | Required |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| GITHUB_PERSONAL_ACCESS_TOKEN | GitHub Personal Access Token for authentication with GitHub MCP server (only required for a local server). Create this token in your GitHub Developer Settings with the minimal permissions you'd like the MCP server to have. | No      |

## Resources

- [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution) - Anthropic's AI principles and ethical guidelines
- [Copilot Tips and Tricks](https://code.visualstudio.com/docs/copilot/copilot-tips-and-tricks) - Tips and best practices for using GitHub Copilot in VS Code
- [GitHub MCP Registry](https://github.com/mcp) - An open catalog and API for publicly available MCP servers
- [VS Code MCP Servers](https://code.visualstudio.com/mcp) - A curated list of MCP servers by VS Code
- [Awesome GitHub Copilot Customizations](https://github.com/github/awesome-copilot) - Collection of community-contributed instructions, prompts, and configurations for GitHub Copilot.
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers) - Collection of reference and community-maintained MCP servers

## Documentation

- [GitHub Copilot](https://docs.github.com/en/copilot) - Overview of GitHub Copilot
- [GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview) - Overview and guide for using GitHub Copilot in Visual Studio Code
- [MCP Server Documentation](https://modelcontextprotocol.io/introduction) - Introduction to Model Context Protocol

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
