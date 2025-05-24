# Azure Architecture Diagram Generator MCP Server

A Model Context Protocol (MCP) server that generates Azure architecture diagrams from natural language descriptions using Python's `diagrams` library.

## Features

- 🏗️ **Natural Language Processing**: Convert text descriptions into structured Azure architecture diagrams
- 🎨 **Visual Diagrams**: Generate both PNG and SVG format diagrams with official Azure icons
- 🐳 **Docker Support**: Fully containerized for easy deployment
- 🔧 **MCP Protocol**: Compatible with MCP clients for seamless integration
- ☁️ **Comprehensive Azure Support**: Covers 15+ Azure service categories including:
  - Compute (VMs, App Service, Functions, AKS)
  - Storage (Blob, Files, Queues, Tables)
  - Databases (SQL Database, Cosmos DB, Redis Cache)
  - Networking (VNet, Load Balancer, Application Gateway)
  - Security & Monitoring services

## Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd genaidiagramsasmcp
   ```

2. **Build the Docker image**:
   ```bash
   docker build -t azure-diagram-mcp .
   ```

3. **Run the container**:
   ```bash
   docker run -it azure-diagram-mcp
   ```

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Graphviz** (required for diagram generation):
   - **Windows**: Download from [graphviz.org](https://graphviz.org/download/) or use `choco install graphviz`
   - **macOS**: `brew install graphviz`
   - **Ubuntu/Debian**: `sudo apt-get install graphviz`

3. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

4. **Run the server**:
   ```bash
   python azure_diagram_server.py
   ```

## Usage Examples

### Basic Diagram Generation

```python
from azure_diagram_server import AzureDiagramGenerator

generator = AzureDiagramGenerator()

# Generate from text description
description = "A web application with Azure App Service, SQL Database, and Redis Cache"
result = generator.generate_diagram_from_text(description, "web_app_diagram")

# Generate from structured JSON
services = [
    {"type": "appservice", "name": "WebApp"},
    {"type": "sqldatabase", "name": "Database"},
    {"type": "redis", "name": "Cache"}
]
result = generator.generate_diagram_from_json(services, "structured_diagram")
```

### Supported Azure Services

The server supports a comprehensive range of Azure services:

| Category | Services |
|----------|----------|
| **Compute** | Virtual Machines, App Service, Functions, AKS, Container Instances |
| **Storage** | Blob Storage, File Storage, Queue Storage, Table Storage |
| **Database** | SQL Database, Cosmos DB, Redis Cache, MySQL, PostgreSQL |
| **Networking** | Virtual Network, Load Balancer, Application Gateway, CDN, DNS |
| **Security** | Key Vault, Active Directory, Security Center |
| **Monitoring** | Monitor, Log Analytics, Application Insights |

## API Reference

### MCP Tools

The server exposes the following MCP tools:

#### `generate_azure_diagram`
Generate an Azure architecture diagram from a text description.

**Parameters:**
- `description` (string): Natural language description of the architecture
- `diagram_name` (string): Name for the generated diagram file
- `format` (string, optional): Output format - "png" or "svg" (default: "png")

**Returns:**
- `success` (boolean): Whether the operation succeeded
- `message` (string): Status message
- `file_path` (string): Path to the generated diagram file
- `services_identified` (array): List of Azure services identified in the description

#### `generate_azure_diagram_from_json`
Generate an Azure architecture diagram from structured service data.

**Parameters:**
- `services` (array): List of service objects with `type` and `name` properties
- `diagram_name` (string): Name for the generated diagram file
- `format` (string, optional): Output format - "png" or "svg" (default: "png")

**Returns:**
- Same as `generate_azure_diagram`

## Configuration

### Environment Variables

Create a `.env` file with the following variables (optional):

```env
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Note**: Azure OpenAI is optional. The server will fall back to basic NLP processing if not configured.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Client    │────│  MCP Server      │────│   Diagrams      │
│                 │    │  (FastMCP)       │    │   Library       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                       ┌──────────────────┐
                       │  Azure OpenAI    │
                       │  (Optional)      │
                       └──────────────────┘
```

## Development

### Project Structure

```
genaidiagramsasmcp/
├── azure_diagram_server.py    # Main MCP server implementation
├── requirements.txt           # Python dependencies
├── Dockerfile                # Container configuration
├── .env                      # Environment variables (create from .env.example)
├── README.md                 # This file
├── tests/                    # Test files
│   ├── test_server_fixed.py  # Fixed test script
│   ├── validate_mcp.py       # Comprehensive validation
│   └── test_mcp_simple.py    # Simple diagram test
└── DEPLOYMENT_SUMMARY.md     # Deployment documentation
```

### Running Tests

```bash
# Test basic functionality
python test_server_fixed.py

# Comprehensive validation
python validate_mcp.py

# Simple diagram generation test
python test_mcp_simple.py
```

### Docker Development

```bash
# Build with no cache to ensure latest code
docker build --no-cache -t azure-diagram-mcp .

# Run with volume mount for development
docker run -v $(pwd):/app -it azure-diagram-mcp
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

1. **Graphviz not found**: Install Graphviz system package
2. **Import errors**: Ensure all Python dependencies are installed
3. **Azure OpenAI errors**: Check your API credentials or use without Azure OpenAI
4. **Docker build fails**: Ensure Docker has sufficient resources allocated

### Support

For issues and questions:
- Create an issue on GitHub
- Check the [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) for detailed deployment information

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) for MCP protocol support
- Uses [Diagrams](https://diagrams.mingrammer.com/) library for diagram generation
- Azure icons provided by the diagrams library
- Follows [Model Context Protocol](https://modelcontextprotocol.io/) specification