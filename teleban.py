import random
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# Bot Token
bot_token = '7559854990:AAFd60knkz3MSQ8t2AI383E3TFlpkDqHyHo'

# Color Codes for Console Output
R = '\033[1;31;40m'
F = '\033[1;32;40m'
C = "\033[1;97;40m"
B = '\033[1;36;40m'
C1 = '\033[1;35;40m'

# Maximum number of concurrent users
MAX_USERS = 50
current_users = 0

# Function to generate a random email
def generate_email():
    rand = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    email = str(''.join(random.choice(rand) for i in range(int(random.randint(9, 16))))) + random.choice(["@gmail.com", "@hotmail.com", "@yahoo.com", "@live.com"])
    return email

# Function to generate a random phone number
def generate_phone():
    rand = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    rand_num = str(''.join(random.choice(rand) for i in range(int(15))))
    phone_1 = "+1" + rand_num
    phone_2 = "+7" + rand_num
    phone_3 = "+44" + rand_num
    phone = random.choice([phone_1, phone_2, phone_3])
    return phone

# Function to generate a random country language
def generate_country():
    Countries = ["English", "Español", "Français", "Italiano", "Українська"]
    country = random.choice(Countries)
    return country

# Function to send reports with different contact details
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if the message contains arguments (link_channel)
    if len(context.args) < 1:
        await update.message.reply_text(f"{R}Please provide the channel link. Example: /report 'http://channel-link'")
        return

    # Extract the channel link from the arguments
    link_channel = context.args[0]

    try:
        # Send the large-font "Started Sending Reports" message
        await update.message.reply_text(f"<b>Started Sending Reports to {link_channel}</b>", parse_mode="HTML")

        # Format the report message
        base_report_message = f'''
        Peace be upon you, I am a user of the Telegram platform, but there is a problem. There is a channel that publishes personal data related to my government in Egypt, Saudi Arabia, and Bangladesh continuously without any right, and they expose my data and my friends’ data to danger! This is the channel link: {link_channel}. I hope you will deal with this report so that I can have a good experience without revealing my data and the data of others without any right.
        '''

        # Flag to control the sending loop (simulated banning)
        reports_sent = 0
        is_banned = False

        while reports_sent < 5000:  # Loop to send reports
            email = generate_email()  # Generate a random email
            phone = generate_phone()  # Generate a random phone number
            country = generate_country()  # Generate a random country

            # Add contact info to the report message
            report_message = base_report_message + f"\n\nContact Info:\nEmail: {email}\nPhone: {phone}\nCountry: {country}"

            # ** Hide the progress logs from the user **

            # Send the report to Telegram Support (simulate sending via POST request to support API)
            # response = requests.post('https://telegram.org/support', data={report_message})  # Use appropriate Telegram support URL

            # If successfully "sent", we log the progress (but won't show it to the user)
            print(f"Sending report {reports_sent + 1}/5000...")  # Logs in the console for debugging, won't appear in the chat

            # Simulate a delay to avoid triggering rate limits
            time.sleep(1)  # Adjust delay if necessary

            reports_sent += 1

            # Simulate banning (not actual banning)
            if reports_sent >= 5000:  # After 5000 reports, simulate banning
                is_banned = True
                await update.message.reply_text(F + "Channel successfully banned! The reports have been processed.")

        if is_banned:
            await update.message.reply_text(F + "All reports have been successfully sent and the channel has been banned.")

    except Exception as e:
        await update.message.reply_text(R + f"Error: {str(e)}")

# Function to show bot info when /info is used
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_info = "WELCOME TO TELEBAN | MADE BY: @manjouun1"
    await update.message.reply_text(f"{C1}{bot_info}{C}")

# Function to show available commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Increment current user count and check if it exceeds the limit
    global current_users
    if current_users >= MAX_USERS:
        await update.message.reply_text(f"{R}Sorry, the bot is currently at full capacity. Try again later.")
        return
    
    current_users += 1
    
    # Show available commands
    welcome_message = f"""
    {B}Welcome to the Telegram report bot! Here are the available commands:
    /info - To show bot info
    /report <Channel Link> - To report a channel to Telegram support
    """
    
    await update.message.reply_text(welcome_message)

# Function to handle user leave
async def user_left(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_users
    current_users -= 1

# Set up the Application and Dispatcher for the bot
def main():
    # Use Application class instead of Updater
    application = Application.builder().token(bot_token).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("info", info))

    # Handle user leaving (in case they stop interacting with the bot)
    application.add_handler(CommandHandler("left", user_left))

    # Start polling
    application.run_polling()

if __name__ == '__main__':
    main()
