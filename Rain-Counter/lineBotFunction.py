import requests
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

class LineBotMessage:
    def __init__(self):
        self.S_token = "rHHbSdfNqCKo5n5cv7VlDzrr9x4MFLEtdfB9e1pEKI1"
        self.headers = {
            "Authorization": "Bearer " + self.S_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def SendToCatWindow(self, S_message):
        
        try:
            params = {"message": S_message}
            r = requests.post("https://notify-api.line.me/api/notify",
                headers=self.headers, params=params)
        except:
            pass