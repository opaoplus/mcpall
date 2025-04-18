# MCPALL

<div align="center">

![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![MCP](https://img.shields.io/badge/MCP-1.6.0%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

<div align="center">
  
[中文](./readme.md) | [English](./readme_en.md) | [日本語](./readme_jp.md) | [한국어](./readme_kr.md)

</div>

## 📑 Project Overview

MCPALL is a multi-functional service collection platform based on Model Context Protocol (MCP), supporting rapid development and integration of various MCP services. The platform is designed to be highly modular, making it easy to extend with new service modules.

## 🚀 Current Modules

| Module Name | Description | Details Link |
|-------------|-------------|--------------|
| 📞 **useronlie** | User phone query service | [View Details](./useronlie/README.md) |
| 📚 **xmol** | Literature retrieval and Q&A system | [View Details](./xmol/README.md) |

## 🛠️ Tech Stack

- **Python 3.11+**: Core development language
- **FastMCP**: MCP protocol implementation framework
- **Communication Protocols**: Supports both HTTP/SSE and STDIO transport methods

## ⚙️ General Development Guide

### Setting Up the Environment

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
├── README.md           # Module detailed documentation
├── run.py              # Startup script
├── pyproject.toml      # Project configuration
└── ...                 # Other configuration files
```

### Steps to Develop a New Module

1. **Create Module Directory Structure**
   ```bash
   mkdir -p new_module/core
   touch new_module/{README.md,run.py,pyproject.toml}
   touch new_module/core/{__init__.py,server.py}
   ```

2. **Implement MCP Server**
   ```python
   # new_module/core/server.py (basic framework)
   from fastmcp import McpServer, Tool, Resource

   class NewModuleServer(McpServer):
       def __init__(self):
           super().__init__("New Module Name")
           # Register tools and resources
           self.register_tool(Tool("Tool Name", self.tool_handler))
           self.register_resource("resource://path", self.resource_handler)
   
       async def tool_handler(self, params):
           # Implement tool logic
           return {"result": "Tool execution result"}
   
       async def resource_handler(self, params):
           # Implement resource access logic
           return {"data": "Resource content"}
   ```

3. **Create Startup Script**
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

4. **Configure Project Dependencies**
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

5. **Write Module README**
   Each module should have its own independent README file, detailing its functionality, configuration, and usage instructions.

## 🚀 Universal Running Method

All modules support two running modes:

```bash
# STDIO mode (suitable for direct integration with Claude Desktop)
cd <module_name>
python run.py

# SSE mode (running as an HTTP service)
cd <module_name>
python run.py --transport sse --host 127.0.0.1 --port 8000
```

## 🏗️ Integration with Claude

1. Configure Claude Desktop (`%AppData%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "<Service Name>": {
      "isActive": true,
      "name": "<Display Name>",
      "url": "http://localhost:<Port>/sse"
    }
  }
}
```

2. Restart Claude Desktop application to apply the configuration

## 🔧 Extensible Ecosystem

MCPALL is designed as an infinitely extensible service ecosystem. Here are some potential expansion directions:

- **Data Processing Services**: Data analysis, visualization, report generation
- **AI Assistant Tools**: Text generation, image processing, speech recognition
- **Development Toolchain**: Code generation, project management, test automation
- **Knowledge Base Services**: Document retrieval, knowledge graphs, Q&A systems
- **Operations Monitoring**: System status, performance monitoring, log analysis

Adding your service to the MCPALL platform only requires following the development standards above, then adding the module directory to the project root.

## 📋 MCP Service Development Core Concepts

### Tools

Tools are callable functions provided by MCP services for performing specific tasks.

```python
# Tool definition example
@server.tool("Tool Name")
async def tool_handler(params):
    # Parameter processing and business logic
    return {"result": "Processing result"}
```

### Resources

Resources are data access points provided by MCP services, identified by URI.

```python
# Resource definition example
@server.resource("resource://path")
async def resource_handler(params):
    # Resource access logic
    return {"data": "Resource content"}
```

### Resource Schema

Through schema definitions, you can declare the structure and validation rules for resources.

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

## 📮 Contact

- Project Maintainer: [Your Name](mailto:your-email@example.com)
- Project Repository: [GitHub](https://github.com/your-username/mcpall) 