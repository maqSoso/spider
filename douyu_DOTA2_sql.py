import requests
from bs4 import BeautifulSoup
import pymysql
import time

def get_DOTA2_anchors():
    url = 'https://www.douyu.com/g_DOTA2'
    html = requests.get(url).text
    soup = BeautifulSoup(html,'lxml')
    anchor = soup.find_all('div',class_='DyListCover HeaderCell is-href')
    res = list()
    for item in anchor[:20]:
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
        res.append(d)
        #res.append('房间名：'+ name +  '\n'+'房间号:'+ numb + '\n' + '热度:'+ hot + '\n' + '主播:'+ user +'\n' +'========================' + '\n')
    return res


def writeTosql(detail_list,curtime,dbconnextion):
    cur = dbconnextion.cursor()
    table_name = 'dota_'+curtime
    sql_create_table = 'create table '+ table_name + '(Name varchar(30),User varchar(30),Hot varchar(10),Numb int)'
    cur.execute(sql_create_table)  #新建一张表

    for i in detail_list:
        sql_insert = "insert into " + table_name + "(Name,User,Hot,Numb) values('%s', '%s','%s', '%d')"
        data = (i['name'],i['user'],i['hot'],int(i['numb']))
        cur.execute(sql_insert % data)


def readFromsql(curtime,dbconnextion):
    table_name = 'dota_' + curtime
    cursor = dbconnextion.cursor()
    sql_read = 'select * from ' + table_name
    cursor.execute(sql_read)
    try:
        # 执行SQL语句
        cursor.execute(sql_read)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            name = row[0]
            user = row[1]
            hot = row[2]
            numb = row[3]
            # 打印结果
            print("name=%s,user=%s,hot=%s,numb=%d" % \
                  (name, user, hot, numb))
    except:
        print("Error: unable to fetch data")

def main():
    curtime = time.strftime("%m%d_%H%M%S", time.localtime())
    db = pymysql.connect('localhost', 'root', '123456', 'testdb')
    detail_list = get_DOTA2_anchors()
    writeTosql(detail_list,curtime,db)
    readFromsql(curtime,db)

    db.commit()
    db.close()

if __name__ == '__main__':
    main()