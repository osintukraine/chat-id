import os
import json
import time
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import ChatAdminRequiredError
from telethon.errors import FloodWaitError

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

def process_chat(chat_id):
    try:
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

        # Return the channel information
        return {
            "Channel name": channel_name,
            "Channel link": f"https://t.me/{channel_link}",
            "About": about,
            "Admin Info": admin_info
        }

    except FloodWaitError as e:
        print(f"Rate limit hit. Sleeping for {e.seconds} seconds.")
        time.sleep(e.seconds)
        return None
    except Exception as e:
        print(f"Failed to process chat ID {chat_id}: {e}")
        return None

def process_from_file(input_file, output_file):
    with open(input_file, 'r') as f:
        chat_ids = json.load(f)

    results = {}

    for chat_id in chat_ids:
        print(f"Processing chat ID {chat_id}...")
        result = process_chat(chat_id)
        if result:
            results[chat_id] = result

        # Add a delay to respect rate limits
        time.sleep(2)  # Adjust delay as necessary

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Processing complete. Results saved to '{output_file}'.")

def main():
    mode = input("Enter mode (single/file): ").strip().lower()

    if mode == 'single':
        chat_id = int(input("Enter chat ID: ").strip())
        result = process_chat(chat_id)
        if result:
            print(json.dumps(result, indent=4, ensure_ascii=False))
    elif mode == 'file':
        input_file = input("Enter input JSON file path: ").strip()
        output_file = input("Enter output JSON file path: ").strip()
        process_from_file(input_file, output_file)
    else:
        print("Invalid mode. Please choose 'single' or 'file'.")

if __name__ == "__main__":
    main()

client.disconnect()
