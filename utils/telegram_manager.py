import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors import UserPrivacyRestrictedError

class TelegramManager:
    """
    A manager for handling Telegram client operations using Telethon.
    """

    def __init__(self, api_id, api_hash, phone, session_name='session_name'):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.phone = phone

    async def start(self):
        await self.client.start(self.phone)
        user = await self.client.get_me()
        print(f"Authenticated as: {user.username}")

    async def disconnect(self):
        await self.client.disconnect()

    async def get_group(self, group_name):
        dialogs = await self.client.get_dialogs()
        for dialog in dialogs:
            if dialog.is_group and dialog.name == group_name:
                return dialog.entity
        return None

    async def get_participants(self, group):
        return await self.client.get_participants(group)

    async def add_user_to_group(self, target_group, user_entity, fwd_limit=100):
        try:
            await self.client(AddChatUserRequest(
                chat_id=target_group.id,
                user_id=user_entity.id,
                fwd_limit=fwd_limit
            ))
            print(f"User {user_entity.id} ({user_entity.username}) added to '{target_group.title}'.")
            await asyncio.sleep(1)
        except UserPrivacyRestrictedError:
            print(f"User {user_entity.id, user_entity.username} has privacy settings that prevent adding to groups.")
        except Exception as e:
            print(f"Error adding user {user_entity.id, user_entity.username}: {e}")