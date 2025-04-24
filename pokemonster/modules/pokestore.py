import asyncio
import json
import random

from pyrogram import Client, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from pokemonster import app
from pokemonster.database import Database
from pokemonster.db.userdb import USERSINFO

with open("pokedex.json") as f:
    jsondata = json.load(f)

DB = Database()
UI = USERSINFO()
pokemon_data = []
buyData = {}


async def get_type_by_weight(weight):
    if weight == 1:
        ptype = "Common"
    elif weight == 2:
        ptype = "Uncommon"
    elif weight == 3:
        ptype = "Rare"
    elif weight == 4:
        ptype = "Epic"
    elif weight == 5:
        ptype = "Legendary"
    elif weight == 10:
        ptype = "God"
    else:
        ptype = "Unknown"
    return ptype


def pokedata(weight) -> list:
    for pokemon in jsondata['poke']:
        if pokemon['weight'] == weight:
            pokemon_data.append(pokemon)
    return random.choice(pokemon_data)


@app.on_message(filters.command("wallet"))
async def wallet(client: Client, message: Message):
    user_id = message.from_user.id
    user = None
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        user = message.reply_to_message.from_user.first_name
    money = await DB.read_money(user_id)
    await message.reply_text(f"{'You' if not user else user} have {money} PokeCoin in {'your' if not user else 'his/her'} wallet\nEarn more by playing and winning /spawn and /trivia .\nMaximum coins wallet can hold: 10K")


@app.on_message(filters.command(["pstore", "pokestore", "pokemart", "pmart"]), group=7)
async def market_message(client: Client, message: Message):

    user_id = message.from_user.id
    money = await DB.read_money(user_id)
    user_id = message.from_user.id
    money = await DB.read_money(user_id)
    buttons = [[InlineKeyboardButton(text="Common (50 PokeCoin)", callback_data=f"buy:common:{user_id}")], [InlineKeyboardButton(text="Uncommon (100 PokeCoin)", callback_data=f"buy:uncommon:{user_id}")], [InlineKeyboardButton(
        text="Rare (200 PokeCoin)", callback_data=f"buy:rare:{user_id}")], [InlineKeyboardButton(text="Epic (300 PokeCoin)", callback_data=f"buy:epic:{user_id}")], [InlineKeyboardButton(text="Legendary (500 PokeCoin)", callback_data=f"buy:legendary:{user_id}")]]

    await message.reply_text(text=f"What do you wanna buy?\nYou have {money} PokeCoin", reply_markup=InlineKeyboardMarkup(buttons))
    buyData[user_id] = {"item": None, "price": None}


@app.on_callback_query(filters.regex(r"^buy:"))
async def market(client: Client, query: CallbackQuery):
    user_id = query.from_user.id if query.from_user else 0
    buttons2 = [[InlineKeyboardButton("Yes", f"confirm:yes:{user_id}")], [
        InlineKeyboardButton("No", f"confirm:no:{user_id}")]]
    data = query.data.split(":")[1]
    data_id = int(query.data.split(":")[-1])

    if user_id == data_id:
        if buyData[user_id]["item"] is None and buyData[user_id]["price"] is None:
            money = await DB.read_money(user_id)
            if data == "common":
                if money >= 50:
                    buy_stuff = "1"
                    price = 50
                else:
                    await query.message.edit("You dont have Enough Money!")
                    return
            elif data == "uncommon":
                if money >= 100:
                    buy_stuff = "2"
                    price = 100
                else:
                    await query.message.edit("You dont have Enough Money!")
                    return
            elif data == "rare":
                if money >= 200:
                    buy_stuff = "3"
                    price = 200
                else:
                    await query.message.edit("You dont have Enough Money!")
                    return
            elif data == "epic":
                if money >= 300:
                    buy_stuff = "4"
                    price = 300
                else:
                    await query.message.edit("You dont have Enough Money!")
                    return
            elif data == "legendary":
                if money >= 500:
                    buy_stuff = "5"
                    price = 500
                else:
                    await query.message.edit("You dont have Enough Money!")
                    return
            else:
                await query.message.reply_text("Invalid Query Selected")
                buyData.pop(user_id)
                return

        buyData[user_id] = {"item": buy_stuff, "price": price}
        rare_poke = await get_type_by_weight(buy_stuff)
        await query.message.reply_to_message.reply_text(text=f"Are You sure you want to buy {rare_poke} Pokemon, worth {price} PokeCoin?", reply_markup=InlineKeyboardMarkup(buttons2))

    else:
        await query.answer("Not for you.")


@app.on_callback_query(filters.regex(r"^confirm"), group=7)
async def confirm(client: Client, query: CallbackQuery):
    user_id = query.from_user.id
    username = query.message.from_user.username
    data = query.data.split(":")[1]
    data_id = int(query.data.split(":")[-1])

    if user_id == data_id:
        if buyData[user_id]["item"] is not None and buyData[user_id]["price"] is not None:
            if data == "yes":
                prev_money = await DB.read_money(user_id)
                info = pokedata(int(buyData[user_id]["item"]))
                pid = info["id"]
                pname = info["name"]
                print(f"\n\n\n{info}\n\n\n\n")
                UI.save_info(query.message.chat.id, user_id, pid)
                new_money = prev_money-buyData[user_id]["price"]
                await DB.subtract_pokecoin(user_id, buyData[user_id]["price"])
                await query.edit_message_text(f"Added {pid}. {pname.capitalize()} to your pokedex in {query.message.chat.title}.\nYou Have {new_money} PokeCoin left")
                await asyncio.sleep(300)
                await query.message.delete()
                pokemon_data.clear()
                buyData.pop(user_id)

            elif data == "no":
                await query.edit_message_text("Please visit Again!")
                await asyncio.sleep(300)
                await query.message.delete()
                pokemon_data.clear()
                buyData.pop(user_id)
            else:
                await query.edit_message_text("Invalid")
    else:
        await query.answer("Not for You.")
