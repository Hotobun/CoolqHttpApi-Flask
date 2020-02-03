import sys 
sys.path.append(".") 
from app.coolq.plugins import weather, sina_ncov, daily

commands = {
    '天气': weather.get_weather_of_city,
    '疫情': sina_ncov.query_ncov,
    '详情': sina_ncov.query_ncov, 
    '一句': daily.get_dialy, 
}

kwargs = {
    '详情': True, 
}

def process(message):
    for key in commands:
        if key in message:
            args = message.replace(key, '')
            return commands[key](args,kwargs.get(key)) if kwargs.get(key) else commands[key](args)

def ProcessMessage(message: str) -> dict:
    if message:  
        result = process(message) 
        return result

if __name__ == "__main__":
    print("hello world!")