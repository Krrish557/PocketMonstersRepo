from pyrogram import filters
from pyrogram.types import Message

from pokemonster import app
from pokemonster.database import Database

db = Database()

# filter incoming messsages to bot in groups and update user info
@app.on_message(filters.group & filters.incoming & ~filters.bot)
async def watcher(_, message: Message):
    id = message.from_user.id
    un = message.from_user.username or "None"
    fn = message.from_user.first_name
    await db.update_user(id, un, fn)
