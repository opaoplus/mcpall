# MCPALL

<div align="center">

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![MCP](https://img.shields.io/badge/MCP-1.6.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

<div align="center">
  
[中文](../../readme.md) | [English](./readme_en.md) | [日本語](./readme_jp.md) | [한국어](./readme_kr.md)

</div>

## 📑 Project Overview

MCPALL is a multi-functional service collection platform based on the Model Context Protocol (MCP), supporting rapid development and integration of various MCP services. The platform is designed to be highly modular, allowing easy extension with new service modules.

## 🚀 Current Modules

| Module Name | Description | Details Link |
|-------------|-------------|--------------|
| 📞 **useronlie** | User phone query service | [View Details](../../useronlie/README.md) |
| 📚 **xmol** | Literature retrieval and Q&A system | [View Details](../../xmol/README.md) |

## 🛠️ Technology Stack

- **Python 3.11+**: Core development language
- **FastMCP**: MCP protocol implementation framework
- **Communication Protocol**: Supports both HTTP/SSE and STDIO transport methods

## ⚙️ General Development Guide

### Install Base Environment

```bash
# Ensure Python 3.11+ is installed
python --version

# Install MCP framework
pip install "mcp[cli]>=1.6.0"

# Recommended to use uv as dependency management tool
pip install uv
```

### Module Structure Standard

Each new module should follow this basic structure:

```
module_name/
├── core/               # Core functionality implementation
│   ├── __init__.py
│   ├── server.py       # MCP server implementation
│   └── ...             # Other functional modules
├── README.md           # Detailed module documentation
├── run.py              # Startup script
├── pyproject.toml      # Project configuration
└── ...                 # Other configuration files
```

### Steps to Develop a New Module

1. **Create module directory structure**
   ```bash
   mkdir -p new_module/core
   touch new_module/{README.md,run.py,pyproject.toml}
   touch new_module/core/{__init__.py,server.py}
   ```

2. **Implement MCP server**
   ```python
   # new_module/core/server.py (basic framework)
   from fastmcp import McpServer, Tool, Resource

   class NewModuleServer(McpServer):
       def __init__(self):
           super().__init__("New Module Name")
           # Register tools and resources
           self.register_tool(Tool("tool_name", self.tool_handler))
           self.register_resource("resource://path", self.resource_handler)
   
       async def tool_handler(self, params):
           # Implement tool logic
           return {"result": "Tool execution result"}
   
       async def resource_handler(self, params):
           # Implement resource access logic
           return {"data": "Resource content"}
   ```

3. **Create startup script**
   ```python
   # new_module/run.py
   import asyncio
   import argparse
   from core.server import NewModuleServer
   
   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
       parser.add_argument("--host", default="127.0.0.1")
       parser.add_argument("--port", type=int, default=8000)
       args = parser.parse_args()
   
       server = NewModuleServer()
       
       if args.transport == "stdio":
           asyncio.run(server.run_stdio())
       else:
           asyncio.run(server.run_sse(host=args.host, port=args.port))
   
   if __name__ == "__main__":
       main()
   ```

4. **Configure project dependencies**
   ```toml
   # new_module/pyproject.toml
   [build-system]
   requires = ["setuptools>=61.0"]
   build-backend = "setuptools.build_meta"
   
   [project]
   name = "new_module"
   version = "0.1.0"
   requires-python = ">=3.11"
   dependencies = [
       "mcp>=1.6.0",
   ]
   ```

5. **Write module README**
   Each module should have its own README file, detailing the module's functionality, configuration, and usage instructions.

## 🚀 General Running Method

All modules support two running modes:

```bash
# STDIO mode (suitable for direct integration with Claude Desktop)
cd <module_name>
uv run run.py

# SSE mode (runs as an HTTP service)
cd <module_name>
uv run run.py --transport sse --host 127.0.0.1 --port 8000
```

## 🐳 Docker Deployment

The project supports deployment and running using Docker, facilitating quick deployment and isolated operation in different environments.

### Using Docker Compose (Recommended)

```bash
# Build all services
docker-compose build

# Start a specific service (e.g., useronlie module in SSE mode)
docker-compose up useronlie-sse

# Run service in background
docker-compose up -d useronlie-sse
```

For detailed Docker deployment instructions, please refer to the [Docker Deployment Guide](../../docker-usage.md).

## 🏗️ Integration with Claude

1. Configure Claude Desktop (`%AppData%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "<service_name>": {
      "isActive": true,
      "name": "<display_name>",
      "url": "http://localhost:<port>/sse"
    }
  }
}
```

2. Restart Claude Desktop application to apply the configuration

## 🔧 Extension Ecosystem

MCPALL is designed as an infinitely expandable service ecosystem. Here are some potential extension directions:

- **Data Processing Services**: Data analysis, visualization, report generation
- **AI Assistance Tools**: Text generation, image processing, speech recognition
- **Development Toolchain**: Code generation, project management, test automation
- **Knowledge Base Services**: Document retrieval, knowledge graphs, Q&A systems
- **Operations Monitoring**: System status, performance monitoring, log analysis

To add your service to the MCPALL platform, simply follow the development standards above and add the module directory to the project root.

## 📋 Core Concepts of MCP Service Development

### Tools

Tools are callable functions provided by the MCP service for performing specific tasks.

```python
# Tool definition example
@server.tool("tool_name")
async def tool_handler(params):
    # Parameter processing and business logic
    return {"result": "Processing result"}
```

### Resources

Resources are data access points provided by the MCP service, identified by URI.

```python
# Resource definition example
@server.resource("resource://path")
async def resource_handler(params):
    # Resource access logic
    return {"data": "Resource content"}
```

### Resource Schema

Through schema definitions, you can declare the structure and validation rules of resources.

```python
# Resource schema example
resource_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "data": {"type": "array", "items": {"type": "string"}}
    }
}
```

For more development details, please refer to the [MCP Development Documentation](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp).

## 📄 License

MIT

## 👥 Contribution Guidelines

1. Fork the project repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## 📮 Contact Information

- Project Maintainer: [Your Name](mailto:your-email@example.com)
- Project Repository: [GitHub](https://github.com/your-username/mcpall) 