# chat-id
interactive python script to find the channel name and channel link from a telegram chat id. 

## how-to use

- git clone this repo
- pythton3 -m venv /path/to/this/repo
- source bin/activate
- pip3 install -r requirements.txt
- python3 chatid.py
- paste the telegram chat ID ie: -1001638301761 you want to get the Link

the result is a json object with the information of the channel. 

# Telegram Chat Information Script

This Python script retrieves detailed information about Telegram chats or channels using their IDs. It supports two modes of operation: processing a single chat ID or batch processing a list of chat IDs from a JSON file.

## Features
- Retrieve chat/channel details, including name, link, and description.
- Fetch information about administrators (if permissions allow).
- Handles Telegram API rate limits.
- Outputs results in a readable JSON format.

## Prerequisites

1. **Python**: Ensure Python 3.7 or later is installed.
2. **Dependencies**: Install required Python libraries.
3. **Telegram API Credentials**: Obtain your `API_ID` and `API_HASH` from [Telegram's Developer Portal](https://my.telegram.org/apps).
4. **Environment File**: Create a `.env` file in the script's directory with the following format:

    ```env
    API_ID=your_api_id
    API_HASH=your_api_hash
    ```

## Installation

1. Clone the repository or download the script file.
2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should include:
    ```
    telethon
    python-dotenv
    ```

## Usage

### Single Chat ID Mode

1. Run the script:

    ```bash
    python script.py
    ```

2. Select `single` mode when prompted.

3. Enter the chat ID interactively:

    ```
    Enter mode (single/file): single
    Enter chat ID: 123456789
    ```

4. The script will fetch and display the details for the given chat ID.

### Batch Processing Mode

1. Prepare an input JSON file containing a list of chat IDs:

    ```json
    [
        1128083841,
        1283178270,
        1487098807
    ]
    ```

2. Run the script:

    ```bash
    python script.py
    ```

3. Select `file` mode when prompted.

4. Enter the paths for the input and output JSON files:

    ```
    Enter mode (single/file): file
    Enter input JSON file path: input.json
    Enter output JSON file path: output.json
    ```

5. The script will process the chat IDs in the input file and save the results in the specified output file.

### Output Example

The output JSON file will look like this:

```json
{
    "1128083841": {
        "Channel name": "Example Channel",
        "Channel link": "https://t.me/example",
        "About": "This is an example channel.",
        "Admin Info": [
            {
                "Admin ID": 123456,
                "Admin Username": "admin_user",
                "Admin First Name": "Admin",
                "Admin Last Name": "User"
            }
        ]
    }
}
```

## Handling Rate Limits

The script automatically detects and handles rate limits using `FloodWaitError`. If a rate limit is hit, it will pause for the required duration before continuing.

## Notes
- Ensure the chat IDs are valid and accessible with the provided API credentials.
- Permissions to fetch administrator details may vary depending on the chat/channel settings.

## License
This script is released under the MIT License.

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes!
