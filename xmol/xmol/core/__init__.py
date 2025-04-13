"""
XMol 核心功能模块

包含文献获取等基础功能
"""

from .content import get_content
from .logger import setup_logger

__all__ = ["get_content", "setup_logger"] 