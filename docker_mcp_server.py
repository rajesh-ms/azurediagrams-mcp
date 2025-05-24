#!/usr/bin/env python3
"""
Docker-compatible MCP Server for Azure Diagram Generation

This server wraps the MCP functionality in a simple HTTP server for Docker deployment.
It provides REST endpoints that can be called from VS Code or other clients.
"""

import json
import logging
import os
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import subprocess
import tempfile
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"Loaded environment from {env_path}")
    else:
        logger.warning("No .env file found")
except ImportError:
    logger.warning("python-dotenv not available, using system environment variables")

# Import the MCP server logic
try:
    from azure_diagram_server import app as mcp_app, AzureDiagramGenerator
    logger.info("MCP server logic imported successfully")
except ImportError as e:
    logger.error(f"Failed to import MCP server: {e}")
    raise SystemExit("Cannot run without MCP server module")

# Create FastAPI app
app = FastAPI(
    title="Azure Diagram Generator MCP Server",
    description="HTTP wrapper for MCP server functionality",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for requests
class DiagramRequest(BaseModel):
    description: str
    output_format: Optional[str] = "png"
    include_title: Optional[bool] = True

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any]

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy", "message": "MCP server is running"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with server info"""
    return {
        "name": "Azure Diagram Generator MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/health": "Health check",
            "/generate-diagram": "Generate Azure architecture diagram",
            "/mcp": "MCP protocol endpoint",
            "/docs": "API documentation"
        }
    }

# Generate diagram endpoint
@app.post("/generate-diagram")
async def generate_diagram_endpoint(request: DiagramRequest):
    """Generate an Azure architecture diagram from natural language description"""
    try:
        logger.info(f"Generating diagram for: {request.description}")
        
        # Create generator instance
        generator = AzureDiagramGenerator()
        
        # Process text with NLP to get structured JSON
        json_data = await generator.process_text_with_nlp(request.description)
        
        # Generate diagram from JSON
        diagram_bytes = generator.generate_diagram_from_json(
            json_data, 
            request.output_format, 
            "TB"  # Default layout direction
        )
        
        # Convert bytes to base64 for JSON response
        import base64
        diagram_base64 = base64.b64encode(diagram_bytes).decode('utf-8')
        
        return {
            "success": True,
            "result": {
                "diagram_base64": diagram_base64,
                "format": request.output_format,
                "size_bytes": len(diagram_bytes),
                "json_data": json_data
            },
            "message": "Diagram generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error generating diagram: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP protocol endpoint for direct MCP communication
@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """Handle MCP protocol requests"""
    try:
        logger.info(f"Handling MCP request: {request.method}")
        
        # Handle different MCP methods
        if request.method == "tools/list":
            return {
                "tools": [
                    {
                        "name": "generate_azure_diagram",
                        "description": "Generate Azure architecture diagrams from natural language descriptions",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string",
                                    "description": "Natural language description of the Azure architecture"
                                },
                                "output_format": {
                                    "type": "string",
                                    "enum": ["png", "svg", "pdf"],
                                    "default": "png",
                                    "description": "Output format for the diagram"
                                },
                                "include_title": {
                                    "type": "boolean",
                                    "default": True,
                                    "description": "Whether to include a title in the diagram"
                                }
                            },
                            "required": ["description"]
                        }
                    }
                ]            }
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            if tool_name == "generate_azure_diagram":
                arguments = request.params.get("arguments", {})
                
                # Create generator instance and process
                generator = AzureDiagramGenerator()
                
                # Get description from arguments
                description = arguments.get("architecture_description", arguments.get("description", ""))
                output_format = arguments.get("output_format", "png")
                
                # Process text with NLP to get structured JSON
                json_data = await generator.process_text_with_nlp(description)
                
                # Generate diagram from JSON
                diagram_bytes = generator.generate_diagram_from_json(json_data, output_format)
                
                # Convert to base64
                import base64
                diagram_base64 = base64.b64encode(diagram_bytes).decode('utf-8')
                
                result = {
                    "diagram_base64": diagram_base64,
                    "format": output_format,
                    "size_bytes": len(diagram_bytes),
                    "json_data": json_data
                }
                
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            else:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown MCP method: {request.method}")
            
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Test endpoint
@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify server functionality"""
    try:
        # Test a simple diagram generation
        generator = AzureDiagramGenerator()
        
        # Process description
        description = "A simple web app with a database"
        json_data = await generator.process_text_with_nlp(description)
        
        # Generate diagram
        diagram_bytes = generator.generate_diagram_from_json(json_data, "png")
        
        return {
            "test": "passed",
            "message": "Diagram generation test successful",
            "result": {
                "size_bytes": len(diagram_bytes),
                "json_data": json_data,
                "description": description
            }
        }
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return {
            "test": "failed",
            "message": str(e)
        }

def main():
    """Main function to run the server"""
    logger.info("Starting Docker MCP Server...")
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Server will run on {host}:{port}")
    
    # Run the server
    uvicorn.run(
        "docker_mcp_server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )

if __name__ == "__main__":
    main()
