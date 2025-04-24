import asyncio
import json
import random
import time

from pyrogram import Client, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from pokemonster import app
from pokemonster.database import Database

from ..config import devs

with open('trivia.json') as f:
    data = json.load(f)

active_trivia = {}
user_cooldowns = {}

DB = Database()


@app.on_message(filters.group & filters.command('trivia'), group=84)
async def trivia(_, message):
    user_id = message.from_user.id
    if user_id in user_cooldowns:
        cooldown_expiry = user_cooldowns[user_id]
        time_left = int(cooldown_expiry - time.time())

        if time_left > 0:
            minutes = time_left // 60
            seconds = time_left % 60
            await message.reply_text(f"Please wait {minutes}:{seconds} seconds before using trivia again.")
            return
        else:
            try:
                user_cooldowns.pop(user_id)
            except KeyError:
                pass
            try:
                active_trivia.pop(user_id)
            except KeyError:
                pass

    if user_id in active_trivia:
        await message.reply_text("You already have an active trivia session.")
        return

    user_cooldowns[user_id] = time.time() + 1800

    quesdata = random.choice(data['results'])
    question = quesdata["question"]
    correct_answer = quesdata["correct_answer"]
    incorrect_answers = quesdata['incorrect_answers']
    all_options = incorrect_answers + [correct_answer]
    random.shuffle(all_options)

    button_list = [
        [InlineKeyboardButton(
            option.capitalize(), callback_data=f"triv:{option.strip().lower()}:{user_id}")]
        for option in all_options
    ]

    question = await message.reply_text(
        question,
        reply_markup=InlineKeyboardMarkup(button_list)
    )

    active_trivia[user_id] = {
        "correct_answer": correct_answer.lower(),
        "expiration_time": time.time() + 15,
        "answered": False
    }
    print(active_trivia)

    await asyncio.sleep(15)
    try:
        if not active_trivia[user_id]["answered"]:
            print("Time up!")
            await question.edit_text("Time Up!")
            active_trivia.pop(user_id, None)
    except KeyError as e:
        print(e)


@app.on_callback_query(filters.regex(r"triv"))
async def handle_callback_query(client, query: CallbackQuery):
    selected_option = query.data.split(':')[1]
    cb_user_id = int(query.data.split(":")[2])
    user_id = query.from_user.id if query.from_user else 0
    if user_id == cb_user_id:
        active_session = active_trivia.get(int(user_id))
        if active_session:
            print("active session found")
            coins = await DB.read_money(cb_user_id)
            correct_option = active_session["correct_answer"]
            if selected_option == correct_option:
                active_trivia[cb_user_id]["answered"] = True
                if int(coins) == 10000:
                    response_text = "Correct answer\nBut your wallet already at it's maximum capicty"
                else:
                    added = 10
                    if int(coins) + 10 > 10000:
                        added = 10000 - int(coins)
                    response_text = f"Correct! 🎉 \nAdded {added} Rubies to your wallet"
                    await DB.add_pokecoin(cb_user_id, added, query.from_user.username)
            else:
                response_text = "Incorrect Answer! ❌"
                active_trivia[cb_user_id]["answered"] = True
                active_trivia.pop(cb_user_id, None)
            await query.message.edit_text(query.message.text + f"\n\n{response_text}")
        else:
            print("active session not found")

    else:
        await query.answer("Not for you")


@app.on_message(filters.command("endtriv") & filters.user(devs), group=84)
async def endtriv(client: Client, message: Message):
    user_cooldowns.clear()
    active_trivia.clear()
    await message.reply_text("Ended all Active Trivia Sessions")
