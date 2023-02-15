from controller.watcher import Watcher
from config.config import Configure

if __name__ == "__main__":
    config = Configure("./config/config.json")

    watcher = Watcher(
        config.user_id, config.password, config.webhook_url, config.targets
    )
    watcher.run()
