import random
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Define the bot token and admin ID
TOKEN = 'YOUR_BOT_TOKEN_HERE'
ADMIN_ID = YOUR_ADMIN_ID  # Replace with your admin's Telegram user ID

# Set up logging
logging.basicConfig(filename='bot_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize lists for approved users and logs
approved_users = set()
user_logs = []

# Payload generation function
def generate_payload(length: int = 4) -> str:
    payload = ''.join(f'\\\\x{random.randint(0, 255):02X}' for _ in range(length))
    return payload

# Command to approve a user
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can approve users.")
        return

    if context.args:
        try:
            user_id = int(context.args[0])
            approved_users.add(user_id)
            await update.message.reply_text(f"User {user_id} has been approved.")
        except ValueError:
            await update.message.reply_text("Please provide a valid user ID.")
    else:
        await update.message.reply_text("Please provide a user ID to approve.")

# Command to disapprove a user
async def disapprove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can disapprove users.")
        return

    if context.args:
        try:
            user_id = int(context.args[0])
            approved_users.discard(user_id)
            await update.message.reply_text(f"User {user_id} has been disapproved.")
        except ValueError:
            await update.message.reply_text("Please provide a valid user ID.")
    else:
        await update.message.reply_text("Please provide a user ID to disapprove.")

# Command to generate a payload
async def payload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in approved_users:
        await update.message.reply_text("You are not approved to use this command.")
        return

    length = int(context.args[0]) if context.args else 4
    payload_code = generate_payload(length)
    user_logs.append(f"{update.effective_user.id} generated payload: {payload_code}")
    await update.message.reply_text(f"`{payload_code}`", parse_mode='MarkdownV2')

# Command to view logs (admin only)
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can view logs.")
        return

    logs_text = "\n".join(user_logs) if user_logs else "No logs available."
    await update.message.reply_text(logs_text)

# Command to view all approved users (admin only)
async def all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can view all users.")
        return

    users_text = "\n".join(str(user) for user in approved_users) if approved_users else "No approved users."
    await update.message.reply_text(users_text)

# Command to clear logs (admin only)
async def clear_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Only the admin can clear logs.")
        return

    user_logs.clear()
    await update.message.reply_text("Logs have been cleared.")

# Command to contact the admin
async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You can contact the admin at Telegram ID: {ADMIN_ID}")

# Command to display help text
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/payload <length> - Generate a random payload.\n"
        "/approve <user_id> - Approve a user (admin only).\n"
        "/disapprove <user_id> - Disapprove a user (admin only).\n"
        "/logs - View logs (admin only).\n"
        "/allusers - View all approved users (admin only).\n"
        "/clearlogs - Clear all logs (admin only).\n"
        "/contact_admin - Get admin contact info.\n"
        "/help - Show this help message."
    )
    await update.message.reply_text(help_text)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /help to see all available commands.")

# Main function to run the bot
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("payload", payload))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("disapprove", disapprove))
    app.add_handler(CommandHandler("logs", logs))
    app.add_handler(CommandHandler("allusers", all_users))
    app.add_handler(CommandHandler("clearlogs", clear_logs))
    app.add_handler(CommandHandler("contact_admin", contact_admin))
    app.add_handler(CommandHandler("help", help_command))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
