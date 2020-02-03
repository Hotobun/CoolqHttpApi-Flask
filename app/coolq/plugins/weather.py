import requests, time, json

def get_weather(city='北京'):
    urldemo = "https://api.easyapi.com/weather/city.json?cityName={}"
    head = {
        'user-agent':'mozilla/5.0',
        'referer':'https://weather.easyapi.com/',
    }
    r = requests.get(urldemo.format(city), headers=head)
    response = r.json()
    if response['status'] == "1":
        data = response['data']
        uptime = time.localtime(data['realtime']['dataUptime'])
        uptime = "最后更新 {}时{}分\n".format(uptime.tm_hour, uptime.tm_min) 
        temperature = '当前温度 {}° {}\n'.format(data['realtime']['weather']['temperature'], data['realtime']['weather']['info'])
        wind = data['realtime']['wind']
        wind = '{}{} {}{}\n'.format(wind['offset'],wind['direct'],wind['windspeed'],wind['power'])     
        quality = "空气质量{} {}\n".format(data['pm25']['pm25']['quality'],data['pm25']['pm25']['pm25'])
        des = data['pm25']['pm25']['des']
        or_info = data['weather'][1]['info']
        infos = [int(x) for x in  [or_info['night'][2],or_info['dawn'][2],or_info['day'][2]]]
        info = '{} {}°~{}°\n'.format(data['realtime']['city_name'],min(infos), max(infos))
        return uptime + info + temperature + wind + quality + des

def get_weather_of_city(city: str) -> str: 
    result = get_weather(city)
    if result:
        return result 

if __name__ == "__main__":
    a = get_weather_of_city('上海浦东')
    if a:
        print(a)