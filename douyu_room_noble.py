from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

def main():
    options = webdriver.ChromeOptions()
    #options.add_argument('--no-sandbox')  #不太知道这个有什么影响
    options.add_argument('headless')
    options.add_argument('-disable-images')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    url = 'http://www.douyu.com/2009'  #还是选取酒神直播间
    driver.get(url)

    time.sleep(8)

    nobel = driver.find_elements_by_class_name("ChatTabContainer-titleWraper--tabLi")
    nobel[1].click() #总共有三个，[1]为贵族class
    noble_num = nobel[1].text[3:-1]  #房间贵族数
    print('当前房间贵宾数为：'+noble_num + '\n')
    #time.sleep(1)
    move = driver.find_element_by_class_name('NobleRankTips')
    ActionChains(driver).move_to_element(move).perform()   #鼠标移动操作
    table = driver.find_elements_by_class_name('NobleRankList-item')

    #noble_list = list()

    for item in table:
        print(item.text.replace('\n','  ') )    #我就不知道第十个人名怎么就打不出来
        #print('=======')

        #tmp = item.text.split('\n')
        #noble_list.append(tmp[-1])  #去掉牌子，只取后面的名字

    #print(noble_list)   #输入形式还没想好

    driver.close()
    driver.quit()

main()