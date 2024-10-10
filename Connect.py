from requests import post as reqPost
from requests import get as reqGet
from requests import session as reqSession
from bs4 import BeautifulSoup
from yaml import load as yamlLoad
from yaml import FullLoader as yamlFullLoader
import urllib.parse
import logging


# Logging设置
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info("Starting")

# 配置文件
config = "./config.yaml"

with open(config,encoding="utf-8") as applist:
    data = yamlLoad(applist, Loader=yamlFullLoader)
    username = data["username"]
    password = data["password"]



'''
---执行登录操作---
'''
if __name__ == "__main__":
    # 创建一个会话对象
    session = reqSession()
    # 获得重定向URL
    url = 'http://100.99.0.1/'
    response = reqGet(url)


    # 检查请求是否成功
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
    else:
        logger.warning(f"请求失败，状态码：{response.status_code}")
        exit()


    # 查找frame标签并提取src属性
    frame = soup.find('frame', {'name': 'mainFrame'})
    if frame is not None:
        src = frame['src']
        parsed_url = urllib.parse.urlparse(src)
        param_str = urllib.parse.parse_qs(parsed_url.query).get('paramStr', [None])[0]
        if param_str:
            logger.info(f"paramStr: {param_str}")
        else:
            logger.warning("未找到paramStr参数")
    else:
        logger.warning("未找到名为 'mainFrame' 的 frame 标签")


    # 定义请求头
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://211.138.195.124',
        'Pragma': 'no-cache',
        'Referer': f'http://211.138.195.124/style/default_szlan/index.jsp?paramStr={param_str}',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    # 定义表单数据
    data = {
        'paramStr': param_str,
        'UserType': '',
        'province': '',
        'pwdType': '1',
        'serviceType': '301',
        'isCookie': 'true',
        'cookieType': '2',
        'UserName': username,
        'PassWord': password,
        'cookie': '2'
    }


    # 发送POST请求
    response = reqPost('http://211.138.195.124/authServlet', headers=headers, data=data, verify=False)


    # 检查响应状态码
    if response.status_code == 200:
        logger.info("请求成功！")
    else:
        logger.warning(f"请求失败，状态码：{response.status_code}")


    logger.info("程序结束")