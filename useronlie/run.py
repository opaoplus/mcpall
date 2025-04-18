#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from core.server import mcp

def main():
    """主入口函数，处理命令行参数并运行服务器"""
    parser = argparse.ArgumentParser(description="用户电话查询MCP服务")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口号")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务器主机地址")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "sse"], 
        default="sse",
        help="传输协议: stdio(标准IO)或sse(服务器发送事件)"
    )
    args = parser.parse_args()
    
    # 输出可用功能
    print("启动用户电话查询MCP服务...")
    print("可用工具: 查询电话")
    print("可用资源: users://all, user://{name}, status://")
    
    # 设置环境变量以配置SSE服务器
    if args.transport == "sse":
        os.environ["FASTMCP_HOST"] = args.host
        os.environ["FASTMCP_PORT"] = str(args.port)
        print(f"使用SSE模式启动服务器，地址: {args.host}:{args.port}")
    else:
        print("使用STDIO模式启动服务器")
    
    # 使用FastMCP内置的run方法运行服务器
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()
