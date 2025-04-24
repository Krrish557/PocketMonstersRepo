from threading import RLock

from motor.motor_asyncio import AsyncIOMotorClient

from ..config import MONGO_NAME2, MONGO_URI2

INSERTION_LOCK = RLock()


class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URI2)
        self.db = self.client[MONGO_NAME2]
        self.msg_freq = self.db.msg_freq
        self.pokecoin = self.db.pokecoin

    async def setup(self):
        try:
            self.client.admin.command("ping")
            print(">> Database Connection Successful! <<")
        except Exception as e:
            print(f"Database Connection Failed: {e}")
            quit(1)

    # update user if they exists in db else add them
    async def update_user(self, user_id: int, username: str, name: str) -> None:
        context = {"user_id": user_id, "username": username, "name": name}
        await self.db.user_base.update_one(
            {"user_id": user_id}, {"$set": context}, upsert=True
        )

    # get user from db
    async def get_user(self, user_id: int) -> dict:
        data = await self.db.user_base.find_one({"user_id": user_id})
        if data:
            return data
        else:
            return {}

    # msg_freq Commands
    async def add_frequency(self, chat_id: int, frequency: int, chat_title: str):
        context = {"chat_title": chat_title, "frequency": frequency}
        await self.msg_freq.update_one(
            {"chat_id": chat_id}, {"$set": context}, upsert=True
        )

    async def read_frequency(self, chat_id) -> int:
        context = {"chat_id": chat_id}
        data = await self.msg_freq.find_one(context)
        if not data:
            return 100
        return data["frequency"]

# pokecoin commands

    async def add_pokecoin(self, user_id: int, money: int, username: str):
        context = {"user_id": user_id}
        data = await self.pokecoin.find_one(context)
        print(f"Added {money} to {username}")
        if data != None:
            old_money = int(data["pokecoin"])
            new_money = int(old_money)+int(money)
        else:
            new_money = money
        context2 = {"username": username, "pokecoin": new_money}
        await self.pokecoin.update_one(
            {"user_id": user_id}, {"$set": context2}, upsert=True
        )

    async def subtract_pokecoin(self, user_id: int, money: int):
        context = {"user_id": user_id}
        data = await self.pokecoin.find_one(context)
        if not data:
            return
        else:
            prev_money = data["pokecoin"]
            new_money = prev_money - money
            context2 = {"pokecoin": new_money}
            await self.pokecoin.update_one(
                {"user_id": user_id}, {"$set": context2}, upsert=True
            )

    async def make_coins_0(self, user_id:int):
        curr = await self.pokecoin.find_one({"user_id": user_id})
        if not curr:
            return
        else:
            reset = {"pokecoin": 0}
            await self.pokecoin.update_one(
                {"user_id": user_id}, {"$set": reset}, upsert=True
            )


    async def read_money(self, user_id: int):
        with INSERTION_LOCK:
            context = {"user_id": user_id}
            data = await self.pokecoin.find_one(context)
            if data != None:
                return data["pokecoin"]
            else:
                return 0

    # If want in ascending order pass False
    async def sorted_money_database(self, descending: bool = True):
        with INSERTION_LOCK:
            # Use 'find' instead of 'find_all'
            curr = await self.pokecoin.find().to_list(None)
            if curr:
                cur = sorted(
                    curr, key=lambda c_id: int(c_id["pokecoin"]), reverse=descending)
                return cur
            else:
                return []
