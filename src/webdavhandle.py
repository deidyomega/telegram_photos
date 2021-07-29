from webdav3.client import Client
import os
from dotenv import load_dotenv
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(filename):
    options = {
        'webdav_hostname': os.environ['WEBDAV_HOSTNAME'],
        'webdav_login':    os.environ['WEBDAV_LOGIN'],
        'webdav_password': os.environ['WEBDAV_PASSWORD']
    }

    client = Client(options)
    client.verify = False
    logger.info('Sending to remote')
    client.upload_sync(remote_path=f"Photos/Telegram/{filename}".replace(os.environ['FOLDER_PATH'] + "/",""), local_path=filename)
    logger.info('Package delievered')

if __name__ == '__main__':
    main(path="")