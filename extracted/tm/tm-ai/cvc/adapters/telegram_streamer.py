import asyncio
import logging
import html
import re
from aiogram import Bot
from aiogram.enums import ParseMode

logger = logging.getLogger("cvc.telegram_streamer")

def convert_markdown_to_telegram_html(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(
        r'```(?:(\w+)\n)?(.*?)```', 
        lambda m: f'<pre><code class="language-{m.group(1) or ""}">{m.group(2)}</code></pre>', 
        text, 
        flags=re.DOTALL
    )
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    text = re.sub(r'(?<![A-Za-z0-9])\*(?!\s)([^\*]+?)(?<!\s)\*(?![A-Za-z0-9])', r'<i>\1</i>', text, flags=re.DOTALL)
    text = re.sub(r'~~(.*?)~~', r'<s>\1</s>', text, flags=re.DOTALL)
    return text

class TelegramStreamer:
    def __init__(self, bot: Bot, chat_id: int, message_id: int):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id
        self.buffer = ""
        self.last_sent = ""
        self.is_flushing = False
        self._stop = False
        self._flush_task = asyncio.create_task(self._flusher())

    async def _flusher(self):
        while not self._stop:
            await asyncio.sleep(1.5)
            await self._flush_now()
            
    async def _flush_now(self):
        if self.buffer != self.last_sent and not self.is_flushing:
            self.is_flushing = True
            try:
                text_to_send = self.buffer[:4000] if self.buffer else "..."
                if not text_to_send.strip():
                    text_to_send = "..."
                
                formatted_text = convert_markdown_to_telegram_html(text_to_send)
                
                await self.bot.edit_message_text(
                    chat_id=self.chat_id,
                    message_id=self.message_id,
                    text=formatted_text,
                    parse_mode=ParseMode.HTML
                )
                self.last_sent = self.buffer
            except Exception as e:
                # e.g., MessageNotModified or rate limit
                pass
            finally:
                self.is_flushing = False

    def push(self, text_chunk: str):
        self.buffer += text_chunk

    async def finalize(self):
        self._stop = True
        if self._flush_task:
            self._flush_task.cancel()
            
        if not self.buffer.strip() and self.last_sent == "":
            try:
                await self.bot.delete_message(self.chat_id, self.message_id)
            except Exception:
                pass
        else:
            await self._flush_now()
