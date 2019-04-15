from bs4 import BeautifulSoup
import requests

def get_html(url):
    return requests.get(url).text

def html_parse():
    for url in all_page():
        soup = BeautifulSoup(get_html(url),'lxml')

        alldiv = soup.find_all('div', class_='pl2')
        names = [a.find('a')['title'] for a in alldiv]

        authers = soup.find_all('p', class_='pl')
        auther = [a.get_text() for a in authers]

        starspan = soup.find_all('span',class_='rating_nums')
        scores = [s.get_text() for s in starspan]

        comments = soup.find_all('span',class_='inq')
        comment = [c.get_text() for c in comments]

        for a,b,c,d, in zip(names,auther,scores,comment):
            name = '书名:' + str(a) + '\n'
            aut = '作者:' + str(b) + '\n'
            socre = '评分:' + str(c) + '\n'
            sum = '简介:' + str(d) + '\n'
            data = name + aut + socre +sum
            f.writelines(data + '=======================' + '\n')


def all_page():
    baseurl = 'https://book.douban.com/top250?start='
    allpage = list()
    for i in range(0,226,25):
        allpage.append(baseurl+str(i))
    return allpage

filename = '豆瓣图书Top250.txt'

f = open(filename, 'w', encoding='utf-8')

html_parse()
f.close()
print('保存成功。')