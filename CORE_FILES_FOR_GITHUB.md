# Core Files for GitHub Repository

## Essential Files (Keep These)
- `azure_diagram_server.py` - Main MCP server implementation
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `README.md` - Project documentation
- `.gitignore` - Git ignore rules
- `.env.example` - Environment template
- `LICENSE` - MIT license
- `DEPLOYMENT_SUMMARY.md` - Deployment documentation
- `GITHUB_DEPLOYMENT_GUIDE.md` - GitHub deployment instructions
- `tests/` directory with test files

## Files to Exclude from GitHub (in .gitignore)
- `.env` - Contains sensitive data
- `*.png`, `*.svg` - Generated diagram files
- `__pycache__/` - Python cache
- Multiple duplicate/backup files
- Docker management scripts (platform-specific)
- Generated output files

## Recommended GitHub Repository Structure
```
azure-diagram-mcp-server/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── Dockerfile
├── azure_diagram_server.py
├── DEPLOYMENT_SUMMARY.md
├── GITHUB_DEPLOYMENT_GUIDE.md
└── tests/
    ├── __init__.py
    ├── test_server_fixed.py
    ├── validate_mcp.py
    └── test_mcp_simple.py
```

## Before Uploading to GitHub
1. The `.gitignore` file will automatically exclude sensitive and generated files
2. Only upload the core files listed above
3. Make sure `.env` is not uploaded (it's in .gitignore)
4. Remove any duplicate or backup files before uploading

## Clean Upload Process
When uploading to GitHub, only select these files:
1. All `.py` files that are core to the project
2. Configuration files (`requirements.txt`, `Dockerfile`, `.env.example`)
3. Documentation files (`README.md`, `LICENSE`, `DEPLOYMENT_SUMMARY.md`, `GITHUB_DEPLOYMENT_GUIDE.md`)
4. The `tests/` directory
5. `.gitignore` file
