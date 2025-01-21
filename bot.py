import logging
from telegram.ext import Application, MessageHandler as TGMessageHandler, filters
import config
from message_handler import MessageHandler

# Configure logging
logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL
)
logger = logging.getLogger(__name__)

# Initialize handler
handler = MessageHandler(config.MAIN_CHANNEL, config.TARGET_CHANNELS)

def main():
    # Create application
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Add handler for ALL types of messages from main channel
    app.add_handler(TGMessageHandler(
        filters.Chat(config.MAIN_CHANNEL) & filters.ALL,  # Catch all message types
        handler.replicate_message
    ))

    logger.info("Bot started successfully!")
    logger.info(f"Monitoring main channel: {config.MAIN_CHANNEL}")
    logger.info(f"Replicating to {len(config.TARGET_CHANNELS)} target channels")
    
    # Run the bot until the user presses Ctrl-C
    app.run_polling()

if __name__ == "__main__":
    main() 