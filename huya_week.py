import json
import urllib.request

url = 'https://www.huya.com/520888'
Burning = 'https://www.huya.com/cache5min.php?m=WeekRank&do=getItemsByPid&pid=1061583819'
LongDD = 'https://www.huya.com/cache5min.php?m=WeekRank&do=getItemsByPid&pid=7017534'
html = urllib.request.urlopen(Burning).read()
html = json.loads(html)
names = html['data']['vWeekRankItem']
for i in names:
    print(i['sNickName'])