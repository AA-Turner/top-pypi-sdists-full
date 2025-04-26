class TelegramSender:

    import time
    import telegram
    from datetime import datetime
    from dateutil.parser import parse

    def __init__(self, token) -> None:
        self.token = token
        self.lastSendTime = None
        self.sendDelay = 12
        self.__bot = self.telegram.Bot(token)

    @property
    def lastSendTime(self):
        return self._lastSendTime
    
    @lastSendTime.setter
    def lastSendTime(self, value):
        if isinstance(value, str):
            try:
                self._lastSendTime = self.parse(value)
            except:
                self._lastSendTime = value
        elif isinstance(value, self.datetime):
            self._lastSendTime = value
        elif value is None:
            self._lastSendTime = value
        else:
            raise ValueError
    
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, value):
        if isinstance(value, str):
            self._token = value
        elif value is None:
            self._token = value
        else:
            raise ValueError
    
    @property
    def sendDelay(self):
        return self._sendDelay
    
    @sendDelay.setter
    def sendDelay(self, value):
        if isinstance(value, int):
            self._sendDelay = float(value)
        elif isinstance(value, float):
            self._sendDelay = value
        elif value is None:
            self._sendDelay = value
        else:
            raise ValueError

    def send(self, chat_id: str, text: str, retry_count=3, **kwargs):
        if retry_count <= 0:
            print("Failed to send the message after multiple attempts.")
            return None
        try:
            if self.lastSendTime:
                total_diff = (self.datetime.now() - self.lastSendTime).total_seconds()
                if total_diff < self.sendDelay:
                    print(f'마지막 메시지 전송 후 {total_diff}초 입니다.\n{self.sendDelay-total_diff}초 후 메시지를 전송합니다.')
                    self.time.sleep(self.sendDelay-total_diff)
            if kwargs:
                msg = self.__bot.sendMessage(chat_id=chat_id, text=text, **kwargs)
            else:
                msg = self.__bot.sendMessage(chat_id=chat_id, text=text)
            self.lastSendTime = self.datetime.now()
        except Exception as e:
            print(f"Error sending message: {e}")
            self.time.sleep(5)  # 일정 시간 대기 후 재시도
            return self.send(chat_id=chat_id, text=text, retry_count=retry_count-1, **kwargs)
        else:
            return msg

    def send_photo(self, chat_id: str, img_path: str, **kwargs):
        try:
            if self.lastSendTime:
                total_diff = (self.datetime.now() - self.lastSendTime).total_seconds()
                if total_diff < self.sendDelay:
                    print(f'마지막 메시지 전송 후 {total_diff}초 입니다.\n{self.sendDelay-total_diff}초 후 메시지를 전송합니다.')
                    self.time.sleep(self.sendDelay-total_diff)
                    if kwargs:
                        msg = self.__bot.sendPhoto(chat_id=chat_id, photo=open(img_path,'rb'), **kwargs)
                    else:
                        msg = self.__bot.sendPhoto(chat_id=chat_id, photo=open(img_path,'rb'))
                    self.lastSendTime = self.datetime.now()
                else:
                    if kwargs:
                        msg = self.__bot.sendPhoto(chat_id=chat_id, photo=open(img_path,'rb'), **kwargs)
                    else:
                        msg = self.__bot.sendPhoto(chat_id=chat_id, photo=open(img_path,'rb'))
                    self.lastSendTime = self.datetime.now()

            else:
                if kwargs:
                    msg = self.__bot.sendPhoto(chat_id=chat_id, photo=open(img_path,'rb'), **kwargs)
                else:
                    msg = self.__bot.sendPhoto(chat_id=chat_id, photo=open(img_path,'rb'))
                self.lastSendTime = self.datetime.now()
        except:
            return self.send_photo(chat_id=chat_id, img_path=img_path)
        else:
            return msg
