from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
import threading
import pymysql

def get_directory(): #找出直播分类
    url = 'https://www.douyu.com/directory'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    partitons = soup.find_all('li', class_='layout-Classify-item')
    res = list()
    for item in partitons[:7]:  #只找前7款游戏
        href = item.find('a')['href']
        game = item.find('a').text
        dict = {
            'name': game,
            'url': href
        }
        res.append(dict)   #返回一个存储字典的数组
    return res

def get_rooms(directory): #找出房间号
    res = list()
    for item in directory:
        url = 'https://www.douyu.com' + item['url']
        html = requests.get(url).text
        soup = BeautifulSoup(html,'lxml')
        rooms_list = soup.find_all('li',class_='layout-Cover-item')
        tmp = list()
        for r in rooms_list[:15]:
            anchor = r.find('h2').text
            room_num = r.find('a')['href']
            hot = r.find('span', class_='DyListCover-hot').text
            d = {
                'directory' : item['name'],
                'anchor' : anchor,
                'room_num' : room_num,
                'hot': hot
            }
            tmp.append(d)
        res.append(tmp)
    return res

def start_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')  # 不太知道这个有什么影响
    options.add_argument('headless')
    options.add_argument('-disable-images')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver

def quit_webdriver(driver):
    driver.quit()

def get_noble_num(db,driver,rooms):
    for item in rooms:  #只查看每款游戏前15的主播
        url = 'https://www.douyu.com' + item['room_num']
        driver.get(url)
        time.sleep(4)
        count = 0
        while count < 4:
            nobel = driver.find_elements_by_class_name("ChatTabContainer-titleWraper--tabLi")
            #move = driver.find_element_by_class_name('NobleRankTips')
            #ActionChains(driver).move_to_element(move).perform()  # 鼠标移动操作
            #NobleRankList_item = driver.find_elements_by_class_name('NobleRankList-item')  #贵族列表
            noble_num = nobel[1].text[3:-1]
            if noble_num != '0':
                break
            else:
                time.sleep(2)
                count+=1
        write_mysql(db,item['directory'],item['anchor'],item['hot'],noble_num)
        print(item['directory']+'---'+item['anchor'] + ':' + noble_num )
    driver.close()

def connect_mysql():
    db = pymysql.connect('localhost', 'root', '123456', 'testdb')
    return db

def write_mysql(db,dir,anchor,hot,noble_sum):
    cur = db.cursor()
    cur_time = str(time.strftime("%m-%d %H:%M", time.localtime()))
    sql_insert = "insert into anchor_hot_noblesum(time,directory,anchor,hot,noble_sum) values('%s', '%s','%s', '%s','%s')"
    data = (cur_time,dir,anchor,hot,noble_sum)
    cur.execute(sql_insert % data)
    db.commit()

def close_mysql(db):
    db.close()

class myThread (threading.Thread):
    def __init__(self, db,driver,rooms):
        threading.Thread.__init__(self)
        self.rooms = rooms
        self.db = db
        self.driver = driver
    def run(self):
        print ("开始进程：" )
        get_noble_num(self.db,self.driver,self.rooms)
        print ("退出线程：" )

def main():
    dirs = get_directory()
    print('以爬取完目录信息')
    rooms = get_rooms(dirs)
    print('以爬取完房间号信息')
    db = connect_mysql()
    thread_list = list()
    driver = start_webdriver()  #事先打开一个webdriver，否则多进程会打开很多个
    for t in range(len(rooms)):
        thread_list.append(myThread(db,driver,rooms[t]))
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    quit_webdriver()
    close_mysql(db)

if __name__ == '__main__':
    main()