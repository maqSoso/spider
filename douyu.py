import requests
from bs4 import BeautifulSoup

def get_directory():
    headers = {
        'Host': 'www.douyu.com',
        'Referer': 'https://www.douyu.com/directory',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'
    }
    url = 'https://www.douyu.com/directory'
    html = requests.get(url, headers = headers).text

    soup = BeautifulSoup(html,'lxml')
    partiton = soup.find_all('li', class_='layout-Classify-item')
    res = list()
    for item in partiton:
        href = 'http://www.douyu.com' + item.find('a')['href']
        game = item.find('a').text
        dict1 = {'name':game, 'url':href}
        res.append(dict1)
    return res

def get_anchor(href):
    html = requests.get(href).text
    soup = BeautifulSoup(html,'lxml')

    anchor = soup.find_all('div',class_='DyListCover HeaderCell is-href')
    res = list()
    for item in anchor[:20]:
        name = item.find('h3')['title']
        numb = item.find('a')['href'][1:]
        hot = item.find('span', class_='DyListCover-hot').text
        user = item.find('h2', class_='DyListCover-user').text

        res.append('房间名：'+ name +  '\n'+'房间号:'+ numb + '\n' + '热度:'+ hot + '\n' + '主播:'+ user +'\n' +'========================' + '\n')
    return res

def save(detail_list, directory_title):
    filename = directory_title + '.txt'
    f = open(filename,'w',encoding='utf-8')
    for i in detail_list:
        f.write(i)

def main():
    results = get_directory()
    result = results[6]
    href = result['url']
    directory_title = result['name']
    detail_list = get_anchor(href)
    save(detail_list,directory_title)

if __name__ == '__main__':
    main()