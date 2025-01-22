import logging
from telegram import Update, MessageEntity
from telegram.ext import ContextTypes
from typing import Dict, Optional, List

class MessageHandler:
    def __init__(self, main_channel: int, target_channels: list[int]):
        self.main_channel = main_channel
        self.target_channels = target_channels
        self.logger = logging.getLogger(__name__)
        self.message_ids: Dict[int, Dict[int, int]] = {}

    async def replicate_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Replicate any type of message from main channel to all target channels"""
        try:
            message = update.channel_post or update.message
            if not message or message.chat.id != self.main_channel:
                return

            self.message_ids[message.message_id] = {}
            
            for channel in self.target_channels:
                try:
                    # Get reply message ID if this is a reply
                    reply_to_id = None
                    if message.reply_to_message:
                        channel_msgs = self.message_ids.get(message.reply_to_message.message_id, {})
                        reply_to_id = channel_msgs.get(channel)

                    # Send message based on type
                    sent_message = await self._send_message(context, channel, message, reply_to_id)
                    
                    # Store message mapping
                    if sent_message:
                        self.message_ids[message.message_id][channel] = sent_message.message_id
                        self.logger.info(f"Message replicated to channel {channel}")
                        
                except Exception as e:
                    self.logger.error(f"Error replicating to channel {channel}: {str(e)}")

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")

    def _get_entities_and_text(self, message) -> tuple[str, List[MessageEntity]]:
        """Extract text and entities while preserving formatting"""
        text = message.text or message.caption or ""
        entities = message.entities or message.caption_entities or []
        return text, entities

    async def _send_message(self, context: ContextTypes.DEFAULT_TYPE, 
                          channel: int, message: Update.message, 
                          reply_to_id: Optional[int] = None):
        """Helper method to send messages based on type"""
        try:
            # Get text and entities
            text, entities = self._get_entities_and_text(message)
            
            if message.text:
                return await context.bot.send_message(
                    chat_id=channel,
                    text=text,
                    entities=entities,
                    reply_to_message_id=reply_to_id,
                    disable_web_page_preview=False  # Enable link previews
                )
            elif message.photo:
                return await context.bot.send_photo(
                    chat_id=channel,
                    photo=message.photo[-1].file_id,
                    caption=text,
                    caption_entities=entities,
                    reply_to_message_id=reply_to_id
                )
            elif message.video:
                return await context.bot.send_video(
                    chat_id=channel,
                    video=message.video.file_id,
                    caption=text,
                    caption_entities=entities,
                    reply_to_message_id=reply_to_id
                )
            elif message.document:
                return await context.bot.send_document(
                    chat_id=channel,
                    document=message.document.file_id,
                    caption=text,
                    caption_entities=entities,
                    reply_to_message_id=reply_to_id
                )
            
        except Exception as e:
            self.logger.error(f"Error sending message: {str(e)}")
            return None

    async def sync_replies(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sync replies from target channels to source channel"""
        try:
            message = update.channel_post
            chat = await context.bot.get_chat(message.chat_id)
            
            # Get text and entities from reply
            text, entities = self._get_entities_and_text(message)
            
            # Format reply with preserved formatting
            reply_text = f"💬 Reply from {chat.title}:\n{text}"
            
            # Adjust entity offsets to account for the prefix
            prefix_length = len(f"💬 Reply from {chat.title}:\n")
            adjusted_entities = []
            for entity in entities:
                new_entity = MessageEntity(
                    type=entity.type,
                    offset=entity.offset + prefix_length,
                    length=entity.length,
                    url=getattr(entity, 'url', None)
                )
                adjusted_entities.append(new_entity)
            
            await context.bot.send_message(
                self.main_channel,
                text=reply_text,
                entities=adjusted_entities,
                disable_web_page_preview=False  # Enable link previews
            )
            self.logger.info(f"Reply synced from {chat.title}")
        except Exception as e:
            self.logger.error(f"Error syncing reply: {str(e)}") 