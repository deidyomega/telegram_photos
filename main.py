import os
import sys
import time
from dotenv import load_dotenv
load_dotenv()
api_id = os.environ['api_id']
api_hash = os.environ['api_hash']

# Import the client
from telethon import TelegramClient, events


# Define some variables so the code reads easier
session = os.environ.get('TG_SESSION', 'printer')

client = TelegramClient('printer', api_id, api_hash)


# This is our update handler. It is called when a new update arrives.
@client.on(events.NewMessage)
async def handler(event):
    if event.message.photo:
        print("Saving Photo")
        await event.message.download_media("/home/omega/Photos/Telegram")
    elif event.message.video:
        print("Saving Video")
        await event.message.download_media("/home/omega/Photos/Telegram")
    elif event.message.media:
        print("Saving Media")
        await event.message.download_media("/home/omega/Photos/Telegram")
    else:
        print("not doing anything")

client.start()
client.run_until_disconnected()
