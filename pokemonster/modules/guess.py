import asyncio
import json
import random
import time
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from pokemonster import app
from pokemonster.database import Database

from ..config import users_filt

# Global variables
with open('pokedex.json') as f:
    data = json.load(f)
unique_event = {}
cooldown = {}
msg_dict = {}
uuid_for_this_event = None

DB = Database()


def uuid_generator():
    now = str(datetime.now())
    ls = ["-", ":", ".", " "]
    final = ""
    for i in now:
        if i in ls:
            final += ""
        else:
            final += i

    return str(final)


@app.on_message(filters.command('spawn'), group=0)
async def hunt(c: Client, message: Message):
    global uuid_for_this_event
    unique_event.clear()
    chat_id = message.chat.id
    if chat_id in cooldown:
        cooldown_expiry = cooldown[chat_id]
        time_left = int(cooldown_expiry - time.time())
        if time_left > 0:
            minutes = time_left // 60
            seconds = time_left % 60
            await message.reply_text(f"Spawn command already used in this Chat\nPlease wait {minutes}:{seconds} seconds before using trivia again.")
            return
    uuid_for_this_event = uuid_generator()
    pokename = rand_poke['name']
    if len(pokename.split(".")) >=2:
            pokename = " ".join([i.strip() for i in pokename.split(".")])
    elif len(pokename.split("-")) >=2:
        pokename = " ".join([i.strip() for i in pokename.split("-")])
    rand_poke = random.choice(data['poke'])
    unique_event[uuid_for_this_event] = {
        "pid": rand_poke['id'],
        "pname": pokename,
        "plink": rand_poke['link'],
        "sent": True,
        "msg_count": 0,
    }
    print(unique_event[uuid_for_this_event])
    msg = await c.send_photo(chat_id=chat_id, photo=unique_event[uuid_for_this_event]['plink'], caption="/Guess what the name of this pokemon is? \n\n\n")
    msg_dict[chat_id] = msg
    cooldown[chat_id] = time.time() + 300
    await asyncio.sleep(60)
    unique_event.clear()
    await msg.delete()


@app.on_message(filters.command("guess") & ~filters.forwarded)
async def guessed_name(c: Client, message: Message):
    global uuid_for_this_event
    try:
        text = message.text.split(None,1)[1]
        if text.strip().lower():
            if uuid_for_this_event and unique_event.get(uuid_for_this_event, {}).get('sent') == True:
                unique_event[uuid_for_this_event]['msg_count'] += 1
                if text == unique_event[uuid_for_this_event]['pname'].lower():
                    if message.from_user.username != None:
                        username = message.from_user.username
                    else:
                        username = message.from_user.first_name
                    coins = await DB.read_money(message.from_user.id)
                    if int(coins) == 10000:
                        response_text = "Correct answer\nBut your wallet already at it's maximum capicty"
                    else:
                        added = 5
                        if int(coins) + 5 > 10000:
                            added = 10000 - int(coins)
                        response_text = f"Correct! 🎉 \nAdded {added} Rubies to your wallet"
                        await DB.add_pokecoin(message.from_user.id, added, username)
                    await message.reply_text(response_text)
                    await msg_dict[message.chat.id].delete()
                    unique_event.clear()
                    cooldown.clear()
                    msg_dict.clear()
                elif text != unique_event[uuid_for_this_event]['pname']:
                    await message.reply_text(f"Wrong Guess, Try Again!")
    except IndexError:
        await message.reply_text(f"Use /spawn to Spawn the pokemon First!")
    except KeyError:
        pass
    except AttributeError:
        await message.reply_text("Format: /guess [Pokemon name]")


@app.on_message(filters.command("endguess") & users_filt)
async def end(client, message: Message):
    unique_event.clear()
    cooldown.clear()
    msg_dict.clear()
    await message.reply_text("Ended Guess sessions")
