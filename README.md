# Copilot Demo

This repository demonstrates use of Github Copilot in VS Code.

## Features

- Use of Model Context Protocol (MCP) servers
- TODO: Add more features

## Prerequisites

- **Git**
- **Visual Studio Code**
  - When opening this project in VS Code, you'll be prompted to install recommended extensions.
- **Docker**
  - Required to run the GitHub MCP server.
- **uv**
  - Required to run the git MCP server and manage python environments.

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

## Environment Variables

| Variable                     | Description                                                                                                                                                                                     | Required |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| GITHUB_PERSONAL_ACCESS_TOKEN | GitHub Personal Access Token for authentication with the GitHub MCP server. Create this token in your Github Developer Settings with the minimal permissions you'd like the MCP server to have. | Yes      |

## Project Structure

TODO: Add description of key files and directories

## Resources

- [Claude's Constitution](https://www.anthropic.com/news/claudes-constitution) - Anthropic's AI principles and ethical guidelines
- [Copilot Tips and Tricks](https://code.visualstudio.com/docs/copilot/copilot-tips-and-tricks) - Tips and best practices for using GitHub Copilot in VS Code
- [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers) - Collection of official and community-maintained MCP servers

## Documentation

- [GitHub Copilot](https://docs.github.com/en/copilot) - Overview of Github Copilot
- [GitHub Copilot in VS Code](https://code.visualstudio.com/docs/copilot/overview) - Overview and guide for using GitHub Copilot in Visual Studio Code
- [MCP Server Documentation](https://modelcontextprotocol.io/introduction) - Introduction to Model Context Protocol
- [GitHub MCP Server](https://github.com/github/github-mcp-server) - Official GitHub Model Context Protocol Server repository

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
