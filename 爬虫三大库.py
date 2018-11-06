import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

try:
    res = requests.get(url='https://blog.starmeow.cn/blog/1/detail/', headers=headers)  # get方法加入请求头
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select("body > section > div > div > header > h1 > a")  # 右键Elements位置---Copy---Copy selector
    print(title)  # [<a title="创建项目初始化">创建项目初始化</a>]

    hot_titles = soup.select("body > section > aside > div.widget.widget_hot > ul > li > a > span.text")  # li:nth-child(1)运行会报错，需改为li
    print(hot_titles)
    """
    复制结果：
    body > section > aside > div.widget.widget_hot > ul > li:nth-child(1) > a > span.text
    结果会报错，需要进行修改
    body > section > aside > div.widget.widget_hot > ul > li:nth-of-type(1) > a > span.text  得到第一个数据
    body > section > aside > div.widget.widget_hot > ul > li > a > span.text  得到所有数据
    """
    for title in hot_titles:
        print(title, title.get_text(), title.get_text() == title.text)
        """
        <span class="text">【Flask微电影】05.搭建前台页面-会员登录注册和会员中心</span> 【Flask微电影】05.搭建前台页面-会员登录注册和会员中心 True
        <span class="text">【Flask微电影】10.搭建后台页面-会员管理、评论管理</span> 【Flask微电影】10.搭建后台页面-会员管理、评论管理 True
        <span class="text">【Flask微电影】11.搭建后台页面-收藏管理、日志管理</span> 【Flask微电影】11.搭建后台页面-收藏管理、日志管理 True
        <span class="text">【Flask微电影】07.搭建后台页面-后台登陆、后台主页页面</span> 【Flask微电影】07.搭建后台页面-后台登陆、后台主页页面 True
        <span class="text">【Flask微电影】01.环境搭建项目目录分析</span> 【Flask微电影】01.环境搭建项目目录分析 True
        """
except requests.exceptions.ConnectionError:  # 出现错误会显示一下内容
    print('拒绝连接')
