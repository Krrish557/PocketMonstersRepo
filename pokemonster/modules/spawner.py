import json
import random

from pyrogram import *
from pyrogram.types import *

from pokemonster import *
from pokemonster.database import Database
from pokemonster.db.userdb import USERSINFO

from ..config import users_filt

# Text
run_away_texts = ['''You Missed the Pokemon!''', '''Oh No! The Pokemon broke free!''', '''Darn! The Pokemon Broke free!''',
                  '''ᴀᴡᴡ! ɪᴛ ᴀᴘᴘᴇᴀʀᴇᴅ ᴛᴏ ʙᴇ ᴄᴀᴜɢʜᴛ!''', '''ᴀᴀʀɢʜ! ᴀʟᴍᴏsᴛ ʜᴀᴅ ɪᴛ!''', '''ɢᴀʜ! ɪᴛ ᴡᴀs sᴏ ᴄʟᴏsᴇ, ᴛᴏᴏ!''']

# Global Variables
with open('pokedex.json') as f:
    data = json.load(f)
spawned = {}
poke_in = {}

DB = Database()
UI = USERSINFO()

# Spawn


@app.on_message(filters.group & filters.all, group=0)
async def send_image(c: Client, message: Message):
    chatid = message.chat.id
    try:
        if spawned[f'{chatid}']["val"]:
            return
    except KeyError:
        pass
    try:
        spawned[f'{chatid}']["appear_msg"] += 1
    except KeyError:
        spawned[f'{chatid}'] = {"val": False,
                                "msg_count": 0, "appear_msg": 1, "m_id": 0}
    msg_freq = await DB.read_frequency(chatid)

    if spawned[f'{chatid}']["appear_msg"] % msg_freq == 0:
        poke_inn = random.choice(data['poke'])
        pokename = poke_inn['name']
        if len(pokename.split(".")) >=2:
            pokename = " ".join([i.strip() for i in pokename.split(".")])
        elif len(pokename.split("-")) >=2:
            pokename = " ".join([i.strip() for i in pokename.split("-")])
        pokeid = poke_inn["id"]
        pokelink = poke_inn['link']
        poke_in[f'{chatid}'] = {"name": pokename,
                                "pokeid": pokeid, "pokelink": pokelink}
        spawned[f'{chatid}'] = {"appear_msg": 0}

        img_send = await app.send_photo(chat_id=message.chat.id, photo=pokelink,
                                        caption=f"A Pokemon appeared!\nAdd it to your Pokedex by typing /catch")
        spawned[f'{chatid}'] = { "msg_count": 0, "val": True, "m_id": img_send.id}

        """msg_count for run appear_msg for number of message after the pokemon appears 
        and m_id to store message id and then delete it when caught or ran"""
        raise ContinuePropagation

# Catch


@app.on_message(filters.command('catch') & filters.group & ~filters.forwarded, group=1)
async def catch(c: Client, message: Message):
    try:
        if not message.from_user:
            await message.reply_text("Looks like you are not an user")
            return
        chatid = message.chat.id
        userid = message.from_user.id
        if not spawned.get(f'{chatid}')["val"]:
            await message.reply_text("How can you catch a pokemon without seeing them?")
            return
        elif spawned.get(f'{chatid}')["val"]:
            try:
                guessed_name = message.text.split(None, 1)[1]
            except IndexError:
                await message.reply_text(text="Type your guessed pokemon name after /catch to catch it")
                return
            pokename = poke_in[f'{chatid}']['name'].lower()
            pok_na = poke_in[f'{chatid}']['name'].split(None)
            pok_na.sort(key=lambda i: len(i))
            pok_na = pok_na[-1].lower()
            if guessed_name.lower() in [pokename, pok_na]:
                pid = poke_in[f'{chatid}']["pokeid"]
                UI.save_info(chatid, userid, pid)
                caught_texts = [f'''All Right!  Pokemon {pokename.capitalize()} was caught by {message.from_user.mention}!''',
                                f'''Gotcha! Pokemon {pokename.capitalize()} was caught by {message.from_user.mention}!''']

                await message.reply_text(text=f"{random.choice(caught_texts)}")
                poke_in[f'{chatid}'].clear()
                spawned[f'{chatid}'] = {"val": False,
                                        "msg_count": 0, "appear_msg": 0, "m_id": 0}
            else:
                await message.reply_text(text="Sorry, wrong guess. Keep trying!")
    except Exception as e:
        await message.reply_text(e)

# Run


@app.on_message(filters.group, group=2)
async def run(c: Client, message: Message):
    chatid = message.chat.id
    try:
        if not spawned[f'{chatid}']["val"]:
            raise ContinuePropagation
    except KeyError:
        raise ContinuePropagation
    if spawned.get(f'{chatid}')["val"]:
        if spawned[f"{chatid}"]["msg_count"] == 30:
            try:
                await app.send_message(message.chat.id, text=f'''{random.choice(run_away_texts)}\nBetter luck next time.\nIts name was {poke_in[f'{chatid}']['name'].capitalize()}\nRemember it next time.''')
            except KeyError:
                pass
            try:
                await app.delete_messages(message.chat.id, int(spawned[f"{chatid}"]["m_id"]))
            except Exception:
                pass
            spawned[f'{chatid}'] = {"val": False,
                                    "msg_count": 0, "appear_msg": 0, "m_id": 0}
            poke_in[f'{chatid}'].clear()
        else:
            spawned[f"{chatid}"]["msg_count"] += 1
            raise ContinuePropagation


@app.on_message(filters.command("cooldown") & users_filt, group=8)
async def cooldown(client: Client, message: Message):
    chatid = message.chat.id
    msg_freq = await DB.read_frequency(chatid)
    msg_left = msg_freq - spawned[f'{chatid}']["appear_msg"]
    await message.reply_text(f"{msg_left} messages for pokemon to spawn in {message.chat.title}.")
