import requests
import datetime
import random

def get_content(date=False):
    url = 'http://open.iciba.com/dsapi/' 
    if date:
        url += "?date={}-{:02d}-{:02d}".format(date.year, date.month, date.day)
    res = requests.get(url, headers={'user-agent':'mozilla/5.0'})
    if res.status_code == 200:
        try:
            return res.json()['content'], res.json()['note']
        except:
            return get_content(random_date())

def random_date():
    start_datetime = datetime.date(2018,1,1)
    today = datetime.date.today()
    start_today_days = (today - start_datetime).days
    return today - datetime.timedelta(days=random.randint(0, start_today_days))

def get_dialy(text = False):
    if text == '每日':
        return get_content()
    elif text in ("再来","随机"):
        return get_content(random_date())

if __name__ == "__main__":
    print(get_dialy("随机"))