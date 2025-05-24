#!/usr/bin/env python3
"""
Validation script for Azure Diagram Generator MCP Server
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from azure_diagram_server import AzureDiagramGenerator, app

async def test_nlp_processing():
    """Test the NLP processing component"""
    print("🧠 Testing NLP Processing...")
    
    generator = AzureDiagramGenerator()
    
    test_descriptions = [
        "Create a web application with SQL database and storage account",
        "Deploy a microservices architecture with function apps, cosmos db, and service bus",
        "Set up a machine learning pipeline with storage, compute, and key vault"
    ]
    
    for i, description in enumerate(test_descriptions, 1):
        print(f"\n📝 Test {i}: {description}")
        try:
            result = await generator.process_text_with_nlp(description)
            print(f"✅ NLP Result: {len(result.get('resources', []))} resources found")
            print(f"   Resources: {[r['name'] for r in result.get('resources', [])]}")
        except Exception as e:
            print(f"❌ NLP Error: {e}")

async def test_diagram_generation():
    """Test the diagram generation component"""
    print("\n🎨 Testing Diagram Generation...")
    
    generator = AzureDiagramGenerator()
    
    # Test with a sample JSON structure
    test_json = {
        "diagram_label": "Test Architecture",
        "resources": [
            {
                "name": "Web App",
                "type": "Azure.WebApp",
                "attributes": {"location": "East US", "sku": "S1"}
            },
            {
                "name": "SQL Database",
                "type": "Azure.SQLDatabase", 
                "attributes": {"location": "East US", "sku": "S2"}
            }
        ],
        "relationships": [
            {
                "source": "Web App",
                "target": "SQL Database",
                "type": "connects_to"
            }
        ],
        "clusters": [
            {
                "name": "Resource Group",
                "resources": ["Web App", "SQL Database"]
            }
        ]
    }
    
    formats = ["png", "svg"]
    for fmt in formats:
        print(f"\n📊 Testing {fmt.upper()} generation...")
        try:
            diagram_bytes = generator.generate_diagram_from_json(test_json, fmt)
            print(f"✅ Generated {fmt.upper()}: {len(diagram_bytes)} bytes")
            
            # Save test diagram
            output_path = f"test_diagram.{fmt}"
            with open(output_path, "wb") as f:
                f.write(diagram_bytes)
            print(f"💾 Saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ Diagram Error: {e}")

async def test_mcp_tool():
    """Test the MCP tool directly"""
    print("\n🔧 Testing MCP Tool...")
    
    test_descriptions = [
        "Simple web app with database",
        "Microservices with API gateway and multiple services"
    ]
    
    for i, description in enumerate(test_descriptions, 1):
        print(f"\n🧪 MCP Test {i}: {description}")
        try:
            # Get the tool function
            tool_func = app._tools["generate_azure_diagram_from_text"]
            
            # Call the tool
            result = await tool_func(
                architecture_description=description,
                output_format="png",
                layout_direction="TB"
            )
            
            print(f"✅ MCP Tool Success: Generated {result.format} image ({len(result.data)} bytes)")
            
            # Save result
            output_path = f"mcp_test_{i}.{result.format}"
            with open(output_path, "wb") as f:
                f.write(result.data)
            print(f"💾 Saved to: {output_path}")
            
        except Exception as e:
            print(f"❌ MCP Tool Error: {e}")

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking Dependencies...")
    
    dependencies = [
        ("FastMCP", "mcp.server.fastmcp"),
        ("Requests", "requests"),
        ("Diagrams", "diagrams"),
        ("JSON", "json"),
        ("Tempfile", "tempfile")
    ]
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}: Available")
        except ImportError:
            print(f"❌ {name}: Missing")

def check_environment():
    """Check environment configuration"""
    print("\n🌍 Checking Environment...")
    
    env_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            display_value = value if "KEY" not in var else f"{value[:8]}***"
            print(f"✅ {var}: {display_value}")
        else:
            print(f"⚠️  {var}: Not set (will use mock processing)")

async def main():
    """Run all validation tests"""
    print("🚀 Azure Diagram Generator MCP Server Validation")
    print("=" * 50)
    
    # Check dependencies and environment
    check_dependencies()
    check_environment()
    
    # Run tests
    try:
        await test_nlp_processing()
        await test_diagram_generation()
        await test_mcp_tool()
        
        print("\n" + "=" * 50)
        print("🎉 Validation Complete!")
        print("\n📋 Summary:")
        print("- NLP processing tested")
        print("- Diagram generation tested") 
        print("- MCP tool integration tested")
        print("- Check generated test files for visual verification")
        
    except Exception as e:
        print(f"\n💥 Validation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
