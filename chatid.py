import os
import json
from dotenv import load_dotenv
from telethon.sync import TelegramClient

# Load the API ID and hash from the .env file
load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Check if a session file already exists
if not os.path.exists('anon.session'):
    # Create a new Telegram client
    client = TelegramClient('anon', api_id, api_hash)
    client.start()
else:
    # Use the existing session file
    client = TelegramClient('anon', api_id, api_hash).start()

# Get the chat ID from the user
chat_id = int(input("Please enter the chat ID: "))

channel = client.get_entity(chat_id)
channel_name = channel.title
channel_link = channel.username

# Create a dictionary with the channel name and link
channel_info = {
    "Channel name": channel_name,
    "Channel link": f"https://t.me/{channel_link}"
}

# Print the dictionary as a JSON object
print(json.dumps(channel_info, indent=4))

client.disconnect()
