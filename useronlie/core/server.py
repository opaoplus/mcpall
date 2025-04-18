from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Optional

# 创建MCP服务器实例
mcp = FastMCP("用户电话查询服务")

# 模拟用户数据库
USER_DATABASE: Dict[str, str] = {
    "张三": "13812345678",
    "李四": "13987654321",
    "王五": "15912345678",
    "赵六": "18612345678",
    "钱七": "17712345678"
}

# 添加电话查询工具
@mcp.tool()
def 查询电话(username: str) -> Dict[str, str]:
    """根据用户名查询电话号码"""
    
    phone = USER_DATABASE.get(username)
    if phone:
        return {"用户名": username, "电话": phone, "状态": "成功"}
    else:
        return {"用户名": username, "电话": "", "状态": "未找到用户"}

# 添加资源 - 获取所有用户列表
@mcp.resource("users://all")
def 获取所有用户() -> Dict[str, Dict[str, str]]:
    """获取所有用户的电话信息"""
    return {"用户": {name: {"电话": phone} for name, phone in USER_DATABASE.items()}}

# 添加动态资源 - 根据用户名获取指定用户
@mcp.resource("user://{name}")
def 获取用户(name: str) -> Dict[str, Optional[str]]:
    """获取指定用户的电话信息"""
    phone = USER_DATABASE.get(name)
    if phone:
        return {"用户名": name, "电话": phone}
    else:
        return {"用户名": name, "电话": None}

# 添加状态检查资源
@mcp.resource("status://")
def 获取状态() -> Dict[str, any]:
    """获取服务状态信息"""
    return {
        "status": "ok",
        "service": "用户电话查询服务",
        "version": "1.0.0",
        "tools": ["查询电话"],
        "resources": ["users://all", "user://{name}", "status://"]
    } 