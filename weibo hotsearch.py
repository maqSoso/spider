import requests
from bs4 import BeautifulSoup

filename = '微博热搜'

f = open(filename, 'w' , encoding='utf-8')
url = 'https://s.weibo.com/top/summary'

requ = requests.get(url).text
soup = BeautifulSoup(requ,'lxml')
title = soup.find_all('td', class_='td-02')
res = list()
for i in range(len(title)):
    tmp = title[i].get_text()
    name = tmp.split('\n')
    web = 'https://s.weibo.com' + title[i].find('a')['href']
    f.writelines(str(i) + name[1]+ ' '+ web+'\n')

f.close()
print('保存成功')
