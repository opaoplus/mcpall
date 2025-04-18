# 用户电话查询MCP服务

基于Model Context Protocol (MCP)的用户电话查询服务演示。本服务使用FastMCP框架实现。

## 功能特点

- 提供用户电话查询工具 `查询电话`
- 支持资源访问 `users://all` 获取所有用户
- 支持动态资源 `user://{name}` 获取指定用户
- 提供状态检查资源 `status://`

## 安装

1. 确保已安装Python 3.11或更高版本
2. 安装依赖：

```bash
pip install -e .
# 或者
pip install "mcp[cli]>=1.6.0"
```

## 运行服务

服务支持两种运行模式：SSE 和 STDIO。

### SSE 模式（默认）

适合通过HTTP连接的网络服务：

```bash
python run.py
# 或指定主机和端口
python run.py --host 127.0.0.1 --port 8080
# 或明确指定SSE模式
python run.py --transport sse
```

服务将在默认端口上启动SSE服务（一般为8000）。

服务启动后可以访问以下端点：
- SSE端点: `http://localhost:8000/sse`
- 状态检查资源: `status://` (通过MCP协议访问)

### STDIO 模式

适合与Claude Desktop或其他MCP客户端直接集成：

```bash
python run.py --transport stdio
```

## 使用方法

### 使用MCP客户端（SSE模式）

可以使用任何支持MCP协议的客户端连接SSE服务：

```python
from mcp.client import McpClient

# 连接到服务器
client = McpClient("http://localhost:8000/sse")
await client.initialize()

# 获取所有用户
users = await client.get_resource("users://all")
print(users)

# 获取特定用户
user = await client.get_resource("user://张三")
print(user)

# 调用工具查询电话
result = await client.call_tool("查询电话", {"用户名": "张三"})
print(result)

# 获取服务状态
status = await client.get_resource("status://")
print(status)
```

### 在Claude Desktop中使用

1. 安装Claude Desktop
2. 打开Claude的配置文件（通常位于`~/Library/Application Support/Claude/claude_desktop_config.json`或Windows下的`%AppData%\Claude\claude_desktop_config.json`）
3. 添加以下配置：

```json
{
  "mcpServers": {
    "用户电话查询": {
      "isActive": true,
      "name": "用户电话查询",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

4. 在Claude Desktop中，你应该能够看到锤子图标，点击后可以使用查询电话工具
5. 尝试输入"查询张三的电话号码"

### 使用MCP CLI工具

如果安装了MCP CLI工具，可以直接使用以下命令测试服务：

```bash
# 测试服务（STDIO模式）
mcp dev run.py

# 连接到SSE服务器（默认运行模式）
mcp connect http://localhost:8000/sse

# 查看可用工具和资源
mcp list tools
mcp list resources

# 调用工具
mcp call 查询电话 --用户名 "张三"

# 获取资源
mcp get users://all
mcp get user://张三
mcp get status://
```

## 状态检查

服务提供了一个简单的状态检查资源，可以用来监控服务是否正常运行：

```
GET status://
```

返回示例：

```json
{
  "status": "ok",
  "service": "用户电话查询服务",
  "version": "1.0.0",
  "tools": ["查询电话"],
  "resources": ["users://all", "user://{name}", "status://"]
}
```

## 模拟数据

服务内置有以下用户数据：

| 用户名 | 电话号码 |
|-------|---------|
| 张三 | 13812345678 |
| 李四 | 13987654321 |
| 王五 | 15912345678 |
| 赵六 | 18612345678 |
| 钱七 | 17712345678 |

## 扩展开发

如需添加更多用户或功能，请修改 `core/server.py` 文件中的相关代码。
