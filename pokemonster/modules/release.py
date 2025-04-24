import json

from pyrogram import *
from pyrogram.types import *

from pokemonster import *
from pokemonster.db.userdb import USERSINFO, Pokemons

with open('pokedex.json') as f:
    data = json.load(f)

@app.on_message(filters.command("release"))
async def release(c: Client, message: Message):
    if not message.from_user:
        await message.reply_text("Looks like you are not an user")
        return
    UI = USERSINFO()
    text = int(message.text.split()[1])
    name = Pokemons.select_name(text)
    mapfetch = UI.pokeList(message.chat.id, message.from_user.id)    
    
    if text in mapfetch:
        await app.send_message(chat_id = message.chat.id, text = f"We will miss you {name.capitalize()}!!")
        UI.save_info(message.chat.id, message.from_user.id, text,reduce=True)
    else:
        await app.send_message(chat_id = message.chat.id, text = "You don't own this Pokemon")
        return