# MCPALL

<div align="center">

![版本](https://img.shields.io/badge/版本-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![MCP](https://img.shields.io/badge/MCP-1.6.0%2B-orange)
![许可证](https://img.shields.io/badge/许可证-MIT-green)

</div>

<div align="center">
  
[中文](./readme.md) | [English](./readme_en.md) | [日本語](./readme_jp.md) | [한국어](./readme_kr.md)

</div>

## 📑 项目概述

MCPALL是一个基于Model Context Protocol (MCP)的多功能服务集合平台，支持快速开发和集成各类MCP服务。该平台设计为高度模块化，可轻松扩展新的服务模块。

## 🚀 当前模块

| 模块名称 | 描述 | 详情链接 |
|---------|------|---------|
| 📞 **useronlie** | 用户电话查询服务 | [查看详情](./useronlie/README.md) |
| 📚 **xmol** | 文献检索和问答系统 | [查看详情](./xmol/README.md) |

## 🛠️ 技术栈

- **Python 3.11+**：核心开发语言
- **FastMCP**：MCP协议实现框架
- **通信协议**：支持HTTP/SSE和STDIO两种传输方式

## ⚙️ 通用开发指南

### 安装基础环境

```bash
# 确保安装Python 3.11+
python --version

# 安装MCP框架
pip install "mcp[cli]>=1.6.0"

# 推荐使用uv作为依赖管理工具
pip install uv
```

### 模块结构标准

每个新模块应遵循以下基本结构：

```
module_name/
├── core/               # 核心功能实现
│   ├── __init__.py
│   ├── server.py       # MCP服务器实现
│   └── ...             # 其他功能模块
├── README.md           # 模块详细文档
├── run.py              # 启动脚本
├── pyproject.toml      # 项目配置
└── ...                 # 其他配置文件
```

### 开发新模块步骤

1. **创建模块目录结构**
   ```bash
   mkdir -p new_module/core
   touch new_module/{README.md,run.py,pyproject.toml}
   touch new_module/core/{__init__.py,server.py}
   ```

2. **实现MCP服务器**
   ```python
   # new_module/core/server.py (基本框架)
   from fastmcp import McpServer, Tool, Resource

   class NewModuleServer(McpServer):
       def __init__(self):
           super().__init__("新模块名称")
           # 注册工具和资源
           self.register_tool(Tool("工具名称", self.tool_handler))
           self.register_resource("resource://path", self.resource_handler)
   
       async def tool_handler(self, params):
           # 实现工具逻辑
           return {"result": "工具执行结果"}
   
       async def resource_handler(self, params):
           # 实现资源访问逻辑
           return {"data": "资源内容"}
   ```

3. **创建启动脚本**
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

4. **配置项目依赖**
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

5. **撰写模块README**
   每个模块应有独立的README文件，详细说明模块的功能、配置和使用方法。

## 🚀 通用运行方法

所有模块支持两种运行模式：

```bash
# STDIO模式 (适合与Claude Desktop直接集成)
cd <module_name>
python run.py

# SSE模式 (作为HTTP服务运行)
cd <module_name>
python run.py --transport sse --host 127.0.0.1 --port 8000
```

## 🐳 Docker 部署

项目支持使用 Docker 进行部署和运行，方便在不同环境中快速部署和隔离运行。

### 使用 Docker Compose（推荐）

```bash
# 构建所有服务
docker-compose build

# 启动特定服务（例如 useronlie 模块的 SSE 模式）
docker-compose up useronlie-sse

# 后台运行服务
docker-compose up -d useronlie-sse
```

详细的 Docker 部署说明请参考 [Docker 部署指南](./docker-usage.md)。

## 🏗️ 集成到Claude

1. 配置Claude Desktop（`%AppData%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "<服务名称>": {
      "isActive": true,
      "name": "<显示名称>",
      "url": "http://localhost:<端口>/sse"
    }
  }
}
```

2. 重启Claude Desktop应用使配置生效

## 🔧 扩展生态

MCPALL设计为可无限扩展的服务生态系统。以下是一些潜在的扩展方向：

- **数据处理服务**：数据分析、可视化、报表生成
- **AI辅助工具**：文本生成、图像处理、语音识别
- **开发工具链**：代码生成、项目管理、测试自动化
- **知识库服务**：文档检索、知识图谱、问答系统
- **运维监控**：系统状态、性能监控、日志分析

将您的服务添加到MCPALL平台只需遵循上述开发标准，然后将模块目录添加到项目根目录即可。

## 📋 MCP服务开发核心概念

### 工具 (Tools)

工具是MCP服务提供的可调用函数，用于执行特定任务。

```python
# 定义工具示例
@server.tool("工具名称")
async def tool_handler(params):
    # 参数处理和业务逻辑
    return {"result": "处理结果"}
```

### 资源 (Resources)

资源是MCP服务提供的数据访问点，通过URI标识。

```python
# 定义资源示例
@server.resource("resource://path")
async def resource_handler(params):
    # 资源访问逻辑
    return {"data": "资源内容"}
```

### 资源模式 (Schema)

通过模式定义，可以声明资源的结构和验证规则。

```python
# 资源模式示例
resource_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "data": {"type": "array", "items": {"type": "string"}}
    }
}
```

更多开发详情，请参考[MCP开发文档](https://github.com/anthropics/anthropic-cookbook/tree/main/mcp)。

## 📄 许可证

MIT

## 👥 贡献指南

1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📮 联系方式

- 项目维护者：[您的姓名](mailto:your-email@example.com)
- 项目仓库：[GitHub](https://github.com/your-username/mcpall)
