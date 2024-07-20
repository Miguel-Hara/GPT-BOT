import os
import openai
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Read environment variables
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PICTURE_URL = os.environ.get('PICTURE_URL')

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Pyrogram Client
app = Client(
    "MyBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Define the inline keyboard buttons
main_buttons = [
    [InlineKeyboardButton("Add me to a group", url="https://t.me/GPT_Autobot?startgroup=True")]
]

# Define the translation text
class Translation:
    START_TXT = "Hey {name},\n\nWelcome to my bot! Send me a message and I will use the OpenAI API to generate a response."

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    
    # Send the picture with the start message
    await client.send_photo(
        chat_id=message.chat.id,
        photo=PICTURE_URL,
        caption=Translation.START_TXT.format(name=message.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(main_buttons)
    )

# Function to get GPT-3 response
async def get_gpt_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating GPT response: {e}")
        return "Sorry, I couldn't process your request."

@app.on_message(filters.text & ~filters.command("start"))
async def handle_message(client, message):
    # Respond to every text message in private chats and groups
    response_text = await get_gpt_response(message.text)
    await client.send_message(chat_id=message.chat.id, text=response_text)

# Run the bot
app.run()
