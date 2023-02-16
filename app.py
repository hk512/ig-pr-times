import logging
import sys

from controller.watcher import Watcher
from config.config import Configure


logging.basicConfig(
    level=logging.INFO, stream=sys.stdout, format="[%(levelname)s][%(asctime)s] %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = Configure("./config/config.json")

    watcher = Watcher(
        config.user_id, config.password, config.webhook_url, config.targets, config.interval_sec
    )
    watcher.run()
