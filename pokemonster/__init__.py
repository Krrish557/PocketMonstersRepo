import logging

from pyrogram import Client

from .config import api_id, hash, token

FORMAT = "[ok] %(message)s"

logging.basicConfig( 

    handlers=[logging.FileHandler("pokemonster\logs\logEvents.txt"), logging.StreamHandler()], 

    level=logging.INFO,

    format=FORMAT, 

    datefmt="[%X]", 

)

logging.getLogger("pyrogram").setLevel(logging.INFO) 


LOGGER = logging.getLogger('[ok]') 

app = Client(
  "client3",
  api_id,
  hash,
  bot_token=token,
  plugins=dict(root="pokemonster.modules")
)