import datetime
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
load_dotenv()

logger.info("VERSION: 1.0.2")
logger.info("Creating Client...")
client = TelegramClient("SESSION", int(os.environ["API_ID"]), os.environ["API_HASH"])
FOLDER_PATH = Path(os.environ["FOLDER_PATH"])
DEBUG = os.environ["DEBUG"] == "true"

async def handle_file_event(event):
    r = await event.message.download_media(FOLDER_PATH)
    base_filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    extension = Path(r).suffix

    new_path = FOLDER_PATH / f"{base_filename}{extension}"

    # if path exists, add a number to the filename
    n = 1
    while new_path.exists() and n < 1000:
        new_path = FOLDER_PATH / f"{base_filename}_{n}{extension}"
        n += 1

    os.rename(r, new_path)
    logger.info("Saved to %s", new_path)

"""
Note for future:
delete incoming=True to allow for quick testing
"""
@client.on(events.NewMessage(incoming=not DEBUG))
async def handler(event):
    if event.message.photo:
        logger.info("Saving Photo")
        await handle_file_event(event)
    elif event.message.video:
        logger.info("Saving Video")
        await handle_file_event(event)
    elif event.message.media and not (event.message.sticker):
        logger.info("Saving File")
        await handle_file_event(event)


logger.info("Starting...")
client.start(
    phone=os.environ["TELEGRAM_PHONE"], password=os.environ["TELEGRAM_PASSWORD"]
)
client.run_until_disconnected()
