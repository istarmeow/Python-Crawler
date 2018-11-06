import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}  # 用于伪装浏览器，便于爬虫的稳定性


def get_info(url):
    html_data = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(html_data.text, 'lxml')
    ranks = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_num')  # 前3个数字加粗，select不能包含strong标签
    # print(ranks[0].get_text().strip(), ranks[4].get_text().strip())  # 获取歌曲的信息
    songs = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > a')
    length_of_times = soup.select('#rankWrap > div.pc_temp_songlist > ul > li > span.pc_temp_tips_r > span')

    for rank, song, length_of_time in zip(ranks, songs, length_of_times):
        data = {
            'rank': rank.get_text().strip(),  # 排名
            'singer': song.get_text().split('-')[0].strip(),  # 歌手
            'name': song.get_text().split('-')[1].strip(),  # 歌曲名
            'url': song.get('href'),  # 歌曲链接
            'length_of_time': length_of_time.get_text().strip()  # 时长
        }
        print(data)
        return data


if __name__ == '__main__':
    get_info('http://www.kugou.com/yy/rank/home/1-8888.html?from=rank')
    top500_list = ['http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(num) for num in range(1, 3)]  # range(1, 24)显示所有页
    for url in top500_list:
        get_info(url)
        time.sleep(2)
