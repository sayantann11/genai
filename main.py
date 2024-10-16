from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Initialize Google Generative AI
genai.configure(api_key='AIzaSyD87R8KSnF5uzCnudTbWgg7_mWFQnOUbzM')
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Your Telegram bot API token
API_TOKEN = '7675399769:AAE16-yEa2y1F5sE6OweYDcHU6X84Dl2qGw'

# Define command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi there!👋 I am your AI companion. What are you interested in?')

# Define message handler
def handle_response(prompt: str) -> str:
    processed: str = prompt.lower()
    # Implement your custom logic for handling responses here
    if prompt.lower() in ("hi", "hello", "hey"):
        response = "How can I help you today? 😊"
    else:
        # Generate response using Google Generative AI
        try:
            response1 = model.generate_content([
                """You are a friendly and engaging AI companion designed specifically for older adults. Your goal is to provide companionship, support, and mental stimulation. You will:
                - Engage in conversation naturally and continue previous conversations.
                - Be sensitive and supportive. Help with word games, trivia, etc.""",
                f"User message: {prompt}"
            ])
            response = response1.text
        except Exception as e:
            response = "Sorry, I couldn't come up with a response at the moment."
    return response

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    print(f'User ({update.message.chat.id}): "{text}"')

    response: str = handle_response(text)
    print('BOT:', response)
    
    await update.message.reply_text(response)

# Main function to start the bot
def main():
    print("Starting bot...")

    # Create the Application and pass it your bot's token
    app = Application.builder().token(API_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))

    # Register a handler for regular messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling for updates (this also includes idle behavior)
    print("Polling...")
    app.run_polling()

# Ensure we use the event loop that's already running
if __name__ == '__main__':
    main()
