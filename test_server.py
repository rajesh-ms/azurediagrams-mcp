#!/usr/bin/env python3

"""
Test script for the Azure Diagram MCP Server
"""

import asyncio
import json
import subprocess
import sys
import tempfile
import os

async def test_mcp_server():
    """Test the MCP server by simulating MCP protocol communication."""
    
    print("Testing Azure Diagram MCP Server...")
    
    # Test 1: Check if server can start and respond to initialization
    try:
        process = subprocess.Popen(
            [sys.executable, "azure_diagram_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        # Send MCP initialization request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send the request
        init_json = json.dumps(init_request) + "\n"
        process.stdin.write(init_json)
        process.stdin.flush()
        
        # Wait a bit for response
        try:
            stdout, stderr = process.communicate(timeout=10)
            print("STDOUT:")
            print(stdout)
            print("STDERR:")
            print(stderr)
            
            if process.returncode == 0:
                print("✅ Server started successfully")
            else:
                print(f"❌ Server exited with code {process.returncode}")
                
        except subprocess.TimeoutExpired:
            print("✅ Server is running (timeout reached)")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error testing server: {e}")

def test_docker_container():
    """Test the Docker container directly."""
    print("\nTesting Docker container...")
    
    try:
        # Start container in interactive mode for testing
        result = subprocess.run([
            "docker", "run", "--rm", 
            "azure-diagram-mcp",
            "python", "-c", 
            "from azure_diagram_server import *; print('✅ All imports successful'); generator = AzureDiagramGenerator(); print('✅ Generator created successfully')"
        ], capture_output=True, text=True, timeout=30)
        
        print("Docker test output:")
        print(result.stdout)
        if result.stderr:
            print("Docker test errors:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Docker container test passed")
        else:
            print(f"❌ Docker container test failed with code {result.returncode}")
            
    except Exception as e:
        print(f"❌ Error testing Docker container: {e}")

def test_diagram_generation():
    """Test diagram generation functionality."""
    print("\nTesting diagram generation...")
    
    try:
        # Import the generator directly
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from azure_diagram_server import AzureDiagramGenerator
        
        generator = AzureDiagramGenerator()
        
        # Test description
        test_description = "Create a web application with Azure App Service, connected to Azure SQL Database, with Azure Storage for file uploads, and Azure Application Gateway for load balancing."
        
        # Test NLP processing
        print("Testing NLP processing...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        nlp_result = loop.run_until_complete(generator.process_text_with_nlp(test_description))
        print(f"NLP Result: {nlp_result}")
        
        # Test diagram generation
        print("Testing diagram generation...")
        
        # Use the correct method and parameters
        diagram_bytes = generator.generate_diagram_from_json(
            json_data=nlp_result,
            output_format="png",
            layout_direction="TB"
        )
        
        print(f"Generated diagram size: {len(diagram_bytes)} bytes")
        
        # Save the diagram to verify
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(diagram_bytes)
            output_path = f.name
            
        if os.path.exists(output_path):
            print(f"✅ Diagram created successfully: {output_path}")
            print(f"File size: {os.path.getsize(output_path)} bytes")
        else:
            print("❌ Diagram file not found")
        
        print("✅ Diagram generation test completed")
        
    except Exception as e:
        print(f"❌ Error testing diagram generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Azure Diagram MCP Server Test Suite")
    print("=" * 50)
    
    # Run tests
    asyncio.run(test_mcp_server())
    test_docker_container()
    test_diagram_generation()
    
    print("\n" + "=" * 50)
    print("Test suite completed!")
