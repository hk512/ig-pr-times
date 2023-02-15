import json


class Configure(object):
    def __init__(self, config_file_path):
        with open(config_file_path, "r") as f:
            data = json.load(f)

        self.user_id = data["user_id"]
        self.password = data["password"]
        self.webhook_url = data["webhook_url"]
        self.targets = data["targets"]
