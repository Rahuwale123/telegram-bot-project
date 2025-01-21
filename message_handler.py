import logging
from telegram import Update
from telegram.ext import ContextTypes
from typing import Union

class MessageHandler:
    def __init__(self, main_channel: int, target_channels: list[int]):
        self.main_channel = main_channel
        self.target_channels = target_channels
        self.logger = logging.getLogger(__name__)
        # Store message mappings
        self.message_ids = {}  # Format: {main_channel_msg_id: {channel_id: channel_msg_id}}

    async def replicate_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Replicate any type of message from main channel to all target channels"""
        try:
            message = update.channel_post or update.message
            
            # Skip if message is not from main channel
            if message.chat.id != self.main_channel:
                return

            # Initialize message mapping for this message
            self.message_ids[message.message_id] = {}

            for channel in self.target_channels:
                try:
                    reply_to_id = None
                    # If this is a reply, get the corresponding message ID in target channel
                    if message.reply_to_message and message.reply_to_message.message_id in self.message_ids:
                        reply_to_id = self.message_ids[message.reply_to_message.message_id].get(channel)

                    # Handle different types of messages
                    sent_message = None
                    if message.text:
                        sent_message = await context.bot.send_message(
                            chat_id=channel,
                            text=message.text,
                            entities=message.entities,
                            reply_to_message_id=reply_to_id
                        )
                    elif message.photo:
                        sent_message = await context.bot.send_photo(
                            chat_id=channel,
                            photo=message.photo[-1].file_id,
                            caption=message.caption,
                            caption_entities=message.caption_entities,
                            reply_to_message_id=reply_to_id
                        )
                    elif message.video:
                        sent_message = await context.bot.send_video(
                            chat_id=channel,
                            video=message.video.file_id,
                            caption=message.caption,
                            caption_entities=message.caption_entities,
                            reply_to_message_id=reply_to_id
                        )
                    elif message.document:
                        sent_message = await context.bot.send_document(
                            chat_id=channel,
                            document=message.document.file_id,
                            caption=message.caption,
                            caption_entities=message.caption_entities,
                            reply_to_message_id=reply_to_id
                        )
                    elif message.audio:
                        sent_message = await context.bot.send_audio(
                            chat_id=channel,
                            audio=message.audio.file_id,
                            caption=message.caption,
                            caption_entities=message.caption_entities,
                            reply_to_message_id=reply_to_id
                        )
                    elif message.voice:
                        sent_message = await context.bot.send_voice(
                            chat_id=channel,
                            voice=message.voice.file_id,
                            caption=message.caption,
                            caption_entities=message.caption_entities,
                            reply_to_message_id=reply_to_id
                        )
                    elif message.animation:
                        sent_message = await context.bot.send_animation(
                            chat_id=channel,
                            animation=message.animation.file_id,
                            caption=message.caption,
                            caption_entities=message.caption_entities,
                            reply_to_message_id=reply_to_id
                        )
                    
                    # Store the mapping of message IDs
                    if sent_message:
                        self.message_ids[message.message_id][channel] = sent_message.message_id
                    
                    self.logger.info(f"Message replicated to channel {channel}")
                except Exception as e:
                    self.logger.error(f"Error replicating to channel {channel}: {str(e)}")
                    continue

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")

    async def sync_replies(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sync replies from target channels to source channel"""
        try:
            message = update.channel_post
            chat = await context.bot.get_chat(message.chat_id)
            reply_text = f"💬 Reply from {chat.title}:\n{message.text}"
            await context.bot.send_message(self.main_channel, reply_text)
            self.logger.info(f"Reply synced from {chat.title}")
        except Exception as e:
            self.logger.error(f"Error syncing reply: {str(e)}") 