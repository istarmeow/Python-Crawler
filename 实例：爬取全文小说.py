import re
import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}
file = open('实例：爬取全文小说.txt', 'a+')  # 以追加的方式创建文件


def get_content(url):
    res = requests.get(url, headers=headers)
    # print(type(res.encoding))  # <class 'str'>
    # print(res.text)  # 头部<meta charset="utf-8">，但是中文乱码
    # print(res.content)  # 二进制响应内容
    if res.status_code == 200:
        # 判断请求码是否为200，这样才能访问
        title = re.findall('<h1>(.*?)</h1>', res.content.decode('utf-8'))[0]
        print(title)
        file.write('\n{}\n{}\n'.format(title, '*' * 180))
        contents = re.findall('<p>(.*?)</p>', res.content.decode('utf-8'), re.S)  # res.content->TypeError: cannot use a string pattern on a bytes-like object
        for content in contents:
            print(content)
            file.write(content + '\n')
    else:
        print('无法法访问' + url)


if __name__ == '__main__':
    get_content('http://www.doupoxs.com/doupocangqiong/12.html')
    urls = ['http://www.doupoxs.com/doupocangqiong/{}.html'.format(page) for page in range(2, 10)]  # 只取到10
    for url in urls:
        get_content(url)
        time.sleep(1)
    file.close()
