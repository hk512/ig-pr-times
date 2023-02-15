import requests
import json


class Notificator(object):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def notify(self, payload):
        _ = requests.post(url=self.webhook_url, data=json.dumps(payload))
