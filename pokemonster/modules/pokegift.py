from pyrogram import *
from pyrogram.enums import ParseMode
from pyrogram.types import *

from pokemonster import *
from pokemonster.db.userdb import USERSINFO, Pokemons


# /poketrade 69 76
@app.on_message(filters.command("pgift"))
async def release(c: Client, message: Message):
    if not message.from_user:
        await message.reply_text("Looks like you are not an user")
        return
    UI = USERSINFO()
    try:
        pokemon_id = int(message.text.split()[1])
    except (ValueError , IndexError):
        await app.send_message(chat_id = message.chat.id, text = f"Provide a Pokemon ID;\nUse /help for help.!!")
        return
    name = Pokemons.select_name(pokemon_id)
    user1 = message.from_user.id
    user1dex = UI.pokeList(message.chat.id, user1)    
    if message.reply_to_message:
        # Get the user ID of the user being replied to
        user2 = message.reply_to_message.from_user.id  

        if pokemon_id in user1dex:
            # Deleting from user1
            await app.send_message(chat_id = message.chat.id, text = f"We will miss you {name.capitalize()}!!")
            UI.save_info(message.chat.id, user1, pokemon_id,reduce=True)
            # Adding to user2
            UI.save_info(message.chat.id, user2,pokemon_id)

        else:
            await app.send_message(chat_id = message.chat.id, text = "You don't own this Pokemon")

    else:
        await message.reply_text("You need to reply to a message to get the ID of the user being replied to.")
    
        return

trading = {} #dict be like {chat_id:{from_user:{pok_id :poke_id,to_tak: poke id to take}}} if to_user agree then to_user:poke_id
to_from_u = {} #{chat:{to_user:from_user}}
p_mode = ParseMode.MARKDOWN
@app.on_message(filters.command("ptrade"))
async def trade_pok(c: Client,m: Message):
    if not m.from_user:
        await m.reply_text("Looks like you are not an user")
        return
    if (len(m.command) != 4 and not m.reply_to_message) or (m.reply_to_message and not len(m.command) == 3):
        txt = "**USAGE**\n`/trade <user id | username> <pokemon id to give> <pokemon id to take>`\nIf you are not passing user id reply to user\ne.g.: `/trade <pokemon id to give> <pokemon id to take>`"
        await m.reply_text(text=txt,parse_mode=p_mode)
        return
    if m.reply_to_message:
        to_user = m.reply_to_message.from_user.id
        try:
            poke_id = int(m.command[1])
            poke_id_to = int(m.command[2])
        except ValueError:
            await m.reply_text(text="Pokemon id should be integer type")
            return
    elif len(m.command) == 4:
        try:
            poke_id = int(m.command[2])
            poke_id_to = int(m.command[3])
        except ValueError:
            await m.reply_text(text="Pokemon id should be integer type")
            return
        try:
            to_user = int(m.command[1])
        except ValueError:
            try:
                to_user = (await c.get_users(m.command[1])).id
            except Exception as e:
                await m.reply_text(f"Unable to find the user due to\n{e}")
                return
    UI = USERSINFO()
    mapfetch = UI.pokeList(m.chat.id, m.from_user.id)
    if poke_id not in mapfetch:
        await m.reply_text(f"You don't have any pokemon with id {poke_id}")
        return
    usss = await app.get_users(to_user)
    to_u = UI.pokeList(m.chat.id,to_user)
    if not to_u:
        await m.reply_text(f"{usss.username if usss.username else usss.mention} user don't have any pokemon")
        return
    if poke_id_to not in to_u:
        await m.reply_text(f"{('@'+usss.username) if usss.username else usss.mention} user don't have any pokemon with id {poke_id_to}")
        return
    try:
        for i,j in to_from_u[m.chat.id].items():
            if (m.from_user.id == i or m.from_user.id == j) and (to_u == i or to_u == j):
                await m.reply_text("One trade is already in progress with this user")
                return
    except KeyError:
        pass
    try:
        to_from_u[m.chat.id][to_user] = m.from_user.id
    except Exception:
        to_from_u[m.chat.id].update({to_user : m.from_user.id})
    try:
        trading[m.chat.id][m.from_user.id] = {"val":poke_id,"to_take":poke_id_to}
    except KeyError:
        if not len(trading):
            trading[m.chat.id] = {m.from_user.id:{"val":poke_id,"to_take":poke_id_to}}
        else:
            trading[m.chat.id][m.from_user.id] = {"val":poke_id,"to_take":poke_id_to}
    txt = f"Trade status: In progress:\n{m.from_user.mention} is offering {poke_id} ({Pokemons.select_name(poke_id)}) in excahnge of [your]([This](tg://user?id={to_u}) {poke_id_to} ({Pokemons.select_name(poke_id_to)})\n\nAsk the user to accept or reject the offer"
    kb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Trade 🤝",f"trade_yes_{m.from_user.id}:{to_user}"),
                InlineKeyboardButton("Decline ✋",f"trade_no_{m.from_user.id}:{to_user}")
            ]
        ]
    )
    await m.reply_text(txt,reply_markup=kb)
    return

def clean_data(chat,user,tou):
    try:
        to_from_u[chat][tou].clear()
    except KeyError:
        pass
    try:
        del trading[chat][user]
    except KeyError:
        pass
    return

@app.on_callback_query(filters.regex("^trade_"),group=-1)
async def wanna_trade(c:Client, q: CallbackQuery):
    UI = USERSINFO()
    data = q.data.split("_")
    if len(data) == 2 and data[1] == "close":
        await q.answer("Closed the menu",True)
        await q.message.delete()
        return
    chat = q.message.chat.id
    to_do = data[1]
    userss = data[2].split(":")
    user = int(userss[0])
    to_user = int(userss[1])
    
    
    if q.from_user.id != to_user:
        await q.answer("This trade is not for you",True)
        return
    if to_do == "no":
        await q.answer("Trade is closed by you")
        await q.edit_message_text(chat,f"Trade status: Rejected\nLooks like {q.from_user.mention} don't want to trade")
        clean_data(chat,user,to_user)
        return
    OwO = await app.get_users(user)
    oWo = q.from_user.mention
    if to_do == "yes":
        fav_user_po = UI.get_user_db(chat,user)["fav_pok"]
        fav_user_to = UI.get_user_db(chat,to_user)["fav_pok"]
        to_give = trading[chat][user]["val"]
        to_take = trading[chat][user]["to_take"]
        try:
            UI.save_info(chat,user,to_give,fav_user_po,True)
            UI.save_info(chat,user,to_take,fav_user_po)
            UI.save_info(chat,to_user,to_take,fav_user_to,True)
            UI.save_info(chat,to_user,to_give,fav_user_to)
        except Exception as e:
            await q.edit_message_text(f"Trade status: Abrupted\nError occured:\n{e}")
            return
        txt = f"Trade Status: Complete\nTrade is complete between {OwO.mention} 🤝 {oWo}"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Close", "trade_close")]])
        await q.edit_message_text(txt,reply_markup=kb)
        clean_data(chat,user,to_user)
        return