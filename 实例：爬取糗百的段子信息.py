import re
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}


def get_info(url):
    res = requests.get(url)
    names = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    sex_levels = re.findall('<div class="articleGender (.*?)Icon">(.*?)</div>', res.text, re.S)
    # print(levels)  # [('man', '40'), ('women', '25'),...]
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>.*?</div>', res.text, re.S)  # <span>前面有\n，</span>后面有\n\n，需要匹配掉
    # print(contents)
    votes = re.findall('<span class="stats-vote"><i class="number">(\d+)</i> 好笑</span>', res.text, re.S)
    # print(votes, len(votes))
    comments = re.findall('<i class="number">(\d+)</i> 评论', res.text, re.S)
    # print(comments, len(comments))
    info_list = list()
    for name, sex_level, content, vote, comment in zip(names, sex_levels, contents, votes, comments):
        info = {
            'name': name.strip(),
            'sex': sex_level[0],
            'level': sex_level[1],
            'content': content.strip(),
            'vote': vote,
            'comment': comment
        }
        # print(info)
        info_list.append(info)
    return info_list


if __name__ == '__main__':
    # get_info('https://www.qiushibaike.com/text/page/1/')
    urls = ['https://www.qiushibaike.com/text/page/{}/'.format(page) for page in range(1, 2)]
    file = open('实例：爬取糗百的段子信息.txt', 'a+')
    for url in urls:
        for info in get_info(url):
            file.write(info['name'] + '\n')
            file.write(info['sex'] + '\n')
            file.write(info['level'] + '\n')
            file.write(info['content'] + '\n')
            file.write(info['vote'] + '\n')
            file.write(info['comment'] + '\n')

    file.close()
