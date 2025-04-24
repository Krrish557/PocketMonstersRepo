import logging
import random

from pyrogram import idle
from pyrogram.types import BotCommand

from pokemonster import app
from pokemonster.database import Database

DB = Database()

FORMAT = "[KRRISH] %(message)s"
logging.basicConfig(
    handlers=[logging.FileHandler(
        "pokemonster\logs\logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
)
LOGGER = logging.getLogger('[KRRISH]')


async def load_start():
    LOGGER.info("[INFO]: Booting.....")

    try:
        LOGGER.info("[INFO]: PYROGRAM BOTS STARTED")

    except Exception as e:
        LOGGER.info(
            f">>>>>>>>>>>>>>>Bot wasn't able to send message in your log channel\n\nERROR: {e}")


async def cmds(app):
    await app.set_bot_commands(
        [
            BotCommand("start", "To check if the bot is running"),
            BotCommand("catch", "Catch the spawned Pokemon"),
            BotCommand("pokedex", "View your Pokedex Collection"),
            BotCommand(
                "ptrade", "Exchange your Pokemons. Type /ptrade for the manual"),
            BotCommand("pfav", "Choose your favourite Pokemon"),
            BotCommand(
                "pgift", "Show your care to new members. Type /pgift for the manual"),
            BotCommand("winner", "See who's the best"),
            BotCommand("leader", "See who's the best"),
            BotCommand("release", "Release the Pokemom"),
            BotCommand("pinfo", "Get info about a Pokemon"),
            BotCommand("devcmds", "Get all dev cmds"),
            BotCommand(
                "updatepower", "If you think your power is not according to the pokemon you have caught"),
            BotCommand("spawn", "Test your knowledge"),
            BotCommand("guess", "Catch the Spawned Pokemon"),
            BotCommand("poketrivia", "Test your knowledge about pokemons"),
            BotCommand(
                "freqchange", "This command will change the number of messages after which pokemon will spawn in your group."),
            BotCommand(
                "pokestore", "You can buy Pokemon of different rarity from here"),
            BotCommand("wallet", "You can check PokeCoins in your wallet"),
            BotCommand("pay", "You can Share money with this command.")

        ])


async def main():
    await app.start()
    await load_start()
    a1 = random.randint(1, 9)
    await app.send_message(chat_id=-1001825502219, text=f"Zinda hu bhenchod!!\nTime taken: 0.{a1}")
    await cmds(app)
    await DB.setup()
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())
