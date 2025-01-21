import logging
import sys
from telegram import Update
from telegram.ext import Application, MessageHandler as TGMessageHandler, filters
import config
from message_handler import MessageHandler

def setup_logging():
    """Configure logging based on platform"""
    logging.basicConfig(
        format=config.LOG_FORMAT,
        level=config.LOG_LEVEL,
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.logger = setup_logging()
        self.handler = MessageHandler(config.MAIN_CHANNEL, config.TARGET_CHANNELS)

    def run(self):
        """Run the bot"""
        try:
            # Initialize application
            app = (
                Application.builder()
                .token(config.BOT_TOKEN)
                .build()
            )

            # Add message handler
            app.add_handler(TGMessageHandler(
                filters.Chat(config.MAIN_CHANNEL) & filters.ALL,
                self.handler.replicate_message
            ))

            # Log startup
            self.logger.info("Bot started successfully!")
            self.logger.info(f"Monitoring main channel: {config.MAIN_CHANNEL}")
            self.logger.info(f"Replicating to {len(config.TARGET_CHANNELS)} target channels")

            # Start the bot (this will block until the bot is stopped)
            app.run_polling(drop_pending_updates=True)

        except Exception as e:
            self.logger.error(f"Error occurred: {str(e)}")
            # Wait before trying to restart
            import time
            time.sleep(10)
            self.run()  # Restart the bot

def main():
    """Main entry point"""
    bot = TelegramBot()
    while True:
        try:
            bot.run()
        except KeyboardInterrupt:
            print("\nBot stopped by user")
            break
        except Exception as e:
            print(f"Fatal error: {str(e)}")
            print("Restarting bot in 10 seconds...")
            import time
            time.sleep(10)
            continue

if __name__ == "__main__":
    main() 