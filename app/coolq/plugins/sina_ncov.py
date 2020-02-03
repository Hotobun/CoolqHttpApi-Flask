import requests
 
sina_ncov_url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json'

def _get(url):
    r = requests.get(url, headers = {'user-agent':'Mozilla/5.0'})  
    r.encoding = 'utf-8' 
    return r.json()['data']

def init_text(item):
    temp = ''
    if int(item.get('conNum', 0)) > 0:
        temp += "确诊{} ".format(item['conNum'])
    elif int(item.get('value', 0)) > 0:
        temp += "确诊{} ".format(item['value'])
    if int(item['susNum']) > 0:
        temp += "疑似{} ".format(item['susNum'])
    if int(item['cureNum']) > 0:
        temp += "治愈{} ".format(item['cureNum'])
    if int(item['deathNum']) > 0:
        temp += "死亡{} ".format(item['deathNum'])
    return temp 

def get_text_data(name, data, head=False, show_all=False):
    worlddata = [] 
    # 新浪数据 确诊人数 国外用value 国内城市用conNum
    if 'value' in data[0]:
        data.sort(key = lambda x : int(x['value']), reverse = True)
    else:
        data.sort(key = lambda x : int(x['conNum']), reverse = True)
    count = {}
    for item in data:
        if 'conNum' not in item:
            item['conNum'] = item['value']
        count['conNum'] = count.get('conNum',0) + int(item['conNum'])
        count['susNum'] = count.get('susNum',0) + int(item['susNum'])
        count['deathNum'] = count.get('deathNum',0) + int(item['deathNum'])
        count['cureNum'] = count.get('cureNum',0) + int(item['cureNum'])
        temp = '{} '.format(item['name']) 
        temp += init_text(item)
        worlddata.append(temp)    
    worldhead = '{} {}'.format(name, init_text(count))
    if head:
        return worldhead.strip("\n")
    result = ''
    
    for text in worlddata if show_all else worlddata[:3]:
        result += text + '\n'
    return worldhead + "\n" + result.strip('\n')

def str_historylist(con, sus, sure, death):
    # 需要4个参数 确诊 疑似 治愈 死亡 
    # all type : str
    result = ''
    result += "确诊{} ".format(con) if con else ''
    result += "疑似{} ".format(sus) if sus else ''
    result += "治愈{} ".format(sure) if sure else ''
    result += "死亡{} ".format(death) if death else ''
    return result

def query_ncov(key, show_all = False): 
    data = _get(sina_ncov_url)
    
    headtime = '新浪{}\n'.format(data['times'])

    all_text = ['世界','疫情','全球']
    chinatext = ['全国','中国','我国','国内','境内']
    worldtext = ['国外','外国', '境外']

    # 历史疫情
    not_month_history = [] 
    for day in data['historylist']:
        if key in day['date']:
            d = day['date'].split('.')
            that_day = '{}月{}日\n'.format(int(d[0]), int(d[1]))
            cn = '全国 {}\n'.format( str_historylist(day['cn_conNum'],day['cn_susNum'], day['cn_cureNum'],day['cn_deathNum']))
            wh = '武汉 {}'.format( str_historylist(day['wuhan_conNum'],day['wuhan_susNum'], day['wuhan_cureNum'],day['wuhan_deathNum']))
            return that_day + cn + wh
        if key.replace('notmonth.','') in day['date']: 
            d = day['date'].split('.')
            that_day = '{}月{}日\n'.format(int(day['date'].split(".")[0]), int(d[1])) 
            cn = '全国 {}\n'.format( str_historylist(day['cn_conNum'],day['cn_susNum'], day['cn_cureNum'],day['cn_deathNum']))
            wh = '武汉 {}'.format( str_historylist(day['wuhan_conNum'],day['wuhan_susNum'], day['wuhan_cureNum'],day['wuhan_deathNum']))
            not_month_history.append(that_day + cn + wh)
    if len(not_month_history) > 0:
        result = ''
        for i in not_month_history:
            result += i
            result += '\n' 
        return result.strip('\n')

    china_head = '全国 确诊{} 疑似{} 治愈{} 死亡{}'.format(data['gntotal'],data['sustotal'],data['curetotal'],data['deathtotal'])
    # 中国疫情
    if key in chinatext and show_all == False: 
        return headtime + china_head
    
    # 境外疫情
    if key in worldtext and show_all == False:
        return headtime + get_text_data('国外',data['otherlist'])

    # 世界疫情
    if key in all_text:
        result = "{}{}\n{}".format(headtime, china_head, get_text_data('国外',data['otherlist'], head=True))
        return result

    # 朝阳特别疫情
    chaoyang = []

    # 省级疫情 
    province_list = data['list']
    city_list = []
    for item in province_list:
        if key == item['name'] or key == item['ename']:
            province_head = '{} '.format(key)
            province_head += init_text(item).strip('\n') 
            if not show_all: 
                return headtime + province_head 
            else:  
                return headtime + get_text_data( item['name'],item['city'],show_all=show_all)
            for city in item['city']:
                city_list.append(city)            
            
    
        # 市级查询   
        for city in item['city']:
            if key in city['mapName']:
                # 朝阳特别疫情
                if key == '朝阳':
                    chaoyang.append("{} {}".format(city['mapName'],init_text(city)))
                    continue
                return headtime + "{} {}".format(city['name'],init_text(city))
    
    # 朝阳疫情
    if chaoyang:
        result = ''
        for i in chaoyang:
            result += i + '\n'
        return headtime + result.strip("\n")

    # 国外疫情
    for item in data['otherlist']:
        if key == item['name']:
            return headtime + "{} {}".format(item['name'], init_text(item))


async def sina_get_ncov_of_city(city: str, show_all = False) -> str:
    result = query_ncov(city, show_all)
    if result:
        return result 

def query_ncov_all(city):
    return query_ncov(city, show_all=True)

if __name__ == "__main__":
    # result = query_ncov('德国')
    result = _get(sina_ncov_url)
    print(result)