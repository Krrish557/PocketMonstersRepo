from pyrogram import filters
from dotenv import load_dotenv
import os

load_dotenv()

devs = [6149191605, 5146000168, 1344569458, 2065219675, 861432102, 1432756163, 6279469935]
users_filt = filters.user(devs)

api_id = int(os.getenv("API_ID"))
hash = os.getenv("API_HASH")
token = os.getenv("BOT_TOKEN")

MONGO_URI = os.getenv("MONGO_URI_1")
MONGO_NAME = os.getenv("MONGO_NAME_1")

MONGO_URI2 = os.getenv("MONGO_URI_2")
MONGO_NAME2 = os.getenv("MONGO_NAME_2")
