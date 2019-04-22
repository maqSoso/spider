import requests
from bs4 import BeautifulSoup
import threading
'''
六个线程同时抓取120个主播
'''
class myThread (threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index
    def run(self):
        print ("开始线程：" )
        get_DOTA2_anchors(self.index)
        print ("退出线程：" )

def get_DOTA2_anchors(index):
    url = 'https://www.douyu.com/g_DOTA2'
    html = requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    anchor = soup.find_all('div',class_='DyListCover HeaderCell is-href')
    res = list()
    for item in anchor[index:index+20]:
        name = item.find('h3')['title']
        numb = item.find('a')['href'][1:]
        hot = item.find('span', class_='DyListCover-hot').text
        user = item.find('h2', class_='DyListCover-user').text
        d = {
            'name':name,
            'user':user,
            'hot':hot,
            'numb':numb
        }
        #res.append(d)
        res.append('房间名：'+ name +  '\n'+'房间号:'+ numb + '\n' + '热度:'+ hot + '\n' + '主播:'+ user +'\n' +'========================' + '\n')
    #return res
    print(res)


def define_muti(num):
    thread_list = list()
    for i in range(num):
        thread_list.append(myThread(i*20))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

def main():
    define_muti(6)

if __name__ == '__main__':
    main()