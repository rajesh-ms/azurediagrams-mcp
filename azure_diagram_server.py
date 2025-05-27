"""
Azure Architecture Diagram Generator MCP Server

This MCP server generates Azure architecture diagrams from natural language descriptions
using the FastMCP library and diagrams package.
"""

import json
import logging
import os
import tempfile
from typing import Dict, Any
from pathlib import Path

# Set up logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
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

# Try to import required packages with proper error handling
try:
    import mcp.server.fastmcp as fastmcp
    from mcp.server.fastmcp import FastMCP
    logger.info("FastMCP imported successfully")
except ImportError as e:
    logger.error(f"Failed to import FastMCP: {e}")
    logger.error("Install with: pip install 'mcp[server]'")
    raise SystemExit("Cannot run without FastMCP")

try:
    import requests
    logger.info("Requests imported successfully")
except ImportError as e:
    logger.error(f"Failed to import requests: {e}")
    logger.error("Install with: pip install requests")
    raise SystemExit("Cannot run without requests")

# Try to import diagrams with fallback
DIAGRAMS_AVAILABLE = False
try:
    from diagrams import Diagram, Cluster
    from diagrams.azure.compute import AppServices, FunctionApps, VM as VirtualMachines
    from diagrams.azure.database import SQLDatabases, CosmosDb
    from diagrams.azure.storage import StorageAccounts, BlobStorage
    from diagrams.azure.network import LoadBalancers, ApplicationGateway, VirtualNetworks
    from diagrams.azure.web import AppServices as WebApps
    from diagrams.azure.analytics import LogAnalyticsWorkspaces
    from diagrams.azure.security import KeyVaults
    from diagrams.azure.integration import AzureServiceBus as ServiceBus
    try:
        from diagrams.azure.ml import MachineLearningServiceWorkspaces as MachineLearningServices
    except ImportError:
        from diagrams.azure.ml import CognitiveServices as MachineLearningServices
    DIAGRAMS_AVAILABLE = True
    logger.info("Diagrams library imported successfully")
except ImportError as e:
    logger.warning(f"Diagrams library not available: {e}")
    logger.warning("Install with: pip install diagrams")
    logger.warning("Also install Graphviz system package")
    
    # Create mock classes for fallback when diagrams is not available
    class MockNode:
        def __init__(self, label="MockNode"): 
            self.label = label
        def __rshift__(self, other): 
            return self
        def __lshift__(self, other):
            return self
      # Mock all the Azure node types
    AppServices = FunctionApps = VirtualMachines = MockNode
    SQLDatabases = CosmosDb = MockNode
    StorageAccounts = BlobStorage = MockNode
    LoadBalancers = ApplicationGateway = VirtualNetworks = MockNode
    WebApps = LogAnalyticsWorkspaces = KeyVaults = MockNode
    ServiceBus = MachineLearningServices = MockNode
    
    class MockDiagram:
        def __init__(self, *args, **kwargs): 
            self.nodes = []
        def __enter__(self): 
            return self
        def __exit__(self, *args): 
            pass
    
    class MockCluster:
        def __init__(self, name="MockCluster", **kwargs): 
            self.name = name
        def __enter__(self): 
            return self
        def __exit__(self, *args): 
            pass
    
    Diagram = MockDiagram
    Cluster = MockCluster

# Create generic fallback classes for when specific Azure nodes aren't available
class GenericCompute:
    def __init__(self, label="Generic Compute"): 
        self.label = label
    def __rshift__(self, other): 
        return self
    def __lshift__(self, other):
        return self

class GenericDatabase:
    def __init__(self, label="Generic Database"): 
        self.label = label
    def __rshift__(self, other): 
        return self
    def __lshift__(self, other):
        return self

class GenericStorage:
    def __init__(self, label="Generic Storage"): 
        self.label = label
    def __rshift__(self, other): 
        return self
    def __lshift__(self, other):
        return self

# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

# Try to import OpenAI client
OPENAI_AVAILABLE = False
try:
    from openai import AzureOpenAI
    OPENAI_AVAILABLE = True
    logger.info("OpenAI client library imported successfully")
except ImportError:
    logger.warning("OpenAI client library not available, using requests fallback")
    AzureOpenAI = None

# Azure resource type mapping to diagrams components
AZURE_NODE_MAP = {
    "Azure.WebApp": AppServices,
    "Azure.FunctionApp": FunctionApps,
    "Azure.VirtualMachine": VirtualMachines,
    "Azure.SQLDatabase": SQLDatabases,
    "Azure.CosmosDB": CosmosDb,
    "Azure.StorageAccount": StorageAccounts,
    "Azure.BlobStorage": BlobStorage,
    "Azure.LoadBalancer": LoadBalancers,
    "Azure.ApplicationGateway": ApplicationGateway,
    "Azure.VirtualNetwork": VirtualNetworks,
    "Azure.KeyVault": KeyVaults,
    "Azure.ServiceBus": ServiceBus,
    "Azure.LogAnalytics": LogAnalyticsWorkspaces,
    "Azure.MachineLearning": MachineLearningServices,
    # Generic fallbacks
    "Azure.Generic": GenericCompute,
}

class AzureDiagramGenerator:
    """Main class for generating Azure architecture diagrams."""
    
    def __init__(self):
        self.check_azure_openai_config()
    
    def check_azure_openai_config(self):
        """Check if Azure OpenAI configuration is available."""
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
            logger.warning("Azure OpenAI configuration not found. Using mock NLP processing.")
    
    async def process_text_with_nlp(self, architecture_description: str) -> Dict[str, Any]:
        """
        Process natural language description using Azure OpenAI to extract structured information.
        """
        if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_API_KEY:
            logger.info("Using mock NLP processing due to missing Azure OpenAI configuration")
            return self._mock_nlp_processing(architecture_description)
        
        prompt = self._create_nlp_prompt(architecture_description)
        
        # Try OpenAI client first
        if OPENAI_AVAILABLE:
            try:
                return await self._process_with_openai_client(prompt)
            except Exception as e:
                logger.error(f"Error with OpenAI client: {e}")
                logger.info("Falling back to requests method")
        
        # Fallback to requests method
        try:
            return await self._process_with_requests(prompt)
        except Exception as e:
            logger.error(f"Error processing with Azure OpenAI (requests): {e}")
            logger.info("Falling back to mock NLP processing")
            return self._mock_nlp_processing(architecture_description)
    
    async def _process_with_openai_client(self, prompt: str) -> Dict[str, Any]:
        """Process with OpenAI client library."""
        client = AzureOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION
        )
        
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Azure architect. Parse the given architecture description and return ONLY valid JSON according to the specified format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.1,
            top_p=0.1
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean the response to extract JSON
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        parsed_json = json.loads(content)
        logger.info("Successfully processed architecture description with Azure OpenAI (client)")
        return parsed_json
    
    async def _process_with_requests(self, prompt: str) -> Dict[str, Any]:
        """Process with requests library as fallback."""
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Azure architect. Parse the given architecture description and return ONLY valid JSON according to the specified format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.1,
            "top_p": 0.1
        }
        
        url = f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        # Enhanced error handling
        if response.status_code == 400:
            logger.error(f"Azure OpenAI 400 error. URL: {url}")
            logger.error(f"Response: {response.text}")
            raise Exception(f"Azure OpenAI API error (400): {response.text}")
        elif response.status_code == 401:
            raise Exception("Azure OpenAI authentication failed. Check your API key.")
        elif response.status_code == 404:
            raise Exception(f"Azure OpenAI deployment '{AZURE_OPENAI_DEPLOYMENT}' not found. Check deployment name.")
        
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # Clean the response to extract JSON
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        parsed_json = json.loads(content)
        logger.info("Successfully processed architecture description with Azure OpenAI (requests)")
        return parsed_json
    
    def _create_nlp_prompt(self, description: str) -> str:
        """Create the prompt for Azure OpenAI to process the architecture description."""
        return f"""
Parse the following Azure architecture description and extract structured information.

Architecture Description: "{description}"

Return the information in this exact JSON format:
{{
  "diagram_label": "Architecture Name",
  "resources": [
    {{
      "name": "Resource Name",
      "type": "Azure.ResourceType",
      "attributes": {{
        "location": "Azure Region",
        "sku": "SKU or Size"
      }}
    }}
  ],
  "relationships": [
    {{
      "source": "Source Resource Name",
      "target": "Target Resource Name",
      "type": "connects_to"
    }}
  ],
  "clusters": [
    {{
      "name": "Cluster Name",
      "resources": ["Resource1", "Resource2"]
    }}
  ]
}}

Guidelines:
- Identify Azure services and map them to appropriate Azure.* types (e.g., Azure.WebApp, Azure.SQLDatabase, Azure.StorageAccount)
- Extract relationships between services (connections, dependencies)
- Group related resources into clusters (resource groups, subnets, etc.)
- Use descriptive names for resources
- Include relevant attributes like location and SKU when mentioned

Return ONLY the JSON, no additional text or explanation.
"""
    
    def _mock_nlp_processing(self, description: str) -> Dict[str, Any]:
        """Mock NLP processing for when Azure OpenAI is not available."""
        logger.info("Using mock NLP processing")
        
        # Simple keyword-based extraction for demonstration
        resources = []
        relationships = []
        clusters = []
        
        # Basic keyword mapping
        if "web app" in description.lower() or "webapp" in description.lower():
            resources.append({
                "name": "Web Application",
                "type": "Azure.WebApp",
                "attributes": {"location": "East US", "sku": "S1"}
            })
        
        if "database" in description.lower() or "sql" in description.lower():
            resources.append({
                "name": "SQL Database",
                "type": "Azure.SQLDatabase",
                "attributes": {"location": "East US", "sku": "S2"}
            })
        
        if "storage" in description.lower():
            resources.append({
                "name": "Storage Account",
                "type": "Azure.StorageAccount",
                "attributes": {"location": "East US", "sku": "Standard_LRS"}
            })
        
        if "function" in description.lower():
            resources.append({
                "name": "Function App",
                "type": "Azure.FunctionApp",
                "attributes": {"location": "East US", "sku": "Consumption"}
            })
        
        # Create relationships if we have multiple resources
        if len(resources) > 1:
            for i in range(len(resources) - 1):
                relationships.append({
                    "source": resources[i]["name"],
                    "target": resources[i + 1]["name"],
                    "type": "connects_to"
                })
        
        # Create a default cluster if we have resources
        if resources:
            clusters.append({
                "name": "Resource Group",
                "resources": [r["name"] for r in resources]
            })
        
        return {
            "diagram_label": "Mock Architecture Diagram",
            "resources": resources,
            "relationships": relationships,
            "clusters": clusters
        }
    
    def generate_diagram_from_json(self, 
                                 json_data: Dict[str, Any],
                                 output_format: str = "png",
                                 layout_direction: str = "TB") -> bytes:
        """
        Generate diagram from structured JSON data.
        """
        try:
            diagram_label = json_data.get("diagram_label", "Azure Architecture")
            resources = json_data.get("resources", [])
            relationships = json_data.get("relationships", [])
            clusters = json_data.get("clusters", [])
            
            # Create temporary file for diagram output
            with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as tmp_file:
                tmp_path = tmp_file.name
            
            # Remove extension from path as diagrams adds it automatically
            tmp_path_no_ext = tmp_path.rsplit('.', 1)[0]
              # Set diagram direction
            direction = "TB" if layout_direction == "TB" else "LR"
            
            # The diagrams library determines format from the filename extension
            # So we don't pass format as a parameter
            with Diagram(diagram_label, filename=tmp_path_no_ext, direction=direction, show=False, outformat=output_format):
                # Create nodes mapping
                nodes = {}
                
                # Process clusters first
                cluster_nodes = {}
                for cluster in clusters:
                    cluster_name = cluster.get("name", "Cluster")
                    cluster_resources = cluster.get("resources", [])
                    
                    with Cluster(cluster_name):
                        for resource in resources:
                            if resource["name"] in cluster_resources:
                                node_class = AZURE_NODE_MAP.get(resource["type"], AZURE_NODE_MAP["Azure.Generic"])
                                node = node_class(resource["name"])
                                nodes[resource["name"]] = node
                                cluster_nodes[resource["name"]] = node
                
                # Create remaining nodes (not in clusters)
                for resource in resources:
                    if resource["name"] not in cluster_nodes:
                        node_class = AZURE_NODE_MAP.get(resource["type"], AZURE_NODE_MAP["Azure.Generic"])
                        node = node_class(resource["name"])
                        nodes[resource["name"]] = node
                
                # Create relationships (edges)
                for relationship in relationships:
                    source_name = relationship.get("source")
                    target_name = relationship.get("target")
                    
                    if source_name in nodes and target_name in nodes:
                        source_node = nodes[source_name]
                        target_node = nodes[target_name]
                        
                        # Create edge between nodes
                        source_node >> target_node
            
            # Read the generated file
            actual_file_path = f"{tmp_path_no_ext}.{output_format}"
            
            try:
                with open(actual_file_path, "rb") as f:
                    diagram_bytes = f.read()
                
                # Clean up temporary file
                os.unlink(actual_file_path)
                
                logger.info(f"Successfully generated {output_format} diagram with {len(resources)} resources")
                return diagram_bytes
                
            except FileNotFoundError:
                # Try alternative file path
                if os.path.exists(tmp_path):
                    with open(tmp_path, "rb") as f:
                        diagram_bytes = f.read()
                    os.unlink(tmp_path)
                    return diagram_bytes
                else:
                    raise Exception(f"Generated diagram file not found at expected location")
            
        except Exception as e:
            logger.error(f"Error generating diagram: {e}")
            raise

# Initialize FastMCP server
app = FastMCP("Azure Diagram Generator")

# Initialize diagram generator
diagram_generator = AzureDiagramGenerator()

@app.tool()
async def generate_azure_diagram_from_text(
    architecture_description: str,
    output_format: str = "png",
    layout_direction: str = "TB"
) -> fastmcp.Image:
    """
    Generate an Azure architecture diagram from a natural language description.
    
    Args:
        architecture_description: Natural language description of the Azure architecture
        output_format: Output format for the diagram (png, svg). Default: png
        layout_direction: Layout direction (TB for top-bottom, LR for left-right). Default: TB
    
    Returns:
        Image object containing the generated diagram
    """
    try:
        logger.info(f"Processing architecture description: {architecture_description[:100]}...")
        
        # Step 1: Process text with NLP to get structured JSON
        json_data = await diagram_generator.process_text_with_nlp(architecture_description)
        
        # Step 2: Generate diagram from JSON
        diagram_bytes = diagram_generator.generate_diagram_from_json(
            json_data, output_format, layout_direction
        )
        
        # Step 3: Return as FastMCP Image
        return fastmcp.Image(
            data=diagram_bytes,
            format=output_format
        )
        
    except Exception as e:
        logger.error(f"Error generating Azure diagram: {e}")
        raise Exception(f"Failed to generate diagram: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Azure Diagram Generator MCP Server...")
    logger.info("Available Azure resource types in node map:")
    for resource_type in AZURE_NODE_MAP.keys():
        logger.info("  - " + resource_type)
    
    # Run the FastMCP server using stdio
    app.run()
