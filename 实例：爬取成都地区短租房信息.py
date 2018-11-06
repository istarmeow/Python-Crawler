import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}  # 用于伪装浏览器，便于爬虫的稳定性


def get_all_links(url):
    """
    得到每个分页的房子url列表
    :param url: 房源列表的分页url
    :return: 得到每一页的所有房源列表
    """
    html_data = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(html_data.text, 'lxml')
    # print(soup)
    links = soup.select('#page_list > ul > li > a')
    res = list()
    for link in links:
        # print(link.get('href'))
        href = link.get('href')  # 获取标签href属性信息，得到进入详情页的URL
        res.append(href)
        time.sleep(2)
    return res


def get_info(url):
    """
    每一个房源信息获取
    :param url: 房源url
    :return: 房源字典信息
    """
    html_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_data.text, 'lxml')
    titles = soup.select('div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em')
    # 复制的结果是：body > div.wrap.clearfix.con_bg > div.con_l > div.pho_info > h4 > em，无法获取，需要去掉body
    title = ''
    if titles:
        title = titles[0].get_text().strip()  # 如果得到的结果不为空，取第一个的值
    addresses = soup.select('div.wrap.clearfix.con_bg > div.con_l > div.pho_info > p > span')
    # print(addresses)
    address = ''
    if addresses:
        address = addresses[0].get_text().strip()
    prices = soup.select('#pricePart > div.day_l > span')
    price = ''
    if prices:
        price = prices[0].get_text()
    images = soup.select('#curBigImage')
    image = ''
    if images:
        image = images[0].get('src')
    names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
    name = ''
    if names:
        name = names[0].get_text()
    sexs = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')
    sex = ''
    if sexs:
        sex = sexs[0].get('class')
    # print(sex)  # ['member_ico1']
    if "member_ico1" in sex:  # 根据class来判断房东的性别，男房东的class="member_ico"
        sex = '女'
    else:
        sex = '男'
    data = {
        'title': title,
        'address': address,
        'price': price,
        'image': image,
        'name': name,
        'sex': sex
    }
    # print(data)
    return data


if __name__ == '__main__':
    # fangzi_list = get_all_links('https://cd.xiaozhu.com/')
    # fangzi_info = get_info('https://cd.xiaozhu.com/fangzi/2148542359.html')
    page_urls = ['https://cd.xiaozhu.com/search-duanzufang-p{}-0/'.format(num) for num in range(1, 4)]  # 准备3页数据
    for page_url in page_urls:
        fangzi_list = get_all_links(page_url)  # 得到每一页的所有房源列表
        time.sleep(2)  # 暂停2秒，防止请求过快导致被服务器拒绝
        for fangzi in fangzi_list:
            print(get_info(fangzi))  # 遍历房源列表，得到每个房源信息
