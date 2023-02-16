import logging
import time

import instaloader

from controller.notificator import Notificator

KEYWORDS = ["PR", "pr"]

logger = logging.getLogger(__name__)


class Target(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.last_check_timestamp = time.time()


class Watcher(object):
    def __init__(self, user_id, password, webhook_url, targets, interval_sec):
        self.user_id = user_id
        self.password = password
        self.notificator = Notificator(webhook_url)
        self.targets = [Target(user_id) for user_id in targets]
        self.interval_sec = interval_sec

    def check(self):
        try:
            loader = instaloader.Instaloader()
            loader.login(self.user_id, self.password)
        except Exception as e:
            logger.error(f"login failed. error={e}")
            return

        for target in self.targets:
            counter = 0

            try:
                profile = instaloader.Profile.from_username(loader.context, target.user_id)
            except Exception as e:
                logger.error(f"{target.user_id} not found. error={e}")
                continue

            try:
                posts = profile.get_posts()
            except Exception as e:
                logger.error(f"{target.user_id}'s post not found. error={e}")
                continue

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
            time.sleep(self.interval_sec)
            try:
                self.check()
            except Exception as e:
                logger.error(f"an unexpected error occurred. error={e}")

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
