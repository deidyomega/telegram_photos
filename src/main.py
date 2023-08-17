import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
load_dotenv()

logger.info("VERSION: 1.0.0")
logger.info("Creating Client...")
client = TelegramClient("SESSION", os.environ["API_ID"], os.environ["API_HASH"])


async def handle_file_event(event):
    r = await event.message.download_media(os.environ["FOLDER_PATH"])
    logger.info("Saved to %s", r)

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
