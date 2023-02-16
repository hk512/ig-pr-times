import requests
import json


class Notificator(object):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def notify(self, payload):
        _ = requests.post(url=self.webhook_url, data=json.dumps(payload))

    def notify_pr_post(self, post, profile):
        self.notify(
            payload={
                "username": "ig-pr-times",
                "attachments": [
                    {
                        "author_name": f"{post.owner_username}",
                        "author_link": f"https://www.instagram.com/{post.owner_username}",
                        "author_icon": profile.profile_pic_url,
                        "text": f"{post.caption}",
                        "image_url": f"{post.url}",
                    }
                ],
            }
        )

    def notify_error(self, message):
        self.notify(
            payload={
                "username": "ig-pr-times",
                "attachments": [
                    {
                        "text": f"{message}",
                    }
                ],
            }
        )


