from pyrogram import Client, filters
import openai
import os

# Initialize OpenAI API
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Initialize Pyrogram Client
bot = Client("my_bot", api_id=os.environ.get('API_ID'), api_hash=os.environ.get('API_HASH'), bot_token=os.environ.get('BOT_TOKEN'))

# /start Command
@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    picture_url = "https://te.legra.ph/file/1f2ac2fe8cdf202799847.jpg"
    await client.send_photo(
        chat_id=message.chat.id,
        photo=picture_url,
        caption=f"Hey {message.from_user.first_name}, Welcome to my bot! Send me a message and I will use the OpenAI API to generate a response.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Add me to group", url="https://t.me/GPT_Autobot?startgroup=True")]
        ])
    )

# Respond to all messages
@bot.on_message(filters.text & ~filters.command("start"))
async def handle_message(client, message):
    response_text = await get_gpt_response(message.text)
    await client.send_message(chat_id=message.chat.id, text=response_text)

# Function to get GPT-3 response
async def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="davinci",  # Or any other GPT-3 engine
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Run the bot
bot.run()
