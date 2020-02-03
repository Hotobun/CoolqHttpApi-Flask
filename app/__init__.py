from flask import Flask
import sys 
sys.path.append(".") 
from app.coolq.coolq_sdk import coolq_bp 

 

def create_app(): 
    app = Flask(__name__)

    app.register_blueprint(coolq_bp)
 
     
    return app

if __name__ == "__main__":
    print("hello world")

    