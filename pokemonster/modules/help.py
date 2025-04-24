import random

from pyrogram import *
from pyrogram.enums import ParseMode as PM
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from pokemonster import *

responses = [
    '''𝗚𝗼𝘁 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀? 𝗛𝗲𝗿𝗲'𝘀 𝘄𝗵𝗮𝘁 𝘆𝗼𝘂 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗸𝗻𝗼𝘄!
✧ 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

➛ /start - To check if the bot is running.
➛ /catch [Pokemon Name] - Catch the spawned Pokemon.
➛ /pokedex - View your Pokedex Collection.
➛ /ptrade - Exchange your Pokemons. Type /ptrade for the manual.
➛ /pfav [Pokemon Id number] - Choose your favourite Pokemon.
➛ /pgift - Show your care to new members. Type /pgift for the manual.
➛ /winner or /leader - See who's the best.
➛ /release - Release the Pokemon.
➛ /pinfo [pokemon id or pokemon name] - Get info about a Pokemon.
➛ /devcmds - Get all dev cmds
➛ /updatepower - If you think your power is not according to the pokemon you have caught.

➛ Every 100 messages, a new Pokemon spawns in the group.
➛ After 35 messages, the Pokemon will run away.

× For more info, join @PokemonCatcherUpdates.''',

    '''𝗕𝗲𝗰𝗼𝗺𝗲 𝗮 𝗠𝗮𝘀𝘁𝗲𝗿 𝗼𝗳 𝗣𝗼𝗸𝗲𝗺𝗼𝗻𝘀 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗵𝗲𝗹𝗽 𝗼𝗳 𝘆𝗼𝘂𝗿 𝗳𝗮𝘃𝗼𝗿𝗶𝘁𝗲 𝗕𝗼𝘁!
✧ 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

- /start: Check if the bot is running.
- /catch [Pokemon Name]: Catch a spawned Pokemon.
- /pokedex: View your Pokedex collection.
- /ptrade: Exchange your Pokemons. Type /ptrade for more info.
- /pfav [Pokemon Id number]: Choose your favorite Pokemon.
- /pgift: Show your care to new members of the community. Type /pgift for more info.
- /winner or /leader: See who's the best.
- /release: Release a Pokemon.
- /pinfo [pokemon id or pokemon name]: Get info about a specific Pokemon.
- /devcmds - Get all dev cmds
- /updatepower - If you think your power is not according to the pokemon you have caught.
- /freqchange - to change the number of messages the pokemon will spawn in your group.
- /spawn - This will spawn a pokemon immediately in your group use (it wont be added to your databases upon catching but it will give you PokeCoins.)
- /guess - This command is to catch guessed pokemon (it wont be added to your databases upon catching but it will give you PokeCoins.)
- /trivia - This will generate a question to test your pokeKnowledge (Upon selecting correct answer you will be granted PokeCoins.)
- /pokestore - You can buy Pokemon of different rarity from here
- /wallet - You can check PokeCoins in your wallet
- /pay - You can share Your money with others.



➛ A new Pokemon spawns in the group every 100 messages.
➛ The Pokemon will run away after 35 messages.

× For more info, join @PokemonCatcherUpdates.''',
    '''𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 𝗼𝘂𝗿 𝗣𝗼𝗸𝗲𝗺𝗼𝗻 𝗧𝗿𝗮𝗶𝗻𝗲𝗿'𝘀 𝘀𝗼𝗰𝗶𝗲𝘁𝘆 !!

─────────────────────

✧  COMMANDS 

- /start: Check if the bot is running.
- /catch [Pokemon Name]: Catch a spawned Pokemon.
- /pokedex: View your Pokedex collection.
- /ptrade: Exchange your Pokemons. Type /ptrade for more info.
- /pfav [Pokemon Id number]: Choose your favorite Pokemon.
- /pgift: Show your care to new members of the community. Type /pgift for more info.
- /winner or /leader: See who's the best.
- /release: Release a Pokemon.
- /pinfo [pokemon id or pokemon name]: Get info about a specific Pokemon.
- /devcmds - Get all dev cmds
- /updatepower - If you think your power is not according to the pokemon you have caught.
- /freqchange - to change the number of messages the pokemon will spawn in your group.
- /spawn - This will spawn a pokemon immediately in your group use (it wont be added to your databases upon catching but it will give you PokeCoins.)
- /guess - This command is to catch guessed pokemon (it wont be added to your databases upon catching but it will give you PokeCoins.)
- /trivia - This will generate a question to test your pokeKnowledge (Upon selecting correct answer you will be granted PokeCoins.)
- /pokestore - You can buy Pokemon of different rarity from here
- /wallet - You can check PokeCoins in your wallet
- /pay - You can share Your money with others.


➛ After 35 messages of spawning the Pokemon will run away into the wilderness.

─────────────────────

× For more info Join @PokemonCatcherUpdates .

XoXo''',
    '''Welcome to our Pokemon training community!

Here are some commands you can use to catch, trade, and manage your Pokemon:

- /start: Check if the bot is running.
- /catch [Pokemon Name]: Catch a spawned Pokemon.
- /pokedex: View your Pokedex collection.
- /ptrade: Exchange your Pokemons. Type /ptrade for more info.
- /pfav [Pokemon Id number]: Choose your favorite Pokemon.
- /pgift: Show your care to new members of the community. Type /pgift for more info.
- /winner or /leader: See who's the best.
- /release: Release a Pokemon.
- /pinfo [pokemon id or pokemon name]: Get info about a specific Pokemon.
- /devcmds - Get all dev cmds
- /updatepower - If you think your power is not according to the pokemon you have caught.
- /freqchange - to change the number of messages the pokemon will spawn in your group.
- /spawn - This will spawn a pokemon immediately in your group use (it wont be added to your databases upon catching but it will give you PokeCoins.)
- /guess - This command is to catch guessed pokemon (it wont be added to your databases upon catching but it will give you PokeCoins.)
- /trivia - This will generate a question to test your pokeKnowledge (Upon selecting correct answer you will be granted PokeCoins.)
- /pokestore - You can buy Pokemon of different rarity from here
- /wallet - You can check PokeCoins in your wallet
- /pay - You can share Your money with others.


Remember, a new Pokemon will appear in the group every 100 messages. After 35 messages, the Pokemon will run away into the wilderness.

For more info and updates, join @PokemonCatcherUpdates.

Good luck on your journey to become the ultimate Pokemon trainer! 🚀🔥
''',
]


@app.on_message(filters.command('help'))
async def helph(c: app, message: Message):

    await message.reply_text(random.choice(responses))
