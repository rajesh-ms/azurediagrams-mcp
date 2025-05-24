---
applyTo: '**'
---
Coding standards, domain knowledge, and preferences that AI should follow.
An MCP server using FastMCP python library that generates azure architecture diagram using "pip install rsaz-diagrams". This server has following components:
- A conceptual NLP component that uses the Azure OpenAI API to understand the text and convert it into a structured JSON format. 
  The prompt used in NLP component should guide LLM to:
    - Identify Azure services, their names, and relevant attributes.
    - Recognize relationships between these services.
    - Understand grouping or clustering (e.g., resources within a resource group or subnet).
    - Output the extracted information in a predefined structured JSON format.
      The JSON format should include:
      {
        "diagram_label": "My Web App Architecture",
        "resources":,
        "relationships":,
        "clusters":
          }
        ]
      }
        example JSON output:
        {
            "diagram_label": "My Web App Architecture",
            "resources": [
                {
                "name": "Web App",
                "type": "Azure.WebApp",
                "attributes": {
                    "location": "East US",
                    "sku": "S1"
                }
                },
                {
                "name": "SQL Database",
                "type": "Azure.SQLDatabase",
                "attributes": {
                    "location": "East US",
                    "sku": "S2"
                }
                }
          "resources": [
            {
              "name": "Web App",
              "type": "Azure.WebApp",
              "attributes": {
                "location": "East US",
                "sku": "S1"
              }
            },
            {
              "name": "SQL Database",
              "type": "Azure.SQLDatabase",
              "attributes": {
                "location": "East US",
                "sku": "S2"
              }
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
              "name": "Resource Group 1",
              "resources": ["Web App", "SQL Database"]
            }
          ]
        }
A diagramming engine that takes this JSON, maps it to diagrams library components, and generates an image. The diagram should be created based on following features:
- generate_diagram_from_json takes the structured JSON from the NLP step.
- It uses the AZURE_NODE_MAP to find the corresponding diagrams library (rsaz-diagrams) class for each resource type.
- It creates nodes, clusters (if specified in the JSON), and relationships (edges) between them.
- It attempts to render the diagram directly to bytes using the graphviz Python library. If this library isn't installed, it falls back to letting diagrams save to a temporary file, then reads and deletes that file.
- CRITICAL DEPENDENCY: The diagrams library relies on Graphviz being installed on the system where this server runs. This is not a Python library but a separate software package. Ensure it's installed and its bin directory is in your system's PATH.
- Each resource should be represented as a node in the diagram.
- Relationships should be represented as edges connecting the nodes.
- Clusters should be represented as groups of nodes, with a label indicating the cluster name.
- The diagram should be visually appealing, with appropriate spacing and alignment.
- The diagram should be exportable in common formats (e.g., PNG, SVG).
- The diagram should be responsive to different screen sizes.
- The diagram should be interactive, allowing users to hover over nodes for more information.
- The diagram should support zooming and panning.

The MCP tool (generate_azure_diagram_from_text) will expose this functionality, taking text input and returning a diagram image with the following features:
- This mcp server is deployed as docker container.
- It takes the architecture_description (string), output_format (string, e.g., "png", "svg", default "png"), and layout_direction (string, e.g., "TB", "LR", default "TB").
- It orchestrates the call to the NLP engine and then the diagramming engine.
- It returns an mcp.server.fastmcp.Image object containing the diagram image bytes and format.

Running the Server:
- Save the code as a Python file (e.g., azure_diagram_server.py).
- Install necessary Python libraries:
```bash
pip install "mcp[server]" diagrams requests graphviz
```
(Note: graphviz here is the Python client library; the Graphviz software itself needs separate installation).
Run the server from your terminal:
```bash
python azure_diagram_server.py
```
The server will then be available for MCP clients to connect to and use the generate_azure_diagram_from_text tool.

