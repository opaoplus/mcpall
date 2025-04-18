"""
XMol MCP服务器

提供文献检索和问答功能的MCP服务器实现
"""

from mcp.server.fastmcp import FastMCP, Context
from core.content import get_content
from dotenv import load_dotenv
import os
import sys
from typing import List, Dict, Any, Optional
import logging
import traceback
import json
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("文献检索助手")

# 文献缓存目录
CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(exist_ok=True)

# 加载环境变量
load_dotenv()

# 获取环境变量
cookie = os.getenv('Cookie', "")
impact = os.getenv('Impact', "8")
lang = os.getenv('lang', "zh")


# 检查必要的配置
if not cookie:
    logger.error("错误：请在.env文件中设置Cookie")
    sys.exit(1)

# 初始化文献获取工具
content_tool = get_content()

# 创建MCP服务器 - 从环境变量获取配置
mcp = FastMCP(
    "文献检索助手", 
    host=os.getenv("FASTMCP_host", "0.0.0.0"),
    port=int(os.getenv("FASTMCP_port", "8000")),
    sse_path=os.getenv("FASTMCP_sse_path", "/sse"),
    debug=os.getenv("FASTMCP_debug", "").lower() == "true",
    log_level=os.getenv("FASTMCP_log_level", "INFO")
)

# 文献缓存
literature_cache = {}


# 定义自定义运行方法
def run(transport="stdio"):
    """运行MCP服务器，使用指定的传输协议"""

    if transport == "sse":
        logger.info(f"运行SSE服务器，监听地址: {mcp.settings.host}:{mcp.settings.port}")
        logger.info(f"SSE路径: {mcp.settings.sse_path}")
        logger.info(f"消息路径: {mcp.settings.message_path}")
    else:
        logger.info("运行STDIO服务器")
    
    # 直接调用mcp的run方法
    mcp.run(transport=transport)


@mcp.prompt()
def system_prompt() -> str:
    """
    系统提示
    """
    return """
    你是一个专业的学术文献检索助手，可以帮助用户查找、理解和分析学术文献。

    工作流程:
    1. 分析用户的学术问题，提取多组关键概念和术语
    2. 使用关键词搜索相关文献
    3. 根据用户需要，获取并展示文献的详细信息
    4. 帮助用户理解和分析文献内容

    使用指南:
    - 当用户提出学术问题时，首先分析问题并提取1-3个关键词，使用3-5组关键词进行搜索
    - 每个关键词应该使用专业术语，不要使用通用术语，如果文献较少，则使用通用术语
    - 使用search_title_by_keywords工具搜索文献，它将返回文献标题列表
    - 如果用户对某篇文献感兴趣，使用get_literature_detail工具获取详情
    - 根据文献内容回答用户问题，并提供专业见解

    注意事项:
    - 关键词应该是学术术语，数量不超过3个以获得最佳结果，应该使用多组关键词进行搜索
    - 每个关键词应该使用专业术语，不要使用通用术语，如果文献较少，则使用通用术语
    - 关键词应该使用专业术语，不要使用通用术语
    - 可以调整影响因子阈值以过滤文献质量
    - 使用页码参数浏览更多搜索结果
    """

def _save_to_cache(literature_list: List[Dict]) -> None:
    """将文献保存到缓存中"""
    try:
        for item in literature_list:
            if 'doi' in item and item['doi'] != "未知DOI":
                # 使用DOI作为唯一标识
                # cache_file = CACHE_DIR / f"{item['doi'].replace('/', '_')}.json"
                # with open(cache_file, 'w', encoding='utf-8') as f:
                #     json.dump(item, f, ensure_ascii=False, indent=2)
                # 同时保存到内存缓存
                literature_cache[item['doi']] = item
        logger.info(f"已缓存{len(literature_list)}篇文献")
    except Exception as e:
        logger.error(f"缓存文献时出错: {str(e)}")

def _get_from_cache(doi: str) -> Optional[Dict]:
    """从缓存中获取文献"""
    try:
        # 先尝试从内存缓存获取
        if doi in literature_cache:
            return literature_cache[doi]
            
        # # 再尝试从文件缓存获取
        # cache_file = CACHE_DIR / f"{doi.replace('/', '_')}.json"
        # if cache_file.exists():
        #     with open(cache_file, 'r', encoding='utf-8') as f:
        #         data = json.load(f)
        #         literature_cache[doi] = data  # 更新内存缓存
        #         return data
        return None
    except Exception as e:
        logger.error(f"从缓存获取文献时出错: {str(e)}")
        return None

def _convert_to_markdown(literature_list: List[Dict]) -> str:
    """将文献列表转换为Markdown格式"""
    if isinstance(literature_list, dict) and literature_list.get('error'):
        return f"### 搜索错误\n\n{literature_list['error']}\n\n{literature_list.get('suggestion', '')}"
        
    try:
        markdown = "### 搜索结果\n\n"
        
        for i, paper in enumerate(literature_list):
            doi = paper.get('doi', '未知DOI')
            markdown += f"{i+1}. **{paper.get('title', '未知标题')}**\n"
            markdown += f"   - 期刊: {paper.get('jounal', '未知期刊')}\n"
            markdown += f"   - 影响因子: {paper.get('impact', '未知')}\n"
            markdown += f"   - 发布日期: {paper.get('pubdata', '未知发布日期')}\n"
            markdown += f"   - DOI: {doi}\n"
            markdown += f"   - [文献链接]({paper.get('url', '#')})\n\n"
            
        markdown += "\n请继续使用 `get_literature_detail` 工具获取特定文献的详细信息，提供DOI作为参数。"
        return markdown
    except Exception as e:
        logger.error(f"转换为Markdown时出错: {str(e)}")
        return f"### 错误\n\n转换搜索结果时出错: {str(e)}"


@mcp.tool()
def search_title_by_keywords(keywords: List[str], impact_factor: str = None, page_index: int = 1, searchSort: str = '') -> str:
    """
    使用关键词列表搜索文献标题，返回Markdown格式的文献标题列表
    
    参数:
    keywords: 关键词列表，例如["CRISPR", "遗传疾病"]，由客户端(LLM)根据用户问题提供，关键词数量建议最多3个
    impact_factor: 影响因子下限，默认使用配置中的值
    page_index: 页码，默认为1
    searchSort: 排序方式，默认为'',为空代表相关性排序，可选值为'publishDate'、publishDate代表按照发布日期排序，'citation'代表按照引用次数排序，'default'代表按照默认排序

    返回:
    Markdown格式的文献标题列表，包含标题、期刊名、影响因子和DOI

    注意事项:
    - 关键词应该是学术术语，数量不超过3个以获得最佳结果，应该使用多组关键词进行搜索
    - 每个关键词应该使用专业术语，不要使用通用术语，如果文献较少，则使用通用术语
    - 关键词应该使用专业术语，不要使用通用术语
    - 可以调整影响因子阈值以过滤文献质量
    - 使用页码参数浏览更多搜索结果
    """
    try:
        # 使用用户提供的影响因子或默认值
        impact_value = impact_factor if impact_factor is not None else impact
        
        logger.info(f"搜索关键词: {keywords}, 影响因子: {impact_value}")
        
        # 获取文献内容
        literature_list = content_tool.get_page_content(
            keywordList=keywords,
            ck=cookie,
            impact=impact_value,
            lang=lang,
            pageindex=page_index,
            searchSort=searchSort
        )
        
        # 检查文献内容是否为空或缺少关键信息
        if isinstance(literature_list, dict) and literature_list.get('error'):
            logger.warning(f"搜索文献返回错误: {literature_list.get('error')}")
            return _convert_to_markdown(literature_list)
            
        if not literature_list or len(literature_list) == 0:
            logger.warning(f"未找到与关键词相关的文献: {keywords}")
            return _convert_to_markdown({
                "error": "未找到相关文献",
                "keywords": keywords,
                "suggestion": "尝试使用不同的关键词或降低关键词长度或降低影响因子要求或减少关键词数量，关键词数量建议最多3个"
            })
        
        # 保存到缓存
        _save_to_cache(literature_list)
        
        # 转换为Markdown格式
        return _convert_to_markdown(literature_list)
        
    except Exception as e:
        logger.error(f"使用关键词搜索文献时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return _convert_to_markdown({
            "error": f"搜索文献时出错: {str(e)}",
            "keywords": keywords,
            "suggestion": "请检查网络连接或Cookie是否有效"
        })

@mcp.tool()
def get_literature_detail(doi: str) -> str:
    """
    根据DOI获取文献的详细信息，包括摘要、作者、引用等
    
    参数:
    doi: 文献的DOI标识符
    
    返回:
    Markdown格式的文献详细信息
    """
    try:
        # 尝试从缓存获取
        cached_literature = _get_from_cache(doi)
        if cached_literature:
            logger.info(f"从缓存获取文献: {doi}")
            return f"### {cached_literature.get('title', '未知标题')}\n\n" + \
                   f"**DOI**: {doi}\n\n" + \
                   f"**期刊**: {cached_literature.get('jounal', '未知期刊')}\n\n" + \
                   f"**发布日期**: {cached_literature.get('pubdata', '未知发布日期')}\n\n" + \
                   f"**影响因子**: {cached_literature.get('impact', '未知')}\n\n" + \
                   f"**摘要**: {cached_literature.get('content', '暂无摘要')}\n\n" + \
                   f"**链接**: [{doi}]({cached_literature.get('url', '#')})"
        
        # 从API获取详细信息
        logger.info(f"从API获取文献: {doi}")
        detail = content_tool.get_literature_detail(doi=doi, ck=cookie, lang=lang)
        
        if isinstance(detail, dict) and detail.get('error'):
            logger.warning(f"获取文献详情返回错误: {detail.get('error')}")
            return f"### 获取文献详情失败\n\n{detail['error']}\n\n{detail.get('suggestion', '')}"
            
        if not detail:
            logger.warning(f"未找到指定DOI的文献: {doi}")
            return f"### 未找到文献\n\nDOI: {doi}\n\n可能的原因:\n- DOI不正确\n- 文献数据库中不存在该文献\n- 网络连接问题"
        
        # 转换为Markdown格式并返回
        return f"### {detail.get('title', '未知标题')}\n\n" + \
               f"**DOI**: {doi}\n\n" + \
               f"**期刊**: {detail.get('jounal', '未知期刊')}\n\n" + \
               f"**发布日期**: {detail.get('pubdata', '未知发布日期')}\n\n" + \
               f"**影响因子**: {detail.get('impact', '未知')}\n\n" + \
               f"**摘要**: {detail.get('content', '暂无摘要')}\n\n" + \
               f"**链接**: [{doi}]({detail.get('url', '#')})"
               
    except Exception as e:
        logger.error(f"获取文献详情时发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        return f"### 错误\n\n获取文献详情时出错: {str(e)}\n\nDOI: {doi}"

@mcp.resource(uri="file:///help.txt")
def help() -> str:
    """提供系统帮助信息，作为资源URI可访问"""
    return """
    # XMol 文献检索助手
    
    欢迎使用XMol文献检索助手！该工具可以帮助您搜索和查看学术文献。
    
    ## 使用流程
    1. 提出您的学术问题
    2. 我会分析您的问题，判断是否可以直接回答
       - 如果不能，将提取多组关键词并搜索相关文献
    3. 展示文献标题列表
    4. 您可以选择感兴趣的文献，获取其详细内容
    5. 会根据多组关键词搜索相关文献
    
    ## 可用工具
    - search_title_by_keywords: 根据关键词搜索文献，返回标题列表
    - get_literature_detail: 根据DOI获取文献的详细信息
    
    ## 搜索技巧
    - 提供1-3个精确的关键词可以获得更好的搜索结果
    - 每个关键词应该使用专业术语，不要使用通用术语，如果文献较少，则使用通用术语
    - 关键词应该是专业术语或准确概念
    - 您可以设置影响因子阈值（默认为8）来筛选高质量文献
    
    ## 示例
    问题: "CRISPR技术在治疗遗传疾病方面的进展？"
    关键词: ["CRISPR", "遗传疾病", "基因治疗"]
    
    问题: "量子计算在药物发现中的应用前景？"
    关键词: ["量子计算", "药物发现"]、["药物发现", "分子模拟"]、["量子计算", "分子模拟"]
    """ 