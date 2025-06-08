---
applyTo: '**'
---

# Custom instructions for Copilot

## Security

Never include the contents of files that match the following path filters in the prompt sent to the LLM servers, even if they're explicitly included in the prompt attachments:
    - "**/.env"

## Github

This repo is called "copilot-demo" and the owner is "damonmcc".

## Agent instructions

Always check for a relevant MCP tool before using the terminal.

Check for python package documentation in the directory `.github/docs`.
