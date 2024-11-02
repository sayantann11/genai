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
    await update.message.reply_text("By the way, would you like to know about any nearby activities happening?")
    await update.message.reply_text("Just reply with the keyword 'Activity' at any time in the chat.")
    await update.message.reply_text("Reply with End to finish the Chat")

# Define message handler
def handle_response(prompt: str) -> str:
    processed: str = prompt.lower()
    responses = []  # List to collect responses

    if processed in ("hi", "hello", "hey"):
        responses.append("How can I help you today? 😊")
        responses.append("By the way, would you like to know about any nearby activities happening?")
        responses.append("Just reply with the keyword 'Activity' at any time in the chat.")

    elif processed == "end":
        responses.append("Thank you for chatting! If you need anything else, feel free to start a new conversation. Have a great day! 🌟")

    elif processed == "activity":
       responses.append(
            "📅 Here are some upcoming activities:\n\n"
            
            "1. Etätapahtuma: Opastajille: iPhone ja Android -puhelinten erot\n"
            "   - When: Pe, 8.11.2024 klo 11-15\n"
            "   - Where: Online (Zoom)\n"
            "   - More info: [Click here](https://www.entersenior.fi/tapahtumat/iphone-ja-android-puhelinten-erot/)\n\n"
            
            "2. Lähitapahtuma: Tekoäly\n"
            "   - When: Ti, 12.11.2024 klo 13-14\n"
            "   - Where: Porvoon pääkirjasto, 2. krs, ryhmätila\n"
            "   - More info: [Click here](https://www.entersenior.fi/tapahtumat/tekoaly-porvoo/)\n\n"
            
            "3. Etätapahtuma: Jäsenille: Digivartti, aiheena Google Kääntäjä\n"
            "   - When: Ke, 13.11.2024 klo 10-10.30\n"
            "   - Where: Online (Zoom)\n"
            "   - More info: [Click here](https://www.entersenior.fi/tapahtumat/jasenille-digivartti-aiheena-google/)\n\n"
            
            "4. Etätapahtuma: Jäsenille: Kysy mitä vaan digistä!\n"
            "   - When: Ma, 25.11.2024 klo 13.30-15.30\n"
            "   - Where: Online (Zoom)\n"
            "   - More info: [Click here](https://www.entersenior.fi/tapahtumat/jasenille-kmv-1124/)\n\n"
            
            "5. Lähitapahtuma: Jäsenille: Joulupuuro\n"
            "   - When: Pe, 29.11.2024 klo 11.30-14.30\n"
            "   - Where: Tekniskan salit, Eerikinkatu 2, 00100 Helsinki\n"
            "   - More info: [Click here](https://www.entersenior.fi/tapahtumat/jasenille-joulupuuro/)\n"
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
            responses.append(response1.text)
        except Exception as e:
            responses.append("Sorry, I couldn't come up with a response at the moment.")

    return "\n".join(responses)  # Join responses with new lines


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    print(f'User ({update.message.chat.id}): "{text}"')

    response: str = handle_response(text)
    print('BOT:', response)
    
    await update.message.reply_text(response)


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
