import json
from threading import RLock

from pokemonster import *
from pokemonster.db import MongoDB

with open('pokedex.json') as f:
    data = json.load(f)


class Pokemons:
    def select_link(pokeid):
        if pokeid == data["poke"][-1]:
            return
        for i in data["poke"]:
            if i["id"] == pokeid:
                return i["link"]
        return

    def select_name(pokeid):
        if pokeid == data["poke"][-1]:
            return
        for i in data["poke"]:
            if i["id"] == pokeid:
                return i["name"]
        return

    def get_po_info(pokeid):
        if pokeid == data["poke"][-1]:
            return
        for i in data["poke"]:
            if i["id"] == pokeid:
                return i
        return

    def get_po_info_by_name(pokname: str):
        pokname = pokname.casefold()
        for i in data["poke"]:
            if i["name"].casefold() == pokname:
                return i
            if i["name"].split("-")[0].casefold() == pokname:
                return i
        return


INSERTION_LOCK = RLock()


class USERSINFO(MongoDB):
    """Class for userinfo"""

    db_name = "user_info"

    def __init__(self) -> None:
        super().__init__(self.db_name)

    def save_info(self, chat_id, user_id, poke_id, fav_poke=0, reduce=False):
        try:
            pinfo = Pokemons.get_po_info(poke_id)
        except Exception:
            return
        p_w = int(pinfo["weight"])
        with INSERTION_LOCK:
            curr = self.find_one(
                {
                    "chat_id": chat_id,
                    "user_id": user_id,
                }
            )
            if curr:
                try:
                    if reduce:
                        try:
                            poke = curr["poke_id"]
                            poke.remove(poke_id)
                        except ValueError:
                            return
                        self.update(
                            {
                                "chat_id": chat_id,
                                "user_id": user_id,
                            },
                            {
                                "poke_id": poke
                            }
                        )
                        self.update(
                            {
                                "chat_id": chat_id,
                                "user_id": user_id,
                            },
                            {
                                "$inc": {"poke_pow": -p_w}
                            },
                            True
                        )
                        return
                    self.update(
                        {
                            "chat_id": chat_id,
                            "user_id": user_id,
                        },
                        {
                            "$push": {"poke_id": poke_id},
                        },
                        True
                    )
                    self.update(
                        {
                            "chat_id": chat_id,
                            "user_id": user_id
                        },
                        {
                            "$inc": {"poke_pow": +p_w}
                        },
                        True
                    )
                    return
                except Exception:
                    poko = [poke_id]
                    self.update(
                        {
                            "chat_id":chat_id,
                            "user_id":user_id
                        },
                        {
                            "poke_id":poko
                        }
                    )
            else:
                poko = [poke_id]
                self.insert_one(
                    {
                        "chat_id": chat_id,
                        "user_id": user_id,
                        "poke_id": poko,
                        "fav_pok": fav_poke,
                        "poke_pow": p_w
                    }
                )
                return

    def get_unique_chat_ids_count(self, want_len=False):
        with INSERTION_LOCK:
            chat_ids = self.find_all()
            chat_ids = {i["chat_id"] for i in chat_ids}
            if want_len:
                quer = len(list(chat_ids))
            else:
                quer = list(chat_ids)
            return quer

    def get_unique_users(self, want_len=False):
        with INSERTION_LOCK:
            curr = self.find_all()
            users = {i["user_id"] for i in curr}
            if want_len:
                quer = len(list(users))
            else:
                quer = list(users)
            return quer

    def get_total_catch(self):
        with INSERTION_LOCK:
            curr = self.find_all()
            leng = []
            for i in curr:
                if i["poke_id"] and len(i["poke_id"]):
                    leng.append(len(i["poke_id"]))
                else:
                    pass
            curr = sum(leng)
            return curr

    def pokeList(self, chatid, userid):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": chatid, "user_id": userid})
            if curr:
                return curr["poke_id"]
            else:
                return []

    def get_user_db(self, chatid, userid):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": chatid, "user_id": userid})
            if curr:
                return curr
            else:
                return None

    def update_total_poke_pow(self, chatid, userid, weight):
        curr = self.find_one({"chat_id": chatid, "user_id": userid})
        if curr:
            self.update({"chat_id": chatid, "user_id": userid},
                        {"poke_pow": weight})
            return True
        return None

    def update_fav_pok(self, chatid, userid, favpok):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": chatid, "user_id": userid})
            if curr:
                self.update({"chat_id": chatid, "user_id": userid}, {
                            "fav_pok": favpok})
                return
            else:
                return

    def update_fav_pok_to_none(self, chatid, userid):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": chatid, "user_id": userid})
            if curr:
                self.update(
                    {"chat_id": chatid, "user_id": userid}, {"fav_pok": 0})
                return
            else:
                return
    # If want in ascending order pass False

    def sorted_weight_db(self, chatid, descending: bool = True):
        with INSERTION_LOCK:
            curr = self.find_all({"chat_id": chatid})
            if curr:
                cur = sorted(
                    curr, key=lambda c_id: c_id["poke_pow"], reverse=descending)
                return cur
            else:
                return []

    # If want in ascending order pass False
    def sorted_weight_db_global(self, descending: bool = True):
        with INSERTION_LOCK:
            curr = self.find_all()
            if curr:
                cur = sorted(
                    curr, key=lambda c_id: c_id["poke_pow"], reverse=descending)
                return cur
            else:
                return []

    def delete_user(self, chatid, userid):
        with INSERTION_LOCK:
            curr = self.find_one({"chat_id": chatid, "user_id": userid})
            if curr:
                self.delete_one({"chat_id": chatid, "user_id": userid})
                return True
            return False
