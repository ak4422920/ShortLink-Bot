import motor.motor_asyncio
from configs import *

class Database:
    def __init__(self, url, db_name):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self.client[db_name]
        self.coll = self.db.users

    async def add_user(self, id):
        if not await self.is_present(id):
            await self.coll.insert_one({"id": id, "api": None, "shortner": None})

    async def is_present(self, id):
        return await self.coll.find_one({"id": id}) is not None

    async def total_users(self):
        return await self.coll.count_documents({})

    async def set_shortner(self, uid, shortner, api):
        await self.coll.update_one({"id": uid}, {"$set": {"shortner": shortner, "api": api}})

    async def get_value(self, key, uid):
        user = await self.coll.find_one({"id": uid}, {"_id": 0, key: 1})
        return user.get(key) if user else None

    async def delete_value(self, key, uid):
        """Delete a specific key (shortner or api) from the user's record."""
        await self.coll.update_one({"id": uid}, {"$unset": {key: ""}})

db = Database(DATABASE_URL, "TechifyBots")
