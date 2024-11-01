from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Initialize Google Generative AI
genai.configure(api_key='AIzaSyD87R8KSnF5uzCnudTbWgg7_mWFQnOUbzM')
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Your Telegram bot API token
API_TOKEN = '8018890768:AAHEqrRwVse8lPS-nx2-S4KeS8Gv4PLChlA'

# Define command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi there!👋 I am your AI companion. What are you interested in?')

# Define message handler
def handle_response(prompt: str) -> str:
    processed: str = prompt.lower()
    # Implement your custom logic for handling responses here
    if prompt.lower() in ("hi", "hello", "hey"):
        response = "How can I help you today? 😊"
    if prompt.lower() in ("Activity"):
        response = (
            "Here are some upcoming activities:\n\n"
            "Etätapahtuma: Opastajille: iPhone ja Android -puhelinten erot\n"
            "Milloin: Pe, 8.11.2024 klo 11-15\n"
            "Missä: etänä Zoomissa\n"
            "Lisää tietoa: https://www.entersenior.fi/tapahtumat/iphone-ja-android-puhelinten-erot/\n\n"
            "Lähitapahtuma: Tekoäly\n"
            "Milloin: Ti, 12.11.2024 klo 13-14\n"
            "Missä: Porvoon pääkirjasto 2 krs. ryhmätila\n"
            "Lisää tietoa: https://www.entersenior.fi/tapahtumat/tekoaly-porvoo/\n\n"
            "Etätapahtuma: Jäsenille: Digivartti, aiheena Google Kääntäjä\n"
            "Milloin: Ke, 13.11.2024 klo 10-10.30\n"
            "Missä: etänä Zoomissa\n"
            "Lisää tietoa: https://www.entersenior.fi/tapahtumat/jasenille-digivartti-aiheena-google/\n\n"
            "Etätapahtuma: Jäsenille: Kysy mitä vaan digistä!\n"
            "Milloin: Ma, 25.11.2024 klo 13.30-15.30\n"
            "Missä: etänä Zoomissa\n"
            "Lisää tietoa: https://www.entersenior.fi/tapahtumat/jasenille-kmv-1124/\n\n"
            "Lähitapahtuma: Jäsenille: Joulupuuro\n"
            "Milloin: Pe, 29.11.2024 klo 11.30-14.30\n"
            "Missä: Tekniskan salit, Eerikinkatu 2, 00100 Helsinki\n"
            "Lisää tietoa: https://www.entersenior.fi/tapahtumat/jasenille-joulupuuro/"
        )
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

    # Check if it's the user's second message
    if context.user_data.get('message_count', 0) == 1:
        await update.message.reply_text("By the way, would you like to know about any nearby activities happening? Just reply with keyword 'Activity'.")
    
    # Increment the message count
    context.user_data['message_count'] = context.user_data.get('message_count', 0) + 1


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
