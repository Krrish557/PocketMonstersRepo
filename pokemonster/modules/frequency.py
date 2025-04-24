from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from pokemonster import app
from pokemonster.database import Database

DB = Database()


@app.on_message(filters.group & filters.command(["freqchange", "fchange", "pfrequency"]))
async def frequency(client: Client, message: Message):

    user_id = message.from_user.id
    chat_id = message.chat.id
    ChatMem = await client.get_chat_member(chat_id, user_id)
    if ChatMem.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        try:
            msg_count = int(message.text.split()[1])
        except IndexError or TypeError:
            await message.reply_text("Enter a Valid number between 100 and 500")
            return
        if int(msg_count) < 50 or int(msg_count) > 500:
            await message.reply_text("Enter a Valid number between 100 and 500")
            return
        try:
            await DB.add_frequency(chat_id, msg_count, message.chat.title)
            await message.reply_text(f"Frequency changed to {msg_count} messages.")

        except Exception as e:
            await message.reply_text(f"something went wrong.")
            print(e)
    else:
        await message.reply_text(f"You are not an Administrator in this chat.")
