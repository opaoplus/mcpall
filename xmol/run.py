#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XMol 文献检索服务启动脚本

该脚本方便使用uv运行服务
"""

import argparse
import os
import sys
import logging
from core.server import mcp, run

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("文献检索助手")

def main():
    """主入口函数，处理命令行参数并运行服务器"""
    parser = argparse.ArgumentParser(description="XMol文献检索和问答系统")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口号")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务器主机地址")
    parser.add_argument("--ssepath", type=str, default="/sse", help="sse路径")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "sse"], 
        default="stdio",
        help="传输协议: stdio(标准IO)或sse(服务器发送事件)"
    )

    args = parser.parse_args()
    
    # 输出可用功能
    print("启动XMol文献检索服务...")
    print("可用工具: search_title_by_keywords, get_literature_detail")
    
    # 设置环境变量以配置SSE服务器
    if args.transport == "sse":
        # 配置服务器参数
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.settings.sse_path = args.ssepath
        
        # 如果开启调试模式，设置日志级别为DEBUG

            
        print(f"使用SSE模式启动服务器，地址: {args.host}:{args.port}")
        print(f"SSE路径: {args.ssepath}")
        print(f"消息路径: {mcp.settings.message_path}")
        

    else:
        print("使用STDIO模式启动服务器")
    
    # 使用自定义的run方法运行服务器
    run(transport=args.transport)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 