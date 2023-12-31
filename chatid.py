import os
import json
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import ChatAdminRequiredError

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

# Get the full channel information
full = client(GetFullChannelRequest(channel))
about = full.full_chat.about

# Try to get the administrators of the chat
try:
    admins = client(GetParticipantsRequest(
        channel, ChannelParticipantsAdmins(), 0, 100, hash=0
    ))

    admin_info = []
    for user in admins.users:
        admin_info.append({
            "Admin ID": user.id,
            "Admin Username": user.username,
            "Admin First Name": user.first_name,
            "Admin Last Name": user.last_name
        })
except ChatAdminRequiredError:
    admin_info = "Cannot retrieve admin info due to lack of permissions."

# Create a dictionary with the channel name, link, about and admin info
channel_info = {
    "Channel name": channel_name,
    "Channel link": f"https://t.me/{channel_link}",
    "About": about,
    "Admin Info": admin_info
}

# Print the dictionary as a JSON object
print(json.dumps(channel_info, indent=4, ensure_ascii=False))

client.disconnect()
