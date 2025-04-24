from pyrogram import Client, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from pokemonster import app
from pokemonster.database import Database

DB = Database()


@app.on_message(filters.command("pay"))
async def pay(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        user_to_pay = message.reply_to_message.from_user.id
        try:
            money = message.text.split()[1]
            buttons = [[InlineKeyboardButton("Yes", f"pay:yes:{user_id}:{user_to_pay}:{money}")], [
                InlineKeyboardButton("No", f"pay:no:{user_id}:{user_to_pay}:{money}")]]

            await message.reply_text(text=f"Are you sure you want to pay {money} PokeCoins to {message.reply_to_message.from_user.mention}?", reply_markup=InlineKeyboardMarkup(buttons))

        except IndexError:
            await message.reply_text("Please Enter a valid Amount to pay!\n\nFormat:/pay {amount}\n<while replying tp the user you want to pay>")
    except AttributeError:
        await message.reply_text("Please reply to the user you want to pay to!\n\nFormat:/pay {amount}\n<while replying tp the user you want to pay>")


@app.on_callback_query(filters.regex(r"pay"))
async def cbpay(client: Client, query: CallbackQuery):
    cb_user_id = query.message.reply_to_message.from_user.id
    data = query.data.split(":")[1]
    user_id = int(query.data.split(":")[2])
    user_to_pay = int(query.data.split(":")[3])
    money = int(query.data.split(":")[4])
    user_prev_money = await DB.read_money(user_id)
    user_to_pay_info = await app.get_users(user_to_pay)

    if cb_user_id == user_id:
        if data == "no":
            await query.message.reply_text("Transaction Cancelled")
            return
        elif data == "yes":
            if int(user_prev_money) >= int(money) and int(money) > 0:
                await DB.add_pokecoin(user_to_pay, money, user_to_pay_info.username)
                await DB.subtract_pokecoin(user_id, money)
                await query.message.edit_caption(f"Added {money} PokeCoins to {user_to_pay_info.mention}'s wallet.")
            else:
                await query.message.edit_caption(f"You dont have enough money.")

    else:
        print("cb user id != user id")
        await query.answer("Not For you")
