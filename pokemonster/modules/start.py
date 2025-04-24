import random

from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import (ChatMember, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from pokemonster import app

button = [[InlineKeyboardButton(
    text="ADD ME", url="http://t.me/pocketmonsters_bot?startgroup=new"),
    InlineKeyboardButton("News",url="https://t.me/PocketMonstersUpdates")]]


def random_text(message):
    responses = [
        f"Are you ready to catch pokemons and become the best of the best trainer of this group, {message.from_user.first_name}?",
        f"Get your Pokeballs ready and start your journey, {message.from_user.first_name}!",
        f"It's time to catch some pokemons, {message.from_user.mention}! Are you ready?",
        f"Let's see who can catch the most powerful pokemons, {message.from_user.mention}. Are you up for the challenge?",
        f"Are you ready to become the very best, like no one ever was, {message.from_user.first_name}?",
        f"Get ready to embark on an epic adventure and catch some amazing pokemons, {message.from_user.username}.",
        f"{message.from_user.first_name}, the world of pokemons is waiting for you. Are you ready to catch 'em all?",
        f"Get your Pokeballs and start catching some amazing pokemons, {message.from_user.mention}!",
        f"Are you ready to explore the world of pokemons and become the greatest trainer of all time, {message.from_user.username}?",
        f"{message.from_user.first_name}, it's time to catch some pokemons and show everyone who's the best trainer in this group!",
        f"Get ready to catch some amazing pokemons and become the ultimate trainer, {message.from_user.first_name}!",
        f"Let's catch some pokemons and have some fun, {message.from_user.mention}!",
        f"{message.from_user.first_name}, the world of pokemons is waiting for you. Are you ready to catch 'em all?",
        f"Are you ready to start your journey and catch some amazing pokemons, {message.from_user.mention}?",
        f"Get ready to catch some amazing pokemons and become the ultimate trainer, {message.from_user.username}!",
        f"Are you ready to become the best trainer in this group, {message.from_user.first_name}? Let's catch some pokemons!",
        f"Get your Pokeballs and start your journey to catch some amazing pokemons, {message.from_user.mention}!",
        f"{message.from_user.first_name}, are you ready to catch some amazing pokemons and become the ultimate trainer?",
        f"Get ready to catch some amazing pokemons and show everyone who's the best trainer in this group, {message.from_user.username}!",
        f"Are you ready to become the very best, like no one ever was, {message.from_user.mention}?",
        f"Get your Pokeballs ready and start your journey to catch some amazing pokemons, {message.from_user.first_name}!",
        f"Let's catch some pokemons and have some fun, {message.from_user.username}!",
        f"{message.from_user.first_name}, it's time to catch some amazing pokemons and become the ultimate trainer!",
        f"Get ready to catch some amazing pokemons and become the best trainer in this group, {message.from_user.mention}!",
        f"Are you ready to start your journey and catch some amazing pokemons, {message.from_user.first_name}?",
        f"Get your Pokeballs and start your journey to become the ultimate trainer, {message.from_user.username}!",
        f"{message.from_user.first_name}, it's time to catch some amazing pokemons and show everyone who's the best trainer in this group!",
        f"Get ready to catch some amazing pokemons and become the ultimate trainer, {message.from_user.mention}!",
        f"Are you ready to start your journey and catch some amazing pokemons, {message.from_user.username}",
        "Get ready to embark on an adventure to become the best Trainer in this group!",
        "𝗪𝗲𝗹𝗰𝗼𝗺𝗲 to 𝗼𝘂𝗿 𝗣𝗼𝗸𝗲𝗺𝗼𝗻 𝗧𝗿𝗮𝗶𝗻𝗲𝗿 bot! 🎉 Get ready to catch 'em all and become the best Trainer in the group! 🔥",
        "🔥👋 𝗛𝗲𝘆 𝘁𝗵𝗲𝗿𝗲, 𝗠𝗮𝘀𝘁𝗲𝗿 𝗧𝗿𝗮𝗶𝗻𝗲𝗿! Ready to embark on an adventure to catch some amazing pokemons? 🌟",
        "🌟🔴 Welcome to our Pokemon Trainer community! Are you ready to train hard, catch rare pokemons and become the ultimate champion? 🏆 Let's do this!",
        "🎉👋 Hello there, new Trainer! Ready to start your journey to catch and train the best pokemons in the group? 🌟 Let's go!",
        "🚀🎮 Ready to blast off into the world of Pokemon and become the best Trainer in the group? 🏆 It's time to catch 'em all and show off your skills!",
        "🌟🔥 Get ready to catch some amazing pokemons and become the strongest Trainer in the group! 💪 Let's show everyone what we're made of!",
        "🐾🎉 Are you ready to catch some rare and powerful pokemons and rise to the top of the leaderboard? 🏆 Let's go on an adventure and become the best Trainer in the group!",
        "🎉👋 Welcome to our Pokemon catching community! Get ready to show off your catching skills, trade pokemons and have fun! 🌟",
        "🌟🔴 Attention all Trainers! It's time to catch 'em all and become the best of the best in the group! 💪 Are you ready?",
        "🚀🔥 Ready to blast off on an adventure to catch some amazing pokemons and become the ultimate Trainer? 🌟 Let's do this!",
        "🐾🎮 Get ready to embark on a journey to become the best Pokemon Trainer in the group! 🏆 Train hard, catch rare pokemons and become a champion!",
        "🌟👋 Hello new Trainer! Ready to catch some amazing pokemons and become the best of the best in the group? 🎉 Let's go on an adventure!",
        "🔴💪 Are you ready to battle other Trainers, catch rare pokemons and become the ultimate champion in the group? 🏆 Let's do this!",
        "🎮🔥 Get ready to show off your Pokemon catching skills and become the best Trainer in the group! 💪 Let's catch 'em all and have some fun!",
        "🚀🌟 Welcome to our Pokemon catching community! Get ready to embark on an adventure, trade pokemons and become the ultimate Trainer! 🏆",
        "🐾👋 Hello there, new Trainer! Ready to catch some amazing pokemons, have fun and become the strongest in the group? 🌟 Let's do this!"
        "It's time to show off your skills and catch some amazing pokemons in this group.",
        "Are you ready to become the ultimate Pokemon master in this group?",
        "Let's catch 'em all! Get ready to become the best Trainer in this group!",
        "The journey to becoming a Pokemon master begins now! Are you ready?",
        "It's time to train hard and catch some incredible pokemons in this group!",
        "Get ready to battle other trainers and show off your amazing skills!",
        "It's time to catch some amazing pokemons and rise to the top of the group's leaderboard!",
        "The road to becoming the very best starts here. Are you ready to catch some pokemons?",
        "Let's embark on a journey to catch and train the best pokemons in this group!",
        "Get ready to explore the world of Pokemon and become the ultimate Trainer in this group!",
        "The adventure to become the best Pokemon Trainer in this group starts now!",
        "Are you ready to catch some amazing pokemons and become the most skilled Trainer in this group?",
        "Let's show off our Pokemon catching skills and become the best Trainer in this group!",
        "It's time to catch some rare and powerful pokemons and become the strongest Trainer in this group!",
        "Get ready to battle against other trainers and become the champion of this group!",
        "Time to show everyone what you're made of! Catch some pokemons and become the top Trainer in this group.",
        "Are you ready to catch some legendary pokemons and become the envy of all the trainers in this group?",
        "Let's catch some amazing pokemons and become the most popular Trainer in this group!",
        "Are you ready to catch some amazing pokemons and dominate this group with your skills?",
        "Let's catch some rare and legendary pokemons together and become the most powerful Trainers in this group!",
        "It's time to build the ultimate team of pokemons and conquer every challenge in this group!"
    ]
    return f"{random.choice(responses)}"


@app.on_chat_member_updated()
async def on_chat_member_updated(client: Client, message: Message):
    if isinstance(message.new_chat_member, ChatMember) and message.new_chat_member.user.id == client.me.id:
        chat_id = message.chat.id
        welcome_text = f"{random_text(message)} \n\Make me admin to play."
        await client.send_message(chat_id, welcome_text)


@app.on_message(filters.command('''start''') & ~filters.bot, group=-4)
async def start(client: Client, message: Message):
    me = await app.get_me()
    if message.chat.type == ChatType.PRIVATE:
        await message.reply_text("""This Doesn't look like its a group :/

☇ Click below to add me ☇""", reply_markup=InlineKeyboardMarkup(button))
    else:
        Check = await app.get_chat_member(message.chat.id, me.id)
        if Check.status == ChatMemberStatus.ADMINISTRATOR:
            await message.reply_text(random_text(message))
        else:
            await message.reply_text("Make me admin to play.")
