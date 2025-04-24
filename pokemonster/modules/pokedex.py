import json
import random

from pyrogram import *
from pyrogram.types import *

from pokemonster import *
from pokemonster.db.userdb import USERSINFO, Pokemons

user_poke = {}
pagelimit = 10
favourite_pokemon = []

async def make_collection(data:list, length:int=10):
    collection = [data[i:i+length] for i in range(0,len(data),length)]
    return collection

async def send_paged_data(message: Message, pokedex: list, userid: int, edit: bool = False, page: int=0):
    global user_poke
    messagepage = []
    count = {}
    for element in pokedex:
        if element not in count:
            count[element] = 1
        else:
            count[element] += 1
    pt = sorted(set(pokedex))
    pt = await make_collection(pt)
    for poke in pt[page]:
        returned_value = Pokemons.select_name(poke)
        if returned_value:
            messagepage.append(
                f"🆔 ID: `{poke}`\n Pokemon: {returned_value.capitalize()}   x{count[poke]}")

    if len(messagepage) != 0:
        text = f"➯ 𝗬𝗼𝘂𝗿 𝗣𝗼𝗸𝗲𝗱𝗲𝘅 𝗜𝗻 𝗚𝗿𝗼𝘂𝗽 {message.chat.title} (Page {page+1} of {len(pt)}):\n\n"
        text += '\n\n'.join(messagepage)
    else:
        text = f"{message.from_user.first_name}'s Pokedex is empty in {message.chat.title}."

    keyboard = []
    if len(pt) > 1:
        if page > 0:
            keyboard.append([InlineKeyboardButton(
                '◀️ Prev', callback_data=f'prev#{page}#{userid}')])
        if page+1 < len(pokedex):
            keyboard.append([InlineKeyboardButton(
                'Next ▶️', callback_data=f'next#{page}#{userid}')])

    if len(keyboard) > 0:
        markup = InlineKeyboardMarkup(keyboard)
    else:
        markup = None
    u_in = USERSINFO().get_user_db(message.chat.id, message.from_user.id)
    exe1 = False
    if u_in:
        exe1 = u_in["fav_pok"]
    # if user dont have favourite pokemon
    if not exe1:
        if edit:
            await app.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.id,
                text=text,
                reply_markup=markup
            )
        else:
            await message.reply_text(
                text=text,
                reply_markup=markup
            )
    # if user have favourite pokemon
    else:
        exe2 = Pokemons.select_link(exe1)
        
        # if user favourite pokemon have no image
        if exe2 == None:
            if edit:
                await app.edit_message_text(	
                    chat_id=message.chat.id,	
                    message_id=message.id,	
                    text=text,	
                    reply_markup=markup	
                )
            else:
                await message.reply_text(	
                    text=text,	
                    reply_markup=markup	
                )
        # if user favourite pokemon have image
        else:
            if edit:
                await app.edit_message_caption(	
                    chat_id=message.chat.id,	
                    message_id=message.id,	
                    caption=text,	
                    reply_markup=markup	
                )
            else:
                await message.reply_photo(
                    photo=exe2,
                    caption=text,
                    reply_markup=markup,
                )

@app.on_message(filters.command("pokedex"))
async def cmdhandler(c: Client, message: Message):
    try:
        if not message.from_user:
            await message.reply_text("Looks like you are not an user")
            return
        chatid = message.chat.id
        userid = message.from_user.id
        plist = USERSINFO().pokeList(chatid, userid)
        if plist:
            pokedex = sorted(plist)
        else:
            pokedex = []
        if not pokedex:
            await message.reply_text(f"{message.from_user.first_name}'s Pokedex is empty in {message.chat.title}.")
        else:
            await send_paged_data(message, pokedex, userid)
    except Exception as e:
        await message.reply_text(e)
        return


@app.on_callback_query(filters.regex("^next#") | filters.regex("^prev#"),group=69)
async def pagination_callback_handler(app, query: CallbackQuery):
    action, page, userid = query.data.split('#')
    page = int(page)
    if query.from_user.id != int(userid):
        return await query.answer('You are not the owner of this message.', show_alert=True)

    pokedex = sorted(USERSINFO().pokeList(query.message.chat.id, query.from_user.id))

    if action == "next":
        await send_paged_data(query.message, pokedex, int(userid), True, page + 1)
        return

    elif action == "prev":
        await send_paged_data(query.message, pokedex, int(userid), True, page - 1)
        return
    


@app.on_message(filters.command("pfav"))
async def favourite_pokemon_function(c: Client, message: Message):
    if not message.from_user:
        await message.reply_text("Looks like you are not an user")
        return
    chatid = message.chat.id
    userid = message.from_user.id
    UI = USERSINFO()
    pokedex = UI.pokeList(chatid, userid)
    fav_p = message.command
    if len(fav_p) != 2:
        await message.reply_text("**USAGE**\n/pfav [id of pokemon]")
        return
    try:
        fav_p = int(fav_p[1])
    except KeyError:
        await message.reply_text("Pokemon id should be numeric")
        return
    if fav_p == 0:
        UI.update_fav_pok_to_none(message.chat.id, message.from_user.id)
        return
    if fav_p in pokedex:
        UI.update_fav_pok(message.chat.id, message.from_user.id,fav_p)
        await message.reply_text(f"Your favourite pokemon have been set.")
    else:
        await message.reply_text(f"You Havn't Caught this Pokemon.")

@app.on_message(filters.command('rmfav'))
async def remove_favourite(c:Client, m:Message):
    if not m.from_user:
        await m.reply_text("Looks like you are not an user")
        return
    UI = USERSINFO()
    await m.reply_text("Your Favourite Pokemon have been Removed.")
    UI.update_fav_pok_to_none(m.chat.id, m.from_user.id)

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

async def get_gen_by_id(id):
    if id>0 and id<=151:
        r = 'Kanto (Generation I)'
    elif id>=152 and id<=251:
        r = "Johto (Generation II)"
    elif id>=252 and id<=386:
        r = "Hoenn (Generation III)"
    elif id>=387 and id<=493:
        r = "Sinnoh (Generation IV)"
    elif id>=494 and id<=649:
        r = "Unova (Generation V)"
    elif id>=650 and id<=721:
        r = "Kalos (Generation VI)"
    elif id>=722 and id<=809:
        r = "Alola (Generation VII)"
    elif id>=810 and id<=900:
        r = "Galar (Generation VIII)"
    elif id>=901 and id<=1010:
        r = "Paldea (Generation IX)"
    else:
        r = "Unknown"
    return r    

@app.on_message(filters.command(["pinfo","pokemoninfo"]))
async def get_pokemon_info(c: Client, m: Message):
    split = m.command
    if len(split) != 2:
        await m.reply_text("**USAGE**\n/pinfo [pokemon id or pokemon name]")
        return
    dd = await m.reply_text("🔍")
    try:
        poke = int(split[1])
        inte = True
        p_info = Pokemons.get_po_info(poke)
        pokename = p_info["name"].capitalize()
    except ValueError:
        poke = split[1]
        inte = False
        p_info = Pokemons.get_po_info_by_name(poke)
        pokename = poke.capitalize()
    
    
    if not p_info:
        await dd.delete()
        await m.reply_text(f"Unable to find any pokemon with {'id' if inte else 'query'} {poke}")
        return
    ptype = await get_type_by_weight(p_info["weight"])
    region = await get_gen_by_id(p_info['id'])
    txt = f"""
⚡️ Extracted pokemon info from database ⚡️ 

➖➖➖➖➖➖➖➖➖➖➖
🆔 Pokemon ID: `{p_info['id']}`
🔅 Pokemon name: `{pokename}`
💎 Pokemon rarity: `{ptype}`
📍 Pokemon Location: `{region}`
➖➖➖➖➖➖➖➖➖➖➖
"""
    is_user = False
    if m.from_user:
        is_user = True
        chat = m.chat.id
        u_in = m.from_user.id
        pokelist = USERSINFO().pokeList(chat,u_in)
        if poke in pokelist:
            total = len([i for i in pokelist if poke == i])
            have = f"\n\n✅ You have this pokemon x{total}"
        else:
            have = "\n\n❌ You don't have this pokemon"    

    if is_user:
        txt += have
    pic = Pokemons.select_link(p_info['id'])
    await dd.delete()
    await m.reply_photo(pic,caption=txt)
    return

@app.on_message(filters.command("updatepower"))
async def update_my_power(c: Client, m: Message):
    try:
        user = m.from_user.id
        chat = m.chat.id
        UI = USERSINFO()
        polist = UI.pokeList(chat,user)
        if not polist:
            await m.reply_text("You haven't caught any pokemon yet")
            return
        ms = await m.reply_text("Updating your power this may take upto a minute")
        p_w = 0
        for i in polist:
            x = Pokemons.get_po_info(int(i))
            p_w += x["weight"]
        UI.update_total_poke_pow(chat,user,p_w)
        await ms.edit_text(f"Updated your power to {p_w}")
        return
    except Exception as e:
        await ms.edit_text(e)
        return
