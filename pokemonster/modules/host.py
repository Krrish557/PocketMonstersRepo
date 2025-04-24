from pyrogram import Client, filters

from pokemonster import app


@app.on_message(filters.command(['alive', 'about', 'hosting']), group=-4)
async def start(client, message):
  await message.reply_text("the bot is hosted by @SpiralTechDivision")
