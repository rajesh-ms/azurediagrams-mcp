#!/usr/bin/env python3
"""
Simple test script for Azure Diagram Generator MCP Server
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from azure_diagram_server import AzureDiagramGenerator

async def test_simple_generation():
    """Test simple diagram generation"""
    print("🔧 Testing Simple Diagram Generation...")
    
    generator = AzureDiagramGenerator()
    
    # Test with a simple architecture description
    description = "Create a web application with SQL database"
    
    try:
        print(f"📝 Processing: {description}")
        
        # Step 1: Test NLP processing
        json_data = await generator.process_text_with_nlp(description)
        print(f"✅ NLP Result: {json_data}")
        
        # Step 2: Test diagram generation with PNG
        try:
            diagram_bytes = generator.generate_diagram_from_json(json_data, "png")
            print(f"✅ PNG Generation: {len(diagram_bytes)} bytes")
            
            if len(diagram_bytes) > 0:
                with open("simple_test.png", "wb") as f:
                    f.write(diagram_bytes)
                print("💾 Saved PNG diagram as simple_test.png")
            else:
                print("⚠️ PNG diagram is empty")
                
        except Exception as e:
            print(f"❌ PNG Generation Error: {e}")
        
        # Step 3: Test diagram generation with SVG  
        try:
            diagram_bytes = generator.generate_diagram_from_json(json_data, "svg")
            print(f"✅ SVG Generation: {len(diagram_bytes)} bytes")
            
            if len(diagram_bytes) > 0:
                with open("simple_test.svg", "wb") as f:
                    f.write(diagram_bytes)
                print("💾 Saved SVG diagram as simple_test.svg")
            else:
                print("⚠️ SVG diagram is empty")
                
        except Exception as e:
            print(f"❌ SVG Generation Error: {e}")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple_generation())
