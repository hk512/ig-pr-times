import instaloader

from controller.notificator import Notificator

INTERVAL_SEC = 60 * 5
LIMIT = 10


class Target(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.latest_post_data = None


class Watcher(object):
    def __init__(self, user_id, password, webhook_url, targets):
        self.user_id = user_id
        self.password = password
        self.notificator = Notificator(webhook_url)
        self.targets = [Target(user_id) for user_id in targets]

    # def check(self):
    #     loader = instaloader.Instaloader()
    #     loader.login(self.user_id, self.password)
    #     loader.dirname_pattern = "src/{target}"
    #
    #     for target in self.targets:
    #         posts = instaloader.Profile.from_username(loader.context, target.user_id).get_posts()
    #         latest_post_data = target.latest_post_data
    #
    #         for post in posts:
    #             if latest_post_data is None or latest_post_data > latest_post_data:
    #                 target.latest_post_data = post.data
    #             post.data
    # if target.latest_post is None:
    #
    # caption = post.caption
    # hashtag = post.caption_hashtags

    def run(self):
        loader = instaloader.Instaloader()
        loader.login(self.user_id, self.password)
        loader.dirname_pattern = "src/{target}"

        posts = instaloader.Profile.from_username(
            loader.context, self.targets[0].user_id
        ).get_posts()
        count = 0
        for post in posts:
            print(post.date)
            print(type(post.date))

            count += 1
            # loader.download_post(post, self.targets[0])
            if count > 0:
                break

    def send_pr_post(self, user_id, url, caption, icon, image_path):
        self.notificator.notify(
            payload={
                "username": "ig-pr-times",
                "attachments": [
                    {
                        "author_name": f"{user_id}",
                        "author_link": f"{url}",
                        "author_icon": f"{icon}",
                        "title": "PR投稿",
                        "text": f"{caption}",
                        "image_url": f"{image_path}",
                        "footer": "Send from Python",
                    }
                ],
            }
        )
