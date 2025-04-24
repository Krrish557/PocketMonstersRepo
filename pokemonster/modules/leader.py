from pyrogram import Client, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from pokemonster import *
from pokemonster.database import Database
from pokemonster.db.userdb import USERSINFO

UI = USERSINFO()
DB = Database()

get_val = {
    4 : "K",
    5 : "K",
    6 : "K",
    7 : "M",
    8 : "M",
    9 : "M",
    10 : "B",
    11 : "B",
    12 : "B",
    13 : "T",
    14 : "T",
    15 : "T",
    16 : "Q"
}

async def convert_to_name(num):
    str_num = str(num)
    length = len(str_num)
    if length < 4:
        return str_num
    if length in [5,8,11,14]:
       divisor = 10**(length-2)
    elif length in [9,12,15]:
        divisor = 10**(length-3)
    elif length == 6:
        divisor = 10**(length-4)
    elif length > 16:
        alias = "Q"
        net = length - 16
        divisor = 10**(length-net) 
    else:
        divisor = 10**(length-1)
    try:
        alias = get_val[length]
    except KeyError:
        pass
    nums = round(int(num)/divisor,2)
    return f"{nums} {alias}"

@app.on_message(filters.command(["leader", "winner"]))
async def leader(c: Client, message: Message):
    chat_id = message.chat.id
    exe = UI.sorted_weight_db(chat_id)
    buttons = [
        [
            InlineKeyboardButton("Richest Traniers", f"lead:money"),
            InlineKeyboardButton("LeaderBoard", f"lead:globe")
        ],
        [
            InlineKeyboardButton("Close ❌","trade_close")
        ]
    ]
    if not exe:
        msg = "Can't fetch top trainers from this chat\nNobody has any Pokemon in this Group :(\nCatch some and come back later ;)"
    elif exe:
        msg = f"🏆 Top Pokemon Trainers in {message.chat.title}\n\n"
        i = 1
        if len(exe) > 10:
            exe = exe[:10]
        for i, a in enumerate(exe):
            u = (a["user_id"])
            try:
                c = await app.get_users(u)
                msg += f"> {i+1}. {c.first_name} — {a['poke_pow']}\n"
            except Exception as e:
                msg += f"> {i+1}. {u} — {a['poke_pow']}\n"
    await message.reply_text(text=msg, reply_markup=InlineKeyboardMarkup(buttons))
    return


@app.on_callback_query(filters.regex(r"lead:"))
async def rich(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    data = query.data.split(":")[1]
    if data == "money":
        buttons = [
            [
                InlineKeyboardButton("Chat LeaderBoard", f"lead:chat"),
                InlineKeyboardButton("LeaderBoard", f"lead:globe")
            ],
            [
                InlineKeyboardButton("Close ❌","trade_close")
            ]
        ]
        exe = await DB.sorted_money_database()
        if not exe:
            msg = "Can't fetch richest pokemon trainers"
            await query.answer(msg,True)
        elif exe:
            await query.answer("Fetching Richest Pokemon Trainers globally please wait",True)
            msg = f"🏆 Richest Pokemon Trainers globally \n\n"
            i = 1
            if len(exe) > 10:
                exe = exe[:10]
            for i, a in enumerate(exe):
                u = (a["user_id"])
                coins = await convert_to_name(a['pokecoin'])
                try:
                    c = await app.get_users(u)
                    msg += f"> {i+1}. {c.first_name} — `{coins}`\n"
                except Exception as e:
                    msg += f"> {i+1}. {u} — `{coins}`\n"
            btn = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(msg,reply_markup=btn)
        return
    elif data == "globe":
        exe = UI.sorted_weight_db_global()
        buttons = [
            [
                InlineKeyboardButton("Richest Traniers", f"lead:money"),
                InlineKeyboardButton("Chat LeaderBoard", f"lead:chat")
            ],
            [
                InlineKeyboardButton("Close ❌","trade_close")
            ]
        ]
        if not exe:
            msg = "Can't fetch globally top pokemon trainers"
            await query.answer(msg,True)
        elif exe:
            await query.answer("Fetching Top Pokemon Trainers Globally please wait",True)
            msg = f"🏆 Top Pokemon Trainers Globally \n\n"
            i = 1
            if len(exe) > 10:
                exe = exe[:10]
            for i, a in enumerate(exe):
                u = (a["user_id"])
                try:
                    c = await app.get_users(u)
                    msg += f"> {i+1}. {c.first_name} — {a['poke_pow']}\n"
                except Exception as e:
                    msg += f"> {i+1}. {u} — {a['poke_pow']}\n"
        await query.edit_message_text(msg,reply_markup=InlineKeyboardMarkup(buttons))
        return
    elif data == "chat":
        exe = UI.sorted_weight_db(chat_id)
        buttons = [
            [
                InlineKeyboardButton("Richest Traniers", f"lead:money"),
                InlineKeyboardButton("LeaderBoard", f"lead:globe")
            ],
            [
                InlineKeyboardButton("Close ❌","trade_close")
            ]
        ]
        if not exe:
            msg = "Can't fetch top trainers from this chat\nNobody has any Pokemon in this Group :(\nCatch some and come back later ;)"
            await query.answer(msg,True)
        elif exe:
            msg = f"🏆 Top Pokemon Trainers in {query.message.chat.title}\n\n"
            await query.answer(f"Fetching Top Pokemon Trainers in {query.message.chat.title} please wait",True)
            i = 1
            if len(exe) > 10:
                exe = exe[:10]
            for i, a in enumerate(exe):
                u = (a["user_id"])
                try:
                    c = await app.get_users(u)
                    msg += f"> {i+1}. {c.first_name} — {a['poke_pow']}\n"
                except Exception as e:
                    msg += f"> {i+1}. {u} — {a['poke_pow']}\n"
        await query.edit_message_text(msg,reply_markup=InlineKeyboardMarkup(buttons))
        return

    
