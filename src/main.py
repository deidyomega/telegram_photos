import os
import sys
import time
from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging
from webdav3.client import Client

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
load_dotenv()

logger.info("Creating Client...")
client = TelegramClient("SESSION", os.environ["API_ID"], os.environ["API_HASH"])


def webdavhandle(filename):
    options = {
        "webdav_hostname": os.environ["WEBDAV_HOSTNAME"],
        "webdav_login": os.environ["WEBDAV_LOGIN"],
        "webdav_password": os.environ["WEBDAV_PASSWORD"],
    }

    client = Client(options)
    client.verify = False
    logger.info("Sending to remote")
    client.upload_sync(
        remote_path=f"Photos/Telegram/{filename}".replace(
            os.environ["FOLDER_PATH"] + "/", ""
        ),
        local_path=filename,
    )
    logger.info("Package delievered")


async def handle_file_event(event):
    r = await event.message.download_media(os.environ["FOLDER_PATH"])
    webdavhandle(r)
    os.remove(r)


# This is our update handler. It is called when a new update arrives.
@client.on(events.NewMessage)
async def handler(event):
    if event.message.out:
        return
    if event.message.photo:
        logger.info("Saving Photo")
        await handle_file_event(event)
    elif event.message.video:
        logger.info("Saving Video")
        await handle_file_event(event)
    elif event.message.media and not (event.message.sticker):
        logger.info("Saving File")
        await handle_file_event(event)
    else:
        logger.info("not doing anything")


logger.info("Starting...")
client.start(
    phone=os.environ["TELEGRAM_PHONE"], password=os.environ["TELEGRAM_PASSWORD"]
)
client.run_until_disconnected()
