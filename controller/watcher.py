import time

import instaloader

from controller.notificator import Notificator

INTERVAL_SEC = 60 * 60

KEYWORDS = ["PR", "pr"]


class Target(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.last_check_timestamp = time.time()


class Watcher(object):
    def __init__(self, user_id, password, webhook_url, targets):
        self.user_id = user_id
        self.password = password
        self.notificator = Notificator(webhook_url)
        self.targets = [Target(user_id) for user_id in targets]

    def check(self):
        loader = instaloader.Instaloader()
        loader.login(self.user_id, self.password)

        for target in self.targets:
            posts = instaloader.Profile.from_username(loader.context, target.user_id).get_posts()
            profile = instaloader.Profile.from_username(loader.context, target.user_id)
            counter = 0
            for post in posts:
                counter += 1
                if post.date.timestamp() > target.last_check_timestamp:
                    caption = post.caption
                    for keyword in KEYWORDS:
                        if keyword in caption:
                            self.send_pr_post(post, profile)
                            break

                if counter > 3 and post.date.timestamp() < target.last_check_timestamp:
                    break

            target.last_check_timestamp = time.time()

    def run(self):
        while True:
            try:
                self.check()
            except Exception as e:
                print(e)

            time.sleep(INTERVAL_SEC)

    def send_pr_post(self, post, profile):
        self.notificator.notify(
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
