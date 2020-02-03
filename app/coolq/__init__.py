import sys 
sys.path.append(".")

from app.coolq.coolq_sdk import CQHttp
from app.coolq.process import ProcessMessage

bot = CQHttp(api_root='http://172.18.0.2:5700/')

@bot.on_message()
def handle_msg(context):
    # bot.send(context, '你好呀，下面一条是你刚刚发的：')
    # return {'reply': context['message'], 'at_sender': False}
    result = ProcessMessage(context['message'])
    if result: 
        if type(result) == str:
            return {'reply': result, 'at_sender': False}
        else:
            for item in result:
                bot.send(context, item)