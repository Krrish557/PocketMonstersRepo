import io
import subprocess
import sys
import traceback
from datetime import datetime
from re import sub

from pyrogram import Client, enums, filters
from pyrogram.errors import RPCError
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardButton as ikb
from pyrogram.types import InlineKeyboardMarkup as ikm
from pyrogram.types import Message

from pokemonster import *
from pokemonster.database import Database
from pokemonster.db.userdb import *

from ..config import devs, users_filt

DB = Database()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.command(["run", "eval", "e"]) & users_filt, group=69)
async def eval(client, message):
    if len(message.text.split()) < 2:
        return await message.reply_text("Input Not Found!")

    cmd = message.text.split(maxsplit=1)[1]
    status_message = await message.reply_text("Processing ...")
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    end = datetime.now()
    ping = (end-start).microseconds / 1000
    final_output = "<b>📎 Input</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>📒 Output</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n\n"
    final_output += f"<b>✨ Taken Time</b>: {ping}<b>ms</b>"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await status_message.edit_text(final_output)


@app.on_message(filters.command("stats") & users_filt)
async def give_bot_stats(c: Client, m: Message):
    UI = USERSINFO()
    tt = await m.reply_text("Fetching stats")
    try:
        total_grp = UI.get_unique_chat_ids_count(True)
        total_users = UI.get_unique_users(True)
        total_catch = UI.get_total_catch()
    except Exception as e:
        await tt.edit_text(e)
        return
    txt = f"""Poketmonster bot current stats:
Total groups : {total_grp}
Total users : {total_users}
Total catches in {total_grp} : {total_catch}"""

    await tt.edit_text(txt)
    return

# Rizoel 5294360309
# Raze 861432102
# Krrish 2065219675
# Ezio 1344569458
only_me = [2065219675, 1344569458, 5294360309, 861432102]


@app.on_message(filters.command("broadcast") & filters.user(only_me))
async def broadcast_message(c: Client, m: Message):
    UI = USERSINFO()
    try:
        grps = UI.get_unique_chat_ids_count(False)
        users = UI.get_unique_users(False)
    except Exception as e:
        await m.reply_text(e)
        return
    repl = m.reply_to_message
    if not repl:
        await m.reply_text("Reply to a message to broadcast it")
        return
    tt = await m.reply_text("Broadcasting...")
    gr = 0
    for i in grps:
        try:
            await repl.forward(i)
        except Exception:
            gr += 1
            pass
    us = 0
    for i in users:
        try:
            await repl.forward(int(i))
        except Exception:
            us += 1
            pass
    await tt.edit_text(f"Broadcasting completed\nFailed to broadcast message to {gr} groups and {us} users")
    return


@app.on_message(filters.command("devcmds"))
async def give_dev_cmds(_, m: Message):
    txt = """
/eval - Used for evaluation of codes.
/compensate - Used to compensate (give) pokemon which are lost due to some error on our side.
/broadcast - Used to broadcast msgs.
/deluser - Used to delete a user
/endguess - Used to end all Guess sessions.
/endtriv - Used to end all Trivia sessions.
/cooldown - Used to chekc how many messages left for pokemon to spawn.
/devpay - Used to Give Money to users.
/devlist - This Will list all devs.
/deduct -Used to take money from users
/restwallet [reply to user] : Clear the wallet of the replied user if replied to a message or rest wallet of every user
    """
    await m.reply_text(txt)


@app.on_message(filters.command("deduct") & filters.user(only_me))
async def deduct_from_user(c: Client, message: Message):
    try:
        user_to_pay_info = message.reply_to_message.from_user
        try:
            money = -abs(int(message.text.split()[1]))
            await DB.add_pokecoin(user_to_pay_info.id, money, user_to_pay_info.username)
            await message.reply_text(f"Added {money} PokeCoins to {user_to_pay_info.mention}'s wallet.")
            return
        except ValueError:
            await message.reply_text("Amount should be integer")
            return
        except IndexError:
            await message.reply_text("Please Enter a valid Amount to pay!\n\nFormat:/deduct {amount}\n<while replying tp the user you want to pay>")
            return
    except AttributeError:
        await message.reply_text("Please reply to the user you want to pay to!\n\nFormat:/deduct {amount}\n<while replying tp the user you want to pay>")
        return


@app.on_message(filters.command("compensate") & filters.user(only_me))
async def give_users_free_pok(c: Client, m: Message):
    repl = m.reply_to_message
    if not repl:
        await m.reply_text("USAGE:\n/comensate [reply to user] pokemon id u want to give")
        return
    elif not repl.from_user:
        await m.reply_text("Reply to an user")
        return
    poke = m.text.split(None)[1:]
    try:
        poke_id = [int(i.strip()) for i in poke]
    except ValueError:
        await m.reply_text("Pass pokemon id")
        return
    except IndexError:
        await m.reply_text("Pass pokemon id which you want to give")
        return
    new = []
    try:
        for i in poke_id:
            USERSINFO().save_info(m.chat.id, repl.from_user.id, int(i))
            new.append(str(i))
    except Exception as e:
        await m.reply_text(e)
        return
    poke_id = ", ".join(new)
    await m.reply_text(f"Successfully given {repl.from_user.mention} {poke_id}")
    return


@app.on_message(filters.command("deluser") & filters.user(only_me))
async def delete_a_user(c: Client, m: Message):
    repl = m.reply_to_message
    UI = USERSINFO()
    if not repl:
        try:
            _id = m.text.split(None, 1)[1]
        except Exception:
            await m.reply_text(f"USAGE\nReply to an user or pass their ObjectID")
            return
        try:
            xx = UI.delete_userby_id(_id)
        except Exception as e:
            await m.reply_text(e)
            return
        if xx:
            txt = "Successfully deleted user"
        else:
            txt = "No user found to delete"

        await m.reply_text(txt)
        return
    else:
        userid = repl.from_user.id
        chatid = m.chat.id
        try:
            xx = UI.delete_user(chatid, userid)
        except Exception as e:
            await m.reply_text(e)
            return
        if xx:
            txt = "Successfully deleted user"
        else:
            txt = "No user found to delete"

        await m.reply_text(txt)
        return


@app.on_message(filters.command("devpay") & users_filt)
async def devpay(client: Client, message: Message):
    try:
        user_to_pay_info = message.reply_to_message.from_user
        try:
            money = abs(int(message.text.split()[1]))
            await DB.add_pokecoin(user_to_pay_info.id, money, user_to_pay_info.username)
            await message.reply_text(f"Added {money} PokeCoins to {user_to_pay_info.mention}'s wallet.")
            print(f"added {money} pokeCoins by {message.from_user.username}")
            return
        except ValueError:
            await message.reply_text("Amount should be integer")
            return
        except IndexError:
            await message.reply_text("Please Enter a valid Amount to pay!\n\nFormat:/devpay {amount}\n<while replying tp the user you want to pay>")
            return
    except AttributeError:
        await message.reply_text("Please reply to the user you want to pay to!\n\nFormat:/devpay {amount}\n<while replying tp the user you want to pay>")
        return


@app.on_message(filters.command("devlist") & users_filt)
async def devlist(client: Client, message: Message):
    txt = "Developers of @PocketMonsters_bot:\n"
    for i in devs:
        txt += "->\t" + (await app.get_users(i)).first_name + "\n"
    await message.reply_text(txt)

@app.on_message(filters.command("resetwallet") & filters.user(only_me),18)
async def rest_wallets(c: Client, m: Message):
    if m.reply_to_message and m.reply_to_message.from_user:
        user = m.reply_to_message.from_user.id
        txt = f"Are you sure you want to rest pokecoins to 0 of {m.reply_to_message.from_user.first_name}?"
    else:
        user = "all"
        txt = "Are you sure you want to rest pokecoins to 0 of all users?"

    btn = [
        [
            ikb("Yes",f"restwallet:{user}"),
            ikb("No","resetwallet:no")
        ]
    ]

    await m.reply_text(txt,reply_markup=ikm(btn))

@app.on_callback_query(filters.regex(r"^resetwallet:"),18)
async def rest_wallet_conformational(c: Client, q: CallbackQuery):
    if q.from_user and (q.from_user.id not in only_me):
        await q.answer("Stay in your limit")
        return
    print("rest wallet")
    split = q.data.split(":")[1]

    if split == "no":
        await q.answer("Cancelled reset wallet protocol")
        await q.edit_message_text("Cancelled reset wallet protocol")
        return
    
    elif split.isdigit():
        await DB.make_coins_0(int(split))
        await q.answer(f"Reset the pokecoins to 0 of {split}")
        await q.edit_message_text("Successfully reset the pokecoins to 0")
        return
    else:
        users = await DB.sorted_money_database()
        if not users:
            await q.edit_message_text("No user found")
        else:
            x = await q.edit_message_text("Starting to reset the wallets")
            for user in users:
                await DB.make_coins_0(int(user["user_id"]))
            await q.answer("Reset pokecoins of all users")
            await x.edit_text("Successfully reset pokecoins of all users")
            return

    

