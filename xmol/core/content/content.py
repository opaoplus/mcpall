"""
XMol 文献内容获取模块
"""

import requests
from bs4 import BeautifulSoup as bs
import random
import re
import time
import logging


# 获取日志记录器
logger = logging.getLogger("文献检索助手.content")



class get_content():
    """
    文献内容获取工具类
    用于从X-MOL网站获取科学文献内容
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }

    def _get_post_data(self, keywordList: list, impact: str) -> dict:  # 关键词列表，影响因子
        """
        获取post请求数据
        """
        post_data = {
            "keywordsRange": "2",
            "keywordList[0].option": keywordList[0]}
        for i, keyword in enumerate(keywordList):
            if keyword and i > 0:
                post_data[f"keywordList[{i}].operator"] = "AND"
                post_data[f"keywordList[{i}].option"] = keyword
        post_data.update({
            "authorList[0].option": "",
            "affiliation": "",
            "journals[0]": "",
            "journals[1]": "",
            "journals[2]": "",
            "journals[3]": "",
            "journals[4]": "",
            "publishDateStart": "",
            "publishDateEnd": "",
            "impactFactorStart": impact,
            "impactFactorEnd": ""
        })

        return post_data

    def _get_ck(self, ck: str) -> dict:  # 获取cookie
        """
        获取cookie,将cookie转换为字典
        """
        ck_dic = {}
        cookies = ck.split(';')
        for cookie in cookies:
            try:
                key, value = cookie.strip().split('=', 1)
                if key in ["UM_distinctid", "atk0210", "rtk0210"]:
                    ck_dic[key.strip()] = value.strip()
            except ValueError:
                logger.warning(f"无法解析Cookie部分: {cookie}")
        return ck_dic

    def _get_url(self, post_data: dict, cookies: str) -> str:  # 获取url
        """
        获取url
        """
        try:
            id = random.randint(333, 999)
            url = f"https://www.x-mol.com/paper/search/searchPaper?date={id}"
            resp = requests.post(url, headers=self.headers, data=post_data, cookies=cookies)
            ex = 'searchLogId=(.*)&readMode'
            id_match = re.search(ex, resp.url)
            if not id_match:
                logger.error(f"无法从URL提取searchLogId: {resp.url}")
                raise ValueError("搜索ID提取失败")
            id_text = id_match.group(1).strip()
            return id_text
        except Exception as e:
            logger.error(f"获取URL时出错: {str(e)}")
            raise

    def get_page_content(self, keywordList: list, ck: str, impact: str = 8,searchSort: str = 'publishDate', lang: str = 'zh', pageindex: int = 1) -> list[dict]:  # 获取页面内容
        """
        获取页面内容
        
        参数:
        keywordList: 关键词列表，如 ["CRISPR", "遗传疾病"]
        ck: Cookie字符串
        impact: 影响因子下限，默认为8
        lang: 语言，默认为'zh'（中文）
        pageindex: 页码，默认为1
        
        返回:
        包含文献信息的字典
        """
        try:
            baseurl = 'https://www.x-mol.com/'

            
            paper_all = []
            logger.info(f"开始搜索关键词: {keywordList}, 影响因子: {impact}, 页码: {pageindex}")
            
            # 通过关键词和影响因子获取页面url
            post_data = self._get_post_data(keywordList, impact)
            cookies = self._get_ck(ck)
            id_text = self._get_url(post_data, cookies)

            url = f"https://www.x-mol.com/paper/search/result?searchLogId={id_text}&readMode={lang}&searchSort={searchSort}&pageIndex={pageindex}"
            logger.debug(f"请求URL: {url}")
            
            resp = requests.request("GET", url, headers=self.headers, cookies=cookies)
            resp.encoding = 'utf-8'
            soup = bs(resp.text, "html.parser")
            
            content_list = soup.find("div", {"class": "magazine-senior-search-results-list"})


            if not content_list:
                logger.warning("未找到文献列表元素")
                return {"error": "未找到文献列表"}
                
            content_li = content_list.find_all("li")
            if not content_li:
                logger.warning("文献列表为空")
                return {"error": "文献列表为空"}
                
            doi_re = 'DOI:(.*)'
            date_pattern = r"Pub Date\s*:\s*(\d{4}-\d{2}-\d{2})"
            for content in content_li:
                paper = {}
                title = content.find("div", {"class": "it-bold space-bottom-m10"}) # 标题
                info = content.find("div", {"class": "div-text-line-one it-new-gary"}) # 期刊和影响因子
                jounal = info.find("em", {"class": "it-blue"}) # 期刊
                impact = info.find("span") # 影响因子
                doi_match = re.search(doi_re, info.text)  # 匹配DOI
                url_elements = content.select("a") # 链接
                pubdata = re.search(date_pattern, info.text)  # 发布日期
                
      
                if len(url_elements) > 3:
                    url = url_elements[3]
                else:
                    logger.warning("未找到URL元素")
                    url = {"href": ""}
                    
                abstract = content.find("div", {"class": "div-text-line-three itsmlink"}) # 摘要
                
                
                paper['title'] = title.text.strip() if title else "未知标题"
                paper['jounal'] = jounal.text.strip() if jounal else "未知期刊"
                paper['impact'] = impact.text.strip() if impact else "未知影响因子"
                paper['pubdata'] = pubdata.group(1).strip() if pubdata else "未知发布日期"
                paper['doi'] = doi_match.group(1).strip() if doi_match else "未知DOI"
                paper['url'] = baseurl + url['href'].strip() if url else "未知URL"
                paper['abstract'] = abstract.text.strip() if abstract else "未知摘要"
                    
                paper_all.append(paper)
                    

            logger.info(f"成功获取文献: {len(paper_all)}篇")
            time.sleep(1)  # 避免频繁请求
            return paper_all
            
        except Exception as e:
            logger.error(f"获取页面内容时出错: {str(e)}")
            return {"error": f"获取文献内容失败: {str(e)}"} 