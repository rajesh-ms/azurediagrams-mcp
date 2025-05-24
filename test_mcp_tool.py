#!/usr/bin/env python3
"""
Test script for MCP tool functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from azure_diagram_server import generate_azure_diagram_from_text

async def test_mcp_tool():
    """Test the MCP tool directly"""
    print("🔧 Testing MCP Tool Directly...")
    
    test_cases = [
        {
            "description": "Simple web app with database",
            "format": "png"
        },
        {
            "description": "Microservices with API gateway and multiple services",
            "format": "svg"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 MCP Test {i}: {test_case['description']}")
        try:
            # Call the MCP tool function directly
            result = await generate_azure_diagram_from_text(
                architecture_description=test_case["description"],
                output_format=test_case["format"],
                layout_direction="TB"
            )
            
            print(f"✅ MCP Tool Success: Generated {test_case['format']} image ({len(result.data)} bytes)")
            
            # Save result
            output_path = f"mcp_tool_test_{i}.{test_case['format']}"
            with open(output_path, "wb") as f:
                f.write(result.data)
            print(f"💾 Saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ MCP Tool Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_tool())
