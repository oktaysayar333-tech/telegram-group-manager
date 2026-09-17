#This is the entry point of your application. It orchestrates the loading of configurations and manages Telegram interactions.
import sys
import asyncio
from utils.config_loader import load_config
from utils.telegram_manager import TelegramManager

# Configuration for group names and excluded users
GROUP_NAME = ''
NEW_CHAT = ''
EXCLUDED_USERS = ['']

async def main():
    """
    Main function to execute the Telegram group management tasks.
    """
    # Load credentials from the configuration file
    creds = load_config()
    telegram = creds.get('telegram', {})
    api_id = telegram.get('api_id')
    api_hash = telegram.get('api_hash')
    phone = telegram.get('phone_number')

    # Validate Telegram credentials
    if not all([api_id, api_hash, phone]):
        print("Insufficient data to connect to Telegram.")
        sys.exit(1)

    # Initialize the Telegram manager
    manager = TelegramManager(api_id, api_hash, phone)

    # Start the Telegram client
    await manager.start()

    # Find the source group
    source_group = await manager.get_group(GROUP_NAME)
    if not source_group:
        print(f"Group '{GROUP_NAME}' not found.")
        await manager.disconnect()
        return
    print(f"Source group '{GROUP_NAME}' found. ID: {source_group.id}")

    # Find the target group
    target_group = await manager.get_group(NEW_CHAT)
    if not target_group:
        print(f"Group '{NEW_CHAT}' not found.")
        await manager.disconnect()
        return
    print(f"Target group '{NEW_CHAT}' found. ID: {target_group.id}")

    print(f"Working with source group: {source_group.title}")

    # Retrieve participants from the source group
    participants = await manager.get_participants(source_group)
    print(f"Total participants in '{source_group.title}': {len(participants)}")

    # Filter out excluded users
    users_to_add = [
        p for p in participants
        if (p.username and p.username not in EXCLUDED_USERS) or (not p.username and str(p.id) not in EXCLUDED_USERS)
    ]

    print(f"Users to add after filtering: {len(users_to_add)}")
    print("Users to add:", [u.username if u.username else u.id for u in users_to_add])

    # Add users to the target group
    for user_entity in users_to_add:
        await manager.add_user_to_group(target_group, user_entity)

    # Disconnect the Telegram client
    await manager.disconnect()

if __name__ == "__main__":
    asyncio.run(main())