<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Azure Architecture Diagram Generator with MCP

This is an MCP Server project that generates Azure architecture diagrams from natural language descriptions.

## Architecture
- The server uses FastMCP Python library to create an MCP server.
- It processes natural language descriptions to extract structured information about Azure resources and relationships.
- It generates diagrams using the Python `diagrams` library.

## Notes for Development
- Use `mcp.server.fastmcp` for MCP server implementation.
- The Azure OpenAI API is used for text processing. Ensure proper credentials are set.
- The `diagrams` library requires Graphviz to be installed on the system.
- The web client is a static HTML page that simulates communication with the MCP server.

You can find more info and examples at https://modelcontextprotocol.io/llms-full.txt
