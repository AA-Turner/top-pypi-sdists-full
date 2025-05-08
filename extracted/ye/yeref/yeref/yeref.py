#!/usr/bin/python3
# region data
import ast
import copy
import asyncio
import base64
import gzip
import binascii
import hashlib
import hmac
import io
import json
import logging
import math
import mimetypes
import os
import random
import re
import subprocess

import aioboto3
import asyncpg
import shutil
import sqlite3
import string
import time
import urllib.parse
import zipfile
from html import unescape
from calendar import monthrange
# import whisper
# pip install openai-whisper
from datetime import datetime, timezone, timedelta
# from contextlib import closing
from math import radians, cos, sin, asin, sqrt
from operator import itemgetter
from pathlib import Path
from random import randrange
from urllib.parse import parse_qsl
from urllib.parse import urlparse
from uuid import uuid4

from aiohttp import FormData
import aiofiles
import aiohttp
import aiosqlite
import cairo
import cv2
import emoji
import httplib2
import numpy as np
import requests
import speech_recognition as sr
from PIL import Image, ExifTags
from PIL import ImageOps, ImageDraw, ImageFont
from aiogram import html
from aiogram import types, Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramRetryAfter
from aiogram.types import KeyboardButtonRequestChat, ChatAdministratorRights, LabeledPrice, LinkPreviewOptions, \
    ReactionTypeEmoji, CopyTextButton, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.utils.text_decorations import markdown_decoration
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
from exiftool import ExifToolHelper
from fpdf import FPDF
# import g4f
# from g4f.client import Client
# from g4f.client import AsyncClient
# from g4f.client import Client as G4FClient
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from gtts import gTTS
from loguru import logger
from moviepy import AudioFileClip, VideoClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
from moviepy.video.fx.Crop import Crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from oauth2client.service_account import ServiceAccountCredentials
from openai import AsyncOpenAI
from pydub import AudioSegment
from pyrogram import enums, Client, utils
from pyrogram.errors import FloodWait, UserAlreadyParticipant, UsernameInvalid, BadRequest, SlowmodeWait, \
    UserDeactivatedBan, SessionRevoked, SessionExpired, AuthKeyUnregistered, AuthKeyInvalid, AuthKeyDuplicated, \
    InviteHashExpired, InviteHashInvalid, ChatAdminRequired, UserDeactivated, UsernameNotOccupied, ChannelBanned
from pyrogram.raw import functions
from pyrogram.raw.functions.account import SetPrivacy, SetAccountTTL, SetAuthorizationTTL
from pyrogram.raw.functions.channels import UpdateUsername
from pyrogram.raw.functions.messages import SendReaction
from pyrogram.raw.functions.phone import CreateGroupCall, GetGroupCallJoinAs, SaveDefaultGroupCallJoinAs
from pyrogram.raw.functions.phone import StartScheduledGroupCall
from pyrogram.raw.types import InputGroupCall
from pyrogram.raw.types import InputPrivacyKeyStatusTimestamp, InputPrivacyValueAllowAll, InputPrivacyKeyChatInvite, \
    InputPrivacyKeyAddedByPhone, InputPrivacyKeyForwards, InputPrivacyKeyPhoneNumber, InputPrivacyValueAllowContacts, \
    AccountDaysTTL, InputPrivacyValueDisallowAll, InputPrivacyKeyPhoneCall, InputPrivacyKeyVoiceMessages, \
    InputPrivacyKeyProfilePhoto
from pyrogram.raw.types import ReactionEmoji
# from pytgcalls import PyTgCalls
# from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, GroupCallConfig
# from pytgcalls.types import Update, GroupCallParticipant
from pytoniq_core import Address, begin_cell, Cell, StateInit
from rembg import remove
from stegano import lsb, exifHeader
from telegraph.aio import Telegraph

from yeref.l_ import l_inline_demo, l_inline_bot, l_inline_post, l_inline_media, l_inline_channel, l_inline_group, \
    l_inline_find, l_inline_ai, l_inline_target, l_inline_user, l_inline_tools, l_inline_work, l_post_finish, \
    l_post_time_future, l_generate_calendar_time, l_post_button, l_post_media_toobig, l_post_text, l_post_media, \
    l_post_media_wait, l_post_text_limit, l_me, l_all, l_ids, l_spoiler_text, l_preview_text, l_gallery_text, \
    l_buttons_text, l_weekday_1, l_weekday_2, l_weekday_3, l_weekday_4, l_weekday_5, l_weekday_6, l_weekday_7, \
    l_month_1, l_month_2, l_month_3, l_month_4, l_month_5, l_month_6, l_month_7, l_month_8, l_month_9, l_month_10, \
    l_month_11, l_month_12, l_broadcast_finish, l_broadcast_process, l_post_has_restricted, l_gallery, l_btn, \
    l_post_datetime, l_off, l_post_new, l_post_delete, l_post_change, l_silence, l_grp_btn1, l_grp_btn2, \
    l_choose_direction, l_post_buttons, l_pin, l_preview, l_spoiler, l_broadcast_start, l_post_timer, l_post_date, \
    l_enter, l_subscribe_channel_for_post, l_chn_btn1, l_chn_btn2, l_post_publish, l_recipient, l_inline_sticker, \
    l_template_is_ready, l_all_json, l_one_json, l_order_act, l_rand_act, l_msg_photo, l_msg_gif, l_msg_video, \
    l_msg_video_note, l_msg_audio, l_msg_voice, l_msg_document, l_msg_sticker, l_msg_dice, l_msg_web, l_sec, \
    l_act_wait_title, l_msg_quiz, l_msg_text, l_inline_tonest, l_inline_support, l_donate, l_post_sticker_toobig, \
    l_web_version, l_payment_of_post, l_payment_check_token, l_podcast_start, l_chn_no_rights_for_media, \
    l_refund_title, l_refund_already_done, l_refund_success, l_refund_incorrect, \
    l_tools_has_restricted, l_bot_need_start_add, l_chn_need_boost_for_story, l_bot_need_restart_extra_bot, \
    l_bot_pub_with_payment


# region group links
payment_link = 'http://bagazhznaniy.ru/wp-content/uploads/2014/03/zhivaya-priroda.jpg'
# channel_library_ru_link = 'https://t.me/+f-0AbTALTOg4ODBk'
# channel_library_en_link = 'https://t.me/+CHIMCacxEZw4YjA8'
channel_library_ru_link = 'https://t.me/+KUyJAnkLu8g4ODk0'
channel_library_en_link = 'https://t.me/+iM5BLUu5V6RkMjY0'
channel_library_ru = -1001484489131
channel_library_en = -1001481302043
# -1001481302043
# -1001484489131
# donate_deposit_rub = 'https://t.me/ferey_channel_europe/32'
# donate_deposit_eur = 'https://t.me/ferey_channel_europe/44'
donate_deposit_rub = 'https://t.me/$DizA-t9DwVD6AAAAmzy9_KV6nFA'
donate_deposit_eur = 'https://t.me/$zERl3d9DwVD7AAAAAzKRFdwjhDY'
channel_public_ru = 'https://t.me/ferey_channel_europe'
channel_public_en = 'https://t.me/ferey_channel_en'

ferey_logo_person = 'https://fereysitnerya.github.io/ferey/nft-logo-person.png'
ferey_thumb = 'https://telegra.ph/file/bf7d8c073cdfa91b6d624.jpg'
ferey_theme = 'https://t.me/addtheme/lzbKZktZjqv5VDdY'
ferey_wp = 'https://t.me/bg/Mr2tXPkzQUoGAgAAv-ssUh01-P4'
ferey_set = 'https://t.me/addstickers/ferey_sticker_by_FereyStickerBot'
ferey_emoji = 'https://t.me/addemoji/ferey_emoji_by_FereyStickerBot'

text_jpeg = 'https://telegra.ph/file/0c675e5a3724deff3b2e1.jpg'
bot_logo_jpeg = 'https://telegra.ph/file/99d4f150a52dcf78b3e8a.jpg'
channel_logo_jpeg = 'https://telegra.ph/file/8418e1cd70484eac89477.jpg'
group_logo_jpeg = 'https://telegra.ph/file/a55c9f4e74b86b0b4f55f.jpg'
user_logo_jpeg = 'https://telegra.ph/file/3c14f9f5ed347e51785c7.jpg'
payment_photo = 'https://telegra.ph/file/75747cf7bc68f45a0e8b8.jpg'
logo_photo = 'https://telegra.ph/file/4882ddb35357f1b079659.jpg'
collection_photo = 'https://telegra.ph/file/77bfaa86d45d85a40db0a.jpg'
nft_photo = 'https://telegra.ph/file/835e01e37e17e28638e50.jpg'
post_photo = 'https://telegra.ph/file/fceb60dfdc58efccf9585.jpg'

photo_jpg = 'https://telegra.ph/file/d39e358971fc050e4fc88.jpg'
gif_jpg = 'https://telegra.ph/file/e147d6798a43fb1fc4bea.jpg'
video_jpg = 'https://telegra.ph/file/692d65420f9801d757b0c.jpg'
video_note_jpg = 'https://telegra.ph/file/a0ebd72b7ab97b8d6de24.jpg'
audio_jpg = 'https://telegra.ph/file/15da5534cb4edfbdf7601.jpg'
voice_jpg = 'https://telegra.ph/file/10ada321eaa60d70a125d.jpg'
sticker_jpg = 'https://telegra.ph/file/986323df1836577cbe55d.jpg'
document_jpg = 'https://telegra.ph/file/28b6c218157833c0f4030.jpg'
web_jpg = 'https://fereysitnerya.github.io/ferey/web-jpg.jpg'

bot_instruction_ru = 'https://telegra.ph/FereyBotBot-11-13'
user_instruction_ru = 'https://telegra.ph/FereyUserBot-11-15'
channel_instruction_ru = 'https://telegra.ph/FereyChannelBot-10-21'
group_instruction_ru = 'https://telegra.ph/FereyGroupBot-11-13'
demo_instruction_ru = 'https://telegra.ph/FereyDemoBot-11-15'
tools_instruction_ru = 'https://telegra.ph/FereyToolsBot-11-15'
post_instruction_ru = 'https://telegra.ph/FereyPostBot-11-15'
media_instruction_ru = 'https://telegra.ph/FereyMediaBot-11-15'
find_instruction_ru = 'https://telegra.ph/FereyFindBot-11-15'
ai_instruction_ru = 'https://telegra.ph/FereyAIBot-11-15'
codex_instruction_ru = 'https://telegra.ph/FereyCodexBot-01-30'
tonest_instruction_ru = 'https://telegra.ph/FereyTONestBot-05-20'

bot_instruction_en = 'https://telegra.ph/FereyBotBot-11-13'
user_instruction_en = 'https://telegra.ph/FereyUserBot-11-15'
channel_instruction_en = 'https://telegra.ph/FereyChannelBot-10-21'
group_instruction_en = 'https://telegra.ph/FereyGroupBot-11-13'
demo_instruction_en = 'https://telegra.ph/FereyDemoBot-11-15'
tools_instruction_en = 'https://telegra.ph/FereyToolsBot-11-15'
post_instruction_en = 'https://telegra.ph/FereyPostBot-11-15'
media_instruction_en = 'https://telegra.ph/FereyMediaBot-11-15'
find_instruction_en = 'https://telegra.ph/FereyFindBot-11-15'
ai_instruction_en = 'https://telegra.ph/FereyAIBot-11-15'
codex_instruction_en = 'https://telegra.ph/FereyCodexBot-01-30'
tonest_instruction_en = 'https://telegra.ph/FereyTONestBot-05-20'

codex_instruction_ru = 'https://telegra.ph/Kodeks-04-12'
codex_instruction_en = 'https://telegra.ph/Codex-04-12-6'
# endregion


# region default
BOT_CBAN_ = '☐☐☑☐☐'
BOT_CTRANSLATE_ = '☐'
BOT_CPAY_ = '☐☐☐☐☐'
BOT_CINTEGRATION_ = '☐☐'
BOT_CNOTIFICATION_ = '☐☐☐'
BOT_CUSER_ = '☐☑☐'
BOT_CADMIN_ = '☐☑'

BOT_VARS_ = '{"BOT_PROMO": "#911", "BOT_CHANNEL": 0, "BOT_CHANNELTID": 0, "BOT_GROUP": 0, "BOT_GROUPTID": 0, "BOT_CHATGPT": "", "BOT_GEO": 0, "BOT_TZ": "+00:00", "BOT_DT": "", "BOT_LZ": "en", "BOT_LC": "en", "BOT_ISSTARTED": 0, "BOT_ISMENTIONED": 0}'
BOT_LSTS_ = '{"BOT_ADMINS": [], "BOT_COMMANDS": ["/start"]}'
USER_VARS_ = '{"USER_TEXT": "", "USER_REACTION": "", "USER_PUSH": "", "USER_EMAIL": "", "USER_PROMO": "", "USER_CONTACT": "", "USER_GEO": "", "USER_UTM": "", "USER_ID": 0, "USER_DT": "", "USER_TZ": "+00:00", "USER_LC": "en", "USER_LZ": "en", "USER_ISADMIN": 0, "USER_ISBLOG": 0, "USER_ISPREMIUM": 0, "USER_BALL": 0, "USER_RAND": 0, "USER_QUIZ": 0, "USER_DICE": 0, "MSGID_PAID": 0, "DATE_TIME": 0}'
USER_LSTS_ = '{"USER_UTMREF": [], "USER_PAYMENTS": []}'

UB_CONFIG_ = '☑☑☑☐☐☑☑☐☐☐☐☐☐'
UB_CMONITOR_ = '☐'
UB_CPODCAST_ = '☐☐☑'
UB_CNOTIFY_ = '☑☑☐'

UB_CDECOR_ = '☐☑☐'
UB_CREACTION_ = '☑☐☑'
UB_CTRANSLATE_ = '☐☐'
UB_CTRANSCRIBE_ = '☐☐'

UB_CGEO_ = '☑☑☑☐'
UB_CSENDCNT_ = 1
UB_VARS_ = '{"UB_PROMO": "#911", "UB_CHANNEL": 0, "UB_CHANNELTID": 0, "UB_GROUP": 0, "UB_GROUPTID": 0, "USER_COMMENT": "","UB_TZ": "+00:00", "UB_DT": "", "UB_LZ": "en", "UB_LC": "en"}'
UB_LSTS_ = '{}'

GROUPP_CONFIG_ = '☑☐☑☐☐☐☐☑☐☐☐☐☑☑☑☐☑'
GROUPP_CCHECK_ = '☐☑☐☐☐☐'
GROUPP_CBAN_ = '☐☐☑☐☐'
GROUPP_CCHANNEL_ = '☑☐'
GROUPP_CNEURO_ = '☐☐☐☐☐☐☐☐'
GROUPP_CLINK_ = '☑☑☑'
GROUPP_CSYMBOL_ = '☐☐'
GROUPP_CMEDIA_ = '☑☑☑☑☑☑☑☑☑☐☐'
GROUPP_CFLOOD_ = 0
GROUPP_CDIALOG_ = '☑☑☑'
GROUPP_CLEN_ = 0
GROUPP_CTIMER_ = 0
GROUPP_CWORK_ = ''
GROUPP_CINVITECNT_ = 1
GROUPP_CUSERDELAY_ = 1
GROUPP_CUSER_ = '☐☑☐☐☑'
GROUPP_CADMIN_ = '☑☐'
GROUPP_CPAY_ = '☐☐'
GROUPP_CCOMMENT_ = '☑☑'

CHANNEL_CONFIG_ = '☑☑☑☐☐☐☐'
CHANNEL_CCHECK_ = '☑☐☐☐☐'
CHANNEL_CBAN_ = '☐☐☑☐☐'
CHANNEL_CDECOR_ = '☐☐☐'
CHANNEL_CSYSTEM_ = '☑'
CHANNEL_CPAY_ = '☐☐☐'
CHANNEL_CUSER_ = '☐☑'
# endregion


# region html
html_404 = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><script src="https://telegram.org/js/telegram-web-app.js"></script><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>​</title>
    <style>
        body {{ background-image: url('https://telegra.ph/file/4b093c7e2b68f9f2915b0.jpg'); background-size: cover; background-position: center; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
        .container {{ text-align: center; padding: 30px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; }}
        .error-code {{ font-size: 100px; color: #2c3e50; margin: 0; }}
        .go-back {{ margin-top: 20px; text-decoration: none; color: #3498db; }}
    </style>
</head>
<body>
    <div class="container"><h1 class="error-code">404</h1><a href="https://t.me/FereyBotBot?start=error" class="go-back">@FereyBotBot</a></div>
    <script>
        let tg = window.Telegram.WebApp
        tg.SettingsButton.isVisible = true
        tg.SettingsButton.onClick(async () => {{ tg.openTelegramLink('https://t.me/FereyDemoBot') }})
    </script>
</body>
</html>
"""
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://unpkg.com/@tonconnect/ui@latest/dist/tonconnect-ui.min.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>​</title>

    <style>
        html {{ box-sizing: border-box; }}
        *,*::before, *::after {{ box-sizing: inherit; font-family: Arial, sans-serif; font-weight: 100;}}
        a {{ text-decoration: none; }}
        span {{ color: #007bff; }}
        body {{ margin: 0; padding: 0; overflow-x: hidden; background: var(--tg-theme-bg-color); color: var(--tg-theme-text-color); }}

        .text b, .text u, .text i, .text a, .text code, .text span {{ display: inline; }}
        .text code {{ font-family: 'Courier New', monospace; background-color: #f5f5f5; }}
        .text {{ width: 100%; text-align: justify; color: var(--tg-theme-section-header-text-color); }}   
        .text span {{ margin: -1px; }}

        .container-wrapper {{ max-width: 768px; height: 100vh;  padding: 4px; margin: 0 auto; display: flex; flex-direction: column; justify-content: space-between; gap: 4px; }}
        .container {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; font-size: 14px; gap: 4px; }}

        .media-wrapper {{ -webkit-text-stroke: 0.5px rgba(50, 50, 50, 0.99); position: relative; width: 100%; min-height: 33vh; display: flex; justify-content: center; align-items: flex-start; max-width: 100%; overflow: hidden; }}
        .media {{ width: 100%; max-height: 33vh; object-fit: cover; height: auto; }}
        .media:not(.rounded-media) {{ border-radius: 4px; }}
        .rounded-media {{ border-radius: 50%; }}

        .buttons-wrapper {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 4px;
        }}
        .buttons-row {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 4px;
        }}
        .button {{
            width: 100%;
            height: 35px;

            display: flex;
            justify-content: center;
            align-items: center;
            
            border: 0.1px solid rgba(50, 50, 50, 0.99) !important;
            background-color: var(--tg-theme-button-color);
            color: var(--tg-theme-button-text-color);
            text-align: center;
            border-radius: 4px;
            cursor: pointer;
        }}        
        #media-number {{
            position: absolute;
            top: 1%;
            left: 1%;
            padding: 16px;
            padding-top: 19px;
            font-size: 10px;

            cursor: pointer;
            color: rgba(254, 254, 254, 1.0);
        }}
        #media-prev {{
            position: absolute;
            top: 45%;
            left: 1%;
            padding: 16px;
            cursor: pointer;
            color: rgba(254, 254, 254, 1.0);
        }}
        #media-next {{
            position: absolute;
            top: 45%;
            right: 1%;
            padding: 16px;
            cursor: pointer;
            color: rgba(254, 254, 254, 1.0);
        }}
        .dot {{
            cursor: pointer;
            height: 10px;
            width: 10px;
            margin: 0 2px;

            background-color: rgba(254, 254, 254, 1.0);
            border-radius: 50%;
            border: 0.5px solid rgba(50, 50, 50, 0.99);
            display: inline-block;
            transition: background-color 0.6s ease;
            opacity: 0.2;
        }}

        #media-dots {{ position: absolute; bottom: 1%;  text-align: center; padding: 16px; }}
        .active, .dot:hover {{ opacity: 1; }}
        #media-prev:hover {{ opacity: 0.6; }}
        #media-next:hover {{ opacity: 0.6; }}

        .footer {{
            display: flex;
            flex-direction: column;
            margin-bottom: 4px;
            font-size: 10px;
            gap: 20px;
            user-select: none;
            -webkit-user-select: none;
        }}

        .footer-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        #footer-view {{ color: var(--tg-theme-hint-color); }}
        #footer-link {{ color: var(--tg-theme-link-color); }}
        .happy-container {{ display: flex; flex-direction: column; gap: 5px; }}
        .happy {{ display: flex; justify-content: space-between; }}
        .happy-inner {{ display: flex; align-items: center; }}
        #link {{ text-decoration: underline; color: var(--tg-theme-hint-color); cursor: pointer; }}

        .round-button {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-image: url(https://fereysitnerya.github.io/ferey/red-button.png);
            background-size: cover;
            border: none;
            cursor: pointer;
            margin: 0 5px;
            background-color: rgba(255, 255, 255, 0);
        }}

        .info {{ text-align: center; color: var(--tg-theme-hint-color); }}
    </style>
</head>
<body>
    <div class="container-wrapper">
        <div class="container">{0}{1}{2}</div>
        <div class="footer">
            <div class="happy-container">
                <div class="happy">
                    <div class="happy-inner">
                        <div><a id="link">Click on</a></div>
                        <div><button class="round-button" onclick="transaction()"></button></div>
                    </div>
                    <div id="connect"></div>
                </div>
                <div class="info">and 1 random person in the world will become happy</div>
            </div>

            <div class="footer-inner"><div id="footer-view">👁 {3}</div><div><a id="footer-link" href="{4}">{5}</a></div></div>
        </div>
    </div>
    <script>
        let tg = window.Telegram.WebApp
        tg.ready()
        console.log('script start', tg.initData)
        if (tg.initData === '') throw new Error('404')
        console.log(tg.initDataUnsafe['start_param'])
        let lang = (tg.initData === '') ? 'en' : tg.initDataUnsafe['user']['language_code']
        let theme = tg.colorScheme.toUpperCase()
        let addressContractFriendly = "{9}"
        let owner = "{10}"
        let stateInit = "{11}"
        let shade = "{12}"
        if (addressContractFriendly == '') document.querySelector('.happy-container').style.display = 'none'
        
        const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({{
            manifestUrl: 'https://fereysitnerya.github.io/ferey/tonconnect-manifest.json',
            buttonRootId: 'connect',
            language: lang,
            twaReturnUrl: 'https://t.me/FereyDemoBot',
            uiPreferences: {{ theme: theme, borderRadius: 's' }}
        }})

        document.addEventListener("DOMContentLoaded", async () => {{
            let mediaElement = document.querySelector('.media')
            const mediaList = {8}
            let currentIndex = 0

            async function updateMedia() {{
                let mediaNumber = document.getElementById('media-number');

                if (mediaElement && mediaNumber) {{
                    let currentMedia = mediaList[currentIndex];

                    let newMediaElement;
                    if (currentMedia.endsWith('.mp4')) {{
                        newMediaElement = document.createElement('video');
                        newMediaElement.className = 'media';
                        newMediaElement.src = currentMedia;
                        newMediaElement.controls = true;
                        newMediaElement.autoplay = true;
                        newMediaElement.loop = true;
                        newMediaElement.muted = true;
                    }} 
                    else {{
                        newMediaElement = document.createElement('img');
                        newMediaElement.className = 'media';
                        newMediaElement.src = currentMedia;
                        newMediaElement.alt = 'Media';
                    }}
                    mediaElement.replaceWith(newMediaElement);
                    mediaElement = newMediaElement;

                    mediaNumber.textContent = (currentIndex + 1) + '/' + mediaList.length;
                    const dots = document.getElementsByClassName('dot');
                    for (let i = 0; i < dots.length; i++) dots[i].classList.remove('active');
                    dots[currentIndex].classList.add('active');
                }}
            }}

            let mediaPrev = document.getElementById('media-prev');
            if (mediaPrev) {{
                mediaPrev.addEventListener('click', async () => {{
                    currentIndex = (currentIndex - 1 + mediaList.length) % mediaList.length;
                    await updateMedia()
                }})
            }}

            let mediaNext = document.getElementById('media-next');
            if (mediaNext) {{
                mediaNext.addEventListener('click', async () => {{
                    currentIndex = (currentIndex + 1) % mediaList.length;
                    await updateMedia()
                }})
            }}

            await updateMedia();
            const roundedMedia = document.querySelectorAll('.rounded-media');
            for (let i = 0; i < roundedMedia.length; i++) roundedMedia[i].style.width = "auto";

            tonConnectUI.uiOptions = {{ language: lang, uiPreferences: {{ theme: theme }} }}
            tg.SettingsButton.isVisible = true
            tg.SettingsButton.onClick(async () => {{ tg.openTelegramLink('https://t.me/FereyDemoBot') }})
            
            let [linkText, hintText] = await translateClick()
            document.getElementById("link").textContent = linkText
            document.querySelector(".info").textContent = hintText

            document.getElementById("link").addEventListener("click", async (event) => {{
                event.preventDefault()
                tg.openLink(`https://tonviewer.com/${{addressContractFriendly}}`, {{try_instant_view: true}})
            }})  
            document.querySelector('[data-tc-button="true"]').style.height = "35px";
            
            if (shade !== "0") {{
                if (shade === "white") {{
                    document.querySelectorAll('.button').forEach(button => {{
                        button.style.backgroundColor = 'white'
                        button.style.color = 'black'
                    }})
                }}
                else if (shade === "black") {{
                    document.querySelectorAll('.button').forEach(button => {{
                        button.style.backgroundColor = 'black'
                    }})
                }}
                else if (shade === "orange") {{
                    document.querySelectorAll('.button').forEach(button => {{
                        button.style.backgroundColor = 'orange'
                    }})
                }}
                else if (shade === "green") {{
                    document.querySelectorAll('.button').forEach(button => {{
                        button.style.backgroundColor = 'green'
                    }})
                }}
                else if (shade === "purple") {{
                    document.querySelectorAll('.button').forEach(button => {{
                        button.style.backgroundColor = 'purple'
                    }})
                }}
                else if (shade === "blue") {{
                    document.querySelectorAll('.button').forEach(button => {{
                        button.style.backgroundColor = 'var(--tg-theme-button-color)';
                    }})
                }}
            }}
            
            let currentMonth = (new Date()).getMonth()
            if (currentMonth === 10 || currentMonth === 11 || currentMonth === 0) {{
                var link = document.createElement('link')
                link.href = 'https://cdn.jsdelivr.net/gh/Alaev-Co/snowflakes/dist/snow.min.css'
                link.rel = 'stylesheet'
                document.head.appendChild(link)

                var script = document.createElement('script')
                script.src = 'https://cdn.jsdelivr.net/gh/Alaev-Co/snowflakes/dist/Snow.min.js'
                document.body.appendChild(script)
                script.onload = function () {{ new Snow() }}
            }}
        }})

        async function transaction() {{
            let message = [{{
                address: addressContractFriendly,
                amount: 50000000,
                payload: "",
                stateInit: stateInit,
            }}]
            console.log('transcation', message);

            try {{
                console.log(`https://tonviewer.com/${{addressContractFriendly}}`);
                const result = await tonConnectUI.sendTransaction({{ validUntil: Math.round(Date.now() / 1000) + 5*60, messages: message, }});
            }} catch (e) {{
                console.log(e)
                if (!tonConnectUI.connected) {{ tg.showAlert(await translateAlert()); }}
            }}
        }}
        async function translateAlert() {{
            result = "First, you need to connect a TON wallet"
            if (lang === "zh") {{ result = "首先，你需要连接一吨钱包"; }}
            else if (lang === "ar") {{ result = "أولا ، تحتاج إلى توصيل محفظة طن" }}
            else if (lang === "es") {{ result = "Primero debe conectar la billetera TON"; }}
            else if (lang === "ru") {{ result = "Сначала необходимо подключить TON-кошелек"; }}
            else if (lang === "fr") {{ result = "Vous devez d'abord connecter TON portefeuille"; }}
            return result;
        }}
        async function translateClick() {{
            let linkText = "Click on"
            let hintText = "and 1 random person in the world will become happy"

            if (lang === "zh") {{
                linkText = "点击"
                hintText = "世界上有一个随机的人会变得快乐"
            }}
            else if (lang === "ar") {{
                linkText = "انقر على"
                hintText = "و 1 شخص عشوائي في العالم سوف تصبح سعيدة"
            }}
            else if (lang === "es") {{
                linkText = "Haga clic en"
                hintText = "y 1 persona al azar en el mundo será feliz"
            }}
            else if (lang === "ru") {{
                linkText = "Жми на"
                hintText = "и 1 случайный человек в мире станет счастливым"
            }}
            else if (lang === "fr") {{
                linkText = "Cliquez sur"
                hintText = "et 1 personne au hasard dans le monde sera heureux"
            }}
            return [linkText, hintText];
        }}

        async function fetchData(url) {{
            try {{
                const response = await fetch(url);
                console.log('response:', response)
            }} catch (error) {{
                console.log('Error fetching data:', error);
                return null;
            }}
        }}

        async function handleButtonClick(button) {{
            const url = button.dataset.url;
            const idArr = button.id.split("-");

            let getUrl;
            if (idArr[1] === 'payment') {{
                tg.openInvoice(url, async (status) => {{
                    getUrl = `/{6}?msg_id={7}&btn_id=${{idArr[2]}}&cnt_id=${{idArr[3]}}&kind=${{idArr[1]}}&status=${{status}}&${{tg.initData}}`;
                    await fetchData(getUrl);
                    location.reload();
                }});
            }} else if (idArr[1] === 'contact') {{
                tg.requestContact(async (status) => {{
                    getUrl = `/{6}?msg_id={7}&btn_id=${{idArr[2]}}&cnt_id=${{idArr[3]}}&kind=${{idArr[1]}}&status=${{status}}&${{tg.initData}}`;
                    await fetchData(getUrl);
                    location.reload();
                    console.log(getUrl);
                }});
            }} else if (idArr[1] === 'like') {{
                getUrl = `/{6}?msg_id={7}&btn_id=${{idArr[2]}}&cnt_id=${{idArr[3]}}&kind=${{idArr[1]}}&status=click&${{tg.initData}}`;
                await fetchData(getUrl);
                location.reload();
            }} else if (url.startsWith('https://t.me/')) {{
                tg.openTelegramLink(url);
                getUrl = `/{6}?msg_id={7}&btn_id=${{idArr[2]}}&cnt_id=${{idArr[3]}}&kind=${{idArr[1]}}&status=link&${{tg.initData}}`;
                await fetchData(getUrl);
                location.reload();
            }} else {{
                tg.openLink(url, {{try_instant_view: true}});
                getUrl = `/{6}?msg_id={7}&btn_id=${{idArr[2]}}&cnt_id=${{idArr[3]}}&kind=${{idArr[1]}}&status=link&${{tg.initData}}`;
                await fetchData(getUrl);
                location.reload();
            }}
        }}

        let buttonsClass = document.getElementsByClassName('button');
        let startUrl = `/web?tgWebAppStartParam={6}_{7}&${{tg.initData}}`;
        console.log('startUrl = ', startUrl);
        fetchData(startUrl);
        for (let i = 0; i < buttonsClass.length; i++)  buttonsClass[i].addEventListener('click', async () => {{ await handleButtonClick(buttonsClass[i]); }});
    </script>
</body>
</html>
"""
html_donations = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://unpkg.com/@tonconnect/ui@latest/dist/tonconnect-ui.min.js"></script>
    <script src="{0}"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Web3</title>

    <style>
        html {{
            box-sizing: border-box;
        }}

        *,
        *::before,
        *::after {{
            box-sizing: inherit;
            font-family: Arial, sans-serif;
            font-weight: 100;
            user-select: none;
            -webkit-user-select: none;
        }}

        body {{
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            background: var(--tg-theme-bg-color);
            color: var(--tg-theme-text-color);
        }}

        .container {{
            position: relative;
            max-width: 768px;
            height: 100vh;
            padding: 4px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .container-inner {{
            max-width: 768px;
            height: 100vh;
            padding: 4px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            gap: 12px;
        }}
        
        #languageSelect, #themeSelect {{
            border-radius: 4px !important;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            font-size: 10px;
            background: var(--tg-theme-bg-color);
        }}
        
        #connect {{
            position: absolute;
            top: 4px;
            right: 4px;
        }}

        .counter,
        .invoice,
        .main,
        .comment,
        .action {{
            display: flex;
            align-items: center;
            justify-content: space-around;
            text-align: center;
            font-size: 16px;
            cursor: auto;
        }}

        .comment {{
            margin-top: 20px;
            margin-bottom: 20px;
        }}

        .counter-before,
        .counter-after,
        .invoice-before,
        .invoice-after,
        .main-before,
        .main-after,
        .comment-before,
        .comment-after {{
            flex: 1;
            font-size: 16px;
            color: var(--tg-theme-section-header-text-color);
        }}

        .counter-inner {{
            min-width: 120px;
            max-width: 120px;
        }}

        #segments {{
            font-size: 20px;
            color: rgba(222, 222, 222, 1.0);
            background-color: rgba(22, 22, 22, 1.0);
            padding: 9px 9px 9px 9px;
            border-radius: 24px;
            text-align: center;
        }}

        .invoice-inner {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            cursor: pointer;
        }}

        .invoice-inner input[type="number"] {{
            border-radius: 24px;
            padding: 9px 9px 9px 9px;
            text-align: center;
            color: rgba(140, 150, 160, 0.99);
            font-size: 16px
            min-width: 120px;
            max-width: 120px;
            min-height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
        }}

        .round-button {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background-image: url(https://fereysitnerya.github.io/ferey/red-button.png);
            background-size: cover;
            border: none;
            cursor: pointer;
            padding: 0;
            margin: 0;
            background-color: rgba(255, 255, 255, 0);
        }}

        .comment-inner input[type="text"] {{
            border-radius: 24px;
            padding: 9px 9px 9px 9px;
            text-align: center;
            color: rgba(140, 150, 160, 0.99);
            min-width: 120px;
            max-width: 120px;
            min-height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
        }}

        .comment-after-button {{
            border-radius: 24px;
            padding: 9px;
            background-color: rgba(65, 160, 240, 1.0);
            color: rgba(250, 250, 250, 1.0);
            border: none;
            max-width: 95%;
            min-height: 40px;
            font-size: 16px;
            cursor: pointer;
        }}

        #link {{
            text-align: center;
            color: #aaaaaa;
            cursor: pointer;
        }}

        .action {{
            display: none;
        }}

        .comment-before-button,
        .action-ton-button {{
            border-radius: 24px;
            min-height: 40px;
            padding: 9px;
            font-size: 16px;
            white-space: nowrap;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
        }}

        .action-get-button {{
            border-radius: 24px;
            border: none;
            background-color: rgba(65, 160, 240, 1.0);
            color: rgba(250, 250, 250, 1.0);

            min-height: 40px;
            padding: 9px;
            font-size: 16px;
            cursor: pointer;
            white-space: nowrap;
        }}

        .action-del-button {{
            border-radius: 24px;
            background-color: rgba(250, 250, 250, 1.0);
            color: rgba(65, 160, 240, 1.0);

            min-height: 40px;
            padding: 9px;
            font-size: 16px;
            cursor: pointer;
            white-space: nowrap; 
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
        }}

        .comment-before,
        .action-before {{
            position: absolute;
            left: calc(0% + 4px);
        }}

        .comment-inner,
        .action-inner {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            padding: 0 5px;
        }}

        .comment-after,
        .action-after {{
            position: absolute;
            right: calc(0% + 4px);
        }}
        #balance {{
            font-size: 14px;
        }}
        .footer {{
            display: flex;
            flex-direction: column;

            margin-bottom: 4px;
            font-size: 10px;
            gap: 16px;
        }}

        .footer-inner {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        }}

        #footer-view {{
            color: rgba(140, 150, 160, 0.99);
        }}

        #footer-link {{
            color: rgba(140, 150, 160, 0.99);
            text-decoration: none;
        }}
        
        .owner-text {{
            width: 100%;
            text-align: justify;
            display: none;
            color: var(--tg-theme-section-header-text-color);
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="container-inner">
            <div class="header">
                <div class="theme">
                    <select id="themeSelect">
                        <option value="LIGHT">🌖</option>
                        <option value="DARK">🌒</option>
                    </select>
                </div>
                <div class="language">
                    <select id="languageSelect">
                        <option value="en">🇬🇧</option>
                        <option value="zh">🇨🇳</option>
                        <option value="ar">🇦🇪</option>
                        <option value="es">🇪🇸</option>
                        <option value="ru">🇷🇺</option>
                        <option value="fr">🇫🇷</option>
                    </select>
                </div>
                <div id="connect"></div>
            </div>

            <div class="counter">
                <div class="counter-before">Made happy</div>
                <div id="segments" class="counter-inner">000000</div>
                <div class="counter-after">people</div>
            </div>

            <div class="invoice">
                <div class="invoice-before">Make happy:</div>
                <div class="invoice-inner">
                    <input type="number" id="invoice-input" step="0.1" min="0" value="0.05">
                </div>
                <div class="invoice-after">people</div>
            </div>

            <div class="main">
                <div class="main-before">Click on the smart contract button</div>
                <div><button class="round-button" onclick="transaction()"></button></div>
                <div class="main-after">and somewhere in the world, 1 random person will become happy</div>
            </div>

            <div class="comment">
                <div class="comment-before"><button disabled class="comment-before-button">A wish:</button></div>
                <div class="comment-inner"><input type="text" id="comment-input" maxlength="64" placeholder="..."></div>
                <div class="comment-after"><button class="comment-after-button" onclick="comment()">Generate</button>
                </div>
            </div>

            <a id="link">View the transaction</a>

            <div class="owner-text">
                You are logged in as the owner: you can withdraw funds to the balance of the connected wallet or delete
                the
                smart
                contract:
            </div>

            <div class="action">
                <div class="action-before"><button disabled id="balance" class="action-ton-button">0.000000 TON</button>
                </div>
                <div class="action-inner"><button class="action-get-button" onclick="get()">Withdraw</button></div>
                <div class="action-after"><button class="action-del-button" onclick="del()">Delete</button></div>
            </div>
        </div>
        <div class="footer-inner">
            <div id="footer-view">👁 0</div>
            <div><a id="footer-link" href="{1}">{2}</a></div>
        </div>
    </div>
    <script>
        let c = 0
        let b = 0
        let isInit = 0
        let tg = window.Telegram.WebApp;
        tg.ready()
        console.log('start', tg)
        if (tg.initData === '') throw new Error('404');
        let lang = (tg.initData === '') ? 'en' : tg.initDataUnsafe['user']['language_code']
        let theme = tg.colorScheme.toUpperCase();
        let payload_get = 'te6cckEBAQEABgAACAAAA48mr63n';
        let payload_del = 'te6cckEBAQEABgAACAAAA5BtVOCp';
        let addressContractFriendly = "{3}"
        let owner = "{4}"
        let stateInit = "{5}"
        
        let tonConnectUI = new TON_CONNECT_UI.TonConnectUI({{
            manifestUrl: 'https://fereysitnerya.github.io/ferey/tonconnect-manifest.json',
            buttonRootId: 'connect',
            language: lang,
            twaReturnUrl: 'https://t.me/FereyDemoBot',
            uiPreferences: {{ theme: theme, borderRadius: 'm' }} 
        }})

        document.addEventListener("DOMContentLoaded", async () => {{
            document.getElementById("link").href = `https://tonviewer.com/${{addressContractFriendly}}`;
            document.getElementById("link").style.display = "none";
            document.getElementById("invoice-input").value = "1.5";

            const savedTheme = localStorage.getItem('theme');
            if (savedTheme) {{
                await applyTheme(savedTheme);
                document.getElementById('themeSelect').value = savedTheme;
            }}

            document.getElementById('themeSelect').addEventListener('change', async () => {{
                const selectedTheme = event.target.value;
                await applyTheme(selectedTheme);
                localStorage.setItem('theme', selectedTheme);
            }})

            const savedLang = localStorage.getItem('lang');
            if (savedLang) {{
                await applyLang(savedLang);
                document.getElementById('languageSelect').value = savedLang;
            }}

            document.getElementById('languageSelect').addEventListener('change', async () => {{
                const selectedLang = event.target.value;
                await applyLang(selectedLang);
                localStorage.setItem('lang', selectedLang);
            }})

            await comment()
            c = await getCounter(addressContractFriendly);
            isInit = c ? 1 : 0
            let tmp = parseInt(c, 16).toString().padStart(6, '0');
            document.getElementById("segments").textContent = tmp;
            localStorage.setItem('counter', tmp); 
            document.getElementById("footer-view").textContent = `👁 ${{parseInt(c, 16).toString()}}`;
            
            let currentMonth = (new Date()).getMonth()
            if (currentMonth === 10 || currentMonth === 11 || currentMonth === 0) {{
                var link = document.createElement('link')
                link.href = 'https://cdn.jsdelivr.net/gh/Alaev-Co/snowflakes/dist/snow.min.css'
                link.rel = 'stylesheet'
                document.head.appendChild(link)

                var script = document.createElement('script')
                script.src = 'https://cdn.jsdelivr.net/gh/Alaev-Co/snowflakes/dist/Snow.min.js'
                document.body.appendChild(script)
                script.onload = function () {{ new Snow() }}
            }}
        }})

        async function applyTheme(theme) {{
            if (theme === 'DARK') {{
                document.querySelector("body").style.background = "#1E2337";
                document.querySelector("body").style.color = "#F7F9FB";

                document.querySelector(".comment-before-button").style.background = "#1E2337";
                document.querySelector(".comment-before-button").style.color = "rgba(140, 150, 160, 0.99)";
                document.querySelector(".action-ton-button").style.background = "#1E2337";
                document.querySelector(".action-ton-button").style.color = "rgba(140, 150, 160, 0.99)";
            }}
            else {{
                document.querySelector("body").style.background = "#F7F9FB";
                document.querySelector("body").style.color = "#1E2337";

                document.querySelector(".comment-before-button").style.background = "#F7F9FB";
                document.querySelector(".comment-before-button").style.color = "rgba(140, 150, 160, 0.99)";
                document.querySelector(".action-ton-button").style.background = "#F7F9FB";
                document.querySelector(".action-ton-button").style.color = "rgba(140, 150, 160, 0.99)";
            }}
            tonConnectUI.uiOptions = {{ uiPreferences: {{ theme: theme }} }}
        }}

        async function applyLang(lang) {{
            tg.SettingsButton.isVisible = true
            tg.SettingsButton.onClick(async () => {{ tg.openTelegramLink('https://t.me/FereyDemoBot') }})
            
            if (lang === 'zh') {{
                document.querySelector(".counter-before").textContent = "快乐";
                document.querySelector(".counter-after").textContent = "人";
                document.querySelector(".invoice-before").textContent = "快乐:";
                document.querySelector(".invoice-after").textContent = "人";

                document.querySelector(".main-before").textContent = "点击智能合约按钮";
                document.querySelector(".main-after").textContent = "而在世界的某个地方, 1随机的人会变得快乐";
                document.querySelector(".comment-before-button").textContent = "一个愿望:";
                document.querySelector(".comment-after-button").textContent = "生成";

                document.getElementById("link").textContent = "查看交易";
                document.querySelector(".owner-text").textContent = "您以所有者身份登录：您可以将资金提取到连接的钱包的余额或删除智能合约:";
                document.querySelector(".action-get-button").textContent = "带出来";
                document.querySelector(".action-del-button").textContent = "移走";
            }}
            else if (lang === 'ar') {{
                document.querySelector(".counter-before").textContent = "جعل سعيد:";
                document.querySelector(".counter-after").textContent = "الإنسان";
                document.querySelector(".invoice-before").textContent = "اجعلهم سعداء:";
                document.querySelector(".invoice-after").textContent = "الإنسان";

                document.querySelector(".main-before").textContent = "انقر على زر العقد الذكي";
                document.querySelector(".main-after").textContent = "وفي مكان ما في العالم ، 1 شخص عشوائي سوف تصبح سعيدة";
                document.querySelector(".comment-before-button").textContent = "أمنية:";
                document.querySelector(".comment-after-button").textContent = "توليد";

                document.getElementById("link").textContent = "عرض المعاملة";
                document.querySelector(".owner-text").textContent = "لقد قمت بتسجيل الدخول كمالك: يمكنك سحب الأموال إلى رصيد المحفظة المتصلة أو حذف العقد الذكي:";
                document.querySelector(".action-get-button").textContent = "أخرج";
                document.querySelector(".action-del-button").textContent = "إزالة";
            }}
            else if (lang === 'es') {{
                document.querySelector(".counter-before").textContent = "Hecho feliz";
                document.querySelector(".counter-after").textContent = "personas";
                document.querySelector(".invoice-before").textContent = "Hacer feliz:";
                document.querySelector(".invoice-after").textContent = "personas";

                document.querySelector(".main-before").textContent = "Haga clic en el botón de contrato inteligente";
                document.querySelector(".main-after").textContent = "y en algún lugar del mundo, 1 persona al azar será feliz";
                document.querySelector(".comment-before-button").textContent = "Deseo:";
                document.querySelector(".comment-after-button").textContent = "Generar";

                document.getElementById("link").textContent = "Ver transacción";
                document.querySelector(".owner-text").textContent = "Usted ha iniciado sesión como propietario: puede retirar fondos al saldo de la billetera conectada o eliminar el contrato inteligente:";
                document.querySelector(".action-get-button").textContent = "Retirar";
                document.querySelector(".action-del-button").textContent = "Eliminar";
            }}
            else if (lang === 'ru') {{
                document.querySelector(".counter-before").textContent = "Сделаны счастливыми";
                document.querySelector(".counter-after").textContent = "человек";
                document.querySelector(".invoice-before").textContent = "Сделать счастливыми:";
                document.querySelector(".invoice-after").textContent = "человек";

                document.querySelector(".main-before").textContent = "Нажми на кнопку смарт-контракта";
                document.querySelector(".main-after").textContent = "и где-то в мире 1 случайный человек станет счастливым";
                document.querySelector(".comment-before-button").textContent = "Пожелание:";
                document.querySelector(".comment-after-button").textContent = "Генерировать";

                document.getElementById("link").textContent = "Посмотреть транзакцию";
                document.querySelector(".owner-text").textContent = "Вы зашли как владелец: можно вывести средства на баланс подключенного кошелька или удалить смарт-контракт:";
                document.querySelector(".action-get-button").textContent = "Вывести";
                document.querySelector(".action-del-button").textContent = "Удалить";
            }}
            else if (lang === 'fr') {{
                document.querySelector(".counter-before").textContent = "Fait heureux";
                document.querySelector(".counter-after").textContent = "personnes";
                document.querySelector(".invoice-before").textContent = "Rendre heureux:";
                document.querySelector(".invoice-after").textContent = "personnes";

                document.querySelector(".main-before").textContent = "Cliquez sur le bouton du contrat intelligent";
                document.querySelector(".main-after").textContent = "et quelque part dans le monde, 1 personne au hasard deviendra heureuse";
                document.querySelector(".comment-before-button").textContent = "Vœu:";
                document.querySelector(".comment-after-button").textContent = "Générer";

                document.getElementById("link").textContent = "Voir la transaction";
                document.querySelector(".owner-text").textContent = "Vous êtes connecté en tant que propriétaire: vous pouvez retirer des fonds sur le solde du portefeuille connecté ou supprimer le contrat intelligent:";
                document.querySelector(".action-get-button").textContent = "Retirer";
                document.querySelector(".action-del-button").textContent = "Supprimer";
            }}
            else {{
                document.querySelector(".counter-before").textContent = "Made happy";
                document.querySelector(".counter-after").textContent = "people";
                document.querySelector(".invoice-before").textContent = "Make happy:";
                document.querySelector(".invoice-after").textContent = "people";

                document.querySelector(".main-before").textContent = "Click on the smart contract button";
                document.querySelector(".main-after").textContent = "and somewhere in the world, 1 random person will become happy";
                document.querySelector(".comment-before-button").textContent = "A wish:";
                document.querySelector(".comment-after-button").textContent = "Generate";

                document.getElementById("link").textContent = "View the transaction";
                document.querySelector(".owner-text").textContent = "You are logged in as the owner: you can withdraw funds to the balance of the connected wallet or delete the smart contract:";
                document.querySelector(".action-get-button").textContent = "Withdraw";
                document.querySelector(".action-del-button").textContent = "Delete";
            }}
            tonConnectUI.uiOptions = {{ language: lang }}
        }}

        tonConnectUI.onStatusChange(async (wallet) => {{
            console.log('onStatusChange');
            console.log(wallet);
            if (tonConnectUI.connected) {{
                document.getElementById("link").style.display = "block";

                if (owner === tonConnectUI.account.address) {{
                    document.querySelector(".owner-text").style.display = "block";
                    document.querySelector(".action").style.display = "block";
                    await sleep(2222)
                    b = await balance(addressContractFriendly);
                    document.getElementById("balance").innerText = `${{b.toFixed(6)}} TON`;
                }}
                else {{
                    document.querySelector(".owner-text").style.display = "none";
                    document.querySelector(".action").style.display = "none";
                }}
            }}
            else {{
                document.getElementById("link").style.display = "none";
                document.querySelector(".owner-text").style.display = "none";
                document.querySelector(".action").style.display = "none";
            }}
        }})

        document.getElementById('invoice-input').addEventListener('input', async () => {{
            let cnt = parseFloat(document.getElementById('invoice-input').value)
            if (isNaN(cnt)) {{
                cnt = 1
                document.getElementById('invoice-input').value = cnt
            }}
        }})

        async function transaction(tx_type = 0) {{
            console.log('transcation', "tx_type = ", tx_type)
            let amount = document.getElementById("invoice-input").value * 1000000000;
            let payload = "";

            if (tx_type === 1) {{
                amount = 50000000;
                payload = payload_get;
            }}
            else if (tx_type === 2) {{
                amount = 50000000;
                payload = payload_del;
            }}
            else {{
                console.log('isInit = ', isInit)
                if (isInit == 0 && amount < 50000000) {{ amount = 50000000; }}

                if (document.getElementById('comment-input').value !== "") {{
                    const tonweb = new window.TonWeb();
                    let cell = new tonweb.boc.Cell();
                    cell.bits.writeUint(0, 32);
                    cell.bits.writeString(document.getElementById('comment-input').value);

                    try {{
                        let cellBoc = await cell.toBoc();
                        payload = tonweb.utils.bytesToBase64(cellBoc);
                    }} catch (e) {{
                        payload = "te6cckEBAQEAJgAASAAAAAB0b24tc2l0ZSBkb2Vzbid0IHN1cHBvcnQgY29tbWVudB+DAXw="
                    }}
                }}
            }}

            let message = [{{
                address: addressContractFriendly,
                amount: amount,
                payload: payload,
                stateInit: stateInit,
            }}]
            console.log(message);

            try {{
                console.log(`https://tonviewer.com/${{addressContractFriendly}}`);
                const result = await tonConnectUI.sendTransaction({{ validUntil: Math.round(Date.now() / 1000) + 5*60, messages: message, }});
                // tonConnectUI.uiOptions = {{ twaReturnUrl: 'https://t.me/durov'}};
                document.getElementById("link").style.display = "block";

                if (tx_type === 2) {{
                    document.getElementById("segments").textContent = "000000";
                }}
                else {{
                    c = await getCounter(addressContractFriendly);
                    let tmp = parseInt(c, 16).toString().padStart(6, '0');
                    document.getElementById("segments").textContent = tmp;
                    localStorage.setItem('counter', tmp);
                }}
            }} catch (e) {{
                document.getElementById("link").style.display = "none";
                console.log(e)

                if (!tonConnectUI.connected) {{
                    alert(await translateAlert());
                }}
            }}
        }}

        async function comment() {{
            console.log('comment');
            const words = ['aesthetic', 'air', 'alpha', 'boost', 'bravo', 'care', 'cascade', 'change', 'charm', 'cloud', 'codex', 'color', 'connect', 'day', 'demo', 'dream', 'dzen', 'echo', 'element', 'event', 'fest', 'festival', 'field', 'first', 'fit', 'fix', 'flow', 'fly', 'focus', 'forest', 'free', 'fresh', 'fun', 'future', 'gift', 'go', 'grade', 'grape', 'have', 'here', 'high', 'hill', 'hot', 'infinite', 'intensive', 'landing', 'lead', 'league', 'learn', 'level', 'life', 'like', 'lime', 'load', 'look', 'marathon', 'master', 'max', 'medium', 'mind', 'mix', 'mobile', 'more', 'neuro', 'new', 'night', 'note', 'nova', 'ocean', 'omega', 'one', 'orange', 'paint', 'plane', 'platform', 'play', 'podcast', 'portal', 'present', 'pro', 'promo', 'puzzle', 'ready', 'real', 'reality', 'realm', 'round', 'run', 'safe', 'salute', 'scale', 'school', 'sea', 'seminar', 'share', 'sky', 'smart', 'snow', 'social', 'soundcloud', 'special', 'spotify', 'spring', 'star', 'stellar', 'stone', 'subscribe', 'summer', 'sun', 'symposium', 'target', 'team', 'technology', 'telegraph', 'telescope', 'testdrive', 'time', 'top', 'training', 'trend', 'trigger', 'true', 'try', 'turbo', 'unity', 'up', 'vip', 'wait', 'wave', 'win', 'winter', 'wow', 'yes', 'you', 'gracias'];
            const word1 = words[Math.floor(Math.random() * words.length)];
            const word2 = words[Math.floor(Math.random() * words.length)];
            document.getElementById('comment-input').value = word1 + ' ' + word2;
        }}

        async function translateAlert() {{
            let result = "First, you need to connect a TON wallet";
            const savedLang = localStorage.getItem('lang');
            if (savedLang === null) {{
                result = "First, you need to connect a TON wallet"
            }}
            else if (savedLang === "zh") {{
                result = "首先，你需要连接一吨钱包"
            }}
            else if (savedLang === "ar") {{
                result = "أولا ، تحتاج إلى توصيل محفظة طن"
            }}
            else if (savedLang === "es") {{
                result = "Primero debe conectar la billetera TON"
            }}
            else if (savedLang === "ru") {{
                result = "Сначала необходимо подключить TON-кошелек"
            }}
            else if (savedLang === "fr") {{
                result = "Vous devez d'abord connecter TON portefeuille"
            }}
            return result;
        }}

        async function balance(addressContractFriendly) {{
            try {{
                console.log('balance', addressContractFriendly);
                // const tonweb = new window.TonWeb(new TonWeb.HttpProvider('https://testnet.toncenter.com/api/v2/jsonRPC'));
                const tonweb = new window.TonWeb(new TonWeb.HttpProvider('https://toncenter.com/api/v2/jsonRPC'));
                b = await tonweb.getBalance(addressContractFriendly);
                b = b / 1000000000;
            }} catch (error) {{
                console.error('async function balance:', error);
            }} finally {{
                console.log(b);
                return b;
            }}
        }}
        async function getCounter(addressContractFriendly) {{
            try {{
                console.log('getCounter', addressContractFriendly);
                // const tonweb = new window.TonWeb(new TonWeb.HttpProvider('https://testnet.toncenter.com/api/v2/jsonRPC'));
                const tonweb = new window.TonWeb(new TonWeb.HttpProvider('https://toncenter.com/api/v2/jsonRPC'));
                const result = await tonweb.provider.call(addressContractFriendly, 'get_counter', []);
                console.log('GET method result:', result);
                c = (result.exit_code != 0) ? 0 : result.stack[0][1];
            }} catch (error) {{
                console.error('async function getCounter:', error);
            }} finally {{
                console.log(c);
                return c;
            }}
        }}

        async function get() {{
            console.log('get');
            await transaction(1);
        }}
        async function del() {{
            console.log('del');
            await transaction(2);
        }}
        async function sleep(ms) {{
            return new Promise(resolve => {{
                setTimeout(resolve, ms)
            }}
            )
        }}
    </script>
</body>

</html>"""
html_cpay = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/tgs-player.js"></script>
    <script src="https://unpkg.com/@tonconnect/ui@latest/dist/tonconnect-ui.min.js"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Web3</title>

    <style>
        html {{ box-sizing: border-box; }}

        *,
        *::before,
        *::after {{
            box-sizing: inherit;
            font-family: Arial, sans-serif;
            font-weight: 100;
            user-select: none;
            -webkit-user-select: none;
        }}

        body {{
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            background: var(--tg-theme-bg-color);
            color: var(--tg-theme-text-color);
            font-size: 16px;
        }}

        .container {{
            max-width: 768px;
            height: 100vh;
            padding: 4px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            justify-content: flex-start;
            gap: 5px;
        }}

        .header {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            gap: 5px;
        }}

        #link {{
            text-align: center;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
            color: var(--tg-theme-section-header-text-color);
        }}

        .subscribe {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            gap: 5px;
            color: var(--tg-theme-section-header-text-color);
            font-size: 14px;
            width: 100%;
        }}

        .subscribe-link, .subscribe-text, .subscribe-datalist, .subscribe-input, .address-wallet-input, .address-collection-input {{ width: 50%; }}

        .subscribe-input input[type="number"] {{
            border-radius: 8px;
            text-align: center;
            width: 100%;
            height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
        }}

        #subscribe-datalist-id {{
            border-radius: 8px;
            text-align: center;
            width: 100%;
            height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            color: var(--tg-theme-section-header-text-color);
        }}

        .subscribe-inner {{
            width: 50%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 5px;
        }}

        .address-wallet-input input[type="text"] {{
            border-radius: 8px;
            text-align: center;
            width: 100%;
            height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            font-size: 12px;
            padding: 8px;
        }}

        .address-collection-input input[type="text"] {{
            border-radius: 8px;
            text-align: center;
            width: 100%;
            height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            font-size: 12px;
            padding: 8px;
        }}

        #period {{
            border-radius: 8px;
            text-align: center;
            width: 50%;
            height: 40px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            font-size: 12px;
        }}

        .address-wallet {{
            display: none;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            font-size: 14px;
            gap: 5px;
        }}
        
        .address-collection {{
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
            font-size: 14px;
            gap: 5px;
        }}

        .address-wallet-text,
        .address-collection-text {{
            white-space: nowrap;
            color: var(--tg-theme-section-header-text-color);
            width: 50%;
        }}

        .optional {{
            color: var(--tg-theme-hint-color);
            color: rgba(140, 150, 160, 0.99);
            font-size: 10px;
            align-items: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        #lottie {{
            width: 100%;
            height: 190px;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <div class="subscribe-link"><a id="link" href="{0}">{1}</a></div>
            <div id="connect"></div>
        </div>
        <div class="subscribe">
            <div class="subscribe-inner">
                <div class="subscribe-text">Subscription:</div>
                <div class="subscribe-input">
                    <input type="number" id="invoice-input" step="0.1" min="0.05" value="1.0">
                </div>
            </div>
            <div class="subscribe-inner">
                <div class="subscribe-datalist">
                    <input list="subscribe-datalist-list" id="subscribe-datalist-id" value="TON">
                    <datalist id="subscribe-datalist-list">
                        <option value="TON">TON</option>
                        <option value="USDT">USDT</option>
                    </datalist>
                </div>

                <select id="period">
                    <option value="once" selected>Once</option>
                    <option value="week">Week</option>
                    <option value="month">Month</option>
                    <option value="year">Year</option>
                </select>
            </div>
        </div>

        <div class="address-wallet">
            <div class="address-wallet-text">Адрес коллекции монет:*</div>
            <div class="address-wallet-input"><input type="text" id="address-wallet-input-id" minlength="48"
                    maxlength="48" placeholder="for other currencies">
            </div>
        </div>
        <div class="address-collection">
            <div class="address-collection-text">Адрес коллекции NFT:*</div>
            <div class="address-collection-input"><input type="text" id="address-collection-input-id" minlength="48"
                    maxlength="48" placeholder="for NFT checking">
            </div>
        </div>
        <div class="optional">*не обязательные поля</div>
        <div class="sticker">
            <tgs-player id="lottie" autoplay loop mode="normal"
                src="https://raw.githubusercontent.com/fereysitnerya/ferey/main/AnimatedSticker.tgs">
            </tgs-player>
        </div>
    </div>
    <script>
        let tg = window.Telegram.WebApp
        tg.ready()
        console.log('start', tg)
        let lang = (tg.initData === '') ? 'en' : tg.initDataUnsafe['user']['language_code']
        let theme = tg.colorScheme.toUpperCase()
        let tid = "{2}"
        let owner = "{3}"
        let amount = "{4}"
        let currency = "{5}"
        let period = "{6}"
        let wallet = "{7}"
        let collection = "{8}"
        let addrCollectText = "{22}"
        let argument = window.location.href.split("/").pop().split("?")[0]
        
        const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({{
            manifestUrl: 'https://fereysitnerya.github.io/ferey/tonconnect-manifest.json',
            buttonRootId: 'connect',
            language: lang,
            twaReturnUrl: 'https://t.me/FereyDemoBot',
            uiPreferences: {{ theme: theme, borderRadius: 's' }}
        }})
        document.querySelector('[data-tc-button="true"]').style.minWidth = window.getComputedStyle(document.getElementById('address-collection-input-id')).getPropertyValue('width')
        tonConnectUI.onStatusChange(async (wallet) => {{
            document.querySelector('[data-tc-button="true"]').style.minWidth = window.getComputedStyle(document.getElementById('address-collection-input-id')).getPropertyValue('width')
            console.log('onStatusChange', wallet)
            if (tonConnectUI.connected) {{ owner = tonConnectUI.account.address; }}
        }})

        document.addEventListener("DOMContentLoaded", async () => {{            
            document.querySelector('.subscribe-text').textContent = "{9}"
            if (argument === 'cpay') {{
                document.getElementById('period').querySelector('option[value="once"]').textContent = "{10}"
                document.getElementById('period').querySelector('option[value="week"]').textContent = "{11}"
                document.getElementById('period').querySelector('option[value="month"]').textContent = "{12}"
                document.getElementById('period').querySelector('option[value="year"]').textContent = "{13}"
            }}
            else {{
                document.getElementById('period').querySelector('option[value="once"]').textContent = "{10}"
                document.getElementById('period').querySelector('option[value="week"]').remove()
                document.getElementById('period').querySelector('option[value="month"]').remove()
                document.getElementById('period').querySelector('option[value="year"]').remove()
                document.getElementById('period').getElementsByTagName('option')[0].selected = true
            }}
            document.querySelector('.address-collection-text').textContent = "{16}"
            document.getElementById('address-collection-input-id').setAttribute('placeholder', "{17}")
            document.querySelector('.optional').textContent = "{18}"            
            tg.MainButton.show().setParams({{ text: "{19}", is_active: true, is_visible: true }})
            tg.SettingsButton.isVisible = true
            tg.SettingsButton.onClick(async () => {{ tg.openTelegramLink('https://t.me/FereyDemoBot') }})

            document.getElementById("invoice-input").value = amount;
            document.getElementById("subscribe-datalist-id").value = currency;
            document.getElementById("period").value = period;
            document.getElementById("address-collection-input-id").value = collection;
                        
            document.querySelector('[data-tc-button="true"]').style.minWidth = window.getComputedStyle(document.getElementById('address-collection-input-id')).getPropertyValue('width')
            await sleep(333)
            document.querySelector('[data-tc-button="true"]').style.minWidth = window.getComputedStyle(document.getElementById('address-collection-input-id')).getPropertyValue('width')
        }})

        tg.MainButton.onClick(async () => {{
            amount = document.getElementById("invoice-input").value
            currency = document.getElementById("subscribe-datalist-id").value
            period = document.getElementById("period").value
            collection = document.getElementById("address-collection-input-id").value

            if (!(tonConnectUI.connected)) {{ tg.showAlert("{20}"); return }}
            if (collection.length && (collection.length !== 48 || (!collection.startsWith("UQ") && !collection.startsWith("EQ")))) {{ tg.showAlert("{23}"); return }}
            if (amount === 0 || amount === "0" || amount === "" || amount === undefined) {{ tg.showAlert("{24}"); return }}
            if (currency === 0 || currency === "0" || currency === "" || currency === undefined) {{ tg.showAlert("{24}"); return }}
            
            let body = {{
                'tid': tid,
                'owner': owner,
                'amount': amount,
                'currency': currency,
                'period': period,
                'wallet': "",
                'collection': collection,
                'initData': tg.initData,
            }}
            
            await sendRequest("POST", `/${{argument}}save`, body)
            await sleep(333)
            tg.close()
        }})

        async function sleep(ms) {{ return new Promise(resolve => {{ setTimeout(resolve, ms) }} ) }}
        async function sendRequest(method, url, body = null, isFormData = false) {{
            let res = {{}}
            try {{
                const headers = new Headers({{
                    'Cache-Control': 'no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }})
                if (!isFormData) headers.append('Content-Type', 'application/json')
        
                let response
                if (method === 'GET') {{
                    response = await fetch(url, {{
                        method: method
                    }})
                }} else {{
                    response = await fetch(url, {{
                        method: method,
                        body: isFormData ? body : JSON.stringify(body),
                        headers: headers
                    }})
                }}
        
                res = (method === 'POST') ? await response.json() : {{}}
                return res
            }}
            catch (e) {{ console.log(e) }}
            finally {{ return res }}
        }}
    </script>
</body>

</html>"""
html_upay = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/tgs-player.js"></script>
    <script src="https://unpkg.com/@tonconnect/ui@latest/dist/tonconnect-ui.min.js"></script>
    <script src="{18}"></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Web3</title>

    <style>
        html {{ box-sizing: border-box; }}

        *,
        *::before,
        *::after {{
            box-sizing: inherit;
            font-family: Arial, sans-serif;
            font-weight: 100;
            user-select: none;
            -webkit-user-select: none;
        }}

        body {{
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            background: var(--tg-theme-bg-color);
            color: var(--tg-theme-text-color);
            font-size: 16px;
        }}

        .container {{
            max-width: 468px;
            height: 100vh;
            padding: 4px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            justify-content: flex-start;
            gap: 10px;
        }}

        .header {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            gap: 5px;
        }}

        .subscribe-text {{ width: 50%; }}

        #link {{
            text-align: center;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
            color: var(--tg-theme-section-header-text-color);
        }}

        .subscribe {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            color: var(--tg-theme-section-header-text-color);
            font-size: 14px;
            width: 100%;
            gap: 10px;
        }}

        .optional {{
            color: var(--tg-theme-hint-color);
            color: rgba(140, 150, 160, 0.99);
            font-size: 10px;
            align-items: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        #invoice-input {{
            display: none;
            width: 100%;
            height: 40px;
            
            border-radius: 8px;
            padding: 9px 9px 9px 9px;
            text-align: center;
            color: rgba(140, 150, 160, 0.99);
            color: var(--tg-theme-section-header-text-color);
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
        }}

        #ft-send,
        #nft-get,
        #nft-check {{
            width: 100%;
            height: 40px;

            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            border-radius: 8px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            
            font-size: 14px;
            cursor: pointer;
            background-color: var(--tg-theme-button-color);
            color: var(--tg-theme-button-text-color);
        }}

        #ft-link,
        #nft-link {{
            text-align: center;
            font-size: 14px;
            color: var(--tg-theme-hint-color);
            text-decoration: underline;
            cursor: pointer;
            font-size: 10px;
        }}
        
        .subscribe-ft {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 5px;
            width: 100%;
            text-align: center;
        }}
        
        .subscribe-nft {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 5px;
            width: 100%;
            text-align: center;
        }}
        
        #nft-address {{
            width: 100%;
            height: 40px;
            border-radius: 8px;
            border: 0.5px solid rgba(50, 50, 50, 0.99) !important;
            align-items: center;
            text-align: center;
            cursor: pointer;
        }}
        
        #lottie {{
            width: 100%;
            height: 190px;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: space-between;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <div class="subscribe-link"><a id="link" href="{0}">{1}</a></div>
            <div id="connect"></div>
        </div>
        <div class="subscribe">
            <div class="subscribe-ft">
                <div class="subscribe-ft-text">{11} {4} {5} {20}</div>
                <input type="number" id="invoice-input" step="1" min="1" value="2">
                <div id="ft-send">{12} {4} {5}</div>
                <a class="optional" id="ft-link">{5}</a>
            </div>
            <div class="subscribe-nft">
                <div class="subscribe-nft-text">{13}</div>
                <div id="nft-get">{14}</div>
                <div id="nft-check">{15}</div>
                <input type="text" id="nft-address" minlength="48" maxlength="48" placeholder="{16}">
                <a class="optional" id="nft-link">no</a>
            </div>
        </div>
        <div class="sticker">
            <tgs-player id="lottie" autoplay loop mode="normal"
                src="https://raw.githubusercontent.com/fereysitnerya/ferey/main/AnimatedSticker.tgs">
            </tgs-player>
        </div>
    </div>
    <script>
        let tg = window.Telegram.WebApp
        tg.ready()
        console.log('start', tg)
        if (tg.initData === '') throw new Error('404')
        console.log(tg.initDataUnsafe['start_param'])
        let lang = (tg.initData === '') ? 'en' : tg.initDataUnsafe['user']['language_code']
        let theme = tg.colorScheme.toUpperCase()
        let tid = "{2}"
        let owner = "{3}"
        let amount = "{4}"
        let currency = "{5}"
        let period = "{6}"
        let wallet = "{7}"
        let collection = "{8}"
        let display_ft = "{9}"
        let display_nft = "{10}"
        let period_txt = "{20}"
        let uinfo = {{}}
        let argument = "{24}"
        let comments = "{25}"
        let wallet_currency = wallet
        
        let tonConnectUI = new TON_CONNECT_UI.TonConnectUI({{
            manifestUrl: 'https://fereysitnerya.github.io/ferey/tonconnect-manifest.json',
            buttonRootId: 'connect',
            language: lang,
            twaReturnUrl: 'https://t.me/FereyDemoBot',
            uiPreferences: {{ theme: theme, borderRadius: 's' }}
        }})
        tonConnectUI.onStatusChange(async () => {{
            if (tonConnectUI.connected && wallet_currency === wallet) {{ 
                console.log('wallet_currency', wallet_currency)
                
                let wallet_res = await sendRequest("POST", `uwalletcurrency`, {{ 'tid': tid, 'address': tonConnectUI.account.address, 'currency': currency, 'initData': tg.initData }})
                if (wallet_res['wallet'] !== "") {{
                    wallet_currency = wallet_res['wallet']
                    console.log('wallet_currency', wallet_currency, wallet_res)
                }}
            }}
        }})

        document.addEventListener("DOMContentLoaded", async () => {{
            document.querySelector('.subscribe-ft').style.display = display_ft
            document.querySelector('.subscribe-nft').style.display = display_nft
            tg.MainButton.show().setParams({{ text: "{17}", is_active: true, is_visible: true }})
            tg.SettingsButton.isVisible = true
            tg.SettingsButton.onClick(async () => {{ tg.openTelegramLink('https://t.me/FereyDemoBot') }})
            document.getElementById("ft-link").addEventListener("click", async (event) => {{  tg.openLink(`https://tonviewer.com/${{owner}}`, {{ try_instant_view: true }}) }})
            document.getElementById("nft-link").addEventListener("click", async (event) => {{ tg.openLink(`https://tonviewer.com/${{collection}}`, {{ try_instant_view: true }}) }})    
            document.getElementById("nft-get").addEventListener("click", async (event) => {{  tg.openLink(`https://getgems.io/collection/${{collection}}`, {{ try_instant_view: true }}) }})            
            console.log('argument', argument)
            document.getElementById('invoice-input').style.display = (argument === 'ucomment') ? 'block' : 'none'
            
            uinfo = await sendRequest("POST", `${{argument}}info`, {{ 'tid': tid, 'initData': tg.initData }})
            await setParameters()
            
            let currentMonth = (new Date()).getMonth()
            if (currentMonth === 10 || currentMonth === 11 || currentMonth === 0) {{
                var link = document.createElement('link')
                link.href = 'https://cdn.jsdelivr.net/gh/Alaev-Co/snowflakes/dist/snow.min.css'
                link.rel = 'stylesheet'
                document.head.appendChild(link)

                var script = document.createElement('script')
                script.src = 'https://cdn.jsdelivr.net/gh/Alaev-Co/snowflakes/dist/Snow.min.js'
                document.body.appendChild(script)
                script.onload = function () {{ new Snow() }}
            }}
        }})
        
        async function setParameters() {{
            if (Object.keys(uinfo).length > 0) {{
                console.log('uinfo', uinfo)
                document.getElementById('ft-link').textContent = uinfo['uft']
                document.getElementById('nft-link').textContent = uinfo['unft']
                document.getElementById('nft-address').value = uinfo['nft']
                
                if (uinfo['is_uft']) document.getElementById('ft-send').textContent = '✔️ {12} {4} {5}'
                else document.getElementById('ft-send').textContent = '{12} {4} {5}'
                if (uinfo['is_unft']) document.getElementById('nft-get').textContent = '✔️ {15}'
                else document.getElementById('nft-get').textContent = '{15}'
                
                if (argument === 'ucomment') {{
                    document.getElementById('invoice-input').value = uinfo['cnt']
                    console.log('joke', document.getElementById('invoice-input').value)
                    console.log('joke2', uinfo['cnt'])
                    
                    if (uinfo['is_uft']) document.getElementById('ft-send').textContent = `✔️ {12} ${{uinfo['cnt']}} ${{comments}}`
                    else document.getElementById('ft-send').textContent = `{12} ${{uinfo['cnt']}} ${{comments}}`
                }}
            }}
        }}

        if (argument === 'ucomment') {{
            document.getElementById('invoice-input').addEventListener('input', async () => {{
                let cnt = parseInt(document.getElementById('invoice-input').value)
                if (isNaN(cnt) || cnt % 1 !== 0) {{
                    cnt = 1
                    document.getElementById('invoice-input').value = cnt
                }}
                
                document.getElementById('ft-send').textContent = `{12} ${{cnt}} ${{comments}}`
            }})
        }}
        
        document.getElementById('ft-send').addEventListener('click', async () => {{
            try {{
                console.log('click ft-send')
                if (!(tonConnectUI.connected)) {{ tg.showAlert("{19}"); return }}
                let end = (argument === 'upay') ? period : 'comment'
                let nft = document.getElementById('nft-address').value.trim()
                nft = (nft === undefined) ? "" : nft
                const tonweb = new window.TonWeb()
                let cell = new tonweb.boc.Cell()
                let payload = ""
                let message = []
                let amt = amount
                let cnt = 1
                    
                if (argument === 'ucomment') {{
                    cnt = parseInt(document.getElementById('invoice-input').value)
                    amt = (cnt * parseFloat(amount)).toString()
                    console.log(cnt, amt)
                }}
                
                if (wallet_currency !== "") {{
                    let cell2 = new tonweb.boc.Cell();
                    cell2.bits.writeUint(0, 32);
                    cell2.bits.writeString(`${{tid}}_${{tg.initDataUnsafe['user']['id']}}_${{end}}`);
                          
                    cell.bits.writeUint(0xf8a7ea5, 32)
                    cell.bits.writeUint(Date.now(), 64)
                    cell.bits.writeCoins(tonweb.utils.toNano(amt))
                    cell.bits.writeAddress(new tonweb.utils.Address(owner))
                    cell.bits.writeAddress(new tonweb.utils.Address(owner))
                    cell.bits.writeUint(0, 1)
                    cell.bits.writeCoins(tonweb.utils.toNano('0.05'))
                    cell.bits.writeUint(1, 1)
                    cell.refs.push(cell2)
                    
                    try {{
                        let cellBoc = await cell.toBoc()
                        payload = tonweb.utils.bytesToBase64(cellBoc)
                    }} catch (e) {{ payload = "" }}
                    
                    message = [{{
                        address: wallet_currency,
                        amount: tonweb.utils.toNano('0.16').toString(),
                        payload: payload,
                    }}]
                }}
                else {{
                    cell.bits.writeUint(0, 32)
                    cell.bits.writeString(`${{tid}}_${{tg.initDataUnsafe['user']['id']}}_${{end}}`)
                    
                    try {{
                        let cellBoc = await cell.toBoc();
                        payload = tonweb.utils.bytesToBase64(cellBoc);
                    }} catch (e) {{ payload = "" }}
                    
                    message = [{{
                        address: owner,
                        amount: tonweb.utils.toNano(amt).toString(),
                        payload: payload,
                    }}]
                }}
        
                console.log(message)
                const result = await tonConnectUI.sendTransaction({{ validUntil: Math.round(Date.now() / 1000) + 5*60, messages: message, }});

                let body = {{
                    'tid': tid, 
                    'address': tonConnectUI.account.address,
                    'period': period,
                    'nft': nft,
                    'cnt': cnt.toString(),
                    'initData': tg.initData,
                }}
                uinfo = await sendRequest("POST", `${{argument}}ft`, body)
                await setParameters()
            }} catch (error) {{
                console.error('err:', error);
            }}
        }})
                
        document.getElementById('nft-check').addEventListener('click', async () => {{
            if (!(tonConnectUI.connected)) {{ tg.showAlert("{19}"); return }}
            let nft = document.getElementById('nft-address').value.trim()
            nft = (nft === undefined) ? "" : nft
            
            if (collection !== "" && (nft.length !== 48 || (!nft.startsWith("UQ") && !nft.startsWith("EQ")))) {{
                tg.showAlert("{23}")
                await setParameters()
                return 
            }}
            
            if (nft !== "") {{ 
                uinfo = await sendRequest("POST", `${{argument}}nft`, {{ 'tid': tid, 'address': tonConnectUI.account.address, 'collection': collection, 'nft': nft, 'initData': tg.initData }})
                await setParameters()
                tg.showAlert(uinfo['unft'])
                return
            }}
        }})
        
        async function sendRequest(method, url, body = null, isFormData = false) {{
            let res = {{}}
            try {{
                const headers = new Headers({{
                    'Cache-Control': 'no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                }})
                if (!isFormData) headers.append('Content-Type', 'application/json')
        
                let response
                if (method === 'GET') {{
                    response = await fetch(url, {{
                        method: method
                    }})
                }} else {{
                    response = await fetch(url, {{
                        method: method,
                        body: isFormData ? body : JSON.stringify(body),
                        headers: headers
                    }})
                }}
        
                res = (method === 'POST') ? await response.json() : {{}}
                return res
            }}
            catch (e) {{ console.log(e) }}
            finally {{ return res }}
        }}
        async function fetchData(url) {{ try {{ const response = await fetch(url) }} catch (error) {{ console.log('Error fetching data:', error); }} }}
        tg.MainButton.onClick(async () => {{ 
            if (display_ft === 'flex' && !uinfo['is_uft']) {{ tg.showAlert("{21}"); return }}
            else if (display_nft === 'flex' && !uinfo['is_unft']) {{ tg.showAlert("{22}"); return }}
            tg.openTelegramLink("{0}")
        }})
        
        let startUrl = `/web?tgWebAppStartParam=${{tid}}_${{argument}}&${{tg.initData}}`
        console.log('startUrl = ', startUrl)
        fetchData(startUrl)
    </script>
</body>
</html>"""
# endregion


# region TON
def parse_addr(bits: str) -> Address:
    wc = int(bits[1:9], 2)
    if wc >= 128: wc -= 256
    h_hex = format(int(bits[9:], 2), '064x')
    return Address(f"{wc}:{h_hex}")
# endregion


# region aa
usdt_jetton_master = "EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs"

elly_a = 5900268983
my_tid = 5491025132
BOT_TID_TEST = 6066611486
my_tids = ['5900268983', '6179455648', '6236215930', '5754810063', '5491025132', '5360564451', '6281795468']
allowed_paths = ['ferey_extra', 'ferey_bot', 'ferey_user', 'ferey_channel', 'ferey_group', 'ferey_ai', 'ferey_demo',
                 'ferey_tools', 'ferey_tonest', 'ferey_sticker', 'ferey_post', 'ferey_media', 'ferey_find',
                 'ferey_target', 'ferey_codex', 'ferey_fest', 'anna_birthday']
tids_not_for_trans = [5134596871, 5152320320, 5200969162, 5240041587, 5277505344, 5298580533, 5300792695, 5304873693,
                      5318482236, 5372068352, 5380838469, 5456863561, 5588781655, 5621199443, 5805890320, 5846446387,
                      5850795580, 5868482417, 5951232918, 5962132892, 5969907012]
GROUP_ANON_TID = 1087968824
CHANNEL_BOT_ = 136817688
ferey_channel_europe = -1001471122743
ferey_channel_en = -1001833151619
ferey_channel_es = -1001988190840
ferey_channel_fr = -1001942773697
ferey_channel_ar = -1001913015662
ferey_channel_zh = -1001904073819
e18b_bot = '@e18be3f08cf66117744a889900dc_bot'
ferey_demo_bot = 'FereyDemoBot'
e18b_channel = -1001956430283
kjs = 10000
kjs_wa_w = 380
kjs_wa_h = 558
kjs_trg_w = 140
kjs_trg_h = 50
kjs_delta = 75

free_days_in_app = 30
one_minute = 60
one_hour = 3600
seconds_in_day = 86400
old_tid = 7_000_000_000
old_tid_del = 1_000_000_000
lat_company = 59.395881
long_company = 24.658980
bin_empty = b'\xe2\x81\xa0\xe2\x81\xa0'  # .encode("utf-8")
hex_empty = 'e281a0e281a0'  # .encode("utf-8").hex()  || bytes.fromhex()
str_empty = bin_empty.decode('utf-8')  # ​
prefix_100 = "-100"
log_ = f"\033[{92}m%s\033[0m"
bot_father = "@BotFather"
placeholder = '👩🏽‍💻 /content'
SECTION = 'CONFIG'
LINES_ON_PAGE = 5
short_name = 'me'
const_url = 'https://t.me/'
phone_number = '19999999999'
website = 'https://google.com'
facebook = 'https://www.facebook.com'
telegram_account = 'https://t.me'
ferey_telegram_username = 'ferey_support'
ferey_telegram_demo_bot = 'FereyDemoBot'
ferey_address = "Estônia, Tāllin, Mäepealse, 2/1"
ferey_title = "Ferey Inc."
text_developer_info = (
    "/developer_info\n\n"
    "<blockquote>{\n"
    "\t\"developer_name\": \"Ferey Developer\",\n"
    "\t\"contact_email\": \"ferey.sitner.ya@gmail.com\",\n"
    "\t\"website\": \"tonsite://ferey-official.ton\",\n"
    "\t\"terms_of_service\": \"https://telegram.org/tos/mini-apps\",\n"
    "\t\"privacy_policy\": \"https://telegram.org/privacy-tpa\"\n"
    "}</blockquote>"
)
text_privacy_terms = (
    "/privacy /terms\n\n"
    "<blockquote>{\n"
    "\t\"terms_of_service\": \"https://telegram.org/tos/mini-apps\",\n"
    "\t\"privacy_policy\": \"https://telegram.org/privacy-tpa\"\n"
    "}</blockquote>"
)
commands_ru = [types.BotCommand(command="start", description="⚙️ Перезагрузка"),
               types.BotCommand(command="lang", description="🇫🇷 Язык"),
               types.BotCommand(command="happy", description="🐈 Счастье")]
commands_media_ru = [
    types.BotCommand(command="start", description="⚙️ Перезагрузка"),
    types.BotCommand(command="lang", description="🇫🇷 Язык"),
    types.BotCommand(command="add", description="👩🏽‍💻 Добавить медиа"),
    types.BotCommand(command="del", description="👩🏽‍💻 Удалить медиа"),
    types.BotCommand(command="show", description="👩🏽‍💻 Показать медиа"),
    types.BotCommand(command="titles", description="💭 Нейро-титры"),
]
commands_group_ru = [
    types.BotCommand(command="help", description="⚙️ Помощь"),
    types.BotCommand(command="rules", description="👉🏼 Правила"),
    types.BotCommand(command="report", description="❗ Пожаловаться"),
    types.BotCommand(command="thanks", description="🎉 Поблагодарить"),
    types.BotCommand(command="birthday", description="🥳 Поздравить")
]

bot_emj_react = ["👍", "❤", "🔥", "👏", "🎉", "🙏", "👌", "🕊", "🐳", "❤‍🔥", "🌚", "💯", "⚡", "🏆", "💔", "👻", "👨‍💻", "👀", "🎃", "🤝",
                 "✍", "🎄", "☃", "🗿", "🆒", "💘", "🦄", "👾", "🤷‍♂", "🤷‍♀"]
reactions_2 = ['👍', '❤', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '🤬', '😢', '🎉', '🤩', '🙏', '👌', '🕊', '🤡', '🥱', '🥴', '😍', '🐳',
               '❤\u200d🔥', '🌚', '💯', '🤣', '⚡', '🍌', '🏆', '💔', '🤨', '😐', '🍓', '🍾', '💋', '😈', '😴', '😭', '🤓', '👻',
               '👨\u200d💻', '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍', '🤗', '\U0001fae1', '😂', '🎄', '⛄', ' 🆒', '🗿']
reactions_ = ['👍', '👎', '❤', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '🤬', '😢', '🎉', '🤩', '🤮', '💩', '🙏', '👌', '🕊', '🤡', '🥱',
              '🥴', '😍', '🐳', '❤\u200d🔥', '🌚', '💯', '🤣', '⚡', '🍌', '🏆', '💔', '🤨', '😐', '🍓', '🍾', '💋', '😈', '😴', '😭', '🤓',
              '👻', '👨\u200d💻', '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍', '🤗', '\U0001fae1', '🎅', '🎄', '☃', '💅', '🤪', '🗿', '🆒',
              '💘', '🙉', '🦄', '😘', '💊', '🙊', '😎', '👾', '🤷\u200d♂', '🤷', '🤷\u200d♀', '😡', '😂']
emojis_ = ['🙂', '😶‍🌫️', '🫥', '🎃', '😻', '🫶🏽', '🙌🏽', '👍🏽', '🤌🏾', '🫳🏽', '👉🏼', '☝🏽', '👋🏽', '✍🏽', '🙏🏼', '👣', '🫀', '👤', '👥',
           '👮🏽', '👩🏽‍💻', '🥷🏽', '💁🏽‍♂️', '🤷🏽‍♂️', '👕', '🧢', '🎓', '👓', '🐳', '🐋', '🌱', '🌿', '☘️', '🍀', '🍃', '🍂', '🍁', '🌚',
           '🌗', '🌏', '⭐️', '⚡️', '🔥', '☀️', '🌤️', '❄️', '🫧', '🌬️', '🧊', '🥏', '🎗️', '🧩', '🚀', '🗽', '🗿', '⛰️', '🏔️', '🗻',
           '🏠', '🏙️', '💻', '🎥', '🧭', '⏳', '🔋', '💡', '💵', '💰', '💳', '⚒️', '🛡️', '📍', '🪬', '🛋️', '🎉', '✉️', '📬', '📜', '📄',
           '📅', '🧾', '📇', '📋', '🗄️', '📁', '📰', '📘', '📖', '🖤', '〽️', '🔆', '✅', '🌐', '💠', '🔹', '💭', '🚩']
emojis_white = ["🤍", '🙂', '😶‍🌫️', '🫥', '🎃', '😻', '👉🏼', '🙏🏼', '👓', '🐋', '❄️', '🫧', '🌬️', '🧊', '🗻', '🏙️', '🧭', '💡', '✉️',
                '📄', '🧾', '📇', '📋', '📰', '📖', '🌐', '💠', '💭', "🏳", "☁️", "🌨️", "🌧️", "⛈️", "🌩️", "🎂", "🥛", "🍙", "📉", "📈",
                "❔", "❕", "🪙", "🔍", "🪪", "📝", "🏠", "🏛️", "📨", "📤", ]
emojis_black = ["🖤", '🫶🏽', '🙌🏽', '👍🏽', '🤌🏾', '🫳🏽', '👣', '👮🏽', '👩🏽‍💻', '🥷🏽', '💁🏽‍♂️', '🤷🏽‍♂️', '🎓', '🌚', '🗿', '💻', '⚒️',
                '🪬', '🗄️', '🖤', "🏁", "🏴", "🐜", "💣", "✔️", "🔝", "💱", "🎵", "🎶", "🎤", "🎬", '🎥', "📱", "📲", "📞", "📺", "💻",
                "🗝️", "🧳", '🎮']
emojis_orange = ['🧡', '🙂', '😶‍🌫️', '🫥', '🎃', '😻', "🌓", "🌛", "🌕", "🌗", "🌜", '⭐️', '⚡️', '🔥', '☀️', '🌤️', '🎗️', '💰', '〽️',
                 '🔆', "🧨", "💥", "✨", "🥂", "🍪", "🍌", "🍱", "🥞", "🥧", "🥇", "🏆", "🎗️", '🍂', '🍁', '📜', '👋🏽', '🫀', '🚩', "🐻",
                 "🦊", "🌼", "❗", "❓", "💯", "🎨", "📣", "🎈", "🎫", ]
emojis_green = ['💚', '🌱', '🌿', '☘️', '🍀', '🍃', '🧩', '🗽', '⛰️', '🏔️', '🔋', '✅', "🌳", "🌲", "🎄", "🏕️", "🌵", ]
emojis_purple = ['💜', "🎆", "👾", '🦸🏽‍♀️', '🙎🏽‍♀️', '🦄', '🪻', '☂️', '☔️', '🍆', '🫐', '🪁', '🎆', '🔮', '🧬', '⚛️']
emojis_blue = ["💙", "👤", "👥", "🫂", "🗣️", '👮🏽', '👩🏽‍💻', '👕', '🧢', '👓', '🐳', '🐋', '🌏', '❄️', '🫧', '🧊', '🥏', '🗽', '🏙️',
               '🪬', "✈️", "🔬", '💎', '🛋️', '📬', '📘', '📖', '🌐', '💠', '🔹', "🇸🇴", "🦕", "🦋", "🐦", "🐟", "🆙", "🆓", "🆕", "🆗",
               "🆒", ]
animated_emoji = ["🇸🇴", "🏁", "🏴", "🚩", "🏳", "🦕", "🐻", "🐻‍❄", "🦊", "🐼", "🐈", "🦋", "🐛", "🦟", "🐜", "🦙", "🦬", "🦌", "🐎", "🐂",
                  "🐆", "🐦", "🕊️", "🦆", "🦢", "🦉", "🦜", "🦔", "🐟", "🐳", "🐾", "🌳", "🌼", "🌲", "🎄", "🏕️", "🌵", "🍀", "🌿", "🌱",
                  "☘️", "☁️", "🌨️", "🌧️", "⛈️", "🌩️", "🌓", "🌛", "🌕", "🌗", "🌜", "❄️", "☃️", "☀️", "⛅", "🌦️", "🎉", "💣",
                  "🧨", "🔥", "💥", "✨", "⚡", "🎆", "🥂", "🍪", "🍌", "🍱", "🧃", "🎂", "🥫", "🧋", "🍫", "🧁", "🍮", "🍽️", "🥛", "☕",
                  "🧉", "🥞", "🥧", "🍕", "🍙", "🥪", "🥙", "👌🏽", "🤙🏽", "👏🏽", "👇🏽", "👉🏽", "🤞🏽", "💪🏽", "🙌🏽", "🙏🏽", "👣",
                  "🫱🏽‍🫲🏼", "🫶🏽", "☝🏽", "😶‍🌫", "👤", "👥", "🫂", "🗣️", "👩🏽‍💻", "👾", "🫥", "👀", "🗯", "🗿", "🎃", "❤️", "💙", "🤍",
                  "💔", "🖤", "💓", "❤️‍🔥", "📉", "📈", "☑️", "✔️", "✅", "🆙", "🆓", "🆕", "🆗", "🆒", "🔝", "💱", "❗", "❓", "❔",
                  "❕", "💯", "🎵", "🎶", "🥇", "🏆", "🎗️", "🪙", "🧭", "🎨", "🔍", "⏳", "🎓", "🎤", "📣", "🎈", "🎬", "🚀", "✈️", "🚓",
                  "🚕", "📱", "📲", "📞", "📺", "💻", "🖨️", "⚽", "🏀", "🔬", "🔭", "🗝️", "🎫", "🎟", "🪪", "📝", "📰", "📖", "📨", "📤",
                  "📆", "🗂️", "📂", "📚", "📭", "💼", "👜", "🧳", ]
effects = ['💌', '🍓', '😎', '🤍', '🏃', '👍', '🤩', '🔞', '🔝', '🎃', '😇', '👋', '🎁', '🕊', '📣', '📊', '🌚', '🎉', '👌', '💪', '🍿', '🎂',
           '🕺', '🚌', '🥂', '🧠', '💍', '🛷', '✅', '💔', '🥰', '🧺', '🆒', '🎆', '🛁', '🦄', '💥', '🎮', '👀', '🥶', '🍀', '🎤', '🍑', '💓',
           '🔥', '💯', '🧳', '💐', '💸', '🏆', '🤎', '🫀', '🙈', '🌹', '🤙', '👻', '💘', '💃', '🤗', '🙏', '🗿', '👾', '🎨', '🍆', '👑', '✨',
           '🎄', '🏖', '🎈', '👏', '🐳', '💕', '📸', '💎', '🤷', '🐾', '🛍', '🏊\u200d♂', '🧘\u200d♂', '👮\u200d♂', '🏋\u200d♂',
           '❤\u200d🔥', '❤\u200d🩹', '🏴\u200d☠', '🧑\u200d💻', '👮\u200d♀', '🏃\u200d♀', '🏋\u200d♀', '👨\u200d⚕', '🤷\u200d♀',
           '✌', '☃', '☝', '☕', '⚡', '❤', '✍', '❄', '\U0001faa9', '\U0001fae0', '\U0001fae8', '\U0001faf6']
effects_all = {5107584321108051014: '👍', 5104858069142078462: '👎', 5159385139981059251: '❤', 5104841245755180586: '🔥',
               5046509860389126442: '🎉', 5046589136895476101: '💩', 5170169077011841524: '🥰', 5170166362592510656: '👏',
               5048771083361059460: '😁', 5170257231215591956: '🤔', 5158936234294248618: '🤯', 4967494041374556629: '😱',
               5170149264327704981: '🤬', 5046551865169281494: '😢', 5161554034041029689: '🤩', 5125503964049048317: '🤮',
               5066712811023894584: '🙏', 5066947642655769508: '👌', 5095856784057303751: '🕊', 4988252812317033130: '🤡',
               4988134357119009237: '🥱', 4927250902185673331: '🥴', 5066779159678682060: '😍', 5075655057488217321: '🐳',
               5066576334143095943: '❤\u200d🔥', 4961155507164283482: '🌚', 4961017943656759969: '🌭',
               4962976753686414048: '💯', 5066993302453093673: '🤣', 5123236135417415011: '⚡', 5123233223429587601: '🍌',
               5123046001510188023: '🏆', 5123265598893064880: '💔', 5122846324185629167: '🤨', 5066978240002786236: '😐',
               4961016393173566021: '🍓', 4961122255527478034: '🍾', 4963232093787128618: '💋', 4961092903720977544: '🖕',
               4960944078809203417: '😈', 5109477370893435421: '😴', 5069111056337470630: '😭', 5107633812016202563: '🤓',
               5107144215809229474: '👻', 5107153978269893301: '👨\u200d💻', 5107400329004058326: '👀',
               5107491876231971605: '🎃', 4913625371842183765: '🙈', 4913435779100836551: '😇', 4913510691920413388: '😨',
               4916165059018752691: '🤝', 4913460264709391187: '✍', 4913445953878360935: '🤗',
               4913930782671635058: '\U0001fae1', 4990285736302346915: '🎅', 5066610182780355771: '🎄',
               4989997728680380153: '☃', 5003596415478268711: '💅', 5006239241999483552: '🤪', 5006084210859967333: '🗿',
               5006150512270115734: '🆒', 5089139004234793667: '💘', 5089358816366035753: '🙉', 5089416218603946547: '🦄',
               5159305906424382943: '😘', 5089598484131087029: '💊', 5089447945527362129: '🙊', 4925230459375322151: '😎',
               4927184970142712981: '👾', 5068838802655544199: '🤷', 5069188799540495289: '🤷\u200d♂',
               5066849184825475891: '🤷\u200d♀', 4925068178331010095: '😡', 5127791914602463817: '😂',
               5071394291016795490: '☝', 5087137729863484424: '✅', 5067074180982244082: '✌', 5089460564141278042: '✨',
               5066795381770158548: '❄', 5134366251107222485: '🎂', 5044101728060834560: '🎆', 5046284769743077765: '🎈',
               5089131707085358138: '🏴\u200d☠', 5091878604959122376: '🐾', 5071259338849387492: '👅',
               5089234812070265877: '👋', 5089422278802801345: '👑', 5026104105693611449: '👮\u200d♂',
               5026437541184668623: '💃', 4965608262968804599: '💎', 5026421185949205937: '💐', 5121096477199827757: '💥',
               5125520873335292348: '💸', 5089434807222403861: '🔝', 5089216884876772391: '🔞', 5026494110198924646: '🕺',
               5091606991227323336: '🖖', 4965357582907606094: '😊', 5089524022283076814: '😫',
               5089594618660520655: '😵\u200d💫', 5055413967543861653: '🤍', 5055664432856695007: '🤎',
               5026331292283700185: '🤑', 5071299733016806207: '🤒', 5086991627960976320: '🤕', 5071309894909428639: '🤘',
               5066635132245378011: '🤥', 5091342528616072685: '🤦\u200d♂', 5120906893048415743: '🤭',
               5089343350188802996: '🥳', 5120948558526153760: '🥵', 5026486074315113392: '🥶',
               5136788470928245857: '\U0001faa9', 5068809425079239498: '\U0001fae0', 5091663800759747631: '\U0001fae6',
               5089613774214660825: '\U0001fae8', 5026435775953109827: '\U0001faf5', 4967721189309940952: '\U0001faf6',
               5089178556588622814: '🍑', 5091705285848859672: '🍆', 5222212097680620112: '☕', 5271837150545976153: '✊',
               5224269103547567373: '❤\u200d🩹', 5436014903955561968: '🌹', 5276496378313329689: '🍀',
               5307875387903067038: '🍔', 5426962328371349800: '🍿', 5222238451599949657: '🎁', 5208944110479622965: '🎤',
               5445266293575927895: '🎨', 5334946326251586946: '🎮', 5271956091075313012: '🏃',
               5460834880009026589: '🏃\u200d♀', 5188249592247890215: '🏃\u200d♂', 5332333439947394970: '🏊\u200d♂',
               5273737978517145694: '🏋\u200d♀', 5426964153732449060: '🏋\u200d♂', 5287761837012568140: '🏖',
               5233503459327626386: '👨\u200d⚕', 5204413731731160980: '👨\u200d🍳', 5210988154135261581: '👮\u200d♀',
               5219882692102867066: '💌', 5203973364439337911: '💍', 5271946539068037852: '💓', 5362081989757255882: '💕',
               5310138204307868219: '💪', 5305750439948465683: '📊', 5389104167342063261: '📣', 5449359010861956820: '📸',
               5215253864114045785: '😅', 5296605728725800932: '😉', 5213192219682426206: '😋', 5309785694867043246: '😌',
               5402349567310053720: '😏', 5334945003401654009: '😓', 5323481379206339475: '😔', 5271572997172370296: '😕',
               5264778882896108916: '😚', 5201965948264781569: '😞', 5445159022472746552: '😠', 5303031197369126799: '😤',
               5240195692684658955: '😪', 5386405300087569470: '😬', 5246706837335584772: '😰', 5296477528246983373: '😲',
               5208669928357382382: '😳', 5332534946928016204: '😵', 5462909529601623814: '😶\u200d🌫',
               5361647407786378862: '🙅\u200d♂', 5229123365779828990: '🚌', 5404541362135644327: '🛁',
               5427053755340182171: '🛍', 5465575244003556617: '🛷', 5334911489771844419: '🤙', 5253748075440129301: '🤤',
               5454018882874391666: '🤧', 5330199652950096023: '🤫', 5206579593544219932: '🥂',
               5201687174822510819: '\U0001f979', 5113957245121463396: '🧑\u200d💻', 5314503351369472346: '🧘\u200d♂',
               5206341557866738444: '🧠', 4967478970334315349: '🧳', 5359819272136702255: '🧺',
               5429503093584708815: '\U0001fa77', 5317021413385714861: '🫀'}
effects_my = {5107584321108051014: '👍', 5159385139981059251: '❤', 5104841245755180586: '🔥', 5046509860389126442: '🎉',
              5170169077011841524: '🥰', 5170166362592510656: '👏', 5161554034041029689: '🤩', 5066712811023894584: '🙏',
              5066947642655769508: '👌', 5095856784057303751: '🕊', 5075655057488217321: '🐳',
              5066576334143095943: '❤\u200d🔥', 4961155507164283482: '🌚', 4962976753686414048: '💯',
              5123236135417415011: '⚡', 5123046001510188023: '🏆', 5123265598893064880: '💔', 4961016393173566021: '🍓',
              5107144215809229474: '👻', 5107400329004058326: '👀', 5107491876231971605: '🎃', 4913625371842183765: '🙈',
              4913435779100836551: '😇', 4913460264709391187: '✍', 4913445953878360935: '🤗', 5066610182780355771: '🎄',
              4989997728680380153: '☃', 5006084210859967333: '🗿', 5006150512270115734: '🆒', 5089139004234793667: '💘',
              5089416218603946547: '🦄', 4925230459375322151: '😎', 4927184970142712981: '👾', 5068838802655544199: '🤷',
              5066849184825475891: '🤷\u200d♀', 5071394291016795490: '☝', 5087137729863484424: '✅',
              5067074180982244082: '✌', 5089460564141278042: '✨', 5066795381770158548: '❄', 5134366251107222485: '🎂',
              5044101728060834560: '🎆', 5046284769743077765: '🎈', 5089131707085358138: '🏴\u200d☠',
              5091878604959122376: '🐾', 5089234812070265877: '👋', 5089422278802801345: '👑',
              5026104105693611449: '👮\u200d♂', 5026437541184668623: '💃', 4965608262968804599: '💎',
              5026421185949205937: '💐', 5121096477199827757: '💥', 5125520873335292348: '💸', 5089434807222403861: '🔝',
              5089216884876772391: '🔞', 5026494110198924646: '🕺', 5055413967543861653: '🤍', 5055664432856695007: '🤎',
              5026486074315113392: '🥶', 5136788470928245857: '\U0001faa9', 5068809425079239498: '\U0001fae0',
              5089613774214660825: '\U0001fae8', 4967721189309940952: '\U0001faf6', 5089178556588622814: '🍑',
              5091705285848859672: '🍆', 5222212097680620112: '☕', 5224269103547567373: '❤\u200d🩹',
              5436014903955561968: '🌹', 5276496378313329689: '🍀', 5426962328371349800: '🍿', 5222238451599949657: '🎁',
              5208944110479622965: '🎤', 5445266293575927895: '🎨', 5334946326251586946: '🎮', 5271956091075313012: '🏃',
              5460834880009026589: '🏃\u200d♀', 5332333439947394970: '🏊\u200d♂', 5273737978517145694: '🏋\u200d♀',
              5426964153732449060: '🏋\u200d♂', 5287761837012568140: '🏖', 5233503459327626386: '👨\u200d⚕',
              5210988154135261581: '👮\u200d♀', 5219882692102867066: '💌', 5203973364439337911: '💍',
              5271946539068037852: '💓', 5362081989757255882: '💕', 5310138204307868219: '💪', 5305750439948465683: '📊',
              5389104167342063261: '📣', 5449359010861956820: '📸', 5229123365779828990: '🚌', 5404541362135644327: '🛁',
              5427053755340182171: '🛍', 5465575244003556617: '🛷', 5334911489771844419: '🤙', 5206579593544219932: '🥂',
              5113957245121463396: '🧑\u200d💻', 5314503351369472346: '🧘\u200d♂', 5206341557866738444: '🧠',
              4967478970334315349: '🧳', 5359819272136702255: '🧺', 5317021413385714861: '🫀'}
effects_real_all = {'5107584321108051014': '👍', 5104858069142078462: '👎', '5159385139981059251': '❤',
                    '5104841245755180586': '🔥', '5046509860389126442': '🎉', '5046589136895476101': '💩'}
effects_real_my = {'5107584321108051014': '👍', '5159385139981059251': '❤', '5104841245755180586': '🔥',
                   '5046509860389126442': '🎉'}
# random_key = random.choice(list(result.keys()))
# random_value = random.choice(list(result.values()))


themes_ = ['🐥', '⛄', '💎', '👨\u200d🏫', '🌷', '💜', '🎄', '🎮']
extra_prompt = 'hyper-realistic image, iphone photo, ultra-realistic photography, cinematic photo, uhd motion capture, high-contrast image, 8k camera, atmospheric light'
short_description = f"""👩🏽‍💻 Web3ᵀᴼᴺ-@tg-#neuro apps

Start: t.me/FereyDemoBot
🇬🇧🇨🇳🇦🇪🇪🇸🇷🇺🇫🇷
"""
TGPH_TOKEN_MAIN = 'a9335172886eae62ec0743bf8a4e195286ec30cff067da5fd1db2899d008'
TGPH_TOKENS = {
    "https://telegra.ph/pst-FereyDemoBot-05-08": "f8c69d50846e8d55e08f8e3de514f41266e0150434219059f2c91fb4d75f",
    "https://telegra.ph/pst-FereyBotBot-05-08": "e7f943fcc98bac07ad6aaf6e570d0f51abadf02567938c997dbc1ad1923b",
    "https://telegra.ph/pst-FereyPostBot-05-08": "14085be3058c0a25616d094f4bb65c73dc61f783468f01da41d99fb6ace1",
    "https://telegra.ph/pst-FereyMediaBot-05-08": "cf71a596b7ecdc96d30ddffdbf1e26863dd39755f47b4fc343fc3867f373",
    "https://telegra.ph/pst-FereyChannelBot-05-08": "f43f375b8aec531cee0d5048878943a3ccee97da4143d311d5b2c7ed3237",
    "https://telegra.ph/pst-FereyGroupBot-05-08": "c08f94618b94dd25ef75de70c1ed565853efef5479057c68a5720609bb7f",
    "https://telegra.ph/pst-FereyFindBot-05-08": "2d005bb366dc5bef023d58b93d5f45fb9a02a7d2b0f9063a6fc277b5a62d",
    "https://telegra.ph/pst-FereyTargetBot-05-08": "bda8c0a4b7a35101d34252568acd46df7bd3d8d85f4e13dd35f3bddc2f80",
    "https://telegra.ph/pst-FereyToolsBot-05-08": "ea83403eb6ac7d2ad24d7e7a86163be20cd2d7f4734267808e154a8fd0a6",
    "https://telegra.ph/pst-FereyVPNBot-05-08": "38086caf43905ef827715da999aae0be2427ebd7a05d9ff7420543b50613",
    "https://telegra.ph/pst-FereyAIBot-05-08": "bcda631d991c16b4fdfd15e7af6512bcf8fd679fee6bd4c717f6266671a0",
    "https://telegra.ph/pst-FereyUserBot-05-08": "3698a3432c233bef48c238b35cfe94db844858b2ba98594007c7757dcf03",
    "https://telegra.ph/pst-FereyWorkBot-05-08": "d4930b2a9311ad63f7f0ae3d61ca7224ecf76a2434a50161e239a45199c5",
    "https://telegra.ph/pst-FereyAdsBot-05-08": "c1024508f1a5de4f9544dd10793b1401da95de5719bdcf0b4c9f6c26a672", }
buttons_lang = [types.InlineKeyboardButton(text="🇬🇧 en", callback_data=f"lang_en"),
                types.InlineKeyboardButton(text="🇨🇳 zh", callback_data=f"lang_zh"),
                types.InlineKeyboardButton(text="🇦🇪 ar", callback_data=f"lang_ar"),
                types.InlineKeyboardButton(text="🇪🇸 es", callback_data=f"lang_es"),
                types.InlineKeyboardButton(text="🇷🇺 ru", callback_data=f"lang_ru"),
                types.InlineKeyboardButton(text="🇫🇷 fr", callback_data=f"lang_fr"), ]
# logging.getLogger('aiosqlite').setLevel(logging.WARNING)
# logging.getLogger('httpx').setLevel(logging.WARNING)
logging.basicConfig(level=logging.WARNING)
markupAdmin = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text='⬅️ Prev'), types.KeyboardButton(text='↩️ Menu'),
     types.KeyboardButton(text='➡️️ Next')]], resize_keyboard=True, selective=True, row_width=3)
male_names = ['Adam', 'Antonio', 'Albert', 'Alexandr', 'Anton', 'Appolon', 'Artur', 'Askold', 'Avgust', 'Bogdan',
              'Boris', 'Constantin', 'Daniil', 'David', 'Denis', 'Efim', 'Efrem', 'Elizar', 'Emil', 'Emmanuil',
              'Ernest',
              'Ferapont', 'Filipp', 'Foma', 'Gavriil', 'Gedeon', 'German', 'Gordey', 'Ignat', 'Ilarion', 'Iona', 'Iov',
              'Ipolit',
              'Izmail', 'Klim', 'Lazar', 'Lavr', 'Leonid', 'Lev', 'Luka', 'Makar', 'Maksim', 'Mark', 'Markel', 'Marat',
              'Max',
              'Maximus', 'Miron', 'Modest', 'Nazar', 'Nestor', 'Nik', 'Osip', 'Pankrat', 'Pavl', 'Platon', 'Potap',
              'Prohor',
              'Rafail', 'Renat', 'Rodion', 'Roman', 'Ruslan', 'Serge', 'Sidor', 'Sokrat', 'Safron', 'Spiridon',
              'Stepfan',
              'Taras', 'Tihon', 'Timur', 'Trofim', 'Vadim', 'Viktor', 'Vladlen', 'Zahar']
female_names = ['Ada', 'Agla', 'Aida', 'Akulina', 'Alexandra', 'Alina', 'Alisa', 'Alica', 'Alla', 'Angelica',
                'Angelina', 'Anna', 'Avgustina', 'Avgusta', 'Dana', 'Diana', 'Elena', 'Emilia', 'Eva', 'Evelina',
                'Faina',
                'Kristina', 'Ekaterina', 'Kamila', 'Katerina', 'Karolina', 'Kira', 'Lada', 'Lana', 'Larisa', 'Lina',
                'Lianna',
                'Lilia', 'Liza', 'Ludmila', 'Margarita', 'Maria', 'Marina', 'Marta', 'Melania', 'Mila', 'Naina',
                'Oksana',
                'Paulina', 'Regina', 'Renata', 'Roza', 'Sabina', 'Sofia', 'Svetlana', 'Valentina', 'Valeria',
                'Vasilisa',
                'Vasilina', 'Vera', 'Veronika', 'Vilena', 'Viktoria', 'Ksenia', 'Zlata', 'Inessa', 'Inna', 'Irina',
                'Julia']
surnames = ['Abramovich', 'Adler', 'Barak', 'Bauman', 'Beider', 'Belski', 'Berg', 'Berkovich', 'Bernshtein', 'Behold',
            'Bilarchik', 'Binin', 'Bolkovski', 'Botvin', 'Brainin', 'Brodski', 'Bunin', 'Damari', 'Davidovich', 'Dolin',
            'Dorenik', 'Dutnik', 'Gaisin', 'Galich', 'Gandelman', 'German', 'Gershin', 'Gilkin', 'Ginzburg', 'Golanski',
            'Goldberg', 'Gorbik', 'Gurari', 'Gutman', 'Hardin', 'Hazin', 'Ivkin', 'Kabuli', 'Katser', 'Kafka',
            'Kaganin', 'Kamadei', 'Kantor', 'Kaplan', 'Kaplanak', 'Katsman', 'Katz', 'Keller', 'Kim', 'Kogan',
            'Kolchak', 'Konoval', 'Kopelman', 'Kotin', 'Kovalik', 'Kramer', 'Krasnovich', 'Kravets', 'Kristol',
            'Kulisher', 'Lamberg', 'Lazar', 'Lekin', 'Lenski', 'Levan', 'Leviev', 'Levin', 'Levora', 'Levtak', 'Makler',
            'Malik', 'Malkin', 'Mandel', 'Mandelman', 'Markovets', 'Marks', 'Marlin', 'Marshak', 'Mask', 'Mazenger',
            'Meider', 'Mekin', 'Mendes', 'Miller', 'Merkin', 'Miro', 'Mits', 'Mitzer', 'Mizrani', 'Molin', 'Morgen',
            'Morovez', 'Novak', 'Novinski', 'Ohman', 'Pagon', 'Palevi', 'Perelman', 'Perez', 'Polak', 'Pushman',
            'Rabin', 'Rivlin', 'Romanovich', 'Rosalinksi', 'Rosin', 'Rubinski', 'Rudskoi', 'Ruvin', 'Serfin',
            'Sheidlin', 'Shengin', 'Shtal', 'Shuller', 'Shuster', 'Sikora', 'Sitner', 'Sokol', 'Sverdlin', 'Talesnik',
            'Talin', 'Teplinski', 'Tokach', 'Trofim', 'Turski', 'Tverdin', 'Valter', 'Vesman', 'Veller', 'Veniamin',
            'Venski', 'Veron', 'Zakon', 'Zelin', 'Zelman', 'Zlatan']
trg_utms = ['360', 'ad', 'advert', 'aesthetic', 'ai', 'air', 'alpha', 'beta', 'big', 'blog', 'boost', 'bot', 'box',
            'brainstorm', 'bravo', 'buy', 'calc', 'care', 'cascade', 'change', 'channel', 'charm', 'chat', 'front',
            'click', 'cloud', 'club', 'codex', 'color', 'command', 'connect', 'copy', 'course', 'day', 'demo', 'dev',
            'discord', 'discount', 'doc', 'docum', 'document', 'download', 'dream', 'dzen', 'echo', 'element', 'event',
            'facebook', 'fast', 'fest', 'festival', 'field', 'file', 'first', 'fit', 'fix', 'flow', 'fly', 'focus',
            'for', 'forest', 'free', 'fresh', 'fun', 'future', 'get', 'gift', 'giga', 'git', 'go', 'grade', 'grape',
            'guide', 'hackathon', 'have', 'here', 'high', 'hill', 'hot', 'hub', 'ig', 'infinite', 'info', 'intensive',
            'landing', 'last', 'lead', 'league', 'learn', 'lesson', 'level', 'life', 'like', 'lime', 'limit', 'link',
            'linkedin', 'load', 'look', 'map', 'marathon', 'master', 'mastermind', 'max', 'medium', 'meet', 'method',
            'mind', 'mix', 'mobile', 'more', 'msg', 'neuro', 'new', 'newsletter', 'night', 'nike', 'node', 'note',
            'nova', 'number', 'ocean', 'omega', 'one', 'orange', 'paint', 'pinterest', 'plane', 'platform', 'play',
            'podcast', 'portal', 'post', 'present', 'press', 'pro', 'promo', 'puzzle', 'quick', 'ran', 'rate', 'read',
            'ready', 'real', 'reality', 'realm', 'red', 'reddit', 'refer', 'referral', 'review', 'round', 'run', 'safe',
            'salute', 'save', 'scale', 'school', 'sea', 'seminar', 'seo', 'service', 'session', 'set', 'share', 'shop',
            'sky', 'smart', 'snow', 'social', 'soundcloud', 'special', 'spotify', 'spring', 'star', 'stat', 'status',
            'stellar', 'stone', 'subscribe', 'summer', 'sun', 'symposium', 'tap', 'taplink', 'target', 'team', 'tech',
            'technology', 'tele', 'telegram', 'telegraph', 'telescope', 'ten', 'testdrive', 'text', 'this', 'tiktok',
            'time', 'top', 'training', 'trend', 'trigger', 'true', 'try', 'turbo', 'unity', 'university', 'unsubscribe',
            'up', 'utm', 'vimeo', 'vip', 'wait', 'wave', 'web', 'webinar', 'webmaster', 'website', 'week', 'win',
            'winter', 'wordpress', 'work', 'workbook', 'workshop', 'wow', 'x', 'yes', 'you', 'you2b', 'youtube', 'yt',
            'zip', 'gracias']
cat2_mp3 = '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QAEBBgBAAQEGAEABAQYAQAEBBgBAAQEGAEABAQYAQAEBBgBAAQEGAEABAQYAQAEBBgBAAQEGAEABAQYAQAEBBgBAwf8CzeceU00bvzsAAAAASUVORK5CYIIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVUQUdLaXR0ZW4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABUZWxlZ3JhbSBNZXNzZW5nZXIAAAAAAAAAAAAAAABOb3RpZmljYXRpb24gU291bmRzIFZvbC4gMQAAAAAyMDIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/w=='
img_jpg = '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'
text1024 = f"""<code>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Morbi tincidunt augue interdum velit euismod in pellentesque massa. Sit amet aliquam id diam maecenas. Morbi tristique senectus et netus. Eu feugiat pretium nibh ipsum consequat nisl vel. Ipsum dolor sit amet consectetur adipiscing elit duis tristique sollicitudin. Consectetur purus ut faucibus pulvinar elementum integer enim. Dignissim enim sit amet venenatis. Varius vel pharetra vel turpis nunc eget. Erat pellentesque adipiscing commodo elit. Iaculis nunc sed augue lacus viverra vitae congue eu. At imperdiet dui accumsan sit. Viverra vitae congue eu consequat ac. Ut ornare lectus sit amet est placerat in egestas. Libero enim sed faucibus turpis in eu mi bibendum. Quis vel eros donec ac odio tempor orci dapibus ultrices. Turpis massa tincidunt dui ut ornare lectus sit. Sit amet massa vitae tortor condimentum lacinia quis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque</code>"""
text2048 = f"""<code>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Morbi tincidunt augue interdum velit euismod in pellentesque massa. Sit amet aliquam id diam maecenas. Morbi tristique senectus et netus. Eu feugiat pretium nibh ipsum consequat nisl vel. Ipsum dolor sit amet consectetur adipiscing elit duis tristique sollicitudin. Consectetur purus ut faucibus pulvinar elementum integer enim. Dignissim enim sit amet venenatis. Varius vel pharetra vel turpis nunc eget. Erat pellentesque adipiscing commodo elit. Iaculis nunc sed augue lacus viverra vitae congue eu. At imperdiet dui accumsan sit. Viverra vitae congue eu consequat ac. Ut ornare lectus sit amet est placerat in egestas. Libero enim sed faucibus turpis in eu mi bibendum. Quis vel eros donec ac odio tempor orci dapibus ultrices. Turpis massa tincidunt dui ut ornare lectus sit. Sit amet massa vitae tortor condimentum lacinia quis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque. Etiam non quam lacus suspendisse faucibus. Enim praesent elementum facilisis leo. Et netus et malesuada fames. Felis donec et odio pellentesque diam. Tellus id interdum velit laoreet id. Faucibus ornare suspendisse sed nisi lacus sed viverra. Risus sed vulputate odio ut enim blandit volutpat maecenas volutpat. Eget gravida cum sociis natoque penatibus et magnis. Elit at imperdiet dui accumsan. Facilisis gravida neque convallis a cras semper. Pretium viverra suspendisse potenti nullam ac tortor vitae. Non quam lacus suspendisse faucibus interdum posuere lorem ipsum dolor. Purus in mollis nunc sed id semper. Dignissim sodales ut eu sem integer vitae. Ridiculus mus mauris vitae ultricies. Orci sagittis eu volutpat odio facilisis mauris. Quis commodo odio aenean sed adipiscing diam donec adipiscing. Natoque penatibus et magnis dis parturient montes. Libero id faucibus nisl tincidunt eget nullam non nisi est. Vitae elementum curabitur vitae nunc sed velit dignissim sodales ut. Ullamcorper malesuada proin libero</code>"""
text4096 = f"""<code>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Morbi tincidunt augue interdum velit euismod in pellentesque massa. Sit amet aliquam id diam maecenas. Morbi tristique senectus et netus. Eu feugiat pretium nibh ipsum consequat nisl vel. Ipsum dolor sit amet consectetur adipiscing elit duis tristique sollicitudin. Consectetur purus ut faucibus pulvinar elementum integer enim. Dignissim enim sit amet venenatis. Varius vel pharetra vel turpis nunc eget. Erat pellentesque adipiscing commodo elit. Iaculis nunc sed augue lacus viverra vitae congue eu. At imperdiet dui accumsan sit. Viverra vitae congue eu consequat ac. Ut ornare lectus sit amet est placerat in egestas. Libero enim sed faucibus turpis in eu mi bibendum. Quis vel eros donec ac odio tempor orci dapibus ultrices. Turpis massa tincidunt dui ut ornare lectus sit. Sit amet massa vitae tortor condimentum lacinia quis. Nulla malesuada pellentesque elit eget gravida cum sociis natoque. Etiam non quam lacus suspendisse faucibus. Enim praesent elementum facilisis leo. Et netus et malesuada fames. Felis donec et odio pellentesque diam. Tellus id interdum velit laoreet id. Faucibus ornare suspendisse sed nisi lacus sed viverra. Risus sed vulputate odio ut enim blandit volutpat maecenas volutpat. Eget gravida cum sociis natoque penatibus et magnis. Elit at imperdiet dui accumsan. Facilisis gravida neque convallis a cras semper. Pretium viverra suspendisse potenti nullam ac tortor vitae. Non quam lacus suspendisse faucibus interdum posuere lorem ipsum dolor. Purus in mollis nunc sed id semper. Dignissim sodales ut eu sem integer vitae. Ridiculus mus mauris vitae ultricies. Orci sagittis eu volutpat odio facilisis mauris. Quis commodo odio aenean sed adipiscing diam donec adipiscing. Natoque penatibus et magnis dis parturient montes. Libero id faucibus nisl tincidunt eget nullam non nisi est. Vitae elementum curabitur vitae nunc sed velit dignissim sodales ut. Ullamcorper malesuada proin libero nunc consequat interdum. Tincidunt augue interdum velit euismod. Fringilla ut morbi tincidunt augue. Est velit egestas dui id ornare arcu. Vestibulum rhoncus est pellentesque elit. Massa tincidunt dui ut ornare lectus sit. Tristique et egestas quis ipsum suspendisse ultrices gravida dictum. Ornare massa eget egestas purus viverra accumsan in nisl. Tristique nulla aliquet enim tortor at. Imperdiet nulla malesuada pellentesque elit eget gravida cum sociis. Sit amet tellus cras adipiscing. Interdum velit laoreet id donec ultrices tincidunt arcu. Arcu cursus euismod quis viverra nibh. Mattis pellentesque id nibh tortor id aliquet lectus proin nibh. Viverra adipiscing at in tellus integer feugiat. Ipsum faucibus vitae aliquet nec ullamcorper sit amet. Et sollicitudin ac orci phasellus egestas tellus. Enim nulla aliquet porttitor lacus. Sed sed risus pretium quam vulputate dignissim. Gravida dictum fusce ut placerat orci. Vel orci porta non pulvinar neque. Fames ac turpis egestas maecenas pharetra convallis. Sit amet cursus sit amet dictum sit. Tellus in hac habitasse platea dictumst vestibulum rhoncus est pellentesque. Venenatis a condimentum vitae sapien. Facilisis sed odio morbi quis commodo odio aenean sed. Aliquet enim tortor at auctor urna nunc. Non odio euismod lacinia at quis risus sed vulputate odio. Aliquam purus sit amet luctus. In est ante in nibh mauris cursus mattis. Nulla facilisi cras fermentum odio eu feugiat pretium nibh. Ut ornare lectus sit amet est. Nunc mi ipsum faucibus vitae aliquet nec. Ac odio tempor orci dapibus ultrices in iaculis. Et netus et malesuada fames ac turpis. Volutpat est velit egestas dui id ornare. Non pulvinar neque laoreet suspendisse interdum. Egestas diam in arcu cursus euismod quis viverra nibh cras. Nulla pellentesque dignissim enim sit amet venenatis. Enim ut sem viverra aliquet eget. Congue nisi vitae suscipit tellus. Sodales neque sodales ut etiam sit amet. Ut ornare lectus sit amet est. Tincidunt arcu non sodales neque sodales ut etiam. Amet risus nullam eget feli ege</code>"""


# endregion


# region db
def sqlite_lower(value_):
    return value_.lower() if value_ else None


def sqlite_upper(value_):
    return value_.upper() if value_ else None


def ignore_case_collation(value1_, value2_):
    if value1_ is None or value2_ is None:
        return 1
    if value1_.lower() == value2_.lower():
        return 0
    elif value1_.lower() < value2_.lower():
        return -1
    else:
        return 1


async def db_select(sql, param=None, db=None):
    retry = 2
    result = []
    try:
        while retry > 0:
            try:
                async with aiosqlite.connect(db, timeout=15) as con:
                    await con.execute('PRAGMA foreign_keys=ON;')
                    await con.create_function("LOWER", 1, sqlite_lower)
                    async with con.execute(sql, param or ()) as cur:
                        result = await cur.fetchall()
                    break  # Успешное выполнение, выходим из цикла
            except Exception as e:
                logger.info(log_ % str(e))
                # Прекратить попытки при критической ошибке
                if 'no such column' in str(e) or 'unable to open database' in str(e) or 'no such table' in str(e):
                    return result
                await asyncio.sleep(round(random.uniform(1, 2), 2))
                retry -= 1
                # Выполняем VACUUM только при оставшихся попытках
                if retry > 0:
                    async with aiosqlite.connect(db) as con:
                        await con.execute("VACUUM")
    finally:
        return result


async def db_change(sql, param=None, db=None):
    retry = 2
    result = -1
    try:
        while retry > 0:
            try:
                async with aiosqlite.connect(db, timeout=15) as con:
                    await con.execute('PRAGMA foreign_keys=ON;')
                    async with con.cursor() as cur:
                        await cur.execute(sql, param or ())
                        await con.commit()
                        result = cur.lastrowid
                    break
            except Exception as e:
                # logger.info(log_ % str(e))
                logger.info(log_ % f"{os.path.basename(db)}: {str(e)} ({retry=})")
                if 'no such column' in str(e) or 'binding' in str(e) or 'unable to open database' in str(
                        e) or 'no such table' in str(e):
                    return
                await asyncio.sleep(round(random.uniform(1, 2), 2))
                retry -= 1  # Уменьшить количество попыток
                # Только после уменьшения `retry` вызвать VACUUM
                if retry > 0:
                    print(f'start VACUUM, {db=}, {sql=}, {param=}')
                    async with aiosqlite.connect(db) as con:
                        await con.execute("VACUUM")
    finally:
        return result


# async def db_select_pg(sql, param=None, db=None):
#     retry = 2
#     while retry > 0:
#         try:
#             with closing(sqlite3.connect(db, timeout=15)) as con:
#                 con.execute('PRAGMA foreign_keys=ON;')
#                 # con.create_collation("NOCASE", ignore_case_collation)
#                 # con.create_function("LOWER", 1, sqlite_lower)
#                 # con.create_function("UPPER", 1, sqlite_upper)
#                 with closing(con.cursor()) as cur:
#                     if param:
#                         cur.execute(sql, param)
#                     else:
#                         cur.execute(sql)
#
#                     return cur.fetchall()
#         except Exception as e:
#             logger.info(log_ % str(e))
#             await asyncio.sleep(round(random.uniform(1, 2), 2))
#             retry -= 1
#     return []


# async def db_change_pg(sql, param=None, db=None):
#     retry = 2
#     while retry > 0:
#         try:
#             with closing(sqlite3.connect(db, timeout=15)) as con:
#                 con.execute('PRAGMA foreign_keys=ON;')
#                 with closing(con.cursor()) as cur:
#                     if param:
#                         cur.execute(sql, param)
#                     else:
#                         cur.execute(sql)
#
#                     con.commit()
#                     return cur.lastrowid
#         except Exception as e:
#             logger.info(log_ % str(e))
#             await asyncio.sleep(round(random.uniform(1, 2), 2))
#             retry -= 1
#     return -1


async def db_bot_create(db):
    con = sqlite3.connect(db, timeout=10)
    try:
        cur = con.cursor()

        # TRG
        cur.execute('''CREATE TABLE IF NOT EXISTS TRG ( 
            TRG_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            TRG_VID         VARCHAR     UNIQUE NOT NULL,
            TRG_TYPE        VARCHAR,
            TRG_CONTENT     VARCHAR,

            TRG_RIGHTID     VARCHAR,
            TRG_RIGHTTYPE   VARCHAR,
            TRG_LEFTID      VARCHAR,
            TRG_LEFTTYPE    VARCHAR
        )''')

        # ACT
        cur.execute('''CREATE TABLE IF NOT EXISTS ACT ( 
            ACT_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            ACT_VID         VARCHAR     UNIQUE NOT NULL,
            ACT_TYPE        VARCHAR,
            ACT_CONTENT     VARCHAR,

            ACT_NEXTID      VARCHAR,
            ACT_NEXTTYPE    VARCHAR
        )''')

        # MSG
        cur.execute('''CREATE TABLE IF NOT EXISTS MSG ( 
            MSG_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            MSG_VID         VARCHAR     UNIQUE NOT NULL,
            MSG_TYPE        VARCHAR,
            MSG_TEXT        VARCHAR,
            MSG_MEDIA       VARCHAR,
            MSG_BUTTONS     VARCHAR,
            
            MSG_CHKBOX      VARCHAR,
            MSG_TEXTF       VARCHAR,  
            MSG_BUTTONSF    VARCHAR,
            MSG_LC          VARCHAR,
            MSG_TRANSLATED  INTEGER     DEFAULT 0,

            MSG_NEXTID      VARCHAR,
            MSG_NEXTTYPE    VARCHAR
        )''')

        # VIEW
        cur.execute('''CREATE TABLE IF NOT EXISTS VIEW ( 
            VIEW_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            ENT_VID         VARCHAR     NOT NULL,
            ENT_TYPE        VARCHAR     NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            UNIQUE (ENT_VID, ENT_TYPE, CHAT_TID)
        )''')

        # LANG
        cur.execute('''CREATE TABLE IF NOT EXISTS LANG ( 
            LANG_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            MSG_ID          INTEGER,
            MSG_LC          VARCHAR,
            
            MSG_TEXT        VARCHAR,
            MSG_BUTTONS     VARCHAR,
            MSG_TEXTF       VARCHAR,
            MSG_BUTTONSF    VARCHAR,
            UNIQUE (MSG_ID, MSG_LC)
        )''')

        # POST
        cur.execute('''CREATE TABLE IF NOT EXISTS POST ( 
            POST_ID            INTEGER      PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            POST_CHATTID       BIGINT       NOT NULL,
            POST_USERTID       BIGINT       NOT NULL,
            POST_USERTUN       VARCHAR,
            POST_TARGET        VARCHAR,
            POST_TYPE          VARCHAR,
            POST_TEXT          VARCHAR,
            POST_MSGID         VARCHAR,
            POST_TELESCOPE     VARCHAR,
            
            POST_BUTTONS       VARCHAR,
            POST_BLOG          VARCHAR,
            POST_WEB           VARCHAR,
            POST_TZ            VARCHAR,
            POST_DT            VARCHAR,
            POST_TR            VARCHAR,
            POST_STATUS        BOOLEAN     DEFAULT 0,
            
            POST_ISBUTTON      BOOLEAN     DEFAULT 0,
            POST_ISDYNAMIC     BOOLEAN     DEFAULT 0,
            POST_ISSOUND       BOOLEAN     DEFAULT 1,
            POST_ISSILENCE     BOOLEAN     DEFAULT 0,
            POST_ISPIN         BOOLEAN     DEFAULT 0,
            POST_ISPREVIEW     BOOLEAN     DEFAULT 0,
            POST_ISSPOILER     BOOLEAN     DEFAULT 0,
            POST_ISGALLERY     BOOLEAN     DEFAULT 0,
            POST_ISFORMAT      BOOLEAN     DEFAULT 0,
            POST_ISTAG         BOOLEAN     DEFAULT 0,
            POST_ISREACTION    VARCHAR,
            POST_ISEFFECT      VARCHAR,
            POST_ISPODCAST     BOOLEAN     DEFAULT 0,
            POST_ISWINDOW      BOOLEAN     DEFAULT 0,
            
            POST_LNK           VARCHAR,
            POST_FILENAME      VARCHAR,
            POST_FID           VARCHAR,
            POST_FIDNOTE       VARCHAR,
            POSTB_FID          VARCHAR,
            POSTB_FIDNOTE      VARCHAR
        )''')

        # PUSH
        cur.execute('''CREATE TABLE IF NOT EXISTS PUSH ( 
            PUSH_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            CHAT_FULLNAME   VARCHAR,
            CHAT_USERNAME   VARCHAR,
            CHAT_ISPREMIUM  BOOLEAN,
            CHAT_LC         VARCHAR,
            POST_ID         INTEGER     NOT NULL,
            BTN_BID       INTEGER     NOT NULL,
            UNIQUE (CHAT_TID, POST_ID, BTN_BID)
        )''')

        # USER
        cur.execute(f'''CREATE TABLE IF NOT EXISTS USER ( 
            USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            USER_TID        BIGINT      UNIQUE
                                        NOT NULL,
            USER_BID        VARCHAR,
            USER_USERNAME   VARCHAR,
            USER_FULLNAME   VARCHAR,

            USER_VARS       VARCHAR     DEFAULT '{USER_VARS_}',
            USER_LSTS       VARCHAR     DEFAULT '{USER_LSTS_}'
        )''')

        # USERBAN
        cur.execute('''CREATE TABLE IF NOT EXISTS USERBAN ( 
            USERBAN_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            USERBAN_TID         BIGINT      UNIQUE,
            USERBAN_USERNAME    VARCHAR     UNIQUE,
            USERBAN_FULLNAME    VARCHAR,
            USERBAN_BAN         VARCHAR, 
            USERBAN_DT          VARCHAR
        )''')

        # NOTICE
        cur.execute('''CREATE TABLE IF NOT EXISTS NOTICE ( 
            NOTICE_ID           INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            NOTICE_TID          BIGINT,
            NOTICE_TYPE         VARCHAR,
            NOTICE_TXT          VARCHAR,
            NOTICE_FID          VARCHAR,
            UNIQUE (NOTICE_TID, NOTICE_TYPE, NOTICE_TXT, NOTICE_FID)
        )''')

        con.commit()
        cur.close()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        con.close()


async def db_usr_create(db):
    con = sqlite3.connect(db, timeout=10)
    try:
        cur = con.cursor()

        # TRG
        cur.execute('''CREATE TABLE IF NOT EXISTS TRG ( 
            TRG_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            TRG_VID         VARCHAR     UNIQUE NOT NULL,
            TRG_TYPE        VARCHAR,
            TRG_CONTENT     VARCHAR,

            TRG_RIGHTID     VARCHAR,
            TRG_RIGHTTYPE   VARCHAR,
            TRG_LEFTID      VARCHAR,
            TRG_LEFTTYPE    VARCHAR
        )''')

        # ACT
        cur.execute('''CREATE TABLE IF NOT EXISTS ACT ( 
            ACT_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            ACT_VID         VARCHAR     UNIQUE NOT NULL,
            ACT_TYPE        VARCHAR,
            ACT_CONTENT     VARCHAR,

            ACT_NEXTID      VARCHAR,
            ACT_NEXTTYPE    VARCHAR
        )''')

        # MSG
        cur.execute('''CREATE TABLE IF NOT EXISTS MSG ( 
            MSG_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            MSG_VID         VARCHAR     UNIQUE NOT NULL,
            MSG_TYPE        VARCHAR,
            MSG_TEXT        VARCHAR,
            MSG_MEDIA       VARCHAR,
            MSG_BUTTONS     VARCHAR,

            MSG_CHKBOX      VARCHAR,
            MSG_TEXTF       VARCHAR,  
            MSG_BUTTONSF    VARCHAR,
            MSG_LC          VARCHAR,
            MSG_TRANSLATED  INTEGER     DEFAULT 0,

            MSG_NEXTID      VARCHAR,
            MSG_NEXTTYPE    VARCHAR
        )''')

        # VIEW
        cur.execute('''CREATE TABLE IF NOT EXISTS VIEW ( 
            VIEW_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            ENT_VID         VARCHAR     NOT NULL,
            ENT_TYPE        VARCHAR     NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            UNIQUE (ENT_VID, ENT_TYPE, CHAT_TID)
        )''')

        # LANG
        cur.execute('''CREATE TABLE IF NOT EXISTS LANG ( 
            LANG_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            MSG_ID          INTEGER,
            MSG_LC          VARCHAR,

            MSG_TEXT        VARCHAR,
            MSG_BUTTONS     VARCHAR,
            MSG_TEXTF       VARCHAR,
            MSG_BUTTONSF    VARCHAR,
            UNIQUE (MSG_ID, MSG_LC)
        )''')

        # POST
        cur.execute('''CREATE TABLE IF NOT EXISTS POST ( 
            POST_ID            INTEGER      PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            POST_TID           BIGINT       UNIQUE NOT NULL,
            POST_CHATTID       BIGINT       NOT NULL,
            POST_USERTID       BIGINT       NOT NULL,
            POST_USERTUN       VARCHAR,
            POST_TARGET        VARCHAR,
            POST_MSGID         VARCHAR,

            POST_TYPE          VARCHAR,
            POST_TEXT          VARCHAR,
            POST_MEDIA         VARCHAR,
            POST_BUTTONS       VARCHAR,
            POST_CHKBOX        VARCHAR,

            POST_WEB           VARCHAR,
            POST_NFT           VARCHAR,
            POST_PAY           VARCHAR,
            POST_BLOG          VARCHAR,

            POST_WATER         VARCHAR,
            POST_STARS         VARCHAR,    
            POST_WALL          VARCHAR,
            POST_EMOJI         VARCHAR,
            POST_THEME         VARCHAR,
            POST_ISMINTED      BOOLEAN      DEFAULT 0,
            POST_MINTLINK      VARCHAR,
            POST_ISPRIVATE     BOOLEAN      DEFAULT 0,

            POST_TZ            VARCHAR,
            POST_DT            VARCHAR,
            POST_TR            VARCHAR,
            POST_STATUS        BOOLEAN      DEFAULT 0
        )''')

        # # POST
        # cur.execute('''CREATE TABLE IF NOT EXISTS POST (
        #     POST_ID            INTEGER      PRIMARY KEY AUTOINCREMENT
        #                                     UNIQUE
        #                                     NOT NULL,
        #     POST_CHATTID       BIGINT       NOT NULL,
        #     POST_USERTID       BIGINT       NOT NULL,
        #     POST_TARGET        VARCHAR,
        #     POST_TYPE          VARCHAR,
        #     POST_TEXT          VARCHAR,
        #     POST_MSGID         VARCHAR,
        #     POST_TELESCOPE     VARCHAR,
        #
        #     POST_BUTTONS       VARCHAR,
        #     POST_BLOG          VARCHAR,
        #     POST_WEB           VARCHAR,
        #     POST_TZ            VARCHAR,
        #     POST_DT            VARCHAR,
        #     POST_TR            VARCHAR,
        #     POST_STATUS        BOOLEAN     DEFAULT 0,
        #
        #     POST_ISBUTTON      BOOLEAN     DEFAULT 0,
        #     POST_ISDYNAMIC     BOOLEAN     DEFAULT 0,
        #     POST_ISSOUND       BOOLEAN     DEFAULT 1,
        #     POST_ISSILENCE     BOOLEAN     DEFAULT 0,
        #     POST_ISPIN         BOOLEAN     DEFAULT 0,
        #     POST_ISPREVIEW     BOOLEAN     DEFAULT 0,
        #     POST_ISSPOILER     BOOLEAN     DEFAULT 0,
        #     POST_ISGALLERY     BOOLEAN     DEFAULT 0,
        #     POST_ISFORMAT      BOOLEAN     DEFAULT 0,
        #     POST_ISTAG         BOOLEAN     DEFAULT 0,
        #     POST_ISVIA         BOOLEAN     DEFAULT 0,
        #     POST_ISREACTION    VARCHAR,
        #     POST_ISEFFECT      VARCHAR,
        #     POST_ISPODCAST     BOOLEAN     DEFAULT 0,
        #     POST_ISWINDOW      BOOLEAN     DEFAULT 0,
        #
        #     POST_REMOJI        VARCHAR,
        #     POST_TIMER         VARCHAR,
        #     POST_THEME         VARCHAR,
        #     POST_WALL          VARCHAR,
        #     POST_ISDESTRUCT    BOOLEAN     DEFAULT 0,
        #
        #     POST_LNK           VARCHAR,
        #     POST_FILENAME      VARCHAR,
        #     POST_FID           VARCHAR,
        #     POST_FIDNOTE       VARCHAR,
        #     POSTB_FID          VARCHAR,
        #     POSTB_FIDNOTE      VARCHAR
        # )''')

        # PUSH
        cur.execute('''CREATE TABLE IF NOT EXISTS PUSH ( 
            PUSH_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            CHAT_FULLNAME   VARCHAR,
            CHAT_USERNAME   VARCHAR,
            CHAT_ISPREMIUM  BOOLEAN,
            CHAT_LC         VARCHAR,
            POST_ID         INTEGER     NOT NULL,
            BTN_BID       INTEGER     NOT NULL,
            UNIQUE (CHAT_TID, POST_ID, BTN_BID)
        )''')

        # GEO
        cur.execute('''CREATE TABLE IF NOT EXISTS GEO ( 
            GEO_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            USER_TID        BIGINT      UNIQUE
                                        NOT NULL,
            USER_FULLNAME   VARCHAR,
            USER_USERNAME   VARCHAR,
            USER_ISPREMIUM  INTEGER,
            USER_PHOTO      VARCHAR,

            GEO_ISPRIORITY  INTEGER     DEFAULT 0
        )''')

        # JOIN
        cur.execute('''CREATE TABLE IF NOT EXISTS INVITE ( 
            INVITE_ID           INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            INVITE_CHATTID      BIGINT      NOT NULL,
            INVITE_USERTID      BIGINT      NOT NULL,
            INVITE_MSGID        INTEGER,
            INVITE_TYPE         VARCHAR,
            INVITE_DATETIME     DATETIME,
            UNIQUE (INVITE_CHATTID, INVITE_USERTID)
        )''')

        # USER
        cur.execute(f'''CREATE TABLE IF NOT EXISTS USER ( 
            USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            USER_TID        BIGINT      UNIQUE
                                        NOT NULL,
            USER_BID        VARCHAR,
            USER_USERNAME   VARCHAR,
            USER_FULLNAME   VARCHAR,

            USER_VARS       VARCHAR     DEFAULT '{USER_VARS_}',
            USER_LSTS       VARCHAR     DEFAULT '{USER_LSTS_}'
        )''')

        # USERB
        cur.execute(f'''CREATE TABLE IF NOT EXISTS USERB ( 
            USERB_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                         UNIQUE
                                         NOT NULL,
            USERB_TID        BIGINT      UNIQUE
                                         NOT NULL,
            USERB_USERNAME   VARCHAR,
            USERB_FULLNAME   VARCHAR,

            USERB_VARS       VARCHAR     DEFAULT '{USER_VARS_}',
            USERB_LSTS       VARCHAR     DEFAULT '{USER_LSTS_}'
        )''')

        # USERG
        cur.execute(f'''CREATE TABLE IF NOT EXISTS USERG ( 
            USERG_ID            INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            USERG_TID           BIGINT      UNIQUE
                                            NOT NULL,
            USERG_USERNAME      VARCHAR,
            USERG_FULLNAME      VARCHAR,
            USERG_PHONE         VARCHAR,
            USERG_PHOTO         VARCHAR,
            USERG_PHOTOCNT      INTEGER     DEFAULT 0,
            USERG_ISPREMIUM     BOOLEAN     DEFAULT 0,
            
            USERG_RANK          INTEGER     DEFAULT 0,
            USERG_COORDINATES   VARCHAR
        )''')

        # USERBAN
        cur.execute('''CREATE TABLE IF NOT EXISTS USERBAN ( 
            USERBAN_ID          INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            USERBAN_TID         BIGINT      UNIQUE,
            USERBAN_USERNAME    VARCHAR     UNIQUE,
            USERBAN_FULLNAME    VARCHAR,
            USERBAN_BAN         VARCHAR, 
            USERBAN_DT          VARCHAR
        )''')

        con.commit()
        cur.close()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        con.close()


async def db_usr_create_extra(db):
    con = sqlite3.connect(db, timeout=10)
    con.execute('PRAGMA foreign_keys=ON;')
    cur = con.cursor()

    # USER
    cur.execute('''CREATE TABLE IF NOT EXISTS USER ( 
        USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_TID        BIGINT      UNIQUE
                                    NOT NULL,
        USER_USERNAME   VARCHAR,
        USER_FULLNAME   VARCHAR,
        USER_ISPREMIUM  INTEGER,

        USER_UTM        VARCHAR,
        USER_PAY        VARCHAR,
        USER_GEO        VARCHAR,
        USER_PHONE      VARCHAR,
        USER_PROMO      VARCHAR,
        USER_EMAIL      VARCHAR,
        USER_TEXT       VARCHAR,
 
        USER_IP         VARCHAR,
        USER_PLATFORM   VARCHAR,
        USER_DEVICE     VARCHAR,

        USER_DTPAID     VARCHAR, 
        USER_ISPAID     INTEGER     DEFAULT 0,
        USER_TYPAID     VARCHAR,
        USER_TXPAID     VARCHAR,

        USER_DT         VARCHAR,
        USER_TZ         VARCHAR,
        USER_LZ         VARCHAR,
        USER_LC         VARCHAR
    )''')

    # FILE
    cur.execute('''CREATE TABLE IF NOT EXISTS FILE (
        FILE_ID             INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        FILE_FILEID         VARCHAR     NOT NULL,
        FILE_FILENAME       VARCHAR,
        UNIQUE (FILE_FILEID, FILE_FILENAME)
    )''')

    # LIKE
    cur.execute('''CREATE TABLE IF NOT EXISTS LIKE ( 
        LIKE_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_ID         INTEGER     NOT NULL,
        POST_ID         INTEGER     NOT NULL
        )''')

    # OFFER
    cur.execute('''CREATE TABLE IF NOT EXISTS OFFER ( 
        OFFER_ID            INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        OFFER_USERTID       BIGINT      NOT NULL,
        OFFER_TEXT          VARCHAR,
        OFFER_MEDIATYPE     VARCHAR,
        OFFER_FILEID        VARCHAR,
        OFFER_FILEIDNOTE    VARCHAR,
        OFFER_FILENAME      VARCHAR,

        OFFER_TGPHLINK      VARCHAR,
        OFFER_ISTGPH        BOOLEAN     DEFAULT 0,
        OFFER_BUTTON        VARCHAR,
        OFFER_ISBUTTON      BOOLEAN     DEFAULT 0,
        OFFER_ISSPOILER     BOOLEAN     DEFAULT 0,
        OFFER_ISPIN         BOOLEAN     DEFAULT 0,
        OFFER_ISSILENCE     BOOLEAN     DEFAULT 0,
        OFFER_ISGALLERY     BOOLEAN     DEFAULT 0,

        OFFER_STATUS        BOOLEAN     DEFAULT 0,
        OFFER_TZ            VARCHAR,
        OFFER_DT            VARCHAR
    )''')

    # HASH
    cur.execute('''CREATE TABLE IF NOT EXISTS HASH (
        HASH_ID     INTEGER     PRIMARY KEY AUTOINCREMENT,
        HASH_STR    TEXT        NOT NULL UNIQUE,
        HASH_VAL    TEXT        NOT NULL UNIQUE
    )
    ''')

    # UB
    cur.execute(f"""CREATE TABLE IF NOT EXISTS UB ( 
        UB_ID              INTEGER     PRIMARY KEY AUTOINCREMENT
                                       UNIQUE
                                       NOT NULL,
        UB_TID             BIGINT      UNIQUE
                                       NOT NULL,
        OWNER_TID          BIGINT,

        UB_APIID           VARCHAR,
        UB_APIHASH         VARCHAR,
        UB_PATH            VARCHAR,
        UB_CLOUD           VARCHAR,
        UB_PHONE           VARCHAR,
        UB_USERNAME        VARCHAR,
        UB_FIRSTNAME       VARCHAR,
        UB_LASTNAME        VARCHAR,
        UB_BIO             VARCHAR,
        UB_ISPREMIUM       BOOLEAN     DEFAULT 0,
        UB_ISMUTUAL        BOOLEAN     DEFAULT 0,
        UB_PHOTO           VARCHAR,
        UB_PHOTOHASH       VARCHAR,
        UB_ADDLIST         VARCHAR,

        UB_STATUS          VARCHAR,
        UB_PID             VARCHAR,
        UB_CMD             VARCHAR,
        UB_RES             VARCHAR,
        UB_UPDATE          VARCHAR,
        UB_INFO            VARCHAR,
        UB_STAT            VARCHAR,
        UB_WAIT            VARCHAR,
        UB_SPAMBOT         VARCHAR,
        UB_LOGIN           VARCHAR,
        UB_AUTODEL         INTEGER     DEFAULT 0,
        UB_DELAY           INTEGER     DEFAULT 0,
        UB_VOTE            VARCHAR,
        UB_FIRSTMSG        VARCHAR,
        UB_SPAMBOTCNT      INTEGER     DEFAULT 0,
        UB_DELTATIME       VARCHAR,
        UB_USERCNT         INTEGER     DEFAULT 0,

        UB_CHANNELTID      BIGINT,
        UB_CHANNELLINK     VARCHAR,
        UB_BOTUSERNAME     VARCHAR,
        UB_BOTTOKEN        VARCHAR,
        UB_BOTQUERY        VARCHAR,
        UB_BOTMARKUP       VARCHAR,
        UB_BOTISPAID       VARCHAR,
        UB_TOKENTGPH       VARCHAR,
        UB_JSONTGPH        VARCHAR,
        UB_PAGETGPH        VARCHAR,

        UB_CONFIG          VARCHAR     DEFAULT '{UB_CONFIG_}',
        UB_CMONITOR        VARCHAR,
        UB_CMONITORWRD     VARCHAR,
        UB_CMONITORSRC     VARCHAR,
        UB_CPODCAST        VARCHAR     DEFAULT '{UB_CPODCAST_}',
        UB_CPODCASTSRC     VARCHAR,
        UB_CPODCASTDST     VARCHAR,
        UB_CNOTIFY         VARCHAR     DEFAULT '{UB_CNOTIFY_}',
        UB_CNOTIFYSRC     VARCHAR,
        
        UB_CDECOR          VARCHAR     DEFAULT '{UB_CDECOR_}',
        UB_CDECORSPOILER   VARCHAR,
        UB_CREACTION       VARCHAR     DEFAULT '{UB_CREACTION_}',
        UB_CTRANSLATE      VARCHAR     DEFAULT '{UB_CTRANSLATE_}',
        UB_CTRANSLATELANG  VARCHAR,
        UB_CTRANSCRIBE     VARCHAR     DEFAULT '{UB_CTRANSCRIBE_}',
        
        UB_CGEO            VARCHAR     DEFAULT '{UB_CGEO_}',
        UB_CGEOCURID       INTEGER     DEFAULT 0,
        UB_CGEOMSGID       INTEGER,

        UB_VARS            VARCHAR     DEFAULT '{UB_VARS_}',
        UB_LSTS            VARCHAR     DEFAULT '{UB_LSTS_}',
        UB_LZ              VARCHAR     DEFAULT 'en',
        UB_LC              VARCHAR     DEFAULT 'en',
        UB_DT              VARCHAR,
        UB_TZ              VARCHAR,
        UB_IP              VARCHAR,
        UB_PORT            INTEGER,
        UB_ISACTIVE        BOOLEAN     DEFAULT 1,
        UB_ISVERIFIED      INTEGER
    )""")

    con.commit()
    cur.close()
    con.close()


async def db_grp_create(db):
    con = sqlite3.connect(db, timeout=10)
    con.execute('PRAGMA foreign_keys=ON;')
    cur = con.cursor()

    # USER
    cur.execute('''CREATE TABLE IF NOT EXISTS USER ( 
        USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_TID        BIGINT      UNIQUE
                                    NOT NULL,
        USER_USERNAME   VARCHAR,
        USER_FULLNAME   VARCHAR,
        USER_ISPREMIUM  INTEGER,

        USER_UTM        VARCHAR,
        USER_PAY        VARCHAR,
        USER_GEO        VARCHAR,
        USER_PHONE      VARCHAR,
        USER_PROMO      VARCHAR,
        USER_EMAIL      VARCHAR,
        USER_TEXT       VARCHAR,

        USER_DTPAID     VARCHAR, 
        USER_ISPAID     INTEGER     DEFAULT 0,
        USER_TYPAID     VARCHAR,
        USER_TXPAID     VARCHAR,

        USER_DT         VARCHAR,
        USER_TZ         VARCHAR,
        USER_LZ         VARCHAR,
        USER_LC         VARCHAR
    )''')

    # FILE
    cur.execute('''CREATE TABLE IF NOT EXISTS FILE (
        FILE_ID             INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        FILE_FILEID         VARCHAR     NOT NULL,
        FILE_FILENAME       VARCHAR,
        UNIQUE (FILE_FILEID, FILE_FILENAME)
    )''')

    # LIKE
    cur.execute('''CREATE TABLE IF NOT EXISTS LIKE ( 
        LIKE_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_ID         INTEGER     NOT NULL,
        POST_ID         INTEGER     NOT NULL
        )''')

    # OFFER
    cur.execute('''CREATE TABLE IF NOT EXISTS OFFER ( 
        OFFER_ID            INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        OFFER_USERTID       BIGINT      NOT NULL,
        OFFER_TEXT          VARCHAR,
        OFFER_MEDIATYPE     VARCHAR,
        OFFER_FILEID        VARCHAR,
        OFFER_FILEIDNOTE    VARCHAR,
        OFFER_FILENAME      VARCHAR,

        OFFER_TGPHLINK      VARCHAR,
        OFFER_ISTGPH        BOOLEAN     DEFAULT 0,
        OFFER_BUTTON        VARCHAR,
        OFFER_ISBUTTON      BOOLEAN     DEFAULT 0,
        OFFER_ISSPOILER     BOOLEAN     DEFAULT 0,
        OFFER_ISPIN         BOOLEAN     DEFAULT 0,
        OFFER_ISSILENCE     BOOLEAN     DEFAULT 0,
        OFFER_ISGALLERY     BOOLEAN     DEFAULT 0,

        OFFER_STATUS        BOOLEAN     DEFAULT 0,
        OFFER_TZ            VARCHAR,
        OFFER_DT            VARCHAR
    )''')

    # GROUPP
    cur.execute(f"""CREATE TABLE IF NOT EXISTS GROUPP ( 
        GROUPP_ID                   INTEGER     PRIMARY KEY AUTOINCREMENT
                                                UNIQUE
                                                NOT NULL,
        GROUPP_TID                  BIGINT      UNIQUE
                                                NOT NULL,
        OWNER_TID                   BIGINT,
        GROUPP_TYPE                 VARCHAR,
        GROUPP_TITLE                VARCHAR,
        GROUPP_USERNAME             VARCHAR,
        GROUPP_LINK                 VARCHAR,
        GROUPP_JOIN_LINK            VARCHAR,
        GROUPP_PHOTO                VARCHAR,

        GROUPP_CONFIG               VARCHAR     DEFAULT '{GROUPP_CONFIG_}',

        GROUPP_CCHECK               VARCHAR     DEFAULT '{GROUPP_CCHECK_}',
        GROUPP_CCHECKCHANNEL        VARCHAR,
        GROUPP_CCHECKCHANNELTID     BIGINT,
        GROUPP_CCHECKBTNNAME        VARCHAR,
        GROUPP_CHELLOTEXT           VARCHAR,
        GROUPP_CHELLOMEDIA          VARCHAR,
        GROUPP_CHELLOISALERT        VARCHAR,

        GROUPP_CBAN                 VARCHAR     DEFAULT '{GROUPP_CBAN_}',
        GROUPP_CINVITECNT           INTEGER     DEFAULT {GROUPP_CINVITECNT_},
        GROUPP_CINVITESRC           VARCHAR,
        GROUPP_CINVITEDT            VARCHAR,

        GROUPP_CCHANNEL             VARCHAR     DEFAULT '{GROUPP_CCHANNEL_}',
        GROUPP_CNEURO               VARCHAR     DEFAULT '{GROUPP_CNEURO_}',
        GROUPP_CLINK                VARCHAR     DEFAULT '{GROUPP_CLINK_}',
        GROUPP_CSYMBOL              VARCHAR     DEFAULT '{GROUPP_CSYMBOL_}',
        GROUPP_CMEDIA               VARCHAR     DEFAULT '{GROUPP_CMEDIA_}',
        GROUPP_CSTICKER1            VARCHAR,
        GROUPP_CSTICKER0            VARCHAR,

        GROUPP_CFLOOD               INTEGER     DEFAULT {GROUPP_CFLOOD_},
        GROUPP_CDIALOG              VARCHAR     DEFAULT {GROUPP_CDIALOG_},
        GROUPP_CLEN                 INTEGER     DEFAULT {GROUPP_CLEN_},
        GROUPP_CTIMER               INTEGER     DEFAULT {GROUPP_CTIMER_},
        GROUPP_CWORK                VARCHAR     DEFAULT '{GROUPP_CWORK_}',
        GROUPP_CUSER                VARCHAR     DEFAULT '{GROUPP_CUSER_}',
        GROUPP_CUSERDELAY           INTEGER     DEFAULT {GROUPP_CUSERDELAY_},
        GROUPP_CADMIN               VARCHAR     DEFAULT '{GROUPP_CADMIN_}',
        GROUPP_CPAY                 VARCHAR     DEFAULT '{GROUPP_CPAY_}',
        GROUPP_CPAYPRICE            VARCHAR,
        GROUPP_CPAYTOKEN            VARCHAR,
        GROUPP_CPAYADDRESS          VARCHAR,
        GROUPP_CPAYAMOUNT           VARCHAR,
        GROUPP_CPAYCURRENCY         VARCHAR,
        GROUPP_CPAYPERIOD           VARCHAR,
        GROUPP_CPAYWALLET           VARCHAR,
        GROUPP_CPAYCOLLECTION       VARCHAR,
        GROUPP_ADDRESSOWNER         VARCHAR,
        GROUPP_ADDRESSCOLLECTION    VARCHAR,

        GROUPP_CCOMMENT             VARCHAR     DEFAULT '{GROUPP_CCOMMENT_}',
        GROUPP_CCOMMENTADDRESS      VARCHAR,
        GROUPP_CCOMMENTAMOUNT       VARCHAR,
        GROUPP_CCOMMENTCURRENCY     VARCHAR,
        GROUPP_CCOMMENTPERIOD       VARCHAR,
        GROUPP_CCOMMENTWALLET       VARCHAR,
        GROUPP_CCOMMENTCOLLECTION   VARCHAR,
        GROUPP_RULES                VARCHAR,

        GROUPP_PERMISSIONS          VARCHAR,
        GROUPP_PODCAST              VARCHAR,
        GROUPP_PODCASTDATE          VARCHAR,
        GROUPP_ISPROMOTED           INTEGER     DEFAULT 0,

        GROUPP_DT                   VARCHAR,
        GROUPP_TZ                   VARCHAR,
        GROUPP_LZ                   VARCHAR,
        GROUPP_LC                   VARCHAR,
        GROUPP_LASTMSG              VARCHAR,
        GROUPP_ISACTIVE             BOOLEAN     DEFAULT 1,
        GROUPP_ISVERIFIED           INTEGER
    )""")

    con.commit()
    cur.close()
    con.close()


async def db_grp_create_entity(db):
    con = sqlite3.connect(db, timeout=10)
    try:
        cur = con.cursor()

        # USER
        cur.execute('''CREATE TABLE IF NOT EXISTS USER ( 
            USER_ID             INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            USER_TID            BIGINT      UNIQUE
                                            NOT NULL,
            USER_USERNAME       VARCHAR,
            USER_FULLNAME       VARCHAR,
            USER_ISPREMIUM      INTEGER,
            USER_LC             VARCHAR,
            USER_UTM            VARCHAR,
            USER_DT             VARCHAR,

            USER_PAYADDRESS     VARCHAR,
            USER_PAYPERIOD      VARCHAR,
            USER_PAYDT          VARCHAR,
            USER_PAYNFT         VARCHAR,
            USER_PAYNOTIFY      INTEGER     DEFAULT 0,

            USER_COMMENTADDRESS VARCHAR,
            USER_COMMENTPERIOD  VARCHAR,
            USER_COMMENTDT      VARCHAR,
            USER_COMMENTNFT     VARCHAR,
            USER_COMMENTCNT     INTEGER     DEFAULT 0
        )''')

        # POST
        cur.execute('''CREATE TABLE IF NOT EXISTS POST ( 
            POST_ID            INTEGER      PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            POST_TID           BIGINT       UNIQUE NOT NULL,
            POST_CHATTID       BIGINT       NOT NULL,
            POST_USERTID       BIGINT       NOT NULL,
            POST_TARGET        VARCHAR,
            POST_TYPE          VARCHAR,
            POST_TEXT          VARCHAR,
            POST_MEDIA         VARCHAR,
            POST_CHKBOX        VARCHAR,
            POST_WATER         VARCHAR,
            POST_STARS         VARCHAR,
            
            POST_MSGID         VARCHAR,
            POST_TELESCOPE     VARCHAR,

            POST_BUTTONS       VARCHAR,
            POST_BLOG          VARCHAR,
            POST_WEB           VARCHAR,
            POST_WALL          VARCHAR,
            POST_EMOJI         VARCHAR,
            POST_THEME         VARCHAR,
            POST_TZ            VARCHAR,
            POST_DT            VARCHAR,
            POST_TR            VARCHAR,
            POST_STATUS        BOOLEAN     DEFAULT 0,

            POST_ISBUTTON      BOOLEAN     DEFAULT 0,
            POST_ISDYNAMIC     BOOLEAN     DEFAULT 0,
            POST_ISSOUND       BOOLEAN     DEFAULT 1,
            POST_ISSILENCE     BOOLEAN     DEFAULT 0,
            POST_ISPIN         BOOLEAN     DEFAULT 0,
            POST_ISPREVIEW     BOOLEAN     DEFAULT 0,
            POST_ISSPOILER     BOOLEAN     DEFAULT 0,
            POST_ISGALLERY     BOOLEAN     DEFAULT 0,
            POST_ISFORMAT      BOOLEAN     DEFAULT 0,
            POST_ISTAG         BOOLEAN     DEFAULT 0,
            POST_ISREACTION    VARCHAR,
            POST_ISEFFECT      VARCHAR,
            POST_ISPODCAST     BOOLEAN     DEFAULT 0,

            POST_ISWINDOW      BOOLEAN     DEFAULT 0,
            POST_ISDESTROY     BOOLEAN     DEFAULT 0,

            POST_LNK           VARCHAR,
            POST_FILENAME      VARCHAR,

            POST_FID           VARCHAR,
            POST_FIDNOTE       VARCHAR
        )''')

        # VIEW
        cur.execute('''CREATE TABLE IF NOT EXISTS VIEW ( 
            VIEW_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            ENT_VID         VARCHAR     NOT NULL,
            ENT_TYPE        VARCHAR     NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            UNIQUE (ENT_VID, ENT_TYPE, CHAT_TID)
        )''')

        # PUSH
        cur.execute('''CREATE TABLE IF NOT EXISTS PUSH ( 
            PUSH_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            CHAT_FULLNAME   VARCHAR,
            CHAT_USERNAME   VARCHAR,
            CHAT_ISPREMIUM  BOOLEAN,
            CHAT_LC         VARCHAR,
            POST_ID         INTEGER     NOT NULL,
            BTN_BID       INTEGER     NOT NULL,
            UNIQUE (CHAT_TID, POST_ID, BTN_BID)
        )''')

        # FLOOD
        cur.execute('''CREATE TABLE IF NOT EXISTS FLOOD ( 
            FLOOD_ID            INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            FLOOD_CHATTID       BIGINT      NOT NULL,
            FLOOD_USERTID       BIGINT      NOT NULL,
            FLOOD_USERNAME      VARCHAR, 
            FLOOD_FIRSTNAME     VARCHAR, 
            FLOOD_VALUE         INTEGER     DEFAULT 0,
            FLOOD_DT            DATETIME,
            UNIQUE (FLOOD_CHATTID, FLOOD_USERTID)
        )''')

        # INVITE
        cur.execute('''CREATE TABLE IF NOT EXISTS INVITE ( 
            INVITE_ID           INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            INVITE_CHATTID      BIGINT      NOT NULL,
            INVITE_USERTID      BIGINT      NOT NULL,
            INVITE_MSGID        INTEGER,
            INVITE_TYPE         VARCHAR,
            INVITE_DT           DATETIME,
            INVITE_UTM          VARCHAR,
            UNIQUE (INVITE_CHATTID, INVITE_USERTID)
        )''')

        # KARMA
        cur.execute('''CREATE TABLE IF NOT EXISTS KARMA ( 
            KARMA_ID            INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            KARMA_CHATTID       BIGINT      NOT NULL,
            KARMA_USERTID       BIGINT      NOT NULL,
            KARMA_USERNAME      VARCHAR,
            KARMA_FIRSTNAME     VARCHAR,
            KARMA_STATUS        INTEGER     DEFAULT 0,
            UNIQUE (KARMA_CHATTID, KARMA_USERTID)
        )''')

        # DIALOG
        cur.execute('''CREATE TABLE IF NOT EXISTS DIALOG ( 
            DIALOG_ID           INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            DIALOG_DT           VARCHAR,
            DIALOG_LC           VARCHAR,
            DIALOG_LASTMSGID    INTEGER,
            DIALOG_LASTUSRID    BIGINT,
            DIALOG_CONTENT      VARCHAR,
            DIALOG_ISANSWERED   INTEGER
        )''')

        con.commit()
        cur.close()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        con.close()


async def db_chn_create(db):
    con = sqlite3.connect(db, timeout=10)
    con.execute('PRAGMA foreign_keys=ON;')
    cur = con.cursor()

    # USER
    cur.execute('''CREATE TABLE IF NOT EXISTS USER ( 
        USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_TID        BIGINT      UNIQUE
                                    NOT NULL,
        USER_USERNAME   VARCHAR,
        USER_FULLNAME   VARCHAR,
        USER_ISPREMIUM  INTEGER,
        USER_GAMES      VARCHAR,
        USER_VARS       VARCHAR,

        USER_DTPAID     VARCHAR, 
        USER_ISPAID     INTEGER     DEFAULT 0,
        USER_TYPAID     VARCHAR,
        USER_TXPAID     VARCHAR,
        
        USER_UTM        VARCHAR,
        USER_DT         VARCHAR,
        USER_TZ         VARCHAR,
        USER_LZ         VARCHAR,
        USER_LC         VARCHAR
    )''')

    # FILE
    cur.execute('''CREATE TABLE IF NOT EXISTS FILE (
        FILE_ID             INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        FILE_FILEID         VARCHAR     NOT NULL,
        FILE_FILENAME       VARCHAR,
        UNIQUE (FILE_FILEID, FILE_FILENAME)
    )''')

    # LIKE
    cur.execute('''CREATE TABLE IF NOT EXISTS LIKE ( 
        LIKE_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                    UNIQUE
                                    NOT NULL,
        USER_ID         INTEGER     NOT NULL,
        POST_ID         INTEGER     NOT NULL
        )''')

    # OFFER
    cur.execute('''CREATE TABLE IF NOT EXISTS OFFER ( 
        OFFER_ID            INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
        OFFER_USERTID       BIGINT      NOT NULL,
        OFFER_TEXT          VARCHAR,
        OFFER_MEDIATYPE     VARCHAR,
        OFFER_FILEID        VARCHAR,
        OFFER_FILEIDNOTE    VARCHAR,
        OFFER_FILENAME      VARCHAR,

        OFFER_TGPHLINK      VARCHAR,
        OFFER_ISTGPH        BOOLEAN     DEFAULT 0,
        OFFER_BUTTON        VARCHAR,
        OFFER_ISBUTTON      BOOLEAN     DEFAULT 0,
        OFFER_ISSPOILER     BOOLEAN     DEFAULT 0,
        OFFER_ISPIN         BOOLEAN     DEFAULT 0,
        OFFER_ISSILENCE     BOOLEAN     DEFAULT 0,
        OFFER_ISGALLERY     BOOLEAN     DEFAULT 0,

        OFFER_STATUS        BOOLEAN     DEFAULT 0,
        OFFER_TZ            VARCHAR,
        OFFER_DT            VARCHAR
    )''')

    # CHANNEL
    cur.execute(f"""CREATE TABLE IF NOT EXISTS CHANNEL ( 
        CHANNEL_ID                 INTEGER      PRIMARY KEY AUTOINCREMENT
                                                UNIQUE
                                                NOT NULL,
        CHANNEL_TID                BIGINT       UNIQUE
                                                NOT NULL,
        OWNER_TID                  BIGINT,
        CHANNEL_TYPE               VARCHAR,
        CHANNEL_TITLE              VARCHAR,
        CHANNEL_USERNAME           VARCHAR,
        CHANNEL_LINK               VARCHAR,
        CHANNEL_JOIN_LINK          VARCHAR,
        CHANNEL_PHOTO              VARCHAR,
        CHANNEL_STICKERPACK        VARCHAR,
        CHANNEL_EMOJIPACK          VARCHAR,
        CHANNEL_ISPROMOTED         INTEGER      DEFAULT 0,
        CHANNEL_LASTMSG            VARCHAR,
        CHANNEL_CPAYDONCNT         INTEGER      DEFAULT 0,
        CHANNEL_VARS               VARCHAR,
        
        CHANNEL_CCHECK             VARCHAR      DEFAULT '{CHANNEL_CCHECK_}',
        CHANNEL_CCHECKCHANNEL      VARCHAR,
        CHANNEL_CCHECKCHANNELTID   BIGINT,
        
        CHANNEL_CBAN               VARCHAR      DEFAULT '{CHANNEL_CBAN_}',
        CHANNEL_CBANCLEARING       INTEGER      DEFAULT 0,
        CHANNEL_CBANDELETING       INTEGER      DEFAULT 0,
        
        CHANNEL_CDECOR             VARCHAR      DEFAULT '{CHANNEL_CDECOR_}',
        CHANNEL_CFOOTER            VARCHAR,

        CHANNEL_PODCAST            VARCHAR,
        CHANNEL_PODCASTDATE        VARCHAR,
        CHANNEL_CSYSTEM            VARCHAR     DEFAULT '{CHANNEL_CSYSTEM_}',
        
        CHANNEL_CPAY                 VARCHAR     DEFAULT '{CHANNEL_CPAY_}',
        CHANNEL_CPAYPRICE            VARCHAR,
        CHANNEL_CPAYTOKEN            VARCHAR,
        CHANNEL_CPAYCOLLECTION       VARCHAR,
        CHANNEL_CPAYMASTER           VARCHAR,
        CHANNEL_CPAYAMOUNT           VARCHAR,
        CHANNEL_CPAYCURRENCY         VARCHAR,
        CHANNEL_CPAYPERIOD           VARCHAR,
        
        CHANNEL_OWNERADDRESS         VARCHAR,
        CHANNEL_COLLECTIONADDRESS    VARCHAR,
        CHANNEL_COLLECTIONINDEX      VARCHAR    DEFAULT '0',
        CHANNEL_COLLECTIONPRIVATE    VARCHAR,
        
        CHANNEL_MASTERADDRESS        VARCHAR,
        CHANNEL_MASTERSYMBOL         VARCHAR,
        CHANNEL_MASTERPRIVATE        VARCHAR,
        
        CHANNEL_CUSER                VARCHAR    DEFAULT '{CHANNEL_CUSER_}',
        CHANNEL_CADMIN               VARCHAR,
        
        CHANNEL_DT                 VARCHAR,
        CHANNEL_TZ                 VARCHAR,
        CHANNEL_LZ                 VARCHAR,
        CHANNEL_LC                 VARCHAR,
        CHANNEL_ISACTIVE           BOOLEAN      DEFAULT 1,
        CHANNEL_ISNFTUSERNAME      BOOLEAN      DEFAULT 0
    )""")

    con.commit()
    cur.close()
    con.close()


async def db_chn_create_entity(db):
    con = sqlite3.connect(db, timeout=10)
    try:
        cur = con.cursor()

        # USER
        cur.execute('''CREATE TABLE IF NOT EXISTS USER ( 
            USER_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            USER_TID        BIGINT      UNIQUE
                                        NOT NULL,
            USER_USERNAME   VARCHAR,
            USER_FULLNAME   VARCHAR,
            USER_ISPREMIUM  INTEGER,
            USER_GAMES      VARCHAR,
            USER_VARS       VARCHAR,
            
            USER_DTPAID     VARCHAR, 
            USER_ISPAID     INTEGER     DEFAULT 0,
            USER_TYPAID     VARCHAR,
            USER_TXPAID     VARCHAR,
            
            USER_UTM        VARCHAR,
            USER_DT         VARCHAR,
            USER_TZ         VARCHAR,
            USER_LZ         VARCHAR,
            USER_LC         VARCHAR
        )''')

        # JOIN
        cur.execute('''CREATE TABLE IF NOT EXISTS INVITE ( 
            INVITE_ID           INTEGER     PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            INVITE_CHATTID      BIGINT      NOT NULL,
            INVITE_USERTID      BIGINT      NOT NULL,
            INVITE_MSGID        INTEGER,
            INVITE_TYPE         VARCHAR,
            INVITE_DATETIME     DATETIME,
            UNIQUE (INVITE_CHATTID, INVITE_USERTID)
        )''')

        # POST
        cur.execute('''CREATE TABLE IF NOT EXISTS POST ( 
            POST_ID            INTEGER      PRIMARY KEY AUTOINCREMENT
                                            UNIQUE
                                            NOT NULL,
            POST_TID           BIGINT       UNIQUE NOT NULL,
            POST_CHATTID       BIGINT       NOT NULL,
            POST_USERTID       BIGINT       NOT NULL,
            POST_USERTUN       VARCHAR,
            POST_TARGET        VARCHAR,
            POST_MSGID         VARCHAR,
            
            POST_TYPE          VARCHAR,
            POST_TEXT          VARCHAR,
            POST_MEDIA         VARCHAR,
            POST_BUTTONS       VARCHAR,
            POST_CHKBOX        VARCHAR,

            POST_WEB           VARCHAR,
            POST_NFT           VARCHAR,
            POST_PAY           VARCHAR,
            POST_BLOG          VARCHAR,

            POST_WATER         VARCHAR,
            POST_STARS         VARCHAR,     
            POST_WALL          VARCHAR,
            POST_EMOJI         VARCHAR,
            POST_THEME         VARCHAR,
            POST_ISMINTED      BOOLEAN      DEFAULT 0,
            POST_MINTLINK      VARCHAR,
            POST_ISPRIVATE     BOOLEAN      DEFAULT 0,
            
            POST_TZ            VARCHAR,
            POST_DT            VARCHAR,
            POST_TR            VARCHAR,
            POST_STATUS        BOOLEAN      DEFAULT 0
        )''')

        # VIEW
        cur.execute('''CREATE TABLE IF NOT EXISTS VIEW ( 
            VIEW_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            ENT_VID         VARCHAR     NOT NULL,
            ENT_TYPE        VARCHAR     NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            UNIQUE (ENT_VID, ENT_TYPE, CHAT_TID)
        )''')

        # PUSH
        cur.execute('''CREATE TABLE IF NOT EXISTS PUSH ( 
            PUSH_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            CHAT_TID        BIGINT      NOT NULL,
            CHAT_FULLNAME   VARCHAR,
            CHAT_USERNAME   VARCHAR,
            CHAT_ISPREMIUM  BOOLEAN,
            CHAT_LC         VARCHAR,
            
            POST_ID         INTEGER     NOT NULL,
            BTN_BID       INTEGER     NOT NULL,
            UNIQUE (CHAT_TID, POST_ID, BTN_BID)
        )''')

        # BOOST
        cur.execute('''CREATE TABLE IF NOT EXISTS BOOST ( 
            BOOST_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
                                         UNIQUE
                                         NOT NULL,
            BOOST_TID       BIGINT       NOT NULL,
            CHAT_TID        BIGINT,
            USER_TID        BIGINT,
            BOOST_STARTDT   VARCHAR,
            BOOST_FINISHDT  VARCHAR,
            BOOST_SRC       VARCHAR
        )''')

        # # CONTACT
        # cur.execute('''CREATE TABLE IF NOT EXISTS CONTACT (
        #     CONTACT_ID         INTEGER     PRIMARY KEY AUTOINCREMENT
        #                                  UNIQUE
        #                                  NOT NULL,
        #     CHAT_TID        BIGINT,
        #     USER_TID        BIGINT,
        #     CONTACT_DT      VARCHAR
        # )''')

        con.commit()
        cur.close()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        con.close()


async def db_select_columnames(TABLE_NAME=None, db=None):
    data = []
    try:
        con = sqlite3.connect(db, timeout=10)
        con.execute('PRAGMA foreign_keys=ON;')
        cur = con.cursor()

        cur.execute(f"SELECT * FROM {TABLE_NAME} limit 1")
        data = [i[0] for i in cur.description]
        data = data[8:]

        cur.close()
        con.close()
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return data


async def db_select_pg(sql, param=None, db_pool=None, db_config=None):
    retry = 1
    result = []
    try:
        while retry > 0:
            try:
                if db_pool:
                    async with db_pool.acquire() as conn:
                        result = await conn.fetch(sql, *(param or ()))
                        logger.info(log_ % f"SQL: {sql}, PARAM: {param}")
                else:
                    conn = await asyncpg.connect(**db_config)
                    try:
                        result = await conn.fetch(sql, *(param or ()))
                        logger.info(log_ % f"SQL: {sql}, PARAM: {param}")
                    finally:
                        await conn.close()
                break
            except Exception as e:
                logger.info(log_ % f"{str(e) + str(param)} ({sql=})")
                if 'does not exist' in str(e) or 'invalid input syntax' in str(e):
                    return result
                await asyncio.sleep(round(random.uniform(1, 2), 2))
                retry -= 1
    finally:
        return result


async def db_change_pg(sql, param=None, db_pool=None, db_config=None):
    retry = 1
    result = -1
    try:

        while retry > 0:
            try:
                if db_pool:
                    # print(f"{db_pool=}")
                    async with db_pool.acquire() as conn:
                        result = await conn.execute(sql, *(param or ()))
                        logger.info(log_ % f"SQL: {sql}, PARAM: {param}")
                else:
                    print(f"else")
                    conn = await asyncpg.connect(**db_config)
                    try:
                        result = await conn.execute(sql, *(param or ()))
                        logger.info(log_ % f"SQL: {sql}, PARAM: {param}")
                    finally:
                        await conn.close()
                break
            except Exception as e:
                logger.info(log_ % f"Error: {str(e) + str(param)} ({sql=})")
                if 'does not exist' in str(e) or 'invalid input syntax' in str(e):
                    return result
                await asyncio.sleep(round(random.uniform(1, 2), 2))
                retry -= 1
    finally:
        return result


async def is_my_db_exists(PG_PASS_MAIN, BASE_D):
    result = conn = None
    try:
        conn = await asyncpg.connect(
            host=BASE_D["host"],
            port=BASE_D["port"],
            database="template1",
            user="postgres",  # user with rules
            password=PG_PASS_MAIN,
        )

        databases = await conn.fetch("SELECT datname FROM pg_database WHERE datistemplate = false;")
        result = len([db for db in databases if db['datname'] == BASE_D["database"]]) > 0
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if conn: await conn.close()
        logger.info(log_ % f"is_my_db_exists = {result}")
        return result


async def reset_database_and_role(PG_PASS_MAIN, BASE_D, is_all=False):
    conn = None
    try:
        conn = await asyncpg.connect(
            host=BASE_D["host"],
            port=BASE_D["port"],
            database="template1",
            user="postgres",
            password=PG_PASS_MAIN,
        )

        databases = await conn.fetch("SELECT datname FROM pg_database WHERE datistemplate = false;")
        db_names = [db['datname'] for db in databases if db['datname'] not in ('template0', 'template1')]

        logger.info(log_ % f"===== for in {db_names=}")
        for db_name in db_names:
            logger.info(log_ % f"DB: {db_name}")
            try:
                if is_all is False and db_name != BASE_D["database"]: continue
                await conn.execute(f"""
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = '{db_name}';
                """)
                await conn.execute(f"DROP DATABASE IF EXISTS {db_name};")
                logger.info(log_ % f"DB {db_name} droped.")
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        roles = await conn.fetch(
            "SELECT rolname FROM pg_roles WHERE rolname NOT IN ('postgres') AND rolname NOT LIKE 'pg_%';")
        logger.info(log_ % f"===== for in {[role['rolname'] for role in roles]=}")
        for role in roles:
            try:
                if is_all is False and role['rolname'] != BASE_D["user"]: continue
                logger.info(log_ % f"ROLE: {role['rolname']}")
                await conn.execute(f"DROP ROLE IF EXISTS {role['rolname']};")
                logger.info(log_ % f"ROLE: {role['rolname']} deleted.")
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        if is_all:  # database "postgres" already exists (so, no need to reset password)
            await conn.execute('CREATE DATABASE postgres;')
            await conn.execute(f"ALTER USER postgres WITH PASSWORD '{PG_PASS_MAIN}';")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if conn:
            await conn.close()


async def create_role_and_database(PG_PASS_MAIN, BASE_D):
    conn = None
    try:
        logger.info(log_ % f"create_role_and_database ...")
        # host = "/tmp" if os.path.dirname(__file__).startswith('/Users') else "localhost"
        conn = await asyncpg.connect(
            host=BASE_D["host"],
            port=BASE_D["port"],
            database="postgres",
            user='postgres',
            password=PG_PASS_MAIN,
        )

        await conn.execute(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '{BASE_D['user']}') THEN
                    CREATE ROLE {BASE_D['user']} WITH LOGIN PASSWORD '{BASE_D['password']}';
                END IF;
            END $$;
        """)
        logger.info(log_ % str(f"ROLE: {BASE_D['user']} SUCCESS"))

        await conn.execute(f"CREATE DATABASE {BASE_D['database']} WITH OWNER {BASE_D['user']};")
        logger.info(log_ % str(f"DB: {BASE_D['database']} SUCCESS"))
        # psql -U bot_user -d bot_db -h localhost -p 5432

        # #!/bin/bash
        # sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'xxx';"
        # PG_HBA="/etc/postgresql/$(ls /etc/postgresql)/main/pg_hba.conf"
        # sudo sed -i 's/peer/md5/g' "$PG_HBA"
        # sudo systemctl restart postgresql

        # ALTER USER postgres WITH PASSWORD 'xxx';
        # psql -U postgres -h localhost -W
        # sudo systemctl restart postgresql

        # host    all             all             0.0.0.0/0            md5
        # nano /etc/postgresql/16/main/pg_hba.conf
        # listen_addresses = '*'
        # nano /etc/postgresql/16/main/postgresql.conf
        # sudo systemctl restart postgresql
    except asyncpg.exceptions.DuplicateDatabaseError:
        logger.info(log_ % f"DB {BASE_D['database']} DuplicateDatabaseError")
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if conn:
            await conn.close()


async def check_schema_exists(schema_name, db_pool):
    result = False
    try:
        async with db_pool.acquire() as conn:
            # schema_name = f'USER_{USER_TID}'
            query = """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.schemata 
                    WHERE schema_name = $1
                );
            """
            result = await conn.fetchval(query, schema_name.lower())
        print(f"check_schema_exists {schema_name=} {result=}, {db_pool=}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


# endregion


# region menu
async def post_offer(bot, data, BASE_D):
    try:
        for item in data:
            try:
                OFFER_ID, OFFER_USERTID, OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_FILEIDNOTE, OFFER_BUTTON, OFFER_ISBUTTON, OFFER_TGPHLINK, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, OFFER_DT, OFFER_TZ = item

                sign_ = OFFER_TZ[0]
                h_, m_ = OFFER_TZ.strip(sign_).split(':')
                dt_now = datetime.now(timezone.utc)
                if sign_ == "+":
                    dt_cur = dt_now + timedelta(hours=int(h_), minutes=int(m_))
                else:
                    dt_cur = dt_now - timedelta(hours=int(h_), minutes=int(m_))
                timedelta_ = (dt_cur - datetime.strptime(OFFER_DT, "%d-%m-%Y %H:%M").replace(tzinfo=timezone.utc))

                if timedelta_.days >= 0 and timedelta_.seconds >= 0:
                    sql = "UPDATE OFFER SET OFFER_DT=NULL, OFFER_STATUS=0 WHERE OFFER_ID=$1"
                    await db_change_pg(sql, (OFFER_ID,), BASE_D)

                    asyncio.create_task(
                        broadcast_send_admin(bot, OFFER_USERTID, 'en', OFFER_ID, BASE_D, []))
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def bots_by_inline(chat_id, message, BASE_D):
    result = []
    try:
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)

        data = [['👩🏽‍💻 @FereyDemoBot', l_inline_demo[lz],
                 "<a href='https://t.me/FereyDemoBot?start=inline'>@FereyDemoBot</a>"],
                ['👩🏽‍💻 @FereyBotBot', l_inline_bot[lz],
                 "<a href='https://t.me/FereyBotBot?start=inline'>@FereyBotBot</a>"],
                ['👩🏽‍💻 @FereyPostBot', l_inline_post[lz],
                 "<a href='https://t.me/FereyPostBot?start=inline'>@FereyPostBot</a>"],
                ['👩🏽‍💻 @FereyMediaBot', l_inline_media[lz],
                 "<a href='https://t.me/FereyMediaBot?start=inline'>@FereyMediaBot</a>"],
                ['👩🏽‍💻 @FereyChannelBot', l_inline_channel[lz],
                 "<a href='https://t.me/FereyChannelBot?start=inline'>@FereyChannelBot</a>"],
                ['👩🏽‍💻 @FereyGroupBot', l_inline_group[lz],
                 "<a href='https://t.me/FereyGroupBot?start=inline'>@FereyGroupBot</a>"],
                ['👩🏽‍💻 @FereyFindBot', l_inline_find[lz],
                 "<a href='https://t.me/FereyFindBot?start=inline'>@FereyFindBot</a>"],
                ['👩🏽‍💻 @FereyAIBot', l_inline_ai[lz], "<a href='https://t.me/FereyAIBot?start=inline'>@FereyAIBot</a>"],
                ['👩🏽‍💻 @FereyStickerBot', l_inline_sticker[lz],
                 "<a href='https://t.me/FereyStickerBot?start=inline'>@FereyStickerBot</a>"],
                # ['👩🏽‍💻 @FereyTargetBot', l_inline_target[lz],
                #  "<a href='https://t.me/FereyTargetBot?start=inline'>@FereyTargetBot</a>"],
                ['👩🏽‍💻 @FereyUserBot', l_inline_user[lz],
                 "<a href='https://t.me/FereyUserBot?start=inline'>@FereyUserBot</a>"],
                ['👩🏽‍💻 @FereyToolsBot', l_inline_tools[lz],
                 "<a href='https://t.me/FereyToolsBot?start=inline'>@FereyToolsBot</a>"],
                # ['👩🏽‍💻 @FereyWorkBot', l_inline_work[lz],
                #  "<a href='https://t.me/FereyWorkBot?start=inline'>@FereyWorkBot</a>"],
                ['👩🏽‍💻 @FereyTONestBot', l_inline_tonest[lz],
                 "<a href='https://t.me/FereyTONestBot?start=inline'>@FereyTONestBot</a>"],
                ['👩🏽‍💻 @FereySupportBot', l_inline_support[lz],
                 "<a href='https://t.me/FereySupportBot?start=inline'>@FereySupportBot</a>"], ]

        for i in range(0, len(data)):
            title, desc, text = data[i]

            input_message_content = types.InputTextMessageContent(message_text=text, disable_web_page_preview=False)
            result.append(
                types.InlineQueryResultArticle(id=str(uuid4()), title=title, description=desc, thumb_url=bot_logo_jpeg,
                                               input_message_content=input_message_content))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_buttons_main(lz, bot_un, BASE_D):
    result = []
    try:
        result = [types.InlineKeyboardButton(text="👩🏽‍💼", url=f"tg://user?id={my_tid}"),
                  types.InlineKeyboardButton(text="🔗",
                                             url=f'https://t.me/share/url?url=https%3A%2F%2Ft.me%2F{bot_un}&text=%40{bot_un}'),
                  types.InlineKeyboardButton(text=f"♥️{(await read_likes(BASE_D))}", callback_data=f"like"),
                  types.InlineKeyboardButton(text="ᵗᶢᴿᴬᴾᴴ",
                                             web_app=types.WebAppInfo(url='https://telegra.ph/Links-07-05-462')),
                  types.InlineKeyboardButton(text="ᶜᵸᴬᴺᴺᴱᴸ", url=f"https://t.me/{get_tg_channel(lz)}"),
                  types.InlineKeyboardButton(text="ᴮᴼᵀ⁺", switch_inline_query_current_chat=f"~")]
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def send_request_chat(bot, chat_id, lz, is_group=False):
    result = []
    try:
        reply_markup = ReplyKeyboardBuilder()

        if is_group:
            # print(f"{is_group=}")

            user_administrator_rights = ChatAdministratorRights(is_anonymous=False,  # !
                                                                can_manage_chat=True, can_delete_messages=True,
                                                                can_manage_video_chats=True, can_restrict_members=True,
                                                                can_promote_members=False,  # can_promote_members=True,
                                                                can_change_info=False, can_invite_users=True,
                                                                can_post_stories=True, can_edit_stories=False,
                                                                can_delete_stories=False, can_post_messages=True,
                                                                can_edit_messages=True, can_pin_messages=True,
                                                                can_manage_topics=None)

            kb_entity = KeyboardButtonRequestChat(request_id=1, chat_is_channel=False, chat_is_forum=None,
                                                  chat_has_username=None, chat_is_created=None,
                                                  user_administrator_rights=user_administrator_rights,
                                                  bot_administrator_rights=user_administrator_rights,
                                                  bot_is_member=True)

            reply_markup.add(*[types.KeyboardButton(text=l_grp_btn1[lz], request_chat=kb_entity),
                               types.KeyboardButton(text=l_grp_btn2[lz])])
        else:
            user_administrator_rights = ChatAdministratorRights(is_anonymous=True, can_manage_chat=True,
                                                                can_delete_messages=True, can_manage_video_chats=True,
                                                                can_restrict_members=True, can_promote_members=False,
                                                                # can_promote_members=True,
                                                                can_change_info=False, can_invite_users=True,
                                                                can_post_stories=True, can_edit_stories=False,
                                                                can_delete_stories=False, can_post_messages=True,
                                                                can_edit_messages=True, can_pin_messages=True,
                                                                can_manage_topics=True)

            kb_entity = KeyboardButtonRequestChat(request_id=1, chat_is_channel=True, chat_is_forum=False,
                                                  chat_has_username=None, chat_is_created=None,
                                                  user_administrator_rights=user_administrator_rights,
                                                  bot_administrator_rights=user_administrator_rights,
                                                  bot_is_member=True)

            reply_markup.add(*[types.KeyboardButton(text=l_chn_btn1[lz], request_chat=kb_entity),
                               types.KeyboardButton(text=l_chn_btn2[lz])])

        reply_markup = reply_markup.as_markup(resize_keyboard=True, is_persistent=True,
                                              input_field_placeholder=placeholder)
        await bot.send_message(chat_id=chat_id, text=l_choose_direction[lz], reply_markup=reply_markup)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


# endregion


# region pst
async def convert_tgs_to_json(tgs_path, output_path=None):
    result = None
    try:
        print(f"Начало конвертации {tgs_path} в JSON.")
        output_path = output_path or tgs_path.replace(".tgs", ".json")

        with gzip.open(tgs_path, 'rb') as f:
            json_data = json.loads(f.read().decode('utf-8'))
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as json_file:
            await json_file.write(json.dumps(json_data, ensure_ascii=False, separators=(',', ':')))

        print(f"Конвертация завершена. JSON файл сохранен по адресу: {output_path}")
        result = output_path
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def convert_json_to_tgs(json_path, output_path=None):
    result = None
    try:
        print(f"Начало конвертации {json_path} в TGS.")
        output_path = output_path or json_path.replace(".json", ".tgs")

        async with aiofiles.open(json_path, 'r', encoding='utf-8') as json_file:
            json_data = await json_file.read()

        with gzip.open(output_path, 'wb') as tgs_file:
            tgs_file.write(json_data.encode('utf-8'))

        print(f"Конвертация завершена. TGS файл сохранен по адресу: {output_path}")
        result = output_path
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def convert_webm_to_mp4(webm_path, MEDIA_D, ENT_TID):
    result = None
    try:
        file_begin, ext = os.path.splitext(webm_path)
        output_path = os.path.join(MEDIA_D, str(ENT_TID), f"{os.path.basename(file_begin)}_copy.mp4")

        cmd = [
            "ffmpeg", "-y", "-i", webm_path,  # Входной файл
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",  # Настройки кодирования
            "-c:a", "aac", "-b:a", "128k",  # Кодек для аудио
            output_path  # Выходной файл
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            print(f"Конвертация завершена: {output_path}")
        else:
            print(f"Ошибка: {stderr.decode()}")

        print(f"Конвертация завершена. mp4 файл сохранен по адресу: {output_path}")
        result = output_path
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def add_water_to_photo(POST_FNAME, POST_FNAME_COPY, POST_WATER, EXTRA_D):
    result = None
    try:
        # file_begin, ext = os.path.splitext(webm_path)
        # output_path = os.path.join(MEDIA_D, str(ENT_TID), f"{os.path.basename(file_begin)}_copy.mp4")

        image = Image.open(POST_FNAME)
        image = await correct_orientation(image)
        image = image.convert('RGB')
        image.save(POST_FNAME, format="JPEG")

        width, height = image.size
        draw = ImageDraw.Draw(image)

        truetype_ = os.path.join(EXTRA_D, 'Roboto-Regular.ttf')
        font_sz = 25
        font = ImageFont.truetype(truetype_, font_sz)

        text = POST_WATER
        text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]

        padding = 10
        bg_radius = 15
        bg_color = (0, 0, 0, 128)
        x = width - text_w - 40
        y = height - text_h - 40

        # rounded
        bg_x1, bg_y1 = x - padding, y - padding
        bg_x2, bg_y2 = x + text_w + padding, y + text_h + padding

        bg = Image.new("RGBA", (bg_x2 - bg_x1, bg_y2 - bg_y1), (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(bg)
        bg_draw.rounded_rectangle((0, 0, bg_x2 - bg_x1, bg_y2 - bg_y1), bg_radius, fill=bg_color)

        image.paste(bg, (bg_x1, bg_y1), bg)

        # add txt to upper layer
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        image.save(POST_FNAME_COPY)

        result = POST_FNAME_COPY
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def correct_txt_tags_for_tg(txt):
    result = txt
    try:
        if not txt or txt == str_empty: return

        print(f"correct_txt_tags_for_tg start {txt=}")
        txt = re.sub(
            r'<div class="tgui-79024fcb6d81ad79" style="display: inline-block; padding: 0px 4px;">(.*?)</div>',
            r'<blockquote>\1</blockquote>', txt)

        txt = re.sub(
            r'<div class="tgui-79024fcb6d81ad79" style="border-left-width: 2px; border-left-style: solid; border-left-color: purple; padding: 0px 4px;">(.*?)</div>',
            r'<blockquote expandable>\1</blockquote>', txt)

        txt = re.sub(
            r'<div class="tgui-86f452d8e92a2075 tgui-aff2a6268e887037" style="display: inline-block; white-space: pre-wrap; cursor: pointer;">(.*?)</div>',
            r'<tg-spoiler>\1</tg-spoiler>', txt
        )

        txt = re.sub(
            r'<div class="tgui-86f452d8e92a2075" style="display: inline-block; white-space: pre-wrap; cursor: pointer;">(.*?)</div>',
            r'<tg-spoiler>\1</tg-spoiler>', txt)

        txt = re.sub(r'<span style="color: rgba\(0, 123, 247, \.99\);">(#[^<]+)</span>', r'\1', txt)
        txt = txt.replace('&nbsp;', '').replace('<br>', '')
        txt = re.sub(r'</div>\s*<div>', '\n', txt)
        txt = re.sub(r'</?div>', '\n', txt)
        txt = txt.replace('<span style="caret-color: var(--tg-theme-hint-color);">', '')
        txt = txt.replace('</span>', '')
        txt = re.sub(r'</?div[^>]*>', '', txt)
        result = txt[0:4096].strip()
        print(f"correct_txt_tags_for_tg finish {result=}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_btn_pushes(BOT_TID, MSG_BUTTONS, ENT_VID, ENT_TYPE, BASE_P, PROJECT_USERNAME):
    result = MSG_BUTTONS
    try:
        print(f"{MSG_BUTTONS=} before")
        schema_name = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'BOT'
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'

        sql = f"""
            SELECT BTN_BID, COUNT(*) 
            FROM {schema_name}_{BOT_TID}.PUSH 
            WHERE ENT_VID=$1 AND ENT_TYPE=$2 
            GROUP BY BTN_BID
        """
        data_cnt = await db_select_pg(sql, (ENT_VID, ENT_TYPE), BASE_P)
        pushes_dict = {row[0]: str(row[1]) for row in data_cnt}

        for btn in MSG_BUTTONS:
            btn['pushes'] = upper_register_sync(pushes_dict.get(btn['bid'], '0'))

        print(f"{MSG_BUTTONS=} after")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def detect_post_type(links):
    result = 'document'
    try:
        types_set = set()
        for link in links:
            l = link.lower()
            if l.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                types_set.add('photo')
            elif l.endswith(('.gif', '.giff')):
                types_set.add('gif')
            elif l.endswith(('.mp4', '.mov', '.webm')):
                types_set.add('video')
            elif l.endswith(('.mp3', '.wav')):
                types_set.add('audio')
            elif l.endswith('.ogg'):
                types_set.add('voice')
            elif l.endswith(('.webp', '.webm')):
                types_set.add('sticker')
            elif l.endswith('.pdf'):
                types_set.add('document')
            else:
                types_set.add('document')
        result = 'document' if len(types_set) > 1 else types_set.pop()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result
# endregion


# region cmd
async def run_shell(cmd):
    result = None
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()

        logger.info(log_ % f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            logger.info(log_ % f'{stdout.decode()}')
            result = f'[stdout]\n{stdout.decode()}'
        if stderr:
            logger.info(log_ % f'{stderr.decode()}')
            result = f'[stderr]\n{stderr.decode()}'
        else:
            result = str(proc.returncode)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def send_response(UB_TID, UB_TOKENTGPH, WEBHOOK_HOST, PROJECT_PATH, cmd, param=None):
    try:
        if param is None:
            param = ''
        elif isinstance(param, dict) and not param:
            param = {}

        json_ = {
            'tid': UB_TID,
            'token': UB_TOKENTGPH,
            'cmd': cmd,
            'param': param,
            'ans': True
        }
        url = f"{WEBHOOK_HOST}/{PROJECT_PATH}/client_set"
        # print(f"{url=}")
        logger.info(log_ % str(f"{url=}"))
        timestamp = str(utils.datetime_to_timestamp(datetime.now(timezone.utc)))
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={timestamp: json_}) as response:
                await response.json()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


# endregion


# region pay
async def get_pay_btn(bot, chat_id, lz, payload='donate', stars=1):
    try:
        reply_markup = InlineKeyboardBuilder().add(
            types.InlineKeyboardButton(text=f"{l_donate[lz]} {stars}★", pay=True))
        await bot.send_invoice(chat_id=chat_id, title='★', description=str_empty,
                               payload=payload, currency='XTR',
                               prices=[LabeledPrice(label="XTR", amount=stars)],
                               message_effect_id='5159385139981059251',  # heart
                               reply_markup=reply_markup.as_markup())
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def star_invoice_link(bot, PROJECT_USERNAME, chat_id, stars, payload='-', subscription_period=2592000,
                            photo_url=None):
    result = None
    try:
        invoice = await bot.create_invoice_link(title=PROJECT_USERNAME,
                                                description=f"{stars}",
                                                payload=payload,
                                                currency='XTR',
                                                photo_url=photo_url,
                                                prices=[LabeledPrice(label="XTR", amount=stars)],
                                                subscription_period=subscription_period)
        if invoice and chat_id:
            result = invoice
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def list_star_invoice_link(bot, PROJECT_USERNAME, PROJECT_TYPE):
    try:
        chat_id = 1

        stars = 1
        payload = '-'
        r_ = await star_invoice_link(bot, PROJECT_USERNAME, chat_id, stars, payload, None)
        print(f"star_invoice_link_{stars} = '{r_}'")

        stars = 10
        payload = 'donate'
        r_ = await star_invoice_link(bot, PROJECT_USERNAME, chat_id, stars, payload, None)
        print(f"star_invoice_link_{stars} = '{r_}'")

        stars = 50
        payload = 'material'
        r_ = await star_invoice_link(bot, PROJECT_USERNAME, chat_id, stars, payload, None)
        print(f"star_invoice_link_{stars} = '{r_}'")

        stars = 100
        payload = 'donate'
        r_ = await star_invoice_link(bot, PROJECT_USERNAME, chat_id, stars, payload, None)
        print(f"star_invoice_link_{stars} = '{r_}'")

        stars = 1
        payload = '1'
        subscription_period = 2592000
        r_ = await bot.create_invoice_link(title=f"#{PROJECT_TYPE}",
                                           description=f"@{PROJECT_USERNAME}",
                                           payload=payload,
                                           currency='XTR',
                                           prices=[LabeledPrice(label="XTR", amount=stars)],
                                           subscription_period=subscription_period)  # 604800 2592000

        print(f"star_invoice_subscription_{stars} = '{r_}'")

        stars = 250
        payload = '1'
        subscription_period = 2592000
        r_ = await bot.create_invoice_link(title=f"#{PROJECT_TYPE}",
                                           description=f"@{PROJECT_USERNAME}",
                                           payload=payload,
                                           currency='XTR',
                                           prices=[LabeledPrice(label="XTR", amount=stars)],
                                           subscription_period=subscription_period)  # 604800 2592000

        print(f"star_invoice_subscription_{stars} = '{r_}'")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def refund_star_payment_fun(bot, state, chat_id, lz, username, telegram_payment_id):
    res = None
    try:
        try:
            # extra_bot = Bot(token='6967737444:AAEkvk2-hY_eKSRkj0AiycN5RJzDCUUJW9I')
            # res = await extra_bot.refund_star_payment(user_id=chat_id, telegram_payment_charge_id=telegram_payment_id)
            res = await bot.refund_star_payment(user_id=chat_id, telegram_payment_charge_id=telegram_payment_id)
            # await extra_bot.session.close()

            text = f"👩🏽‍💻 <b>{l_refund_title[lz]}</b>: @{username} [<code>{chat_id}</code>]"
            await bot.send_message(chat_id=my_tid, text=text, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.info(log_ % str(e))  # CHARGE_NOT_FOUND
            if 'REFUND_FAILED' in str(e):
                print(f"stars were used to buy a gift")
            if 'CHARGE_ALREADY_REFUNDED' in str(e):
                text = l_refund_already_done[lz]
                await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, )
                await state.clear()
                return

        print(f"{res=}")
        if res:
            text = l_refund_success[lz]
            await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, )
            await state.clear()
        else:
            text = l_refund_incorrect[lz]
            await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, )
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def check_sub_is_paid(user_payments, bot_cpayperiod):
    result = False
    try:
        for payment in user_payments:
            if payment.get('TYPE') == 'SUB':
                print(f"{payment=}")
                if bot_cpayperiod == 'once':
                    result = True
                    break
                elif bot_cpayperiod == 'month':
                    dt_end = payment.get('DT_END')
                    if dt_end == '0':
                        result = True
                        break
                    dt_end_time = datetime.strptime(dt_end, '%d-%m-%Y_%H-%M-%S').replace(tzinfo=timezone.utc)
                    if datetime.now(timezone.utc) <= dt_end_time:
                        result = True
                        break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


# endregion


# region neuro
async def get_openai_key(file_keys):
    result = None
    try:
        async with aiofiles.open(file_keys, 'r') as f:
            lines = await f.readlines()

        lines_new = []
        random.shuffle(lines)
        for key_ in lines:
            try:
                if key_.strip() == '': continue
                result = key_.strip()
                lines_new.append(key_.strip() + '\n')
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        async with aiofiles.open(file_keys, 'w') as f:
            await f.writelines(lines_new)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def del_openai_key(del_key, file_keys):
    try:
        async with aiofiles.open(file_keys, 'r') as f:
            lines = await f.readlines()

        lines_new = []
        random.shuffle(lines)
        for key_ in lines:
            try:
                if key_.strip() == del_key: continue
                lines_new.append(key_.strip() + '\n')
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        async with aiofiles.open(file_keys, 'w') as f:
            await f.writelines(lines_new)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def get_txt_wrapper(file_keys):
    result = None
    try:
        async with aiofiles.open(file_keys, 'r') as f:
            lines = await f.readlines()

        lines_new = []
        random.shuffle(lines)
        for key_ in lines:
            try:
                if key_.strip() == '': continue
                result = key_.strip()
                lines_new.append(key_.strip() + '\n')
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        async with aiofiles.open(file_keys, 'w') as f:
            await f.writelines(lines_new)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_time_time(is_bid=False):
    result = None
    try:
        if is_bid:
            result = str(int(time.time() * (1000 ** 1)) + random.randint(100, 999))[6:]
        else:
            result = str(int(time.time() * (1000 ** 2)) + random.randint(100, 999))
        await asyncio.sleep(0.05)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def train_ent_chatgpt(bot, ENT_TID, ENT_USERNAME, ENT_TYPE, EXTRA_D, BASE_D, lz, prompt='', BOT_TOKEN_=None):
    result_txt = [{'role': 'system', 'content': f'You are a helpful assistant for Telegram {ENT_TYPE}.'},
                  {'role': 'assistant', 'content': 'ok'}, ]
    result_img = ''
    try:
        KEYS_JSON = os.path.join(EXTRA_D, 'keys.json')
        print(f"train_ent_chatgpt start, {ENT_TYPE=}")

        # region init
        if ENT_TYPE == 'bot':
            extra_bot = Bot(token=BOT_TOKEN_)
            short = await extra_bot.get_my_short_description()
            short = short.short_description if short.short_description else ''
            desc = await extra_bot.get_my_description()
            desc = desc.description if desc.description else ''

            bot_info = f'Now I give you some details about this telegram app: @username is `@{ENT_USERNAME}`, ' \
                       f'description is `{desc}`. ' \
                       f'And short description is `{short}`'
            result_txt.append({'role': 'user', 'content': bot_info}),
            result_img = f"{short}"
            if len(result_img) < 40: result_img = f"{result_img} {desc}"
            await extra_bot.session.close()
        elif ENT_TYPE in ['channel', 'group', 'supergroup']:
            get_chat_ = await bot.get_chat(int(ENT_TID))
            info_ = f'Now I give you some details about this telegram {ENT_TYPE}: link is `{ENT_USERNAME}`, ' \
                    f'description is `{get_chat_.description}`, title is `{get_chat_.title}`'
            result_txt.append({'role': 'user', 'content': info_}),
            result_img = f"{get_chat_.description}, {get_chat_.title}"
        # endregion

        print(f"0 {BASE_D=}")
        if ENT_TYPE == 'bot':
            # region MSG
            sql = f"SELECT MSG_TEXT, MSG_BUTTONS FROM BOT_{ENT_TID}.MSG"
            data = await db_select_pg(sql, (), BASE_D)

            for item in data[:5]:
                try:
                    MSG_TEXT, MSG_BUTTONS = item
                    MSG_BUTTONS = ast.literal_eval(MSG_BUTTONS) if MSG_BUTTONS else []
                    MSG_BUTTONS = ', '.join([it['lbl'] for it in MSG_BUTTONS if it and 'lbl' in it])

                    if MSG_TEXT:
                        result_txt.append({'role': 'user',
                                           'content': f'There is a message of this telegram {ENT_TYPE}: {MSG_TEXT[:128]}'})  # result_img = f"{result_img}{MSG_TEXT}\n"
                    if MSG_BUTTONS:
                        result_txt.append({'role': 'user',
                                           'content': f'There are some buttons of this telegram {ENT_TYPE}: {MSG_BUTTONS}'})  # result_img = f"{result_img}{MSG_BUTTONS}\n"
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))  # endregion
        elif ENT_TYPE in ['channel']:
            print(1, BASE_D, ENT_TID)
            sql = "SELECT CHANNEL_LASTMSG FROM \"CHANNEL\" WHERE CHANNEL_TID=$1"
            data_chn = await db_select_pg(sql, (ENT_TID,), BASE_D)
            CHANNEL_LASTMSG = data_chn[0][0]

            if CHANNEL_LASTMSG:
                result_txt.append({'role': 'user',
                                   'content': f'There is a message of this telegram {ENT_TYPE}: {CHANNEL_LASTMSG}'})  # result_img = f"{result_img}. {CHANNEL_LASTMSG[:32]}\n"
        elif ENT_TYPE in ['group']:
            sql = "SELECT GROUPP_LASTMSG FROM \"GROUPP\" WHERE GROUPP_TID=$1"
            data_chn = await db_select_pg(sql, (ENT_TID,), BASE_D)
            GROUPP_LASTMSG = data_chn[0][0]

            if GROUPP_LASTMSG:
                result_txt.append({'role': 'user',
                                   'content': f'There is a message of this telegram {ENT_TYPE}: {GROUPP_LASTMSG}'})  # result_img = f"{result_img}. {CHANNEL_LASTMSG[:32]}\n"

        # region pst
        schema_name = 'USER'
        if ENT_TYPE == 'bot':
            schema_name = 'BOT'
        elif ENT_TYPE == 'channel':
            schema_name = 'CHANNEL'
        elif ENT_TYPE == 'group':
            schema_name = 'GROUPP'

        sql = f"SELECT POST_TEXT, POST_BUTTONS FROM {schema_name}_{str(ENT_TID).replace('-', '')}.POST"
        data = await db_select_pg(sql, (), BASE_D)

        for item in data[:5]:
            try:
                POST_TEXT, POST_BUTTONS = item

                if POST_TEXT:
                    result_txt.append({'role': 'user',
                                       'content': f'There is a message of this telegram {ENT_TYPE}: {POST_TEXT[:64]}'})  # if POST_BUTTONS:  #     result_txt.append({'role': 'user',  #                        'content': f'There are some buttons of this telegram {ENT_TYPE}: {POST_BUTTONS}'})
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        result_txt.append(
            {'role': 'user', 'content': f'So, this is all the information that exists about this {ENT_TYPE}. '
                                        'Your task is to generate new marketing text no more than 1024 symbols'})

        if prompt:
            result_txt.append({'role': 'user', 'content': prompt})

        result_txt.append({'role': 'user', 'content': f'. Please give answer in ISO language code: `{lz}`'})
        result_inter = f"{result_img} {prompt}".replace('  ', '')

        print(f"{result_inter=}")
        if is_all_latin(result_inter):
            result_img = f"{result_inter}"
            # result_img = f"{prompt}"
        else:
            lst = await outsource_generate({'type': 'tl', 'prompt': result_inter}, KEYS_JSON)
            if len(lst) and lst[0]['answer']:
                if ':' not in prompt and ':' in lst[0]['answer'] and len(lst[0]['answer'].split(':')) == 2:
                    result_inter = lst[0]['answer'].split(':')[-1]
                else:
                    result_inter = lst[0]['answer']
            result_img = f"{result_inter}"
            print(f"{result_img=}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result_txt, result_img


async def pst_gen_ent(bot, chat_id, KEYS_JSON, state, lc, lz, POST_TYPE, ENT_TID, ENT_TYPE, ENT_USERNAME, ENT_TITLE,
                      MEDIA_D,
                      EXTRA_D, BASE_D, prompt='', ENT_TOKEN_=None):
    result = dst = None
    try:
        if prompt in ['➡️️ Next', '/Next']: prompt = ''
        openai_keys = os.path.join(EXTRA_D, 'keys.json')
        prompt_txt, prompt_img = await train_ent_chatgpt(bot, ENT_TID, ENT_USERNAME, ENT_TYPE, BASE_D, EXTRA_D, BASE_D,
                                                         lz, prompt, ENT_TOKEN_)
        templ = os.path.join(MEDIA_D, str(ENT_TID), datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f'))
        POST_FIDNOTE = BOT_TOKEN = POSTB_FID = POSTB_FIDNOTE = None
        if ENT_TYPE == 'bot':
            BASE_D = os.path.join(EXTRA_D, 'db.db')
            sql = "SELECT BOT_TOKEN FROM \"BOT\" WHERE BOT_TID=$1"
            data = await db_select_pg(sql, (ENT_TID,), BASE_D)
            if not len(data): return
            BOT_TOKEN = data[0][0]

        if POST_TYPE == 'text':
            # print(f"{prompt_txt=}")
            lst = await outsource_generate({'type': 'txt', 'prompt': prompt_txt}, openai_keys)
            if not len(lst): return

            if ':' not in prompt and ':' in lst[0]['answer'] and len(lst[0]['answer'].split(':')) == 2:
                res = lst[0]['answer'].split(':')[-1]
            else:
                res = lst[0]['answer']

            print(f"{res=}")
            await state.update_data(POST_TEXT=res.strip())
        elif POST_TYPE in ['photo', 'gif', 'animation', 'sticker', 'video', 'telescope']:
            lst = await outsource_generate({'type': 'img', 'prompt': prompt_img}, openai_keys)
            print(f"{str(lst)[:256]=}")
            if not len(lst): return

            dst = os.path.join(MEDIA_D, str(ENT_TID), f"{templ}.png")
            if not str(lst[0]['answer']).startswith('https://'):
                async with aiofiles.open(dst, "wb") as f:
                    await f.write(base64.b64decode(lst[0]['answer']))
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(lst[0]['answer']) as response:
                        res = await response.read()

                        async with aiofiles.open(dst, 'wb') as f:
                            await f.write(res)

            if POST_TYPE in ['gif', 'animation']:
                dst_gif = f"{templ}.gif"
                dst_gif = await convert_png_to_gif(dst, dst_gif)

                POST_LNK = await get_link_for_media(bot, chat_id, dst, KEYS_JSON)
                res = await bot.send_animation(chat_id=chat_id, animation=types.FSInputFile(dst_gif))

                POST_TYPE = 'animation'
                POST_FID = res.animation.file_id
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.gif')}"
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_animation(chat_id=chat_id, animation=types.FSInputFile(dst_gif))
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    await extra_bot.session.close()
                    POSTB_FID = res2.animation.file_id
                if os.path.exists(dst_gif): os.remove(dst_gif)
            elif POST_TYPE == 'sticker':
                dst_webp = f"{templ}.webp"
                image = Image.open(dst)
                image = await correct_orientation(image)
                image.save(dst_webp, format="webp", quality=30)

                POST_LNK = await get_link_for_media(bot, chat_id, dst, KEYS_JSON)
                res = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(dst_webp))

                POST_TYPE = 'sticker'
                POST_FID = res.sticker.file_id
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.webp')}"
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(dst_webp))
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    await extra_bot.session.close()
                    POSTB_FID = res2.sticker.file_id
                if os.path.exists(dst_webp): os.remove(dst_webp)
            elif POST_TYPE == 'video':
                dst_mp4 = f"{templ}.mp4"
                dst_mp4 = await convert_png_to_mp4(ENT_TID, dst, dst_mp4, MEDIA_D)

                POST_LNK = await get_link_for_media(bot, chat_id, dst_mp4, KEYS_JSON)
                res = await bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))

                POST_TYPE = 'video'
                POST_FID = res.video.file_id
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    await extra_bot.session.close()
                    POSTB_FID = res2.video.file_id
                if os.path.exists(dst_mp4): os.remove(dst_mp4)
            elif POST_TYPE in ['video_note', 'telescope']:
                dst_new = os.path.join(MEDIA_D, str(ENT_TID),
                                       datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.png'))
                img = Image.open(dst)
                img = await correct_orientation(img)
                new_size = (640, 640)
                resized_img = img.resize(new_size)
                resized_img.save(dst_new)

                dst_mp4 = f"{templ}.mp4"
                dst_mp4 = await convert_png_to_mp4(ENT_TID, dst_new, dst_mp4, MEDIA_D)
                POST_LNK = await get_link_for_media(bot, chat_id, dst_mp4, KEYS_JSON)

                res = await bot.send_video_note(chat_id=chat_id, video_note=types.FSInputFile(dst_mp4))
                res_note = await bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                await bot.delete_message(chat_id, res_note.message_id)
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_video_note(chat_id=chat_id, video_note=types.FSInputFile(dst_mp4))
                    res_note2 = await extra_bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    await extra_bot.delete_message(chat_id, res_note2.message_id)
                    await extra_bot.session.close()
                    POSTB_FID = res2.video_note.file_id
                    POSTB_FIDNOTE = res_note2.video.file_id

                if os.path.exists(dst_mp4): os.remove(dst_mp4)
                if os.path.exists(dst_new): os.remove(dst_new)

                POST_TYPE = 'video_note'
                POST_FID = res.video_note.file_id
                POST_FIDNOTE = res_note.video.file_id
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"
            else:
                POST_LNK = await get_link_for_media(bot, chat_id, dst, KEYS_JSON)
                res = await bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(dst))

                POST_TYPE = 'photo'
                POST_FID = res.photo[-1].file_id
                print(f"{POST_FID=}")
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.png')}"
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(dst))
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    await extra_bot.session.close()
                    POSTB_FID = res2.photo[-1].file_id

            await bot.delete_message(chat_id, res.message_id)
            if dst and os.path.exists(dst): os.remove(dst)

            await state.update_data(POST_TYPE=POST_TYPE, POST_LNK=POST_LNK, POST_FILENAME=POST_FILENAME,
                                    POST_FID=POST_FID, POST_FIDNOTE=POST_FIDNOTE, POSTB_FID=POSTB_FID,
                                    POSTB_FIDNOTE=POSTB_FIDNOTE)
        elif POST_TYPE in ['audio', 'voice']:
            lst = await outsource_generate({'type': 'txt', 'prompt': prompt_txt}, openai_keys)
            if not len(lst): return
            MSG_TEXT = lst[0]['answer']

            MSG_TEXT = await format_text(MSG_TEXT)
            print(f"{MSG_TEXT=}")
            lst = await outsource_generate(
                {'type': 'tts', 'prompt': MSG_TEXT, 'lc': lc, 'dir_name': os.path.join(MEDIA_D, str(ENT_TID))},
                openai_keys)
            if not len(lst): return

            thumbnail = types.FSInputFile(os.path.join(EXTRA_D, 'img.jpg'))
            dst = lst[0]['answer']
            if POST_TYPE == 'audio':
                res = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst), thumbnail=thumbnail,
                                           title=ENT_TITLE, performer=ENT_USERNAME, disable_notification=True)
                await bot.delete_message(chat_id, res.message_id)
                POST_FID = res.audio.file_id

                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst),
                                                      thumbnail=thumbnail, title=ENT_TITLE, performer=ENT_USERNAME)
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    await extra_bot.session.close()
                    POSTB_FID = res2.audio.file_id
            else:
                res = await bot.send_voice(chat_id=chat_id, voice=types.FSInputFile(dst), disable_notification=True)
                POST_FID = res.voice.file_id
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res2 = await extra_bot.send_voice(chat_id=chat_id, voice=types.FSInputFile(dst))
                    await extra_bot.delete_message(chat_id, res2.message_id)
                    POSTB_FID = res2.voice.file_id

                res_note = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst), thumbnail=thumbnail,
                                                title=ENT_TITLE, performer=ENT_USERNAME, disable_notification=True)
                await bot.delete_message(chat_id, res_note.message_id)
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res_note2 = await extra_bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst),
                                                           thumbnail=thumbnail, title=ENT_TITLE, performer=ENT_USERNAME)
                    await extra_bot.delete_message(chat_id, res_note2.message_id)
                    await extra_bot.session.close()
                    if res_note2.audio: POSTB_FIDNOTE = res_note2.audio.file_id

                if res_note.audio:
                    POST_FIDNOTE = res_note.audio.file_id
                else:
                    audio_ = AudioFileClip(dst)
                    video_clip = VideoClip(lambda t: np.zeros((480, 640, 3), dtype=np.uint8), duration=audio_.duration)
                    video_clip = video_clip.with_audio(audio_)
                    file_name_video = dst[:dst.rfind('.')] + '.mp4'
                    video_clip.write_videofile(file_name_video, codec="libx264", audio_codec="aac", fps=24)

                    res_note = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(file_name_video),
                                                    thumbnail=thumbnail, title=ENT_TITLE, performer=ENT_USERNAME,
                                                    disable_notification=True)
                    await bot.delete_message(chat_id, res_note.message_id)
                    if BOT_TOKEN:
                        extra_bot = Bot(token=BOT_TOKEN)
                        res_note2 = await extra_bot.send_audio(chat_id=chat_id,
                                                               audio=types.FSInputFile(file_name_video),
                                                               thumbnail=thumbnail, title=ENT_TITLE,
                                                               performer=ENT_USERNAME)
                        await extra_bot.delete_message(chat_id, res_note2.message_id)
                        await extra_bot.session.close()
                        if res_note2.audio: POSTB_FIDNOTE = res_note2.audio.file_id

                    if os.path.exists(file_name_video): os.remove(file_name_video)
                    if res_note.audio: POST_FIDNOTE = res_note.audio.file_id
            await bot.delete_message(chat_id, res.message_id)

            POST_LNK = None
            try:
                audio_ = AudioFileClip(dst)
                video_clip = VideoClip(lambda t: np.zeros((480, 640, 3), dtype=np.uint8), duration=audio_.duration)
                video_clip = video_clip.with_audio(audio_)
                file_name_video = dst[:dst.rfind('.')] + '.mp4'
                video_clip.write_videofile(file_name_video, codec="libx264", audio_codec="aac", fps=24)
                POST_LNK = await get_link_for_media(bot, chat_id, file_name_video, KEYS_JSON)
                if os.path.exists(file_name_video): os.remove(file_name_video)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
            finally:
                pass
            if os.path.exists(dst): os.remove(dst)

            print(f"{POST_LNK=}")
            await state.update_data(POST_TYPE=POST_TYPE, POST_LNK=POST_LNK, POST_FILENAME=os.path.basename(dst),
                                    POST_FID=POST_FID, POST_FIDNOTE=POST_FIDNOTE, POSTB_FID=POSTB_FID,
                                    POSTB_FIDNOTE=POSTB_FIDNOTE)
        else:
            lst = await outsource_generate({'type': 'txt', 'prompt': prompt_txt}, openai_keys)
            if not len(lst): return
            MSG_TEXT = lst[0]['answer']

            dst_txt = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.txt')
            async with aiofiles.open(dst_txt, 'w') as f:
                await f.write(str(MSG_TEXT))

            dt_ = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.zip')
            dst = os.path.join(MEDIA_D, str(ENT_TID), dt_)
            with zipfile.ZipFile(dst, 'w') as zipf:
                zipf.write(dst_txt, arcname=f'%d-%m-%Y_%H-%M-%S-%f.txt')
            if os.path.exists(dst_txt): os.remove(dst_txt)

            res = await bot.send_document(chat_id=chat_id, document=types.FSInputFile(dst),
                                          thumbnail=types.FSInputFile(os.path.join(EXTRA_D, 'parse.jpg')),
                                          disable_notification=True, disable_content_type_detection=True)
            await bot.delete_message(chat_id, res.message_id)
            POST_FID = res.document.file_id
            if os.path.exists(dst): os.remove(dst)

            await state.update_data(POST_TYPE=POST_TYPE, POST_FILENAME=os.path.basename(dst), POST_FID=POST_FID)

        result = True
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if dst and os.path.exists(dst): os.remove(dst)
        return result


async def pst_gen_ent2(bot, chat_id, lc, lz, page, POST_TID, POST_TYPE, POST_MEDIA, ENT_TID, PROJECT_TYPE, ENT_USERNAME,
                       ENT_TITLE, MEDIA_D, EXTRA_D, BASE_D, prompt='', ENT_TOKEN_=None, request_app=None):
    result = dst = None
    try:
        POST_MEDIA = json.loads(POST_MEDIA) if isinstance(POST_MEDIA, str) else POST_MEDIA
        print(f"pst_gen_ent2 start", POST_MEDIA)
        print(f"{ENT_TOKEN_=}, {bot.id=}")
        KEYS_JSON = os.path.join(EXTRA_D, 'keys.json')
        prompt_txt, prompt_img = await train_ent_chatgpt(bot, ENT_TID, ENT_USERNAME, PROJECT_TYPE, EXTRA_D, BASE_D, lz,
                                                         prompt, ENT_TOKEN_)

        os.makedirs(os.path.join(MEDIA_D, str(ENT_TID)), exist_ok=True, mode=0o777)
        templ = os.path.join(MEDIA_D, str(ENT_TID), datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f'))
        POST_FIDNOTE = BOT_TOKEN = None
        if PROJECT_TYPE == 'bot': BOT_TOKEN = ENT_TOKEN_

        print(f"after train_ent_chatgpt: {POST_TYPE=}, {prompt_txt} {prompt_img}")
        if POST_TYPE == 'text':
            print(f"{prompt_txt=}")
            lst = await outsource_generate({'type': 'txt', 'prompt': prompt_txt}, KEYS_JSON)
            if not len(lst): return
            if ':' not in prompt and ':' in lst[0]['answer'] and len(lst[0]['answer'].split(':')) == 2:
                result = lst[0]['answer'].split(':')[-1]
            else:
                result = lst[0]['answer']
            print(f"{result=}")
        elif POST_TYPE in ['photo', 'gif', 'animation', 'sticker', 'video', 'video_note', 'web']:
            lst = await outsource_generate({'type': 'img', 'prompt': prompt_img}, KEYS_JSON)
            if not len(lst): return

            print(f"{str(lst)[:256]=}")
            dst = os.path.join(MEDIA_D, str(ENT_TID), f"{templ}.png")

            if not str(lst[0]['answer']).startswith('https://'):
                async with aiofiles.open(dst, "wb") as f:
                    await f.write(base64.b64decode(lst[0]['answer']))
            else:
                print(f"получается мы тут {lst[0]['answer']=}")
                async with aiohttp.ClientSession() as session:
                    async with session.get(lst[0]['answer']) as response:
                        res = await response.read()

                        async with aiofiles.open(dst, 'wb') as f:
                            await f.write(res)

            if POST_TYPE in ['gif', 'animation', 'web']:
                dst_gif = f"{templ}.gif"
                dst_gif = await convert_png_to_gif(dst, dst_gif)

                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res = await extra_bot.send_animation(chat_id=chat_id, animation=types.FSInputFile(dst_gif))
                    await extra_bot.delete_message(chat_id, res.message_id)
                    await extra_bot.session.close()
                else:
                    res = await bot.send_animation(chat_id=chat_id, animation=types.FSInputFile(dst_gif))
                    await bot.delete_message(chat_id, res.message_id)

                POST_TYPE = 'gif' if POST_TYPE in ['gif', 'animation'] else 'web'
                POST_FID = res.animation.file_id
                POST_LNK = await get_link_for_media(bot, chat_id, dst_gif, KEYS_JSON)
                POST_LNK2 = gif_jpg
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.gif')}"

                if os.path.exists(dst_gif): os.remove(dst_gif)
            elif POST_TYPE == 'sticker':
                dst_webp = f"{templ}.webp"

                if random.shuffle([True, False]):
                    image = Image.open(dst)
                    image = await correct_orientation(image)
                    image.save(dst_webp, format="webp", quality=30)

                    if BOT_TOKEN:
                        extra_bot = Bot(token=BOT_TOKEN)
                        res = await extra_bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(dst_webp))
                        await extra_bot.delete_message(chat_id, res.message_id)
                        await extra_bot.session.close()
                    else:
                        res = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(dst_webp))
                        await bot.delete_message(chat_id, res.message_id)

                    POST_FID = res.sticker.file_id
                else:
                    if BOT_TOKEN:
                        extra_bot = Bot(token=BOT_TOKEN)
                        print(f"item_to_dynamic_sticker start ....")
                        POST_FID, _ = await item_to_dynamic_sticker(extra_bot, chat_id, dst, 'sticker', 'video', False,
                                                                    True, False, True)
                        await extra_bot.session.close()
                    else:
                        res = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(dst_webp))
                        POST_FID, _ = await item_to_dynamic_sticker(bot, chat_id, dst, 'sticker', 'video', False,
                                                                    True, False, True)

                POST_LNK = await get_link_for_media(bot, chat_id, dst, KEYS_JSON)
                POST_LNK2 = sticker_jpg
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.webp')}"

                if os.path.exists(dst_webp): os.remove(dst_webp)
            elif POST_TYPE == 'video':
                dst_mp4 = f"{templ}.mp4"
                dst_mp4 = await convert_png_to_mp4(ENT_TID, dst, dst_mp4, MEDIA_D)

                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res = await extra_bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                    await extra_bot.delete_message(chat_id, res.message_id)
                    await extra_bot.session.close()
                else:
                    res = await bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                    await bot.delete_message(chat_id, res.message_id)

                POST_FID = res.video.file_id
                POST_LNK = await get_link_for_media(bot, chat_id, dst_mp4, KEYS_JSON)
                POST_LNK2 = video_jpg
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"

                if os.path.exists(dst_mp4): os.remove(dst_mp4)
            elif POST_TYPE in ['video_note', 'telescope']:
                dst_new = os.path.join(MEDIA_D, str(ENT_TID),
                                       datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.png'))
                img = Image.open(dst)
                img = await correct_orientation(img)
                new_size = (640, 640)
                resized_img = img.resize(new_size)
                resized_img.save(dst_new)
                dst_mp4 = f"{templ}.mp4"
                dst_mp4 = await convert_png_to_mp4(ENT_TID, dst_new, dst_mp4, MEDIA_D)

                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res = await extra_bot.send_video_note(chat_id=chat_id, video_note=types.FSInputFile(dst_mp4))
                    await extra_bot.delete_message(chat_id, res.message_id)

                    res_note = await extra_bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                    await extra_bot.delete_message(chat_id, res_note.message_id)
                    await extra_bot.session.close()
                else:
                    res_note = await bot.send_video_note(chat_id=chat_id, video_note=types.FSInputFile(dst_mp4))
                    await bot.delete_message(chat_id, res_note.message_id)

                    res = await bot.send_video(chat_id=chat_id, video=types.FSInputFile(dst_mp4))
                    await bot.delete_message(chat_id, res.message_id)

                POST_FID = res.video_note.file_id
                POST_FIDNOTE = res_note.video.file_id
                POST_LNK = await get_link_for_media(bot, chat_id, dst_mp4, KEYS_JSON)
                POST_LNK2 = video_note_jpg
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"

                if os.path.exists(dst_mp4): os.remove(dst_mp4)
                if os.path.exists(dst_new): os.remove(dst_new)
            else:
                if BOT_TOKEN:
                    print(f"заходим сюда")
                    extra_bot = Bot(token=BOT_TOKEN)
                    res = await extra_bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(dst))
                    await extra_bot.delete_message(chat_id, res.message_id)
                    await extra_bot.session.close()
                else:
                    res = await bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(dst))
                    await bot.delete_message(chat_id, res.message_id)

                POST_TYPE = 'photo'
                POST_FID = res.photo[-1].file_id
                POST_LNK = await get_link_for_media(bot, chat_id, dst, KEYS_JSON)
                POST_LNK2 = photo_jpg
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.png')}"

            print(f'{POST_TYPE=}')
            if page == 'MSG':
                if POST_LNK.endswith(('.mp4', '.gif', '.webm', '.mov', '.mp3')):
                    POST_LNK2 = await jpg_video_preview(bot, POST_TID, KEYS_JSON, POST_LNK, ENT_TID, POST_TYPE,
                                                        POST_FID, BASE_D, MEDIA_D, BOT_TOKEN)
                else:
                    POST_LNK2 = await jpg_photo_preview(bot, POST_TID, KEYS_JSON, POST_LNK, ENT_TID, POST_TYPE, MEDIA_D)

            if POST_MEDIA and len(POST_MEDIA) and POST_MEDIA[0]['file_type'] == POST_TYPE:
                POST_MEDIA.append({"file_id": POST_FID, "file_id_note": POST_FIDNOTE, "fileb_id": POST_FID,
                                   "fileb_id_note": POST_FIDNOTE, "file_type": POST_TYPE, "file_name": POST_FILENAME,
                                   "file_link": POST_LNK, "file_link2": POST_LNK2})
            else:
                POST_MEDIA = [{"file_id": POST_FID, "file_id_note": POST_FIDNOTE, "fileb_id": POST_FID,
                               "fileb_id_note": POST_FIDNOTE, "file_type": POST_TYPE, "file_name": POST_FILENAME,
                               "file_link": POST_LNK, "file_link2": POST_LNK2}]
            if POST_MEDIA and len(POST_MEDIA) > 10:
                POST_MEDIA = POST_MEDIA[len(POST_MEDIA) - 10:]
                print(f"len(POST_MEDIA) > 10 now", len(POST_MEDIA))

            result = POST_MEDIA
        elif POST_TYPE in ['audio', 'voice']:
            lst = await outsource_generate({'type': 'txt', 'prompt': prompt_txt}, KEYS_JSON)
            if not len(lst): return
            MSG_TEXT = lst[0]['answer']

            print(f"{prompt_txt=}, {lst=}")
            # MSG_TEXT = await format_text(MSG_TEXT)
            print(f"{MSG_TEXT=}")
            lst = await outsource_generate(
                {'type': 'tts', 'prompt': MSG_TEXT, 'lc': lc, 'dir_name': os.path.join(MEDIA_D, str(ENT_TID))},
                KEYS_JSON)
            if not len(lst): return

            thumbnail = types.FSInputFile(os.path.join(EXTRA_D, 'img.jpg'))
            dst = lst[0]['answer']
            if POST_TYPE == 'audio':
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res = await extra_bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst),
                                                     thumbnail=thumbnail, title=ENT_TITLE, performer=ENT_USERNAME)
                    await extra_bot.delete_message(chat_id, res.message_id)
                    await extra_bot.session.close()
                else:
                    res = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst), thumbnail=thumbnail,
                                               title=ENT_TITLE, performer=ENT_USERNAME, disable_notification=True)
                    await bot.delete_message(chat_id, res.message_id)

                POST_LNK2 = audio_jpg
                POST_FID = res.audio.file_id
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp3')}"
            else:
                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res = await extra_bot.send_voice(chat_id=chat_id, voice=types.FSInputFile(dst))
                    await extra_bot.delete_message(chat_id, res.message_id)
                else:
                    res = await bot.send_voice(chat_id=chat_id, voice=types.FSInputFile(dst), disable_notification=True)
                    await bot.delete_message(chat_id, res.message_id)

                if BOT_TOKEN:
                    extra_bot = Bot(token=BOT_TOKEN)
                    res_note = await extra_bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst),
                                                          thumbnail=thumbnail, title=ENT_TITLE, performer=ENT_USERNAME)
                    await extra_bot.delete_message(chat_id, res_note.message_id)
                    await extra_bot.session.close()
                else:
                    res_note = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(dst), thumbnail=thumbnail,
                                                    title=ENT_TITLE, performer=ENT_USERNAME, disable_notification=True)
                    await bot.delete_message(chat_id, res_note.message_id)

                if res_note.audio:
                    POST_FIDNOTE = res_note.audio.file_id
                else:
                    audio_ = AudioFileClip(dst)
                    video_clip = VideoClip(lambda t: np.zeros((480, 640, 3), dtype=np.uint8), duration=audio_.duration)
                    video_clip = video_clip.with_audio(audio_)
                    file_name_video = dst[:dst.rfind('.')] + '.mp4'
                    video_clip.write_videofile(file_name_video, codec="libx264", audio_codec="aac", fps=24)

                    if BOT_TOKEN:
                        extra_bot = Bot(token=BOT_TOKEN)
                        res_note = await extra_bot.send_audio(chat_id=chat_id,
                                                              audio=types.FSInputFile(file_name_video),
                                                              thumbnail=thumbnail, title=ENT_TITLE,
                                                              performer=ENT_USERNAME)
                        await extra_bot.delete_message(chat_id, res_note.message_id)
                        await extra_bot.session.close()
                    else:
                        res_note = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(file_name_video),
                                                        thumbnail=thumbnail, title=ENT_TITLE, performer=ENT_USERNAME,
                                                        disable_notification=True)
                        await bot.delete_message(chat_id, res_note.message_id)

                    if res_note.audio: POST_FIDNOTE = res_note.audio.file_id

                    if os.path.exists(file_name_video): os.remove(file_name_video)

                POST_LNK2 = voice_jpg
                POST_FID = res.voice.file_id
                POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.ogg')}"

            print(f"{dst=}")
            print(f"{os.path.exists(dst)=}")
            POST_LNK = None
            try:
                audio_ = AudioFileClip(dst)
                video_clip = VideoClip(lambda t: np.zeros((480, 640, 3), dtype=np.uint8), duration=audio_.duration)
                video_clip = video_clip.with_audio(audio_)
                file_name_video = dst[:dst.rfind('.')] + '.mp4'
                video_clip.write_videofile(file_name_video, codec="libx264", audio_codec="aac", fps=24)
                POST_LNK = await get_link_for_media(bot, chat_id, file_name_video, KEYS_JSON)
                if os.path.exists(file_name_video): os.remove(file_name_video)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
            finally:
                pass

            if page == 'MSG':
                if POST_LNK.endswith(('.mp4', '.gif', '.webm', '.mov', '.mp3')):
                    POST_LNK2 = await jpg_video_preview(bot, POST_TID, KEYS_JSON, POST_LNK, ENT_TID, POST_TYPE,
                                                        POST_FID, BASE_D, MEDIA_D, BOT_TOKEN)
                else:
                    POST_LNK2 = await jpg_photo_preview(bot, POST_TID, KEYS_JSON, POST_LNK, ENT_TID, POST_TYPE, MEDIA_D)

            if POST_MEDIA and len(POST_MEDIA) and POST_MEDIA[0]['file_type'] == POST_TYPE:
                POST_MEDIA.append({"file_id": POST_FID, "file_id_note": POST_FIDNOTE, "fileb_id": POST_FID,
                                   "fileb_id_note": POST_FIDNOTE, "file_type": POST_TYPE, "file_name": POST_FILENAME,
                                   "file_link": POST_LNK, "file_link2": POST_LNK2})
            else:
                POST_MEDIA = [{"file_id": POST_FID, "file_id_note": POST_FIDNOTE, "fileb_id": POST_FID,
                               "fileb_id_note": POST_FIDNOTE, "file_type": POST_TYPE, "file_name": POST_FILENAME,
                               "file_link": POST_LNK, "file_link2": POST_LNK2}]
            if POST_MEDIA and len(POST_MEDIA) > 10:
                POST_MEDIA = POST_MEDIA[len(POST_MEDIA) - 10:]
                print(f"len(POST_MEDIA) > 10 now", len(POST_MEDIA))
            result = POST_MEDIA

            if os.path.exists(dst): os.remove(dst)

            print(f"{POST_LNK=}")
        else:
            lst = await outsource_generate({'type': 'txt', 'prompt': prompt_txt}, KEYS_JSON)
            if not len(lst): return
            if ':' not in prompt and ':' in lst[0]['answer'] and len(lst[0]['answer'].split(':')) == 2:
                MSG_TEXT = lst[0]['answer'].split(':')[-1]
            else:
                MSG_TEXT = lst[0]['answer']

            print(f"{MSG_TEXT=}")
            dst_txt = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.txt')
            async with aiofiles.open(dst_txt, 'w') as f:
                await f.write(str(MSG_TEXT))

            # pdf = FPDF()
            # pdf.add_page()
            # pdf.set_font("Arial", size=12)
            # dst_txt = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.txt')
            # pdf.multi_cell(0, 10, str(MSG_TEXT))
            # pdf.output(dst_txt)

            print(f"{os.path.exists(dst_txt)=}")
            dt_ = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.zip')
            dst = os.path.join(MEDIA_D, str(ENT_TID), dt_)
            with zipfile.ZipFile(dst, 'w') as zipf:
                arcname = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.txt')
                zipf.write(dst_txt, arcname=arcname)
            if os.path.exists(dst_txt): os.remove(dst_txt)

            # pst_download
            print(f"{os.path.exists(dst)=}")
            resb = None
            if BOT_TOKEN:
                extra_bot = Bot(token=BOT_TOKEN)
                print(f"{BOT_TOKEN=}")
                resb = await extra_bot.send_document(chat_id=chat_id, document=types.FSInputFile(dst),
                                                     thumbnail=types.FSInputFile(os.path.join(EXTRA_D, 'parse.jpg')),
                                                     disable_notification=True, disable_content_type_detection=True)
                print(f"{resb=}")
                await extra_bot.delete_message(chat_id, resb.message_id)
                await extra_bot.session.close()

            res = await bot.send_document(chat_id=chat_id, document=types.FSInputFile(dst),
                                          thumbnail=types.FSInputFile(os.path.join(EXTRA_D, 'parse.jpg')),
                                          disable_notification=True, disable_content_type_detection=True)
            print(f"{res=}")
            await bot.delete_message(chat_id, res.message_id)

            POST_FID = res.document.file_id
            POSTB_FID = resb.document.file_id if resb else POST_FID

            print(f"{POST_FID=}")
            # POST_LNK = await get_link_for_media(bot, chat_id, dst, KEYS_JSON)
            POST_FILENAME = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.zip')}"
            POST_LNK = POST_LNK2 = document_jpg

            print(f"{POST_MEDIA=}")
            if POST_MEDIA and len(POST_MEDIA) and POST_MEDIA[0]['file_type'] == POST_TYPE:
                POST_MEDIA.append(
                    {"file_id": POST_FID, "file_id_note": POST_FIDNOTE, "fileb_id": POSTB_FID,
                     "fileb_id_note": POST_FIDNOTE, "file_type": POST_TYPE, "file_name": POST_FILENAME,
                     "file_link": POST_LNK, "file_link2": POST_LNK2})
            else:
                POST_MEDIA = [{"file_id": POST_FID, "file_id_note": POST_FIDNOTE, "fileb_id": POSTB_FID,
                               "fileb_id_note": POST_FIDNOTE, "file_type": POST_TYPE, "file_name": POST_FILENAME,
                               "file_link": POST_LNK, "file_link2": POST_LNK2}]
            if POST_MEDIA and len(POST_MEDIA) > 10:
                POST_MEDIA = POST_MEDIA[len(POST_MEDIA) - 10:]
                print(f"len(POST_MEDIA) > 10 now", len(POST_MEDIA))
            result = POST_MEDIA

            if os.path.exists(dst): os.remove(dst)
    except Exception as e:
        logger.info(log_ % str(e))
        if 'chat not found' in str(e).lower():
            result = 'error'
    finally:
        print(f"finally {result=}")
        if dst and os.path.exists(dst): os.remove(dst)

        if request_app:
            request_app.setdefault('user_data', {}).setdefault(chat_id, {})['gen_status'] = True
            request_app.setdefault('user_data', {}).setdefault(chat_id, {})['gen_type'] = POST_TYPE
            request_app.setdefault('user_data', {}).setdefault(chat_id, {})['gen_result'] = result
        return result


async def recognize_speech(chat_id, lc, MEDIA_D, file_name, model='base'):
    result = text = file_wav = None
    try:
        # try:
        #     model = whisper.load_model(model)
        #     tmp = model.transcribe(file_name)
        #     text = tmp['text']
        # except Exception as e:
        #     logger.info(log_ % f"whisper error: {e}")

        if not text or text == '':
            ext = file_name.split('.')[-1]
            recognizer = sr.Recognizer()
            file_wav = os.path.join(MEDIA_D, f"{chat_id}.wav")

            try:
                if ext == 'mp3':
                    audio = AudioSegment.from_mp3(file_name)
                elif ext == 'ogg':
                    audio = AudioSegment.from_ogg(file_name)
                else:
                    audio = AudioSegment.from_file(file_name, format=ext)
                audio.export(file_wav, format="wav")
            except:
                video_clip = VideoFileClip(file_name)
                audio_clip = video_clip.audio
                audio_clip.write_audiofile(file_wav, codec='pcm_s16le')
                audio_clip.close()
                video_clip.close()

            with sr.AudioFile(file_wav) as source:
                try:
                    recognizer.adjust_for_ambient_noise(source)
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language=lc)
                except:
                    pass

        if not text or text == '': raise Exception
        result = text.strip()
        logger.info(log_ % f"recognition: {text[:32]}")
    except Exception as e:
        logger.info(log_ % str(e) + f"{model}")
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if file_name and os.path.exists(file_name): os.remove(file_name)
        if file_wav and os.path.exists(file_wav): os.remove(file_wav)
        return result


async def g4f_chat_completion(result_txt):
    result = None
    try:
        logger.info(log_ % f"g4f starting...\n{result_txt[-1]}")

        cnt = 1
        while cnt >= 0:
            try:
                # client = G4FClient()
                # result = client.chat.completions.create(model="gpt-3.5-turbo", messages=result_txt)
                # print(response.choices[0].message.content)
                # client = AsyncClient()
                # result = await client.chat.completions.create(model="gpt-3.5-turbo", messages=result_txt)
                # result = await g4f.ChatCompletion.create_async(model=g4f.models.default, messages=result_txt, )
                # provider=g4f.Provider.Bing)
                # from g4f.client import Client
                # client = Client()
                # response = client.chat.completions.create(
                #     model="gpt-4o-mini",
                #     # messages=[{"role": "user", "content": "Как много ног у кота?"}],
                #     messages=result_txt,
                #     web_search=False
                # )
                from g4f.client import AsyncClient
                client = AsyncClient()
                print(f"{result_txt=}")
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=result_txt,
                    web_search=False
                )
                result = response.choices[0].message.content
                print(f"g4f_chat_completion {result=}")
                if not result: raise Exception
                # result = result.choices[0].message.content
                # result = 'txt'
                if 'bing' in result.lower() and ':' in result: result = result[result.find(':') + 1:]
                if '1024' in result.lower() and ':' in result: result = result[result.find(':') + 1:]
                if 'bing' in result.lower() and '.' in result: result = result[result.find('.') + 1:]
                if '\n' in result:
                    res = result.split('\n\n')[0]
                    if '[1]:' in res:
                        ix = result.find('\n\n')
                        result = result[ix:].strip()

                    if '[3]:' in result:
                        result = result.split('[3]:')[-1]

                    if '[4]:' in result:
                        result = result.split('[4]:')[-1]

                    result = result.replace('[^1^]', '').replace('[1]', '').replace('[^2^]', '').replace('[2]',
                                                                                                         '').replace(
                        '[^3^]', '').replace('[3]', '').replace('[^4^]', '').replace('[4]', '')
                    result = result.replace('https://bing.com/search?q=', '').replace('""', '').replace('dw.com',
                                                                                                        '').replace(
                        'Википедия', '')
                    result = result.replace(' , ', ', ').replace('\n: ', '').replace('\n\n: ', '').replace(' — ',
                                                                                                           ' - ').replace(
                        '/ru/', '')
                    result = result.replace('%D0%', '').replace('%D1%', '').replace('%87%', '').replace('%82%',
                                                                                                        '').replace(
                        '%BE%', '').replace('%B0%', '').replace('%B5%', '').replace('%B1%', '').replace('%8B%',
                                                                                                        '').replace(
                        '%BA%', '').replace('%80%', '').replace('%8E%', '').replace('()', '').replace('https://www.',
                                                                                                      '').replace(' .',
                                                                                                                  '.')
                    result = result.replace('Источник: ', '').replace('8782BE', '').replace('82B0BABEB5', '').replace(
                        'B1BE828B', '').replace('B8', '').replace('BAB0BA', '').replace('BEBDB8', '').replace(
                        '80B0B1BE82B08E82', '').replace('a-41716550', '').replace(' – DW – ', '')
                    result = result.strip()
                if 'bing' in result.lower() and '.' in result:
                    tmp = result.split('\n\n')
                    if len(tmp) > 1:
                        result = result.replace(tmp[0], '')
                if 'copilot' in result.lower():
                    result = result[result.find(':') + 1:]
                    if '---' in result: result = result[result.find('---') + 1:].strip()
                if 'copilot' in result.lower():
                    result = result[result.find('.') + 1:]
                    if '---' in result: result = result[result.find('---') + 1:].strip()

                result = result.replace('[^4^][4]', '').replace('[^4^]', '').replace('«', '').replace('»', '')
                result = result.replace('[^5^][5]', '').replace('[^5^]', '').replace('[8]', '').replace('[9]', '')
                result = result.replace('Bing', '').strip().replace('**', '').replace('""', '')
                result = result.replace('**', '').rstrip('.')

                break
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(3, 4), 2))
            finally:
                cnt -= 1
    except Exception as e:
        logger.info(log_ % f"{str(e)}")
    finally:
        return result


async def outsource_generate(lst, path='link_path'):
    result = []
    try:
        data_ = []
        if isinstance(lst, dict): lst = [lst]

        for item in lst:
            try:
                if item['type'] == 'tgph':
                    file_path = item['prompt']

                    if not item['prompt'].startswith('https://'):
                        if os.path.getsize(file_path) > 5242880: continue
                        ext = str(file_path[file_path.rfind('.'):]).lower()
                        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']: continue

                        async with aiofiles.open(file_path, 'rb') as f:
                            file_content = await f.read()

                        file_content_hex = binascii.hexlify(file_content).decode('utf-8')
                        file_name = os.path.basename(file_path)
                        data_.append({'type': item['type'], 'prompt': file_content_hex, 'extra': 'file_path',
                                      'file_name': file_name})
                    else:
                        data_.append({'type': item['type'], 'prompt': item['prompt'], 'extra': 'link_path'})
                elif item['type'] == 'txt':
                    prompt = item['prompt']

                    if isinstance(prompt, str):
                        prompt = [{"role": "system", "content": 'You are a helpful assistant for Telegram'},
                                  {"role": "user", "content": prompt}]

                    data_.append({'type': item['type'], 'prompt': prompt})
                elif item['type'] == 'img':
                    if item['prompt'] == 'variation':
                        prompt = item['prompt'].strip()
                        ext = str(item['file_path'][item['file_path'].rfind('.'):]).lower()
                        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webp']: continue
                        if os.path.getsize(item['file_path']) > 5242880: continue

                        src = os.path.join(item['dir_name'], item['file_path'])
                        dst = datetime.now(timezone.utc).strftime(f"%f-{os.path.basename(item['file_path'])}")
                        dst = os.path.join(item['dir_name'], dst)
                        shutil.copyfile(src, dst)

                        jpg_path = Path(dst)
                        png_path = jpg_path.with_suffix(".png")
                        image = Image.open(str(jpg_path))
                        image = await correct_orientation(image)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                            image.save(dst, format="JPEG", quality=15)
                        else:
                            image.save(dst, format="JPEG", quality=55)
                        image = Image.open(str(jpg_path))
                        image = await correct_orientation(image)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                            image.save(str(png_path), format="PNG", quality=15)
                        else:
                            image.save(str(png_path), format="PNG", quality=50)
                        item['file_path'] = png_path

                        async with aiofiles.open(item['file_path'], 'rb') as f:
                            file_content = await f.read()
                        file_content = binascii.hexlify(file_content).decode('utf-8')
                        file_name = os.path.basename(item['file_path'])
                        if os.path.exists(dst): os.remove(dst)
                        if os.path.exists(png_path): os.remove(png_path)
                    else:
                        special_characters = ['\'', '\"', '`', '~', '*', '_', '|', '#', '$', '[', ']', '(', ')', '{',
                                              '}', ';', '<', '>', '@']
                        special_characters += emojis_
                        prompt = item['prompt'].replace('```py\n', '')
                        for char in special_characters: prompt = prompt.replace(char, '')
                        # , in shades of green
                        prompt = f"{prompt[:256]}"

                        if 'lc' in item and item['lc'] != 'en':
                            print('lc != en', item['lc'], prompt)
                            lst = await outsource_generate({'type': 'tl', 'prompt': prompt}, path)
                            prompt = lst[0]['answer']
                            print('prompt after', prompt)

                        prompt = f"{prompt} {extra_prompt}".strip()
                        # prompt = f"{prompt}"
                        file_content = ''
                        file_name = '' if 'file_name' not in item else item['file_name']

                    count = 1 if 'count' not in item else item['count']
                    data_.append({'type': item['type'], 'prompt': prompt, 'count': count, 'file_name': file_name,
                                  'file_content': file_content})
                elif item['type'] == 'tts':
                    prompt = item['prompt'][:4095]
                    lc = 'en' if 'lc' not in item else item['lc']
                    dir_name = '' if 'dir_name' not in item else item['dir_name']

                    # special_characters = ['\'', '\"', '`', '~', '*', '_', '|', '#', '$', '[', ']', '(', ')', '{',
                    #                       '}', ';', '<', '>', '@']
                    # special_characters += emojis_
                    # for char in special_characters: prompt = prompt.replace(char, '')

                    data_.append({'type': item['type'], 'prompt': prompt, 'lc': lc, 'dir_name': dir_name})
                elif item['type'] == 'stt':
                    async with aiofiles.open(item['prompt'], 'rb') as f:
                        file_content = await f.read()
                    file_content_hex = binascii.hexlify(file_content).decode('utf-8')
                    lc = '' if 'lc' not in item else item['lc']

                    data_.append({'type': item['type'], 'prompt': file_content_hex, 'lc': lc})
                elif item['type'] == 'tl':
                    prompt = item['prompt']
                    lc = 'en' if 'lc' not in item else item['lc']

                    if isinstance(prompt, str):
                        # prompt = [{"role": "system", "content": 'You are a helpful translator'}, {"role": "user", "content": f"Translate the following text (to `{lc}`-ISO language code, send me only translations without quotes, colon, explanations. Only translation whithout prefix 'The translation of'), but do not remove tags: {prompt}"}]
                        # prompt = [
                        #     {"role": "system", "content": "You are a helpful translator"},
                        #     {"role": "user",
                        #      "content": f"Translate the following text to the language with ISO code `{lc}`, keep tags, output only translation without quotes, colons, or explanations: {prompt}"}
                        # ]
                        # prompt = [
                        #     {"role": "system",
                        #      "content": "You are a precise translator. Always preserve all tags, symbols, and formatting."},
                        #     {"role": "user",
                        #      "content": f"Translate the following text to the language with ISO code `{lc}`. Keep all tags, symbols, and formatting unchanged. Output only the translation: {prompt}"}
                        # ]

                        if lc in ['en', 'zh', 'es', 'ar', 'ru', 'fr']:
                            lang_map = {
                                "en": "English",
                                "zh": "Chinese",
                                "es": "Spanish",
                                "ar": "Arabic",
                                "ru": "Russian",
                                "fr": "French",
                            }
                            prompt = [
                                {"role": "system",
                                 "content": "You are a precise translator. Keep all tags, symbols, and formatting, only output, without explanations"},
                                {"role": "user",
                                 "content": f"Translate text to {lang_map[lc]} language: {prompt}"}
                            ]
                        else:
                            prompt = [
                                {"role": "system",
                                 "content": "You are a precise translator. Always preserve all tags, symbols, and formatting."},
                                {"role": "user",
                                 "content": f"Translate the following text to the language with ISO code `{lc}`. Keep all tags, symbols, and formatting unchanged. Output only the translation: {prompt}"}
                            ]

                    data_.append({'type': item['type'], 'prompt': prompt, 'lc': lc})
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        if data_[0]['type'] not in ['stt']: print(f"{data_=}")
        print(f"{path=}")
        if str(path).startswith('http'):
            timeout = aiohttp.ClientTimeout(total=6 * 60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url=path, json={'lst': data_}) as response:
                    resp = await response.read()
                    result = json.loads(resp.decode('utf-8'))['lst']

                    for i in range(len(result)):
                        if result[i]['type'] == 'tts':
                            file_content_binary = binascii.unhexlify(result[i]['answer'])
                            dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.mp3")
                            dst_mp3 = os.path.join(result['dir_name'], dt_)

                            async with aiofiles.open(dst_mp3, 'wb') as f:
                                await f.write(file_content_binary)
                            result[i] = {'type': result[i]['type'], 'answer': dst_mp3}
        else:
            for item in data_:
                try:
                    if item['type'] not in ['stt', 'tgph']: print(log_ % f"{str(item)}")

                    if item['type'] == 'tgph':
                        if item['extra'] == 'link_path':
                            async with aiohttp.ClientSession() as session:
                                async with session.get(item['prompt']) as response:
                                    resp = await response.read()
                                    ext = item['prompt'].rsplit('.', 1)[-1] if '.' in item['prompt'] else 'jpg'
                                    file_path = datetime.now(timezone.utc).strftime(f"%d-%m-%Y_%H-%M-%S-%f.{ext}")

                                    async with aiofiles.open(file_path, 'wb') as f:
                                        await f.write(resp)
                        else:
                            file_content_binary = binascii.unhexlify(item['prompt'])
                            file_path = f"{round(time.time())}-{item['file_name']}"

                            async with aiofiles.open(file_path, 'wb') as f:
                                await f.write(file_content_binary)

                        try:
                            cnt = 2
                            while cnt >= 0:
                                try:
                                    res = await Telegraph().upload_file(file_path)
                                    result.append(
                                        {'type': item['type'], 'answer': f"https://telegra.ph{res[0]['src']}"})
                                    break
                                except Exception as e:
                                    logger.info(log_ % str(e))
                                    await asyncio.sleep(round(random.uniform(6, 11), 2))
                                finally:
                                    cnt -= 1
                        finally:
                            if os.path.exists(file_path): os.remove(file_path)
                    elif item['type'] == 'txt':
                        is_res = False
                        # prompt = item['prompt']

                        providers = await get_neuro_keys(path, "text")
                        for provider_name, provider_keys in providers.items():
                            for api_key in provider_keys:
                                try:
                                    print(f"{provider_name}: {api_key}")

                                    if provider_name == 'proxyapi':
                                        base_url = "https://api.proxyapi.ru/openai/v1"
                                        client = AsyncOpenAI(api_key=api_key, base_url=base_url)

                                        if str(api_key).endswith("Lg7I"):
                                            model_ = "gpt-3.5-turbo"
                                        else:
                                            model_ = "gpt-4o-mini"

                                        res = await client.chat.completions.create(model=model_,  # "gpt-3.5-turbo"
                                                                                   messages=item['prompt'],
                                                                                   max_tokens=2400, stream=False)
                                        result.append({'type': item['type'], 'answer': res.choices[0].message.content})
                                        is_res = True
                                        break
                                except Exception as e:
                                    logger.info(log_ % f"{api_key} " + str(e))
                                    # await asyncio.sleep(round(random.uniform(3, 4), 2))

                        print(f"{isinstance(item['prompt'], list)}")
                        if not is_res:
                            res = await g4f_chat_completion(item['prompt'])
                            if res:
                                result.append({'type': item['type'], 'answer': res})
                                print(f"g4f: {res}")
                    elif item['type'] == 'img':
                        providers = await get_neuro_keys(path, "image")
                        for provider_name, provider_keys in providers.items():
                            for api_key in provider_keys:
                                try:
                                    print(f"{provider_name}: {api_key}")

                                    if provider_name == 'prodia':
                                        url = 'https://api.prodia.com/v1/sdxl/generate'
                                        payload = {"prompt": item['prompt']}
                                        headers = {"accept": "application/json", "content-type": "application/json",
                                                   "X-Prodia-Key": api_key}

                                        async with aiohttp.ClientSession() as session:
                                            async with session.post(url, json=payload, headers=headers) as response:
                                                res = await response.json()
                                                job_id = res['job']

                                            attempts = 5
                                            url = f'https://api.prodia.com/v1/job/{job_id}'
                                            await asyncio.sleep(1)
                                            while attempts > 0:
                                                async with session.get(url, headers=headers) as response:
                                                    res = await response.json()
                                                    status = res['status']
                                                    if status.lower() == 'succeeded':
                                                        result.append({'type': item['type'], 'answer': res['imageUrl']})
                                                        return
                                                attempts -= 1
                                                await asyncio.sleep(3)
                                    elif provider_name == 'monster':
                                        url = 'https://api.monsterapi.ai/v1/generate/sdxl-base'
                                        payload = {"enhance": False, "optimize": False, "safe_filter": True,
                                                   "prompt": item['prompt']}
                                        headers = {"accept": "application/json", "content-type": "application/json",
                                                   "authorization": f'Bearer {api_key}'}

                                        async with aiohttp.ClientSession() as session:
                                            async with session.post(url, json=payload, headers=headers) as response:
                                                res = await response.json()
                                                job_id = res['process_id']

                                            attempts = 5
                                            url = f'https://api.monsterapi.ai/v1/status/{job_id}'
                                            await asyncio.sleep(2)

                                            while attempts > 0:
                                                async with session.get(url, headers=headers) as response:
                                                    res = await response.json()
                                                    status = res['status']
                                                    if status.lower() == 'completed':
                                                        result.append({'type': item['type'],
                                                                       'answer': res['result']['output'][0]})
                                                        return
                                                attempts -= 1
                                                await asyncio.sleep(3)
                                    elif provider_name == 'stablehorde':
                                        url = 'https://stablehorde.net/api/v2/generate/async'
                                        payload = {
                                            "prompt": item['prompt'],
                                            "params": {
                                                "width": 512,
                                                "height": 512,
                                                "cfg_scale": 10,
                                                "sampler_name": "k_euler_a"  # k_euler, k_lms, k_dpmpp_sde
                                            }
                                        }
                                        headers = {
                                            "Content-Type": "application/json",
                                            "apikey": api_key
                                        }

                                        async with aiohttp.ClientSession() as session:
                                            print("Отправка запроса на генерацию изображения...")
                                            async with session.post(url, json=payload, headers=headers) as response:
                                                res = await response.json()
                                                job_id = res.get("id")
                                                if not job_id:
                                                    print("Ошибка: Job ID не получен")
                                                    return

                                                print(f"Задача принята, Job ID: {job_id}")

                                            attempts = 7
                                            status_url = f'https://stablehorde.net/api/v2/generate/status/{job_id}'
                                            await asyncio.sleep(3)

                                            while attempts > 0:
                                                async with session.get(status_url, headers=headers) as response:
                                                    res = await response.json()
                                                    print(f"Статус задачи: {res}")

                                                    queue_position = res.get("queue_position", "неизвестно")
                                                    wait_time = res.get("wait_time", "неизвестно")
                                                    print(
                                                        f"Позиция в очереди: {queue_position}, ожидаемое время: {wait_time} сек.")

                                                    if "generations" in res and res["generations"]:
                                                        r_img = res["generations"][0]["img"]
                                                        if str(r_img).endswith('.png'):
                                                            r_img = f"{r_img}.png"

                                                        print(f"Изображение готово: {r_img}")
                                                        result.append({'type': item['type'], 'answer': r_img})
                                                        return

                                                attempts -= 1
                                                print(f"Попытка {7 - attempts} не удалась, ждем 4 секунды...")
                                                await asyncio.sleep(4)

                                            print("Все попытки исчерпаны, изображение не было получено.")
                                    elif provider_name == 'fusionbrain':
                                        # continue
                                        api_key = provider_keys[0]["API_KEY"]
                                        secret_key = provider_keys[0]["SECRET_KEY"]

                                        url_ = 'https://api-key.fusionbrain.ai/key/api/v1/'
                                        headers = {
                                            'X-Key': f'Key {api_key}',
                                            'X-Secret': f'Secret {secret_key}',
                                        }

                                        # модели res=[{'id': 4, 'name': 'Kandinsky', 'version': 3.1,}]
                                        # async with aiohttp.ClientSession() as session:
                                        #     async with session.get(url + 'models', headers=headers) as response:
                                        #         res = await response.json()
                                        #         print(f"модели {res=}")
                                        #         model_id = res[0]['id']

                                        model_id = 4
                                        payload = {
                                            "type": "GENERATE",
                                            "numImages": 1,
                                            # "width": 1024,
                                            # "height": 1024,
                                            "width": 512,
                                            "height": 512,
                                            "generateParams": {"query": item['prompt']}
                                        }
                                        data = FormData()
                                        data.add_field('model_id', str(model_id))
                                        data.add_field('params', json.dumps(payload), content_type='application/json')
                                        async with aiohttp.ClientSession() as session:
                                            u_ = url_ + 'text2image/run'
                                            async with session.post(u_, headers=headers, data=data) as response:
                                                res = await response.json()
                                                if 'uuid' not in res:
                                                    print("Ошибка: в ответе нет 'uuid'", res)
                                                    return
                                                job_id = res['uuid']

                                        # Проверяем статус генерации
                                        attempts = 15
                                        status_url = url_ + f'text2image/status/{job_id}'
                                        await asyncio.sleep(10)

                                        while attempts > 0:
                                            async with aiohttp.ClientSession() as session:
                                                async with session.get(status_url, headers=headers) as response:
                                                    res = await response.json()
                                                    if res['status'].lower() == 'done':
                                                        base64_img = res['images'][0]  # Получаем base64 картинку
                                                        result.append({'type': item['type'], 'answer': base64_img})
                                                        return
                                            attempts -= 1
                                            await asyncio.sleep(3)
                                    elif provider_name == 'huggingface':
                                        url = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2'
                                        payload = {"inputs": item['prompt']}
                                        headers = {"Authorization": f"Bearer {api_key}",
                                                   "Content-Type": "application/json"}

                                        async with aiohttp.ClientSession() as session:
                                            async with session.post(url, json=payload, headers=headers) as response:
                                                if response.status == 200:
                                                    buffer = io.BytesIO()
                                                    async for chunk in response.content.iter_chunked(1024):
                                                        buffer.write(chunk)

                                                    buffer.seek(0)
                                                    encoded_image = base64.b64encode(buffer.read()).decode()

                                                    result.append({'type': item['type'], 'answer': encoded_image})
                                                    return
                                    elif provider_name == 'proxyapi':
                                        base_url = "https://api.proxyapi.ru/openai/v1"
                                        client = AsyncOpenAI(api_key="sk-dR9xp1ei1uciIMd2ZPb3tdY8piZ4ICnn",
                                                             base_url=base_url)

                                        res = await client.images.generate(prompt=item['prompt'],
                                                                           model=f"dall-e-2",
                                                                           n=1,  # max 1 for dalle-3
                                                                           quality="standard",
                                                                           response_format='url',
                                                                           # size="1024x1024",
                                                                           # size="512x512",
                                                                           size="256x256",
                                                                           )
                                        for it in res.data:
                                            result.append({'type': item['type'], 'answer': it.url})
                                            return
                                except Exception as e:
                                    logger.info(log_ % f"{api_key} " + str(e))
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))
                    elif item['type'] == 'tts':
                        dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.mp3")
                        dst_mp3 = os.path.join(item['dir_name'], dt_)
                        input_ = str(item['prompt'].replace('```py\n', ''))
                        input_ = re.sub(r'<[^>]+>', '', input_)
                        print(f"======================================")
                        print(f"{input_=}")

                        providers = await get_neuro_keys(path, "tts")
                        for provider_name, provider_keys in providers.items():
                            for api_key in provider_keys:
                                try:
                                    print(f"{provider_name}: {api_key}")

                                    if provider_name == 'elevenlabs':
                                        headers = {"Accept": "application/json", "Content-Type": "application/json",
                                                   "xi-api-key": api_key, }
                                        data = {"text": input_, "model_id": "eleven_multilingual_v2",
                                                "voice_settings": {"stability": 0.5, "similarity_boost": 0.8,
                                                                   "style": 0.0,
                                                                   "use_speaker_boost": True}}
                                        voices = {'Charlotte': 'XB0fDUnXU5powFXDhCwa',
                                                  'Dorothy': 'ThT5KcBeYPX3keUQqHPh', 'Emily': 'LcfcDJNUP1GQjkzn1xUU',
                                                  'Glinda': 'z9fAnlkpzviPz146aGWa', 'Lily': 'pFZP5JQG7iQjIQuC4Bku',
                                                  'Nicole': 'piTKgcLEGmPE4e6mEKli'}
                                        voice_id = random.choice(list(voices.values()))
                                        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
                                        async with aiohttp.ClientSession() as session:
                                            async with session.post(url, headers=headers, json=data) as response:
                                                async with aiofiles.open(dst_mp3, "wb") as f:
                                                    async for chunk in response.content.iter_chunked(1024):
                                                        chunk: bytes
                                                        await f.write(chunk)
                                    elif provider_name == 'openai':
                                        base_url = "https://api.proxyapi.ru/openai/v1"
                                        client = AsyncOpenAI(api_key=api_key, base_url=base_url)

                                        response = await client.audio.speech.create(
                                            model="tts-1",
                                            input=input_,
                                            voice=random.choice(['alloy', 'shimmer'])
                                        )
                                        try:
                                            response.stream_to_file(dst_mp3)
                                        except:
                                            try:
                                                audio_data = await response.aread()
                                                async with aiofiles.open(dst_mp3, "wb") as f:
                                                    await f.write(audio_data)
                                            except:
                                                pass
                                    elif provider_name == 'polly':
                                        access_key_id = provider_keys[0]["access_key_id"]
                                        secret_access_key = provider_keys[0]["secret_access_key"]

                                        async with (aioboto3.Session().client("polly",
                                                                              region_name="us-east-1",
                                                                              aws_access_key_id=access_key_id,
                                                                              aws_secret_access_key=secret_access_key)
                                                    as polly):

                                            print(f"{item['lc']=}")
                                            names = {
                                                'ar': ['Hala', 'Zayd', 'Zeina'],
                                                'ca': ['Arlet'],
                                                'da': ['Naja', 'Mads'],
                                                'de': ['Vicki', 'Daniel'],
                                                'en': ['Olivia', 'Amy', 'Danielle', 'Joanna', 'Stephen', 'Ruth',
                                                       'Matthew'],
                                                'es': ['Lucia', 'Sergio', 'Mia', 'Lupe', 'Pedro'],
                                                'fi': ['Suvi'],
                                                'fr': ['Lea', 'Remi'],
                                                'hi': ['Kajal'],
                                                'it': ['Bianca'],
                                                'ja': ['Takumi', 'Kazuha', 'Tomoko'],
                                                'ko': ['Seoyeon'],
                                                'nb': ['Ida'],
                                                'nl': ['Laura', 'Lisa'],
                                                'pl': ['Ola'],
                                                'pt': ['Camila', 'Thiago'],
                                                'ro': ['Carmen'],
                                                'ru': ['Maxim', 'Tatyana'],
                                                'sv': ['Elin'],
                                                'tr': ['Filiz'],
                                                'zh': ['Hiujin', 'Zhiyu'],
                                            }
                                            voice_list = names.get(item['lc'], names['en'])
                                            print(f"{voice_list=}")
                                            VoiceId = random.choice(voice_list)
                                            # VoiceId = 'Lea'
                                            print(f"{VoiceId=}")

                                            response = await polly.synthesize_speech(
                                                Text=input_,
                                                OutputFormat="mp3",
                                                VoiceId=VoiceId
                                                # LanguageCode="ru-RU"
                                            )
                                            async with aiofiles.open(dst_mp3, "wb") as f:
                                                await f.write(await response["AudioStream"].read())
                                    elif provider_name == 'hume':
                                        access_key_id = provider_keys[0]["access_key_id"]
                                        secret_access_key = provider_keys[0]["secret_access_key"]

                                        token = await get_access_token_hume(access_key_id, secret_access_key)
                                        print(f"{token=}")
                                        if not token: continue

                                        url = "https://api.hume.ai/v0/tts"
                                        headers = {
                                            "Content-Type": "application/json",
                                            "Authorization": f"Bearer {token}"
                                        }
                                        data = {
                                            "utterances": [
                                                {
                                                    "text": input_,
                                                    "description": "A friendly and professional voice"
                                                }
                                            ]
                                        }

                                        print(f"start hume post")
                                        async with aiohttp.ClientSession() as session:
                                            async with session.post(url, headers=headers, json=data) as resp:
                                                response_json = await resp.json()
                                                audio_base64 = response_json["generations"][0]["audio"]
                                                audio_data = base64.b64decode(audio_base64)
                                                async with aiofiles.open(dst_mp3, "wb") as f:
                                                    await f.write(audio_data)
                                    elif provider_name == 'proxyapi':
                                        base_url = "https://api.proxyapi.ru/openai/v1"
                                        client = AsyncOpenAI(api_key=api_key, base_url=base_url)

                                        response = await client.audio.speech.create(
                                            model="tts-1",
                                            input=input_,
                                            voice=random.choice(['alloy', 'shimmer'])
                                        )

                                        audio_data = await response.aread()
                                        async with aiofiles.open(dst_mp3, "wb") as f:
                                            await f.write(audio_data)

                                    print(f"{dst_mp3=}")
                                    print(f"{os.path.getsize(dst_mp3)=}")
                                    print(f"{os.path.exists(dst_mp3)=}")

                                    if os.path.exists(dst_mp3) and os.path.getsize(dst_mp3):
                                        result.append({'type': item['type'], 'answer': dst_mp3})
                                        return
                                except Exception as e:
                                    logger.info(log_ % str(e))
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))

                        special_characters = ['\'', '\"', '`', '~', '*', '_', '|', '#', '$', '[', ']', '(', ')', '{',
                                              '}', ':', ';', '<', '>', '@', '-', '+', '=']
                        special_characters += emojis_
                        tmp_text = item['prompt'].replace('```py\n', '')
                        for char in special_characters: tmp_text = tmp_text.replace(char, '')
                        gTTS(text=tmp_text, lang=item['lc'], slow=False).save(dst_mp3)

                        result.append(
                            {'type': item['type'], 'answer': dst_mp3})  # if os.path.exists(dst_mp3): os.remove(dst_mp3)
                    elif item['type'] == 'stt':
                        is_res = False
                        res = None
                        text = ''
                        dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.mp3")
                        src_mp3 = os.path.abspath(os.path.join(os.path.dirname(__file__), dt_))
                        dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.wav")
                        file_wav = os.path.abspath(os.path.join(os.path.dirname(__file__), dt_))
                        file_content_binary = binascii.unhexlify(item['prompt'])

                        try:
                            async with aiofiles.open(src_mp3, 'wb') as f:
                                await f.write(file_content_binary)

                            providers = await get_neuro_keys(path, "text")
                            for provider_name, provider_keys in providers.items():
                                for api_key in provider_keys:
                                    try:
                                        print(f"{provider_name}: {api_key}")

                                        if provider_name == 'proxyapi':
                                            base_url = "https://api.proxyapi.ru/openai/v1"
                                            client = AsyncOpenAI(api_key=api_key, base_url=base_url)

                                            res = await client.audio.transcriptions.create(model="whisper-1",
                                                                                           file=open(src_mp3, "rb"))

                                            result.append({'type': item['type'], 'answer': res.text})
                                            is_res = True
                                            break
                                    except Exception as e:
                                        logger.info(log_ % f"{api_key} " + str(e))
                                        await asyncio.sleep(round(random.uniform(3, 4), 2))

                            if not res:
                                cnt = 1
                                while cnt >= 0:
                                    url = 'http://185.203.119.249:8000/transcribe/'
                                    try:
                                        async with aiohttp.ClientSession() as session:
                                            async with session.post(url,
                                                                    data={'file': open(src_mp3, "rb")}) as response:
                                                res = await response.json()
                                                text = res['text']
                                        is_res = True
                                        break
                                    except Exception as e:
                                        logger.info(log_ % str(e))
                                        await asyncio.sleep(round(random.uniform(3, 4), 2))
                                    finally:
                                        cnt -= 1

                            if not is_res:
                                print('not is_res (stt)')
                                ext = src_mp3.split('.')[-1]
                                recognizer = sr.Recognizer()

                                try:
                                    if ext == 'mp3':
                                        audio = AudioSegment.from_mp3(src_mp3)
                                    elif ext == 'ogg':
                                        audio = AudioSegment.from_ogg(src_mp3)
                                    else:
                                        audio = AudioSegment.from_file(src_mp3, format=ext)
                                    audio.export(file_wav, format="wav")
                                except:
                                    video_clip = VideoFileClip(src_mp3)
                                    audio_clip = video_clip.audio
                                    audio_clip.write_audiofile(file_wav, codec='pcm_s16le')
                                    audio_clip.close()
                                    video_clip.close()

                                with sr.AudioFile(file_wav) as source:
                                    try:
                                        print(f"sr.AudioFile(file_wav)")
                                        recognizer.adjust_for_ambient_noise(source)
                                        audio_data = recognizer.record(source)
                                        text = recognizer.recognize_google(audio_data, language=item['lc'])
                                        print(f"{text=}")
                                    except Exception as e:
                                        logger.info(log_ % str(e))
                                        await asyncio.sleep(round(random.uniform(0, 1), 2))

                            result.append({'type': item['type'], 'answer': str(text).rstrip('.').strip()})
                        finally:
                            if src_mp3 and os.path.exists(src_mp3): os.remove(src_mp3)
                            if file_wav and os.path.exists(file_wav): os.remove(file_wav)
                    elif item['type'] == 'tl':
                        is_res = False

                        providers = await get_neuro_keys(path, "text")
                        for provider_name, provider_keys in providers.items():
                            for api_key in provider_keys:
                                try:
                                    print(f"{provider_name}: {api_key}")

                                    if provider_name == 'proxyapi':
                                        base_url = "https://api.proxyapi.ru/openai/v1"
                                        client = AsyncOpenAI(api_key=api_key, base_url=base_url)

                                        if str(api_key).endswith("Lg7I"):
                                            model_ = "gpt-3.5-turbo"
                                        else:
                                            model_ = "gpt-4o-mini"

                                        res = await client.chat.completions.create(model=model_,
                                                                                   messages=item['prompt'],
                                                                                   max_tokens=1200, stream=False)
                                        r_a = res.choices[0].message.content
                                        r_a = str(r_a).lstrip('`').rstrip('`').strip()
                                        result.append({'type': item['type'], 'answer': r_a})
                                        is_res = True
                                        break
                                except Exception as e:
                                    logger.info(log_ % f"{api_key} " + str(e))
                                    # await asyncio.sleep(round(random.uniform(3, 4), 2))

                        if not is_res:
                            res = await g4f_chat_completion(item['prompt'])
                            if res:
                                result.append({'type': item['type'], 'answer': res})
                except Exception as e:
                    logger.info(log_ % str(e))  # await asyncio.sleep(round(random.uniform(0, 1), 2))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_neuro_keys(file_path, type_="image"):
    result = None
    try:
        async with aiofiles.open(file_path, 'r') as file:
            content = await file.read()
            data = json.loads(content)
            result = data[type_]
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def outsource_handle_old(lst, path='link_path'):
    result = []
    try:
        data_ = []
        if isinstance(lst, dict): lst = [lst]

        for item in lst:
            try:
                if item['type'] == 'tgph':
                    file_path = item['prompt']

                    if not item['prompt'].startswith('https://'):
                        if os.path.getsize(file_path) > 5242880: continue
                        ext = str(file_path[file_path.rfind('.'):]).lower()
                        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']: continue

                        async with aiofiles.open(file_path, 'rb') as f:
                            file_content = await f.read()

                        file_content_hex = binascii.hexlify(file_content).decode('utf-8')
                        file_name = os.path.basename(file_path)
                        data_.append({'type': item['type'], 'prompt': file_content_hex, 'extra': 'file_path',
                                      'file_name': file_name})
                    else:
                        data_.append({'type': item['type'], 'prompt': item['prompt'], 'extra': 'link_path'})
                elif item['type'] == 'txt':
                    prompt = str(item['prompt']).strip()

                    if isinstance(prompt, str):
                        prompt = [{"role": "system", "content": 'You are a helpful assistant for Telegram'},
                                  {"role": "user", "content": prompt}]

                    data_.append({'type': item['type'], 'prompt': prompt})
                elif item['type'] == 'img':
                    if item['prompt'] == 'variation':
                        prompt = item['prompt']
                        ext = str(item['file_path'][item['file_path'].rfind('.'):]).lower()
                        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.mp4']: continue
                        if os.path.getsize(item['file_path']) > 5242880: continue

                        src = os.path.join(item['dir_name'], item['file_path'])
                        dst = datetime.now(timezone.utc).strftime(f"%f-{os.path.basename(item['file_path'])}")
                        dst = os.path.join(item['dir_name'], dst)
                        shutil.copyfile(src, dst)

                        jpg_path = Path(dst)
                        png_path = jpg_path.with_suffix(".png")
                        image = Image.open(str(jpg_path))
                        image = await correct_orientation(image)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                            image.save(dst, format="JPEG", quality=15)
                        else:
                            image.save(dst, format="JPEG", quality=55)
                        image = Image.open(str(jpg_path))
                        image = await correct_orientation(image)
                        if image.mode != 'RGB':
                            image = image.convert('RGB')
                            image.save(str(png_path), format="PNG", quality=15)
                        else:
                            image.save(str(png_path), format="PNG", quality=50)
                        item['file_path'] = png_path

                        async with aiofiles.open(item['file_path'], 'rb') as f:
                            file_content = await f.read()
                        file_content = binascii.hexlify(file_content).decode('utf-8')
                        file_name = os.path.basename(item['file_path'])
                        if os.path.exists(dst): os.remove(dst)
                        if os.path.exists(png_path): os.remove(png_path)
                    else:
                        special_characters = ['\'', '\"', '`', '~', '*', '_', '|', '#', '$', '[', ']', '(', ')', '{',
                                              '}', ';', '<', '>', '@']
                        special_characters += emojis_
                        prompt = item['prompt'].replace('```py\n', '')
                        for char in special_characters: prompt = prompt.replace(char, '')
                        # , in shades of green
                        prompt = f"{prompt[:512]} {extra_prompt}"

                        file_content = ''
                        file_name = '' if 'file_name' not in item else item['file_name']

                    count = 1 if 'count' not in item else item['count']
                    data_.append({'type': item['type'], 'prompt': prompt, 'count': count, 'file_name': file_name,
                                  'file_content': file_content})
                elif item['type'] == 'tts':
                    prompt = str(item['prompt'][:4095]).strip()
                    lc = 'en' if 'lc' not in item else item['lc']
                    dir_name = '' if 'dir_name' not in item else item['dir_name']

                    data_.append({'type': item['type'], 'prompt': prompt, 'lc': lc, 'dir_name': dir_name})
                elif item['type'] == 'stt':
                    async with aiofiles.open(item['prompt'], 'rb') as f:
                        file_content = await f.read()
                    file_content_hex = binascii.hexlify(file_content).decode('utf-8')
                    lc = '' if 'lc' not in item else item['lc']

                    data_.append({'type': item['type'], 'prompt': file_content_hex, 'lc': lc})
                elif item['type'] == 'tl':
                    prompt = str(item['prompt']).strip()
                    lc = 'en' if 'lc' not in item else item['lc']

                    if isinstance(prompt, str):
                        prompt = [{"role": "system", "content": 'You are a helpful translator'}, {"role": "user",
                                                                                                  "content": f"Translate the following text (to `{lc}`-ISO language code, send me only translations without quotes, colon, explanations. Only translation whithout prefix 'The translation of'): {prompt}"}]

                    data_.append({'type': item['type'], 'prompt': prompt, 'lc': lc})
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        if str(path).startswith('http'):
            timeout = aiohttp.ClientTimeout(total=6 * 60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url=path, json={'lst': data_}) as response:
                    resp = await response.read()
                    result = json.loads(resp.decode('utf-8'))['lst']

                    for i in range(len(result)):
                        if result[i]['type'] == 'tts':
                            file_content_binary = binascii.unhexlify(result[i]['answer'])
                            dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.mp3")
                            dst_mp3 = os.path.join(result['dir_name'], dt_)

                            async with aiofiles.open(dst_mp3, 'wb') as f:
                                await f.write(file_content_binary)
                            result[i] = {'type': result[i]['type'], 'answer': dst_mp3}
        else:
            for item in data_:
                try:
                    if item['type'] not in ['stt', 'tgph']: print(log_ % f"{str(item)}")

                    if item['type'] == 'tgph':
                        if item['extra'] == 'link_path':
                            async with aiohttp.ClientSession() as session:
                                async with session.get(item['prompt']) as response:
                                    resp = await response.read()
                                    ext = item['prompt'].rsplit('.', 1)[-1] if '.' in item['prompt'] else 'jpg'
                                    file_path = datetime.now(timezone.utc).strftime(f"%d-%m-%Y_%H-%M-%S-%f.{ext}")

                                    async with aiofiles.open(file_path, 'wb') as f:
                                        await f.write(resp)
                        else:
                            file_content_binary = binascii.unhexlify(item['prompt'])
                            file_path = f"{round(time.time())}-{item['file_name']}"

                            async with aiofiles.open(file_path, 'wb') as f:
                                await f.write(file_content_binary)

                        try:
                            cnt = 2
                            while cnt >= 0:
                                try:
                                    res = await Telegraph().upload_file(file_path)
                                    result.append(
                                        {'type': item['type'], 'answer': f"https://telegra.ph{res[0]['src']}"})
                                    break
                                except Exception as e:
                                    logger.info(log_ % str(e))
                                    await asyncio.sleep(round(random.uniform(6, 11), 2))
                                finally:
                                    cnt -= 1
                        finally:
                            if os.path.exists(file_path): os.remove(file_path)
                    elif item['type'] == 'txt':
                        is_res = False
                        # prompt = item['prompt']

                        cnt = 2
                        while cnt >= 0:
                            api_key = await get_openai_key(path)

                            try:
                                if not api_key: break
                                client = AsyncOpenAI(api_key=api_key)
                                res = await client.chat.completions.create(model="gpt-3.5-turbo",
                                                                           messages=item['prompt'], max_tokens=1200,
                                                                           stream=False)
                                result.append({'type': item['type'], 'answer': res.choices[0].message.content})
                                is_res = True
                                break
                            except Exception as e:
                                logger.info(log_ % f"{api_key} " + str(e))
                                if 'billing_hard_limit_reached' in str(e).lower():
                                    await del_openai_key(api_key, path)
                                    if not api_key: break
                                elif 'context_length_exceeded' in str(e).lower():
                                    max_content_element = max(item['prompt'], key=lambda x: len(x["content"]))
                                    # item['prompt'].remove(max_content_element)
                                    item['prompt'] = [x for x in item['prompt'] if x != max_content_element]
                                    await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif str(e).lower().startswith('You exceeded your current quota'):
                                    await asyncio.sleep(round(random.uniform(5, 10), 2))
                                    break
                                elif 'try again in' in str(e).lower():
                                    part_ = str(e).lower().split('try again in')[-1]
                                    time_ = part_.split('.')[0]
                                    if 'm' in time_:
                                        await asyncio.sleep(round(random.uniform(41, 49), 2))
                                    else:
                                        await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'try again' in str(e).lower():
                                    await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'seconds' in str(e).lower() or 'too many' in str(e).lower():
                                    await asyncio.sleep(20)
                                elif 'is not supported' in str(e).lower():
                                    break
                                elif 'rate_limit_exceeded' in str(e).lower():
                                    break  # await asyncio.sleep(round(random.uniform(61, 62), 2))
                                else:
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))
                            finally:
                                cnt -= 1

                        print(f"{isinstance(item['prompt'], list)}")
                        if not is_res:
                            res = await g4f_chat_completion(item['prompt'])
                            if res:
                                result.append({'type': item['type'], 'answer': str(res).strip()})
                                print(f"g4f: {res}")
                    elif item['type'] == 'img':
                        cnt = 1
                        model_num = 3
                        while cnt >= 0:
                            api_key = await get_openai_key(path)
                            try:
                                if not api_key: break
                                client = AsyncOpenAI(api_key=api_key)
                                if item['prompt'] == 'variation':
                                    file_path = f"{round(time.time())}-{item['file_name']}"
                                    file_content = binascii.unhexlify(item['file_content'])
                                    async with aiofiles.open(file_path, 'wb') as f:
                                        await f.write(file_content)

                                    try:
                                        res = await client.images.create_variation(image=open(file_path, "rb"), n=1,
                                                                                   response_format='url',
                                                                                   size="1024x1024")
                                    finally:
                                        if os.path.exists(file_path): os.remove(file_path)
                                else:
                                    res = await client.images.generate(prompt=item['prompt'],
                                                                       model=f"dall-e-{model_num}",
                                                                       n=int(item['count']), quality="standard",
                                                                       response_format='url', size="1024x1024")
                                for it in res.data: result.append({'type': item['type'], 'answer': it.url})
                                break
                            except Exception as e:
                                logger.info(log_ % f"{api_key} " + str(e))
                                if 'billing_hard_limit_reached' in str(e).lower():
                                    await del_openai_key(api_key, path)
                                    if not api_key: break
                                elif str(e).lower().startswith('You exceeded your current quota'):
                                    await asyncio.sleep(round(random.uniform(5, 10), 2))
                                    break
                                elif 'try again in' in str(e).lower():
                                    part_ = str(e).lower().split('try again in')[-1]
                                    time_ = part_.split('.')[0]
                                    if 'm' in time_:
                                        await asyncio.sleep(round(random.uniform(41, 49), 2))
                                    else:
                                        await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'try again' in str(e).lower():
                                    await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'seconds' in str(e).lower() or 'too many' in str(e).lower():
                                    await asyncio.sleep(20)
                                elif 'is not supported' in str(e).lower():
                                    break
                                elif 'rate_limit_exceeded' in str(e).lower():
                                    model_num = 2
                                    print(f'change model = {model_num}')
                                    await asyncio.sleep(round(random.uniform(3, 4),
                                                              2))  # break  # await asyncio.sleep(round(random.uniform(61, 62), 2))
                                else:
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))
                            finally:
                                cnt -= 1
                    elif item['type'] == 'tts':
                        is_res = False

                        dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.mp3")
                        dst_mp3 = os.path.join(item['dir_name'], dt_)

                        cnt = 1
                        while cnt >= 0:
                            api_key = await get_openai_key(path)
                            try:
                                if not api_key: break
                                client = AsyncOpenAI(api_key=api_key)
                                # alloy - между мужчиной и женщиной
                                # echo - дурацкий русский
                                # fable - среднее между alloy и echo
                                # onyx - низкий голос (неплохой)
                                # nova - такая 32 летняя девушка
                                # shimmer - между мужчиной и женщиной
                                input_ = str(item['prompt'].replace('```py\n', ''))
                                print(f"{input_=}")
                                response = await client.audio.speech.create(model='tts-1',
                                                                            voice=random.choice(['alloy', 'shimmer']),
                                                                            input=input_)
                                response.stream_to_file(dst_mp3)
                                # response.with_streaming_response(dst_mp3)
                                is_res = True
                                break
                            except Exception as e:
                                logger.info(log_ % f"{api_key} " + str(e))
                                if 'billing_hard_limit_reached' in str(e).lower():
                                    await del_openai_key(api_key, path)
                                    if not api_key: break
                                elif str(e).lower().startswith('You exceeded your current quota'):
                                    await asyncio.sleep(round(random.uniform(5, 10), 2))
                                    break
                                elif 'try again in' in str(e).lower():
                                    part_ = str(e).lower().split('try again in')[-1]
                                    time_ = part_.split('.')[0]
                                    if 'm' in time_:
                                        await asyncio.sleep(round(random.uniform(41, 49), 2))
                                    else:
                                        await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'try again' in str(e).lower():
                                    await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'seconds' in str(e).lower() or 'too many' in str(e).lower():
                                    await asyncio.sleep(20)
                                elif 'is not supported' in str(e).lower():
                                    break
                                elif 'rate_limit_exceeded' in str(e).lower():
                                    break  # await asyncio.sleep(round(random.uniform(61, 62), 2))
                                else:
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))
                            finally:
                                cnt -= 1

                        if not is_res:
                            special_characters = ['\'', '\"', '`', '~', '*', '_', '|', '#', '$', '[', ']', '(', ')',
                                                  '{', '}', ':', ';', '<', '>', '@', '-', '+', '=']
                            special_characters += emojis_
                            tmp_text = item['prompt'].replace('```py\n', '')
                            for char in special_characters: tmp_text = tmp_text.replace(char, '')
                            gTTS(text=tmp_text, lang=item['lc'], slow=False).save(dst_mp3)

                        result.append(
                            {'type': item['type'], 'answer': dst_mp3})  # if os.path.exists(dst_mp3): os.remove(dst_mp3)
                    elif item['type'] == 'stt':
                        is_res = False
                        text = ''
                        dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.mp3")
                        src_mp3 = os.path.abspath(os.path.join(os.path.dirname(__file__), dt_))
                        dt_ = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S-%f.wav")
                        file_wav = os.path.abspath(os.path.join(os.path.dirname(__file__), dt_))
                        file_content_binary = binascii.unhexlify(item['prompt'])

                        async with aiofiles.open(src_mp3, 'wb') as f:
                            await f.write(file_content_binary)

                        cnt = 1
                        while cnt >= 0:
                            api_key = await get_openai_key(path)
                            try:
                                if not api_key: break
                                client = AsyncOpenAI(api_key=api_key)
                                res = await client.audio.transcriptions.create(model="whisper-1",
                                                                               file=open(src_mp3, "rb"))
                                text = res.text
                                is_res = True
                                break
                            except Exception as e:
                                logger.info(log_ % f"{api_key} " + str(e))
                                if 'billing_hard_limit_reached' in str(e).lower():
                                    await del_openai_key(api_key, path)
                                    if not api_key: break
                                elif str(e).lower().startswith('You exceeded your current quota'):
                                    await asyncio.sleep(round(random.uniform(5, 10), 2))
                                    break
                                elif 'try again in' in str(e).lower():
                                    part_ = str(e).lower().split('try again in')[-1]
                                    time_ = part_.split('.')[0]
                                    if 'm' in time_:
                                        await asyncio.sleep(round(random.uniform(41, 49), 2))
                                    else:
                                        await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'try again' in str(e).lower():
                                    await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'seconds' in str(e).lower() or 'too many' in str(e).lower():
                                    await asyncio.sleep(20)
                                elif 'is not supported' in str(e).lower():
                                    break
                                elif 'rate_limit_exceeded' in str(e).lower():
                                    break  # await asyncio.sleep(round(random.uniform(61, 62), 2))
                                else:
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))
                            finally:
                                cnt -= 1

                        if not is_res:
                            print('not is_res (stt)')
                            ext = src_mp3.split('.')[-1]
                            recognizer = sr.Recognizer()

                            try:
                                if ext == 'mp3':
                                    audio = AudioSegment.from_mp3(src_mp3)
                                elif ext == 'ogg':
                                    audio = AudioSegment.from_ogg(src_mp3)
                                else:
                                    audio = AudioSegment.from_file(src_mp3, format=ext)
                                audio.export(file_wav, format="wav")
                            except:
                                video_clip = VideoFileClip(src_mp3)
                                audio_clip = video_clip.audio
                                audio_clip.write_audiofile(file_wav, codec='pcm_s16le')
                                audio_clip.close()
                                video_clip.close()

                            with sr.AudioFile(file_wav) as source:
                                try:
                                    print(f"sr.AudioFile(file_wav)")
                                    recognizer.adjust_for_ambient_noise(source)
                                    audio_data = recognizer.record(source)
                                    text = recognizer.recognize_google(audio_data, language=item['lc'])
                                    print(f"{text=}")
                                except Exception as e:
                                    logger.info(log_ % str(e))
                                    await asyncio.sleep(round(random.uniform(0, 1), 2))

                        result.append({'type': item['type'], 'answer': str(text).rstrip('.').strip()})
                        if os.path.exists(src_mp3): os.remove(src_mp3)
                        if os.path.exists(file_wav): os.remove(file_wav)
                    elif item['type'] == 'tl':
                        is_res = False

                        cnt = 2
                        while cnt >= 0:
                            api_key = await get_openai_key(path)
                            try:
                                if not api_key: break
                                client = AsyncOpenAI(api_key=api_key)
                                res = await client.chat.completions.create(model="gpt-3.5-turbo",
                                                                           messages=item['prompt'], max_tokens=1200,
                                                                           stream=False)
                                result.append({'type': item['type'], 'answer': res.choices[0].message.content})
                                is_res = True
                                break
                            except Exception as e:
                                logger.info(log_ % f"{api_key} " + str(e))
                                if 'billing_hard_limit_reached' in str(e).lower():
                                    await del_openai_key(api_key, path)
                                    if not api_key: break
                                elif str(e).lower().startswith('You exceeded your current quota'):
                                    await asyncio.sleep(round(random.uniform(5, 10), 2))
                                    break
                                elif 'try again in' in str(e).lower():
                                    part_ = str(e).lower().split('try again in')[-1]
                                    time_ = part_.split('.')[0]
                                    if 'm' in time_:
                                        await asyncio.sleep(round(random.uniform(41, 49), 2))
                                    else:
                                        await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'try again' in str(e).lower():
                                    await asyncio.sleep(round(random.uniform(21, 23), 2))
                                elif 'seconds' in str(e).lower() or 'too many' in str(e).lower():
                                    await asyncio.sleep(20)
                                elif 'is not supported' in str(e).lower():
                                    break
                                elif 'rate_limit_exceeded' in str(e).lower():
                                    break  # await asyncio.sleep(round(random.uniform(61, 62), 2))
                                else:
                                    await asyncio.sleep(round(random.uniform(3, 4), 2))
                            finally:
                                cnt -= 1

                        if not is_res:
                            res = await g4f_chat_completion(item['prompt'])
                            if res:
                                result.append({'type': item['type'], 'answer': res})
                except Exception as e:
                    logger.info(log_ % str(e))  # await asyncio.sleep(round(random.uniform(0, 1), 2))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_grant_balance(key_):
    result = False
    try:
        headers = {"Authorization": f"Bearer {key_}"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get("https://api.openai.com/dashboard/billing/credit_grants") as response:
                bdata = await response.json()

                if 'total_available' in bdata and bdata["total_available"] > 0.01:
                    result = True
                    print(f'{key_}: billing_data = {bdata["total_available"]}$')
                else:
                    print(f'{key_}: key is not valid')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_access_token_hume(API_KEY, SECRET_KEY):
    result = None
    try:
        auth = f"{API_KEY}:{SECRET_KEY}".encode()
        encoded_auth = base64.b64encode(auth).decode()
        url = "https://api.hume.ai/oauth2-cc/token"
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=data) as resp:
                response_text = await resp.text()
                print(f"{response_text=}")
                response_json = json.loads(response_text)
                result = response_json["access_token"]
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


# endregion


# region media
async def delete_from_ipfs(MSG_VID, KEYS_JSON):
    try:
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data_keys = json.loads(await f.read())

        for pinata in data_keys["media"]["pinata"]:
            pinata_secret_key = pinata["SECRET_KEY"]
            pinata_headers = {"Authorization": f"Bearer {pinata_secret_key}"}

            url = "https://api.pinata.cloud/v3/files/public"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=pinata_headers) as response:
                    response_json = await response.json()
                    f_ = response_json.get("data", {}).get("files", [])
                    res_ids = [f["id"] for f in f_ if f.get("keyvalues", {}).get("tid") == MSG_VID]

                    for res_id in res_ids:
                        url_ = f"https://api.pinata.cloud/v3/files/public/{res_id}"
                        async with session.delete(url_, headers=pinata_headers) as resp:
                            await resp.json()
                    if len(res_ids): break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


# endregion


# region blockchain
async def get_address_state_init_by_boc(BOT_CRYPTOPAY_ADDRESS, chkCryptopay=True):
    address_owner_raw = address_contract_friendly = state_init = None

    try:
        if not BOT_CRYPTOPAY_ADDRESS or not chkCryptopay: return
        address_owner = Address(BOT_CRYPTOPAY_ADDRESS)
        address_owner_raw = address_owner.to_str(is_user_friendly=False)

        # boc_base64 = "te6ccgECDQEAAYUAART/APSkE/S88sgLAQIBYgIKAgLOAwkCASAECAL3AHQ0wMBcbCSXwTg+kAwjQWbXlfYmFsYW5jZSAmIG1zZ192YWx1ZYP4UMCP+IDAi/iAwcSOCEHc1lAC+mzACghA7msoAqQQCkTPii7aW5jcmVhc2VfYnmP4UMCL+IDDwAQSgUwPwAot2NvdW50ZXKP4UMP4gMCHHAOMCAYAUGAARfBAHY0x8wIMAAkl8E4Ism9wj+FDAg/iAwIIEDj7qOOTAhxwXy448BggiYloChizOTExj+FDAg/iAwcCCAGMjLBVAEzxZY+gISy2rLH4s2dldIzxbJgwb7AOAzi0aGVyZY/hQwAoEDkLrjAluED/LwBwCOi1aGVyZTKP4UMGbHBfLjkIszkxMo/hQwi6bXlfYmFsYW5jZY/hQwcCCAGMjLBVADzxYh+gISy2rLH4s2RlbIzxbJgQCg+wAAETtRNDTH/pAMIAAVQByMsfAc8Wye1UgCASALDAALvc0vgAmMAAu/j/+ACYQ="
        boc_hex_new = "b5ee9c7241020e01000190000114ff00f4a413f4bcf2c80b0102016202090202ce0308020120040701f7007434c0c05c6c2497c1383e900c234166d795f62616c616e63652026206d73675f76616c756583f850c08bf880c1c48e0841dcd65002fa6cc00a0840ee6b2802a4100a44cf8a2eda5b98dc99585cd957d89e63f850c08bf880c3c00412814c0fc00a2dd8dbdd5b9d195ca3f850c3f880c0871c02497c1380074c7e00501d43020c000925f04e08b26f708fe143020fe20302081038fba8e393021c705f2e38f018208989680a18b33931318fe143020fe203070208018c8cb055004cf1658fa0212cb6acb1f8b36765748cf16c98306fb00e0338b4686572658fe143002810390bae3025b840ff2f006008e8b568657265328fe143066c705f2e3908b33931328fe14308ba6d795f62616c616e63658fe143070208018c8cb055003cf1621fa0212cb6acb1f8b364656c8cf16c98100a0fb0000113b513434c7fe900c200015401c8cb1f01cf16c9ed5480201200a0b000bbdcd2f80098c0201200c0d0015ba5e1f00130f8276f22308000bbb1fff001308277727cc"
        code = Cell.one_from_boc(boc_hex_new)
        data = begin_cell().store_uint(0, 32).store_address(address_owner).end_cell()
        state_init_cell = StateInit(code=code, data=data)
        addr = Address((0, state_init_cell.serialize().hash))
        address_contract_friendly = addr.to_str(is_user_friendly=True, is_url_safe=True)
        state_init = base64.b64encode(state_init_cell.serialize().to_boc()).decode('utf-8')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return address_owner_raw, address_contract_friendly, state_init


async def get_nft_info(nft_address):
    owner_addr = collection_addr = None
    try:
        item1 = ['tonapi', f'https://tonapi.io/v2/nfts/{nft_address}', {'accept': 'application/json',
                                                                        'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        item2 = ['toncenter', f'https://toncenter.com/api/v3/nft/items?address={nft_address}',
                 {'accept': 'application/json',
                  'X-API-Key': 'f5739745a824c8e8d49fb61beeab095786357b76a989c7fad7462afe57fcd970'}]
        items = [item2, item1]

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=headers) as response:
                            response.raise_for_status()
                            data = await response.json()

                    print(f"{name=}, ")
                    if name == 'tonapi':
                        owner_addr = data['owner']['address']
                        collection_addr = data['collection']['address']
                    else:
                        #  elif name == 'toncenter'
                        owner_addr = data['nft_items'][0]['owner_address'].lower()
                        collection_addr = data['nft_items'][0]['collection_address'].lower()

                    await asyncio.sleep(1)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return owner_addr, collection_addr


async def get_wallet_addres(address, currency):
    result = ""
    try:
        item1 = ['tonapi', f'https://tonapi.io/v2/accounts/{address}/jettons', {'accept': 'application/json',
                                                                                'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        # item2 = ['toncenter',
        #          f'https://toncenter.com/api/v3/jetton/wallets?owner_address={address}&limit=256&offset=0',
        #          {
        #              'accept': 'application/json',
        #              'X-API-Key': 'f5739745a824c8e8d49fb61beeab095786357b76a989c7fad7462afe57fcd970'
        #          }]
        items = [item1]

        while True:
            # random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=headers) as response:
                            response.raise_for_status()
                            data = await response.json()

                    if name == 'tonapi':
                        arr = [it['wallet_address']['address'] for it in data['balances'] if
                               it['jetton']['symbol'] == currency]
                        print(f"{arr=}")
                        if len(arr):
                            result = arr[0]
                    else:
                        #  if name == 'toncenter'
                        pass

                    await asyncio.sleep(1)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def to_txt_cell(txt):
    result = begin_cell().end_cell()
    try:
        result = begin_cell().store_uint(0, 8).store_snake_string(txt).end_cell()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def uri_metadata(url, result):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data_json = await response.json()

                if 'name' in data_json:
                    result['name'] = data_json['name']
                if 'description' in data_json:
                    result['description'] = data_json['description']
                if 'image' in data_json:
                    result['image'] = data_json['image']
                if 'image_data' in data_json:
                    result['image_data'] = data_json['image_data']
                if 'cover_image' in data_json:
                    result['image'] = data_json['cover_image']
                if 'content_url' in data_json:
                    result['content_url'] = data_json['content_url']

                if 'social_links' in data_json:
                    result['social_links'] = data_json['social_links']
                if 'social' in data_json:
                    result['social_links'] = data_json['social']
                if 'links' in data_json:
                    result['social_links'] = data_json['links']
                if 'websites' in data_json:
                    result['social_links'] = data_json['websites']
                if 'attributes' in data_json:
                    result['attributes'] = data_json['attributes']

                if 'symbol' in data_json:
                    result['symbol'] = data_json['symbol']
                if 'decimals' in data_json:
                    result['decimals'] = data_json['decimals']
                if 'marketplace' in data_json:
                    result['marketplace'] = data_json['marketplace']
                if 'uri' in data_json:
                    result['uri'] = data_json['uri']
        print(f"uri_metadata = {result}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def onchain_metadata(cell, result):
    try:
        dic_meta = cell.preload_dict(256)

        for k, v in dic_meta.items():
            try:
                cell_value = v.load_ref().begin_parse()
                _ = cell_value.load_uint(8)
                string_value = cell_value.load_snake_string()

                if k == int(hashlib.sha256('name'.encode()).hexdigest(), 16):
                    result['name'] = string_value
                elif k == int(hashlib.sha256('description'.encode()).hexdigest(), 16):
                    result['description'] = string_value
                elif k == int(hashlib.sha256('image'.encode()).hexdigest(), 16):
                    result['image'] = string_value
                elif k == int(hashlib.sha256('image_data'.encode()).hexdigest(), 16):
                    result['image_data'] = string_value
                elif k == int(hashlib.sha256('image_data'.encode()).hexdigest(), 16):
                    result['cover_image'] = string_value
                elif k == int(hashlib.sha256('content_url'.encode()).hexdigest(), 16):
                    result['content_url'] = string_value

                elif k == int(hashlib.sha256('social'.encode()).hexdigest(), 16):
                    result['social_links'] = string_value
                elif k == int(hashlib.sha256('social_links'.encode()).hexdigest(), 16):
                    result['social_links'] = string_value
                elif k == int(hashlib.sha256('links'.encode()).hexdigest(), 16):
                    result['social_links'] = string_value
                elif k == int(hashlib.sha256('websites'.encode()).hexdigest(), 16):
                    result['social_links'] = string_value
                elif k == int(hashlib.sha256('attributes'.encode()).hexdigest(), 16):
                    result['attributes'] = string_value

                elif k == int(hashlib.sha256('symbol'.encode()).hexdigest(), 16):
                    result['symbol'] = string_value
                elif k == int(hashlib.sha256('decimals'.encode()).hexdigest(), 16):
                    result['decimals'] = string_value
                elif k == int(hashlib.sha256('marketplace'.encode()).hexdigest(), 16):
                    result['marketplace'] = string_value
                elif k == int(hashlib.sha256('uri'.encode()).hexdigest(), 16):
                    result['uri'] = string_value
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
        print(f"onchain_metadata = {result}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def check_error(data):
    result = False
    try:
        if 'exit_code' in data and data['exit_code'] == -13:
            result = True
            return
        if 'exit_code' in data and data['exit_code'] == 9:
            result = True
            return
        if 'stack' in data and not len(data):
            result = True
            return
        if 'stack' in data and data['stack'][0]['value'] == '0x18fcf':
            result = True
            return
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_link_for_nft(bot, chat_id, file_path, gateway, pinata_headers, EXTRA_D):
    result = None
    try:
        try:
            ext = str(file_path[file_path.rfind('.'):]).lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4'] and os.path.getsize(file_path) < 5242880:
                res = await Telegraph().upload_file(file_path)
                result = f"https://telegra.ph{res[0]['src']}"
                return
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))

        try:
            random_sequence = await generate_random_sequence()
            url = f"https://api.getgems.io/upload-media?type=Nft&sign={random_sequence}"
            getgems_token = await getgems_get(EXTRA_D)
            if not getgems_token: raise Exception
            print(f"{getgems_token=}")
            r1 = random.randint(15, 19)
            r2 = random.randint(7, 19)
            r3 = random.randint(605, 655)
            r4 = random.randint(1, 9)
            r5 = random.randint(15, 29)
            r6 = random.randint(17, 29)
            r7 = random.randint(4, 9)
            r8 = random.randint(1, 9)

            user_agent = f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{r1}_{r2}) AppleWebKit/{r3}.{r4}.{r5} (KHTML, like Gecko) Version/{r6}.{r7}.{r8} Safari/{r3}.{r4}.{r5}'
            headers = {'User-Agent': user_agent,
                       # 'x-auth-token': '118479773683712_C-9a73d982512738969774857e67c962c7.41e976a5fac3eddf41ed6e184a3c0a56',
                       # 'x-auth-token': '123616365768704_C-d99e4d4e1c6eca5eee9b092e1c66c13c.12451e4036ab31d1ff1a34f40db57375',
                       'x-auth-token': getgems_token, }
            form_data = aiohttp.FormData()
            form_data.add_field('file', open(file_path, 'rb'), filename=os.path.basename(file_path))

            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=form_data, headers=headers) as response:
                    res = await response.json()
                    logger.info(log_ % str(res))
                    result = await check_image(res['fileUrl'])
                    return
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
            await bot.send_message(my_tid, str(e))

        metadata = {"name": os.path.basename(file_path), "keyvalues": {"tid": str(chat_id)}}
        files = {'file': (os.path.basename(file_path), open(file_path, 'rb')),
                 'pinataMetadata': (None, json.dumps(metadata), 'application/json'), }
        response = requests.post("https://api.pinata.cloud/pinning/pinFileToIPFS", files=files, headers=pinata_headers)
        response_json = response.json()
        result = f"{gateway}/ipfs/{response_json['IpfsHash']}?filename={os.path.basename(file_path)}"
        print(f"{result=}")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if os.path.exists(file_path): os.remove(file_path)
        return result


async def generate_random_sequence():
    result = "807ae8ba7a"
    try:
        random.seed(datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f'))
        characters = string.digits + string.ascii_lowercase
        result = ''.join(random.choice(characters) for _ in range(10))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def check_image(url):
    result = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content_type = response.headers.get('Content-Type', '')

                if not ('html' in content_type or 'xml' in content_type):
                    result = url
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_link_for_media(bot, chat_id, file_path, KEYS_JSON, is_del=True):
    result = result_id = None
    try:
        if os.path.getsize(file_path) / (1024 * 1024) > 15: return
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())
        # base_name = str(os.path.basename(file_path).replace(' ', '').replace('!', ''))
        base_name = str(os.path.basename(file_path))
        base_name = base_name.replace("\xa0", "").encode("ascii", "ignore").decode("ascii")
        # base_name = base_name.replace("\xa0", " ")  # Заменяем \xa0 на обычный пробел
        base_name = base_name.encode("utf-8", "ignore").decode("utf-8")
        base_name = re.sub(r"[^\w\-.]", "", base_name)
        random_suffix = datetime.now(timezone.utc).strftime('%f')
        base_name = f"r{random_suffix}_{base_name.replace('_', '')}"
        base_name = urllib.parse.quote(base_name)
        print(f"{base_name=}")

        # region telegraph
        # try:
        #     ext = str(file_path[file_path.rfind('.'):]).lower()
        #     if ext in ['.jpg', '.jpeg', '.png', '.gif', '.mp4'] and os.path.getsize(file_path) < 5242880:
        #         res = await Telegraph().upload_file(file_path)
        #         result = f"https://telegra.ph{res[0]['src']}"
        #         return
        # except Exception as e:
        #     logger.info(log_ % str(e))
        #     await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        # region getgems
        # len_ = len(data["media"]["getgems"])
        # random_index = random.randint(0, len_ - 1)
        # getgems_token = data["media"]["getgems"][random_index]
        #
        # try:
        #     random_sequence = await generate_random_sequence()
        #     url = f"https://api.getgems.io/upload-media?type=Nft&sign={random_sequence}"
        #     if not getgems_token: raise Exception
        #     r1 = random.randint(15, 19)
        #     r2 = random.randint(7, 19)
        #     r3 = random.randint(605, 655)
        #     r4 = random.randint(1, 9)
        #     r5 = random.randint(15, 29)
        #     r6 = random.randint(17, 29)
        #     r7 = random.randint(4, 9)
        #     r8 = random.randint(1, 9)
        #
        #     user_agent = f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_{r1}_{r2}) AppleWebKit/{r3}.{r4}.{r5} (KHTML, like Gecko) Version/{r6}.{r7}.{r8} Safari/{r3}.{r4}.{r5}'
        #     headers = {'User-Agent': user_agent, 'x-auth-token': getgems_token, }
        #     form_data = aiohttp.FormData()
        #     form_data.add_field('file', open(file_path, 'rb'), filename=base_name)
        #
        #     async with aiohttp.ClientSession() as session:
        #         async with session.post(url, data=form_data, headers=headers) as response:
        #             res = await response.json()
        #             logger.info(log_ % str(res))
        #             result = await check_image(res['fileUrl'])
        #             return
        # except Exception as e:
        #     logger.info(log_ % str(e))
        #     # await asyncio.sleep(round(random.uniform(0, 1), 2))
        #     if bot: await bot.send_message(my_tid, str(e))
        # endregion

        # region pinata
        for pinata in data["media"]["pinata"]:
            pinata_gateway = pinata["GATEWAY"]
            pinata_secret_key = pinata["SECRET_KEY"]
            pinata_headers = {"Authorization": f"Bearer {pinata_secret_key}"}

            metadata = {"name": base_name, "keyvalues": {"tid": str(chat_id)}}
            form_data = aiohttp.FormData()
            form_data.add_field('file', open(file_path, 'rb'), filename=base_name)
            form_data.add_field('pinataMetadata', json.dumps(metadata), content_type='application/json')

            async with aiohttp.ClientSession() as session:
                async with session.post(url="https://api.pinata.cloud/pinning/pinFileToIPFS", data=form_data,
                                        headers=pinata_headers) as response:
                    response_json = await response.json()
                    if 'IpfsHash' in response_json:
                        result = f"{pinata_gateway}/ipfs/{response_json['IpfsHash']}?filename={base_name}"
                        return
                    else:
                        print(f"{response_json=}")
        # endregion
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if is_del and file_path and os.path.exists(file_path): os.remove(file_path)
        return result


async def get_smc_info(address, KEYS_JSON, is_test_only=False):
    result = {}
    try:
        if address == '': return
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        # item1 = ['tonapi', f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_info',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        # item2 = ['toncenter', f'https://{pfx_testnet}toncenter.com/api/v3/runGetMethod', {'accept': 'application/json',
        #                                                                                   # 'X-API-Key': 'f5739745a824c8e8d49fb61beeab095786357b76a989c7fad7462afe57fcd970',
        #                                                                                   }]
        # item3 = ['tonapi', f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_info',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY'}]
        # items = [item1, item2, item3]

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_info',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/runGetMethod',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])
        print(f"{items=}")

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()

                        result['counter'] = int(data['stack'][0]['num'], 16)
                        print(f"1 tonapi {result=}")
                        result['balance'] = int(data['stack'][1]['num'], 16)
                        print(f"{result=}")
                    else:
                        payload = {"address": address, "method": 'get_info', "stack": []}
                        async with aiohttp.ClientSession() as session:
                            async with session.post(url, headers=headers, json=payload) as response:
                                response.raise_for_status()
                                data = await response.json()
                        if await check_error(data): return

                        result['counter'] = int(data['stack'][0]['value'], 16)
                        print(f"1 toncenrt {result=}")
                        result['balance'] = int(data['stack'][1]['value'], 16)
                        print(f"{result=}")

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_wallet_address(address, master, KEYS_JSON, is_test_only=False, is_TON=False):
    result = {}
    try:
        if address == '': return
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        # /jettons?currencies=ton,usd,rub (in the end)
        # item1 = ['tonapi', f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/jettons/{master}',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        # item2 = ['toncenter',
        #          f'https://{pfx_testnet}toncenter.com/api/v3/jetton/wallets?owner_address={address}&jetton_address={master}&limit=1&offset=0',
        #          {'accept': 'application/json',
        #           # 'X-API-Key': 'f5739745a824c8e8d49fb61beeab095786357b76a989c7fad7462afe57fcd970',
        #           }]
        # item3 = ['tonapi', f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/jettons/{master}',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY'}]
        # items = [item1, item2, item3]
        # items = [item2] этой фукнции

        print(f"1, {is_TON=}, {address=}, {master=},  {KEYS_JSON=}, ")
        items = []
        for provider, keys in data["ton"].items():
            for it in keys:
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/jettons/{master}',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/jetton/wallets?owner_address={address}&jetton_address={master}&limit=1&offset=0',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])
        # print(f"{items=}")

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    if name == 'tonapi':
                        if is_TON: url = f"https://{pfx_testnet}tonapi.io/v2/accounts/{address}"
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()
                                print(f"{name=} {data=}")

                        if is_TON:
                            result['balance'] = data['balance']
                            return

                        result['wallet_address'] = data['wallet_address']['address']
                        result['decimals'] = data['jetton']['decimals']
                        result['balance'] = data['balance']
                        print(f"{name=} {result=}")
                    else:
                        if is_TON: url = f"https://{pfx_testnet}toncenter.com/api/v3/accountStates?address={address}&include_boc=false"

                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()
                                print(f"{name=} {data=}")
                        if await check_error(data): return

                        if is_TON:
                            result['balance'] = data['accounts'][0]['balance']
                            return

                        result['wallet_address'] = data['jetton_wallets'][0]['address']
                        result['balance'] = data['jetton_wallets'][0]['balance']
                        print(f"{name=} 0 {result=}")
                        url2 = f'https://{pfx_testnet}toncenter.com/api/v3/jetton/masters?address={master}&limit=1&offset=0'
                        await asyncio.sleep(1.1)
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url2, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()

                        result['decimals'] = data['jetton_masters'][0]['jetton_content']['decimals']
                        print(f"{name=} 1 {result=}")

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_nft_data(address, KEYS_JSON, is_test_only=False, help_link=None):
    result = {}
    try:
        # nft_address = 'EQCQDb292ilF5eG7deNem-8O4UmJoHMHAsYAAac-eLqM3nok'
        _ = Address(address)
        # https://tonapi.io/v2/blockchain/accounts/{address} - if only balance
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        # item1 = ['tonapi', f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_nft_data',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        # item2 = ['toncenter', f'https://{pfx_testnet}toncenter.com/api/v3/runGetMethod',
        #          {'accept': 'application/json', 'X-API-Key': toncenter_key}]
        # item3 = ['tonapi', f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_nft_data',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY'}]
        # items = [item1, item2, item3]
        # items = [item2]

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_nft_data',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/runGetMethod',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])
        print(f"{items=}")

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item
                    print(f'ame, {url=}, he')

                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                data = await response.json()
                                print(f"{data=}")

                        if 'error' in data or not data['success']: return
                        print(f"pum pum {data['decoded']=}")
                        if not data['decoded']['init']: return
                        result['init'] = data['decoded']['init']
                        print(f"{result['init']=}")
                        result['index'] = data['decoded']['index']
                        result['collection_address'] = data['decoded']['collection_address']
                        result['owner_address'] = data['decoded']['owner_address']
                        result['individual_content'] = data['decoded']['individual_content']

                        cell = Cell.one_from_boc(result['individual_content']).begin_parse()
                        _ = cell.load_uint(8)
                        cont = ''
                        try:
                            cont = cell.load_snake_string()
                        except Exception as _:
                            pass

                        if cont.startswith('/') and not help_link and result['collection_address'] != '':
                            item = await get_collection_data(result['collection_address'], KEYS_JSON)
                            print(f"sdfd {item=}")
                            if 'image' in item:
                                help_link = item['image']
                                print(f"{help_link=}")

                        print(f"{cont=}")
                        if help_link and 'https://s.getgems.io' in help_link:
                            cell = Cell.one_from_boc(result['individual_content']).begin_parse()
                            cont = cell.load_snake_string()
                            substring = 'https://s.getgems.io/nft/c/'
                            extracted_part = help_link[len(substring):help_link.find('/', len(substring))]
                            cont = f"{substring}{extracted_part}/{cont.lstrip('/')}"

                            result = await uri_metadata(cont, result)
                        elif cont.startswith('https://'):
                            result = await uri_metadata(cont, result)
                        else:
                            result = await onchain_metadata(cell, result)
                            if 'uri' in result: result = await uri_metadata(cont, result)
                    else:
                        payload = {"address": address, "method": 'get_nft_data', "stack": []}
                        async with aiohttp.ClientSession() as session:
                            async with session.post(url, headers=headers, json=payload) as response:
                                response.raise_for_status()
                                data = await response.json()
                        print(f"toncenter get_nft_data {data=}")
                        if await check_error(data): return

                        result['init'] = True if data['stack'][0]['value'] == '-0x1' else False
                        result['index'] = int(data['stack'][1]['value'], 16)
                        try:
                            result['collection_address'] = (
                                Cell.one_from_boc(data['stack'][2]['value']).begin_parse().load_address()).to_str(
                                is_bounceable=False, is_test_only=is_test_only)
                        except Exception as _:
                            result['collection_address'] = ''

                        try:
                            result['owner_address'] = (
                                Cell.one_from_boc(data['stack'][3]['value']).begin_parse().load_address()).to_str(
                                is_bounceable=False, is_test_only=is_test_only)
                        except Exception as _:
                            result['owner_address'] = ''

                        print(f"ddd {result=}")
                        cell = Cell.one_from_boc(data['stack'][4]['value']).begin_parse()

                        cont = ''
                        try:
                            _ = cell.load_uint(8)
                            cont = cell.load_snake_string()
                        except Exception as _:
                            pass

                        print(f"cont get_nft_data, {cont}")
                        if cont.startswith('/') and not help_link and result['collection_address'] != '':
                            item = await get_collection_data(result['collection_address'], KEYS_JSON)
                            print(f"sdfd {item=}")
                            if 'image' in item:
                                help_link = item['image']
                                print(f"{help_link=}")

                        if help_link and 'https://s.getgems.io' in help_link:
                            # cell = Cell.one_from_boc(result['individual_content']).begin_parse()
                            # cont = cell.load_snake_string()
                            print(f"cont {cont=}")
                            substring = 'https://s.getgems.io/nft/c/'
                            extracted_part = help_link[len(substring):help_link.find('/', len(substring))]

                            cont = f"{substring}{extracted_part}/{cont.lstrip('/')}"
                            result = await uri_metadata(cont, result)
                        elif cont.startswith('https://'):
                            result = await uri_metadata(cont, result)
                        else:
                            result = await onchain_metadata(cell, result)
                            if 'uri' in result: result = await uri_metadata(cont, result)

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_collection_data(address, KEYS_JSON, is_test_only=False):
    result = {}
    try:
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        # item1 = ['tonapi',
        #          f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_collection_data',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        # item2 = ['toncenter', f'https://{pfx_testnet}toncenter.com/api/v3/runGetMethod',
        #          {'accept': 'application/json', 'X-API-Key': toncenter_key}]
        # item3 = ['tonapi',
        #          f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_collection_data',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY'}]
        # items = [item1, item2, item3]
        # # items = [item2]

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/blockchain/accounts/{address}/methods/get_collection_data',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/runGetMethod',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])
        print(f"{items=}")

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()

                        if 'error' in data or not data['success']: return
                        print('success', data)
                        result['next_item_index'] = data['decoded']['next_item_index']
                        result['owner_address'] = data['decoded']['owner_address']

                        cell = Cell.one_from_boc(data['decoded']['collection_content']).begin_parse()
                        tmp = cell.load_uint(8)
                        print(f"{tmp=}")
                        cont = ''
                        try:
                            cont = cell.load_snake_string()
                        except Exception as _:
                            pass

                        print(f"{cont=}")
                        if cont.startswith('https://'):
                            result = await uri_metadata(cont, result)
                        else:
                            result = await onchain_metadata(cell, result)
                            if 'uri' in result: result = await uri_metadata(cont, result)
                    else:
                        payload = {"address": address, "method": 'get_collection_data', "stack": []}
                        async with aiohttp.ClientSession() as session:
                            async with session.post(url, headers=headers, json=payload) as response:
                                response.raise_for_status()
                                data = await response.json()
                        if await check_error(data): return

                        print(f"{data=}")
                        result['next_item_index'] = int(data['stack'][0]['value'], 16)
                        result['collection_content'] = data['stack'][1]['value']
                        try:
                            result['owner_address'] = (
                                Cell.one_from_boc(data['stack'][2]['value']).begin_parse().load_address()).to_str(
                                is_bounceable=False, is_test_only=is_test_only)
                        except Exception as _:
                            result['owner_address'] = ''

                        print(f"{result=}")
                        cell = Cell.one_from_boc(result['collection_content']).begin_parse()
                        cont = ''
                        try:
                            _ = cell.load_uint(8)
                            cont = cell.load_snake_string()
                        except Exception as _:
                            pass

                        print(f"{cont=}")
                        if cont.startswith('https://'):
                            result = await uri_metadata(cont, result)
                        else:
                            result = await onchain_metadata(cell, result)
                            if 'uri' in result: result = await uri_metadata(cont, result)

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_nft_in_account(address, collection, KEYS_JSON, is_test_only=False, cnt=1):
    result = []
    try:
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        # item1 = ['tonapi',
        #          f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/nfts?collection={collection}&limit={cnt}&offset=0&indirect_ownership=false',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFQTWCA5N2BCKRYAAAAILLMH5NYQ2VQTMVPEFE2TIWZVVPKMCJWJLC3UO3NRVEGJXE5XLPA'}]
        # item2 = ['toncenter',
        #          f'https://{pfx_testnet}toncenter.com/api/v3/nft/items?owner_address={address}&collection_address={collection}&limit={cnt}&offset=0',
        #          {'accept': 'application/json', 'X-API-Key': toncenter_key}]
        # item3 = ['tonapi',
        #          f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/nfts?collection={collection}&limit={cnt}&offset=0&indirect_ownership=false',
        #          {'accept': 'application/json',
        #           'Authorization': 'Bearer AFPJTKEBPOX3AIYAAAAKA2HWOTRNJP5MUCV5DMDCZAAOCPSAYEYS3CILNQVLF2HWKED6USY'}]
        # items = [item1, item2, item3]
        # # items = [item2]

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/nfts?collection={collection}&limit={cnt}&offset=0&indirect_ownership=false',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/nft/items?owner_address={address}&collection_address={collection}&limit={cnt}&offset=0',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])
        # print(f"{items=}")
        # toncenter doesnt understand sbt

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    print(f"{name=}, {item=}")
                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                data = await response.json()
                                print(f"{name=}, {data=}")

                        result = [item["address"] for item in data["nft_items"]]
                    else:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                data = await response.json()
                                print(f"{name=}, {data=}")

                        result = [item["address"] for item in data["nft_items"]]

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_any_activity(address, KEYS_JSON, is_test_only=False):
    result = None
    try:
        if address == '': return
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/actions?account={address}&limit=1&offset=0&sort=desc',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])
        print(f"{pfx_testnet=}, {is_test_only=}, {items=}")

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()

                        result = data['last_activity']
                        print(f"{name=}, {data=}, {result=}")
                    else:
                        print(0)
                        headers.update({
                            "Cache-Control": "no-cache, no-store, must-revalidate",
                            "Pragma": "no-cache",
                            "Expires": "0"
                        })
                        async with aiohttp.ClientSession(headers={"Cache-Control": "no-cache"}) as session:
                            async with session.get(url, headers=headers) as response:
                                data = await response.json()

                        print(f"2 {headers=}, {is_test_only=}")
                        print(f"{name=},  {data=}")
                        if len(data['actions']): result = data['actions'][0]['start_utime']
                        print(f"{name=},  {data=}, {result=}")

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_any_nfts(address, KEYS_JSON, is_test_only=False):
    result = 0
    try:
        if address == '': return
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/nfts?limit=1&offset=0',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/nft/transfers?owner_address={address}&limit=1&offset=0&sort=desc',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()

                        result = len(data['nft_items'])
                        print(f"{data=}, {result=}")
                    else:
                        print(0)
                        headers.update({
                            "Cache-Control": "no-cache, no-store, must-revalidate",
                            "Pragma": "no-cache",
                            "Expires": "0"
                        })
                        async with aiohttp.ClientSession(headers={"Cache-Control": "no-cache"}) as session:
                            async with session.get(url, headers=headers) as response:
                                data = await response.json()

                        print(f"2 toncenter, {headers=}")
                        print(f"{data=}")
                        result = len(data['nft_transfers'])
                        print(f"{data=}, {result=}")

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_any_jettons(address, KEYS_JSON, is_test_only=False):
    result = 0
    try:
        if address == '': return
        _ = Address(address)
        pfx_testnet = "testnet." if is_test_only else ""
        async with aiofiles.open(KEYS_JSON, mode='r') as f:
            data = json.loads(await f.read())

        items = []
        for provider, keys in data["ton"].items():  # provider = "tonapi" или "toncenter"
            for it in keys:  # it = {"all": "..."} или {"testnet": "..."}
                if provider == "tonapi":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('all')
                    if key:
                        items.append([
                            'tonapi',
                            f'https://{pfx_testnet}tonapi.io/v2/accounts/{address}/jettons',
                            {
                                'accept': 'application/json',
                                'Authorization': f'Bearer {key}'
                            }
                        ])
                elif provider == "toncenter":
                    key = it.get('testnet') if is_test_only and 'testnet' in it else it.get('mainnet')
                    if key:
                        items.append([
                            'toncenter',
                            f'https://{pfx_testnet}toncenter.com/api/v3/jetton/transfers?owner_address={address}&limit=1&offset=0&sort=desc',
                            {
                                'accept': 'application/json',
                                'X-API-Key': key
                            }
                        ])

        while True:
            random.shuffle(items)
            for item in items:
                try:
                    name, url, headers = item

                    if name == 'tonapi':
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, headers=headers) as response:
                                response.raise_for_status()
                                data = await response.json()

                        result = len(data['balances'])
                        print(f"{data=}, {result=}")
                    else:
                        print(0)
                        headers.update({
                            "Cache-Control": "no-cache, no-store, must-revalidate",
                            "Pragma": "no-cache",
                            "Expires": "0"
                        })
                        async with aiohttp.ClientSession(headers={"Cache-Control": "no-cache"}) as session:
                            async with session.get(url, headers=headers) as response:
                                data = await response.json()

                        print(f"2 toncenter, {headers=}")
                        print(f"{data=}")
                        result = len(data['jetton_transfers'])
                        print(f"{data=}, {result=}")

                    await asyncio.sleep(0.6)
                    return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
            break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


# endregion


# region neuro pack
async def format_text_to_sticker(txt):
    result = txt
    try:
        if emoji.emoji_count(txt):
            txt = txt.replace('\n\n', ' ')
            txt = txt.replace('\n', ' ')
            entities = []
            emoji.demojize(string=txt, language='en', version=-1,
                           handle_version=lambda emj, emj_data: handle_ver(emj, emj_data, entities))
            distinct_list = list({e['emoji'] for e in entities})
            for it in distinct_list:
                txt = txt.replace(it, '')
        if len(txt.split(':')) == 2 and len(txt.split(':')[0]) > 32 and ':' in txt:
            txt = txt.split(':')[0]
            last_space_index = txt.rfind(' ')
            if last_space_index != -1:
                txt = txt[:last_space_index].strip()
        lim_txt = 80
        if len(txt) > lim_txt:
            cut_position = txt.rfind(' ', 0, lim_txt)
            if cut_position != -1:
                txt = txt[:cut_position]
            else:
                txt = txt[:lim_txt]

        result = txt
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def logo_to_sticker(bot, chat_id, tid, name, stickers, file_photo, title, MEDIA_D, mem_type):
    sticker = file_logo = file_gray = seq_dir = file_webx = None
    try:
        print(f"logo_to_sticker start...")
        if file_photo:
            fn_ = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.png')
            os.makedirs(os.path.join(MEDIA_D, str(tid)), exist_ok=True, mode=0o777)
            file_logo = os.path.join(MEDIA_D, str(tid), fn_)
            shutil.copyfile(file_photo, file_logo)

        if file_logo and os.path.exists(file_logo):
            mem_format = 'static' if random.choice([True, False]) else 'video'
            rnd_emoji = random.choices(animated_emoji, k=random.randint(2, 5))
            rnd_words = random.choices(trg_utms, k=random.randint(2, 5))
            size_kb = 256000 if mem_format == 'video' else 512000
            side_sz = '512' if mem_type == 'regular' else '100'
            w, h = await resize_to_max_side(file_logo, side_sz, mem_type)
            pixels_str = f"{w}x{h}"

            # region size
            quality = 90
            while quality > 0:
                img = Image.open(file_logo)
                img = await correct_orientation(img)
                if img.mode == 'RGBA': img = img.convert('RGB')
                img.save(file_logo, format="JPEG", quality=quality)

                if os.path.getsize(file_logo) < size_kb: break
                quality = 1 if quality == 0 else quality - 10
            # endregion

            # region color
            img = Image.open(file_logo)
            img = await correct_orientation(img)
            img = img.convert("RGBA")
            img.save(file_logo)
            # endregion

            if mem_format == 'static':
                await photo_to_circle(file_logo)

                image = Image.open(file_logo)
                fn_ = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
                file_webx = os.path.join(MEDIA_D, str(tid), fn_)
                image.save(file_webx, format='WEBP')
            else:
                fps = '30'
                frames = 12
                bitrate = '100k'
                seq_dir = os.path.join(MEDIA_D, str(tid), 'seq')
                i_input_data = f'{seq_dir}/frame_%04d.png'
                os.makedirs(seq_dir, exist_ok=True, mode=0o777)
                file_gray = file_logo[:file_logo.rfind('.')] + 'gray.png'

                # region gray
                img = Image.open(file_logo)
                img = await correct_orientation(img)
                img = ImageOps.grayscale(img)
                img = img.convert("RGBA")
                img.save(file_gray)
                # endregion

                for it_png in [file_logo, file_gray]:
                    try:
                        await photo_to_circle(it_png)
                    except Exception as e:
                        logger.info(log_ % str(e))
                        await asyncio.sleep(round(random.uniform(0, 1), 2))

                for i in range(0, frames * 2):
                    it_png = file_logo if i < frames else file_gray
                    shutil.copy(it_png, f"{seq_dir}/frame_{i:04d}.png")

                fn_ = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webm')
                file_webx = os.path.join(MEDIA_D, str(tid), fn_)
                ffmpeg_command = ['ffmpeg', '-i', i_input_data, '-filter_complex_threads', '2', '-c:v', 'libvpx-vp9',
                                  '-r', fps, '-b:v', bitrate, '-crf', '30', '-s', pixels_str, '-pix_fmt', 'yuva420p',
                                  '-t', '3', '-an', '-y', file_webx]

                print(f"{ffmpeg_command=}")
                p = await asyncio.create_subprocess_exec(*ffmpeg_command)
                await p.communicate()

            upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(file_webx),
                                                sticker_format=mem_format)
            sticker = types.InputSticker(sticker=upl.file_id, format=mem_format, emoji_list=rnd_emoji,
                                         keywords=rnd_words)

            if len(stickers):
                await bot.add_sticker_to_set(user_id=chat_id, name=name, sticker=sticker)
            else:
                await bot.create_new_sticker_set(user_id=chat_id, name=name, title=title, stickers=[sticker],
                                                 sticker_type=mem_type, needs_repainting=None)

            stickers.append(sticker)
            print(f"logo_to_sticker success")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
        try:
            if sticker and 'occupied' in str(e):
                await bot.add_sticker_to_set(user_id=chat_id, name=name, sticker=sticker)
                stickers.append(sticker)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        try:
            if file_logo and os.path.exists(file_logo): os.remove(file_logo)
            if file_gray and os.path.exists(file_gray): os.remove(file_gray)
            if file_webx and os.path.exists(file_webx): os.remove(file_webx)
            if seq_dir and os.path.exists(seq_dir): shutil.rmtree(seq_dir)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        return stickers


async def desc_to_sticker(bot, chat_id, name, stickers, username, title, desc, MEDIA_D, mem_type):
    sticker = file_sticker = None
    try:
        print(f"desc_to_sticker start...")
        title = await format_text_to_sticker(title)
        desc = await format_text_to_sticker(desc)
        sticker_txt = f'Sticker\n{title}'
        if username and desc:
            sticker_txt = f"@{username}\n{desc}"
        elif username and not desc:
            sticker_txt = f"@{username}\n{title}"
        elif not username and desc:
            sticker_txt = f'{title[:20]}\n{desc}'

        file_sticker, file_title = await text_layout(sticker_txt, MEDIA_D)
        if file_sticker:
            size_side = '512' if mem_type == 'regular' else '100'
            await resize_to_max_side(file_sticker, size_side, mem_type)
            mem_format = 'static'
            # mem_format = 'static' if random.choice([True, False]) else 'video'

            rnd_emoji = random.choices(animated_emoji, k=random.randint(2, 5))
            rnd_words = random.choices(trg_utms, k=random.randint(2, 5))

            upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(file_sticker),
                                                sticker_format=mem_format)
            sticker = types.InputSticker(sticker=upl.file_id, format=mem_format, emoji_list=rnd_emoji,
                                         keywords=rnd_words)

            if len(stickers):
                await bot.add_sticker_to_set(user_id=chat_id, name=name, sticker=sticker)
            else:
                await bot.create_new_sticker_set(user_id=chat_id, name=name, title=title, stickers=[sticker],
                                                 sticker_type=mem_type, needs_repainting=None)

            stickers.append(sticker)
            print(f"desc_to_sticker success")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
        try:
            if sticker and 'occupied' in str(e):
                await bot.add_sticker_to_set(user_id=chat_id, name=name, sticker=sticker)
                stickers.append(sticker)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        try:
            if file_sticker and os.path.exists(file_sticker): os.remove(file_sticker)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        return stickers


async def text_to_sticker(text, media_dir, img_width):
    result = file_name_part = None
    try:
        font_size = int(img_width * 0.08) - 1
        img_heihgt = font_size + 20
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_heihgt)
        ctx = cairo.Context(surface)

        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        ctx.rectangle(0, 0, img_width, img_heihgt + 2)
        await round_rect(ctx, 0, 0, img_width, int(img_heihgt * 0.9), 8)
        ctx.fill()

        ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(font_size)
        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        ctx.set_source_rgb(128 / 255, 196 / 255, 255 / 255)

        ctx.move_to(15, font_size)
        ctx.show_text(text)
        ctx.stroke()

        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.png')
        file_name = os.path.join(media_dir, file_name_part)
        surface.write_to_png(file_name)
        result = file_name
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result, file_name_part


async def photo_to_circle(file_photo):
    try:
        fill_ = 255
        image = Image.open(file_photo)
        image = await correct_orientation(image)
        image = image.convert("RGBA")
        image.save(file_photo)
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)

        left, top, right, bottom = (0, 0, image.width, image.height)
        draw.pieslice(((left, top), (right, bottom)), 0, 360, fill=fill_, outline=fill_)

        res = Image.new('RGBA', image.size, (0, 0, 0, 0))
        res.paste(image, mask=mask)
        res.save(file_photo)
        res.close()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def resize_to_max_side(input_image_path, target_max_side, mem_type='regular', black_frame=False):
    result_width, result_height = ['512', '512'] if mem_type == 'regular' else ['100', '100']
    try:
        with Image.open(input_image_path) as img:
            width, height = img.size
            target_max_side = int(target_max_side)

            if mem_type == 'custom_emoji':
                # Для custom_emoji масштабируем изображение, сохраняя пропорции
                if width > height:
                    new_width = 100
                    new_height = int((100 / width) * height)
                else:
                    new_height = 100
                    new_width = int((100 / height) * width)

                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                resized_img = resized_img.convert("RGBA")

                # Создаем прозрачный фон 100x100 (RGBA с прозрачностью)
                final_img = Image.new("RGBA", (100, 100), (0, 0, 0, 0))

                # Вставляем изображение по центру прозрачного фона
                x_offset = (100 - new_width) // 2
                y_offset = (100 - new_height) // 2
                final_img.paste(resized_img, (x_offset, y_offset), resized_img)

                # Сохраняем итоговое изображение с прозрачным фоном
                final_img.save(input_image_path)

                result_width, result_height = 100, 100
            else:
                # Обычное поведение для других mem_type
                if width > height:
                    new_width = target_max_side
                    new_height = int((target_max_side / width) * height)
                else:
                    new_height = target_max_side
                    new_width = int((target_max_side / height) * width)

                resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                resized_img = resized_img.convert("RGBA")

                resized_width, resized_height = resized_img.size

                if resized_width != target_max_side and resized_height != target_max_side or black_frame:
                    final_img = Image.new("RGBA", (target_max_side, target_max_side), (0, 0, 0, 0))

                    # Вставляем изменённое изображение по центру
                    x_offset = (target_max_side - resized_width) // 2
                    y_offset = (target_max_side - resized_height) // 2
                    final_img.paste(resized_img, (x_offset, y_offset), resized_img)

                    # Сохраняем изображение с чёрным фоном
                    final_img.save(input_image_path)
                else:
                    # Сохраняем изображение без фона, если одна из сторон равна target_max_side
                    resized_img.save(input_image_path)

                result_width, result_height = resized_width, resized_height
    except Exception as e:
        print(e)
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result_width, result_height


async def create_mem(bot, chat_id, lz, tid, mem_item, username, title, desc, file_photo, IMGFLIP_UN, IMGFLIP_PS,
                     MEDIA_D, mem_type):
    result = mem_format = file_webx = photo_name = video_name = file_mp4 = seq_dir = sticker_png = None
    try:
        mem_id = mem_item.get('id')
        mem_link = mem_item.get('link')
        # mem_link = "https://i.imgflip.com/6nfajj.mp4"
        # mem_link = "https://i.gifer.com/307G.gif"
        # 'https://i.gifer.com/Ao.gif'
        # mem_id = '141956050'
        # mem_link = 'https://i.imgflip.com/sxycb.jpg'
        mem_format = 'static' if mem_link.lower().endswith(('.jpg', '.png')) else 'video'

        title = await format_text_to_sticker(title)
        desc = await format_text_to_sticker(desc)
        lst = [title]
        if desc != '': lst.append(desc)
        if username != '': lst.append(f"@{username}")
        if file_photo != '': lst.append(file_photo)
        if len(lst) == 1: lst.append(f"+ {title}")
        lst = random.sample(lst, 2)
        # lst = [file_photo, title]
        mem_top_txt, mem_bottom_txt = lst
        print(f"{mem_link=}, {lst=}, {mem_format=}")

        rad = 25
        fill_ = 255
        side_sz = 512 if mem_type == 'regular' else 100
        ext = 'webp' if mem_format == 'static' else 'webm'
        fn_ = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.{ext}')
        file_webx = os.path.join(MEDIA_D, str(tid), fn_)

        if mem_format == 'static':
            fn_ = urlparse(mem_link).path.split('/')[-1]
            photo_name = os.path.join(MEDIA_D, str(tid), fn_)

            photo_json = {'91998305': {'top': [373, 123], 'bottom': [373, 373], },
                          '87743020': {'top': [242, 468], 'bottom': [242, 468], },
                          '112126428': {'top': [200, 185], 'bottom': [200, 185], },
                          '131087935': {'top': [70, 470], 'bottom': [70, 470], },
                          '124822590': {'top': [277, 367], 'bottom': [277, 367], },
                          '135256802': {'top': [467, 303], 'bottom': [467, 303], },
                          '438680': {'top': [100, 50], 'bottom': [300, 50], },
                          '322841258': {'top': [115, 85], 'bottom': [115, 85], },
                          '247375501': {'top': [166, 85], 'bottom': [520, 136], },
                          '97984': {'top': [363, 185], 'bottom': [363, 185], },
                          '188390779': {'top': [135, 225], 'bottom': [508, 248], },
                          '110163934': {'top': [257, 108], 'bottom': [677, 152], },
                          '91538330': {'top': [210, 130], 'bottom': [350, 192], },
                          '104937008': {'top': [160, 104], 'bottom': [167, 342], },
                          '93228317': {'top': [206, 187], 'bottom': [206, 187], },
                          '61579': {'top': [173, 247], 'bottom': [173, 247], },
                          '79132341': {'top': [190, 80], 'bottom': [190, 80], },
                          '61544': {'top': [250, 235], 'bottom': [250, 235], },
                          '148909805': {'top': [140, 320], 'bottom': [430, 327], },
                          '27813981': {'top': [320, 76], 'bottom': [320, 370], },
                          '100777631': {'top': [155, 232], 'bottom': [460, 113], },
                          '177682295': {'top': [255, 130], 'bottom': [255, 130], },
                          '166969924': {'top': [153, 101], 'bottom': [153, 101], },
                          '91401121': {'top': [122, 148], 'bottom': [440, 36], },
                          '84341851': {'top': [467, 230], 'bottom': [467, 230], },
                          '21735': {'top': [380, 74], 'bottom': [383, 277], },
                          '221497492': {'top': [278, 243], 'bottom': [278, 243], },
                          '50421420': {'top': [222, 122], 'bottom': [230, 360], },
                          '5496396': {'top': [208, 226], 'bottom': [208, 226], },
                          '110133729': {'top': [222, 80], 'bottom': [600, 80], },
                          '354700819': {'top': [93, 300], 'bottom': [390, 270], },
                          '247756783': {'top': [516, 338], 'bottom': [516, 338], },
                          '153695877': {'top': [128, 78], 'bottom': [365, 141], },
                          '133946291': {'top': [544, 230], 'bottom': [544, 230], },
                          '32399536': {'top': [315, 245], 'bottom': [315, 245], },
                          '542413928': {'top': [300, 140], 'bottom': [677, 140], },
                          '1367068': {'top': [412, 200], 'bottom': [412, 200], },
                          '193286698': {'top': [163, 107], 'bottom': [407, 322], },
                          '36698509': {'top': [200, 200], 'bottom': [200, 200], },
                          '504321965': {'top': [257, 95], 'bottom': [250, 310], },
                          '138766447': {'top': [262, 128], 'bottom': [444, 177], },
                          '61516': {'top': [227, 169], 'bottom': [227, 169], },
                          '8072285': {'top': [250, 210], 'bottom': [250, 210], },
                          '84195720': {'top': [300, 222], 'bottom': [674, 260], },
                          '200497759': {'top': [280, 214], 'bottom': [280, 214], },
                          '405658': {'top': [255, 425], 'bottom': [255, 425], },
                          '228097860': {'top': [160, 100], 'bottom': [136, 410], },
                          '9440985': {'top': [250, 296], 'bottom': [250, 296], },
                          '17862622': {'top': [240, 390], 'bottom': [240, 390], },
                          '11557802': {'top': [126, 364], 'bottom': [126, 364], },
                          '141033994': {'top': [205, 400], 'bottom': [205, 400], },
                          '179315205': {'top': [378, 215], 'bottom': [132, 378], },
                          '195389': {'top': [282, 110], 'bottom': [282, 110], },
                          '23909796': {'top': [540, 120], 'bottom': [540, 120], },
                          '7253945': {'top': [136, 127], 'bottom': [136, 127], },
                          '234856740': {'top': [113, 178], 'bottom': [113, 178], },
                          '44762097': {'top': [170, 226], 'bottom': [170, 226], },
                          '77670505': {'top': [230, 355], 'bottom': [230, 355], },
                          '289357455': {'top': [105, 105], 'bottom': [105, 105], },
                          '1909418': {'top': [305, 130], 'bottom': [305, 130], },
                          '61583': {'top': [300, 323], 'bottom': [300, 323], },
                          '59026813': {'top': [217, 260], 'bottom': [217, 260], },
                          '22148412': {'top': [346, 197], 'bottom': [346, 197], },
                          '40595741': {'top': [290, 100], 'bottom': [290, 270], },
                          '6072577': {'top': [333, 94], 'bottom': [333, 94], },
                          '68277995': {'top': [230, 455], 'bottom': [230, 455], },
                          '18202798': {'top': [326, 158], 'bottom': [326, 158], },
                          '61520': {'top': [430, 200], 'bottom': [430, 200], },
                          '153355886': {'top': [460, 125], 'bottom': [460, 375], },
                          '24329059': {'top': [236, 297], 'bottom': [236, 297], },
                          '249075000': {'top': [380, 228], 'bottom': [380, 228], },
                          '61539': {'top': [423, 176], 'bottom': [423, 176], },
                          '195329883': {'top': [286, 325], 'bottom': [286, 325], },
                          '232518173': {'top': [208, 361], 'bottom': [208, 361], },
                          '90785501': {'top': [383, 174], 'bottom': [383, 174], },
                          '369104176': {'top': [362, 160], 'bottom': [362, 160], },
                          '141956050': {'top': [210, 200], 'bottom': [210, 200], }, }
            x = y = 0
            if mem_top_txt == file_photo:
                x, y = photo_json[mem_id]['top']
                mem_top_txt = ''
            elif mem_bottom_txt == file_photo:
                x, y = photo_json[mem_id]['bottom']
                mem_bottom_txt = ''

            data = {'template_id': mem_id, 'username': IMGFLIP_UN, 'password': IMGFLIP_PS, 'text0': mem_top_txt,
                    'text1': mem_bottom_txt, }
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.imgflip.com/caption_image', data=data) as response:
                    res = await response.json()
                    if not res['success']: return

                    async with session.get(res['data']['url']) as img_response:
                        img_content = await img_response.read()

                    async with aiofiles.open(photo_name, 'wb') as file:
                        await file.write(img_content)

            if x:
                img = Image.open(photo_name)
                width, height = img.size  # 0,02
                img = await correct_orientation(img)
                logo = Image.open(file_photo)
                l_ = int(math.sqrt(width * height * 0.03))
                logo = logo.resize((l_, l_))
                logo = logo.convert("RGBA")
                img.paste(logo, (int(x - l_ / 2), int(y - l_ / 2)), logo)
                img.save(photo_name)

                img.save(file_webx, format='WEBP')
                await resize_to_max_side(file_webx, side_sz, mem_type)
            else:
                img = Image.open(photo_name)

                img.save(file_webx, format='WEBP')
                await resize_to_max_side(file_webx, side_sz, mem_type)

            # region round image
            image = Image.open(file_webx)
            w, h = image.size
            mask = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask)
            left, top, right, bottom = (0, 0, image.width, image.height)
            draw.pieslice(((left, top), (left + 2 * rad, top + 2 * rad)), 180, 270, fill=fill_, outline=fill_)
            draw.pieslice(((right - 2 * rad, top), (right, top + 2 * rad)), 270, 0, fill=fill_, outline=fill_)
            draw.pieslice(((left, bottom - 2 * rad), (left + 2 * rad, bottom)), 90, 180, fill=fill_, outline=fill_)
            draw.pieslice(((right - 2 * rad, bottom - 2 * rad), (right, bottom)), 0, 90, fill=fill_, outline=fill_)
            draw.rectangle((left + rad, top, right - rad, bottom), fill=fill_)
            draw.rectangle((left, top + rad, right, bottom - rad), fill=fill_)
            res = Image.new('RGBA', image.size, (0, 0, 0, 0))
            res.paste(image, mask=mask)
            res.save(file_webx)
            # endregion

            print(f"{w}x{h}")
        else:
            fn_ = urlparse(mem_link).path.split('/')[-1]
            video_name = os.path.join(MEDIA_D, str(tid), fn_)

            async with aiohttp.ClientSession() as session:
                async with session.get(mem_link) as img_response:
                    img_content = await img_response.read()

                async with aiofiles.open(video_name, 'wb') as file:
                    await file.write(img_content)

            frame_index = 0
            fps = '30'
            bitrate = '90k'
            pixels_str = '512x512' if mem_type == 'regular' else '100x100'
            seq_dir = os.path.join(MEDIA_D, str(tid), 'seq')
            os.makedirs(seq_dir, exist_ok=True, mode=0o777)
            i_input_data = f'{seq_dir}/frame_%04d.png'
            file_mp4 = video_name[:video_name.rfind('.')] + '_.mp4'

            # region sticker_png
            try:
                cap = cv2.VideoCapture(video_name)
                if not cap.isOpened(): return
                ret, frame = cap.read()
                img_ext = os.path.join(seq_dir, f"frame_{frame_index:04d}.png")
                cv2.imwrite(img_ext, frame)
                image = Image.open(img_ext)
                width, height = image.size

                if username:
                    lst = [f"@{username}"]
                    if len(title) < 24 and lz != 'zh': lst.append(title)
                    sticker_txt = random.choice(lst)
                else:
                    sticker_txt = title
                sticker_png, file_title = await text_to_sticker(sticker_txt, MEDIA_D, width)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
            # endregion

            # region compress
            # if os.path.getsize(video_name) > 256000:
            try:
                ffmpeg_command = ['ffmpeg', '-i', video_name, '-filter_complex_threads', '2', '-c:v', 'libvpx-vp9',
                                  '-r', fps, '-b:v', bitrate, '-crf', '30', '-pix_fmt', 'yuva420p', '-t', '3', '-an',
                                  '-y', file_mp4]
                p = await asyncio.create_subprocess_exec(*ffmpeg_command)
                await p.communicate()

                if video_name and os.path.exists(video_name) and os.path.exists(file_mp4): os.remove(video_name)
                if os.path.exists(file_mp4): video_name = file_mp4
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
            # endregion

            # region seq
            try:
                cap = cv2.VideoCapture(video_name)
                if not cap.isOpened(): return

                while True:
                    try:
                        ret, frame = cap.read()
                        if not ret: break

                        img_ext = os.path.join(seq_dir, f"frame_{frame_index:04d}.png")
                        cv2.imwrite(img_ext, frame)
                        frame_index += 1
                        image = Image.open(img_ext)
                        width, height = image.size

                        if sticker_png:
                            shift = int(width * 0.09) + 20 - 3
                            new_height = height + shift
                            new_image = Image.new("RGB", (width, new_height), (0, 0, 0))
                            new_image.paste(image, (0, shift))

                            sticker_image = Image.open(sticker_png)
                            new_image.paste(Image.open(sticker_png), (0, 0), sticker_image)
                            if new_image.mode == 'RGBA': new_image = new_image.convert('RGB')
                            new_image.save(img_ext, format="JPEG", quality=90)

                            new_image = new_image.convert("RGBA")
                            new_image.save(img_ext, format="PNG")

                        w, h = await resize_to_max_side(img_ext, side_sz, mem_type)

                        # region round image
                        image = Image.open(img_ext)
                        mask = Image.new('L', image.size, 0)
                        draw = ImageDraw.Draw(mask)
                        left, top, right, bottom = (0, 0, image.width, image.height)
                        draw.pieslice(((left, top), (left + 2 * rad, top + 2 * rad)), 180, 270, fill=fill_,
                                      outline=fill_)
                        draw.pieslice(((right - 2 * rad, top), (right, top + 2 * rad)), 270, 0, fill=fill_,
                                      outline=fill_)
                        draw.pieslice(((left, bottom - 2 * rad), (left + 2 * rad, bottom)), 90, 180, fill=fill_,
                                      outline=fill_)
                        draw.pieslice(((right - 2 * rad, bottom - 2 * rad), (right, bottom)), 0, 90, fill=fill_,
                                      outline=fill_)
                        draw.rectangle((left + rad, top, right - rad, bottom), fill=fill_)
                        draw.rectangle((left, top + rad, right, bottom - rad), fill=fill_)
                        res = Image.new('RGBA', image.size, (0, 0, 0, 0))
                        res.paste(image, mask=mask)
                        res.save(img_ext)
                        # endregion

                        pixels_str = f"{w}x{h}"
                    except EOFError as e:
                        print(e)
                        break
                    except Exception as e:
                        logger.info(log_ % str(e))
                        await asyncio.sleep(round(random.uniform(0, 1), 2))

                ffmpeg_command = ['ffmpeg', '-i', i_input_data, '-filter_complex_threads', '2', '-c:v', 'libvpx-vp9',
                                  '-r', fps, '-b:v', bitrate, '-crf', '30', '-s', pixels_str, '-t', '3', '-pix_fmt',
                                  'yuva420p', '-an', '-y', file_webx]
                p = await asyncio.create_subprocess_exec(*ffmpeg_command)
                await p.communicate()
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
            print(f"{frame_index=}, {pixels_str=}")  # endregion

        upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(file_webx),
                                            sticker_format=mem_format)
        result = upl.file_id
        print(f"{result=} success !")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        try:
            if file_webx and os.path.exists(file_webx): os.remove(file_webx)
            if sticker_png and os.path.exists(sticker_png): os.remove(sticker_png)
            if file_mp4 and os.path.exists(file_mp4): os.remove(file_mp4)
            if photo_name and os.path.exists(photo_name): os.remove(photo_name)
            if video_name and os.path.exists(video_name): os.remove(video_name)
            if seq_dir and os.path.exists(seq_dir): shutil.rmtree(seq_dir)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        return result, mem_format


async def create_neuro_pack(bot, chat_id, lz, tid, username, title, desc, file_photo, IMGFLIP_UN, IMGFLIP_PS,
                            PROJECT_USERNAME, MEDIA_D, EXTRA_D, mem_type):
    result = None
    try:
        # region json
        async with aiofiles.open(os.path.join(EXTRA_D, 'memes.json'), 'r', encoding='utf-8') as file:
            memes_data = json.loads(await file.read())

        items_list = list(memes_data.items())
        random.shuffle(items_list)
        memes_data = dict(items_list)

        # template_ids = list(memes_data.keys())
        # random_keys = random.sample(template_ids, min(20, len(template_ids)))
        # memes_data = {key: memes_data[key] for key in random_keys}
        # endregion

        stickers = []
        username_orig = username
        if username == '':
            username = f"{random.choice(trg_utms)}_{random.choice(trg_utms)}_{random.randrange(100, 999)}"
        else:
            username = f"{username.strip('@')}_{random.randrange(100, 999)}"
        # username = 'bloodysx_65620'
        mem_type_str = 'addstickers' if mem_type == 'regular' else 'addemoji'
        name = f"{username}_by_{PROJECT_USERNAME}"
        logger.info(log_ % f"Start ({mem_type}): -> https://t.me/{mem_type_str}/{username}_by_{PROJECT_USERNAME}")

        stickers = await logo_to_sticker(bot, chat_id, tid, name, stickers, file_photo, title, MEDIA_D, mem_type)
        # if mem_type == 'regular':
        stickers = await desc_to_sticker(bot, chat_id, name, stickers, username_orig, title, desc, MEDIA_D, mem_type)

        i = 0
        lst_type = []
        await photo_to_circle(file_photo)
        for mem_id, mem_item in memes_data.items():
            sticker = None
            try:
                print(f"====== {i=}. {len(lst_type)=}")
                if len(lst_type) >= 6 or not os.path.exists(file_photo): break
                if lst_type.count('static') >= 4 and mem_item.get('link').lower().endswith(('.jpg', '.png')): continue
                if lst_type.count('video') >= 2 and mem_item.get('link').lower().endswith(('.mp4', '.gif')): continue
                if i >= 10: break

                mem_item['id'] = mem_id
                file_id, mem_format = await create_mem(bot, chat_id, lz, tid, mem_item, username_orig, title, desc,
                                                       file_photo, IMGFLIP_UN, IMGFLIP_PS, MEDIA_D, mem_type)
                if file_id:
                    rnd_emoji = random.choices(animated_emoji, k=random.randint(2, 5))
                    rnd_words = random.choices(trg_utms, k=random.randint(2, 5))

                    sticker = types.InputSticker(sticker=file_id, format=mem_format, emoji_list=rnd_emoji,
                                                 keywords=rnd_words)

                    if len(stickers):
                        await bot.add_sticker_to_set(user_id=chat_id, name=name, sticker=sticker)
                    else:
                        await bot.create_new_sticker_set(user_id=chat_id, name=name, title=title, stickers=[sticker],
                                                         sticker_type=mem_type, needs_repainting=None)
                    stickers.append(sticker)
                    lst_type.append(mem_format)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

                try:
                    if sticker and 'occupied' in str(e):
                        await bot.add_sticker_to_set(user_id=chat_id, name=name, sticker=sticker)
                        stickers.append(sticker)
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
                    if 'STICKERS_TOO_MUCH' in str(e):
                        result = f"https://t.me/{mem_type_str}/{username}_by_{PROJECT_USERNAME}"
                        return
            finally:
                i += 1

        result = f"https://t.me/{mem_type_str}/{username}_by_{PROJECT_USERNAME}"
        logger.info(log_ % f"Final ({mem_type}): -> https://t.me/{mem_type_str}/{username}_by_{PROJECT_USERNAME}")
    except TelegramRetryAfter as e:
        logger.info(log_ % f'TelegramRetryAfter {e.retry_after}')
        await asyncio.sleep(e.retry_after)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def handle_mem_pack(bot, chat_id, lz, tid, username, title, desc, file_photo, IMGFLIP_UN, IMGFLIP_PS,
                          PROJECT_USERNAME, MEDIA_D, EXTRA_D, BASE_D, mem_type):
    try:
        print(f"{os.path.exists(file_photo)=}, {desc=}")
        if not os.path.exists(file_photo) or not desc: return
        result = await create_neuro_pack(bot, chat_id, lz, tid, username, title, desc, file_photo, IMGFLIP_UN,
                                         IMGFLIP_PS, PROJECT_USERNAME, MEDIA_D, EXTRA_D, mem_type)

        if result and PROJECT_USERNAME == 'FereyChannelBot' and mem_type == 'regular':
            sql = "UPDATE CHANNEL SET CHANNEL_STICKERPACK=$1 WHERE CHANNEL_TID=$2"
            await db_change_pg(sql, (result, tid,), BASE_D)
            await bot.send_message(chat_id=chat_id, text=result)
        elif result and PROJECT_USERNAME == 'FereyChannelBot' and mem_type == 'custom_emoji':
            sql = "UPDATE CHANNEL SET CHANNEL_EMOJIPACK=$1 WHERE CHANNEL_TID=$2"
            await db_change_pg(sql, (result, tid,), BASE_D)
            await bot.send_message(chat_id=chat_id, text=result)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


# endregion


# region convert
async def return_file_id(bot, BOT_TID, FILE_NAME, MSG_TYPE, IS_LINK, BASE_D, EXTRA_D, MEDIA_D):
    file_id = file_id_note = file_type = BOT_TOKEN = None
    try:
        cnt = 3
        while cnt > 0:
            try:
                sql = "SELECT OWNER_TID, BOT_USERNAME, BOT_FIRSTNAME, BOT_STATUS, BOT_TOKEN, BOT_VARS FROM \"BOT\" WHERE BOT_TID=$1"
                data = await db_select_pg(sql, (int(BOT_TID),), BASE_D)
                print(f"return_file_id {MSG_TYPE=} {data=}")
                if not len(data): return
                OWNER_TID, BOT_USERNAME, BOT_FIRSTNAME, BOT_STATUS, BOT_TOKEN, BOT_VARS = data[0]
                BOT_VARS = json.loads(BOT_VARS) if BOT_VARS else json.loads(BOT_VARS_)
                BOT_LZ = BOT_VARS['BOT_LZ']

                res = None
                extra_bot = Bot(token=BOT_TOKEN)
                if MSG_TYPE == 'web':
                    ext = FILE_NAME[FILE_NAME.rfind('.'):].lower()
                    print(f"ext = {ext}")

                    if ext in ['.png', '.jpg', '.jpeg']:
                        MSG_TYPE = 'photo'
                    elif ext in ['.gif', '.giff']:
                        MSG_TYPE = 'gif'
                    elif ext in ['.mp4']:
                        MSG_TYPE = 'video'
                    else:
                        MSG_TYPE = 'document'

                try:
                    MEDIA = FILE_NAME if IS_LINK else types.FSInputFile(FILE_NAME)
                    if MSG_TYPE == 'photo':
                        res = await extra_bot.send_photo(OWNER_TID, MEDIA, disable_notification=True)
                        file_id = res.photo[-1].file_id
                        file_type = 'photo'
                    elif MSG_TYPE in ['gif', 'animation']:
                        res = await extra_bot.send_animation(OWNER_TID, MEDIA, disable_notification=True)

                        print(f"febore {file_id=}, {file_type=}")
                        if res.animation:
                            file_id = res.animation.file_id
                            file_type = 'gif'
                        elif res.video:
                            file_id = res.video.file_id
                            file_type = 'video'

                        print(f"after {file_id=}, {file_type=}")
                    elif MSG_TYPE == 'video':
                        width = height = duration =None
                        if not IS_LINK:
                            try:
                                cap = cv2.VideoCapture(FILE_NAME)
                                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))

                                print(f"{width=}, {height=}")
                            except Exception as e:
                                logger.info(log_ % str(e))
                                await asyncio.sleep(round(random.uniform(0, 1), 2))

                        res = await extra_bot.send_video(chat_id=OWNER_TID,
                                                         video=MEDIA,
                                                         duration=duration,
                                                         width=width,
                                                         height=height,
                                                         disable_notification=True)

                        if res.video:
                            file_id = res.video.file_id
                            file_type = 'video'
                        elif res.animation:
                            file_id = res.animation.file_id
                            file_type = 'gif'
                    elif MSG_TYPE in ['video_note', 'telescope']:
                        FILE_NAME = await hand_video_note(FILE_NAME, IS_LINK, BOT_TID, MEDIA_D)

                        res = await extra_bot.send_video_note(OWNER_TID, types.FSInputFile(FILE_NAME),
                                                              disable_notification=True)

                        if res.video_note:
                            file_id = res.video_note.file_id
                            file_id_note = await send_video_my(extra_bot, OWNER_TID, MEDIA)
                            IS_LINK = 0
                            file_type = 'video_note'
                        elif res.animation:
                            file_id = res.animation.file_id
                            file_type = 'gif'
                        elif res.video:
                            file_id = res.video.file_id
                            file_type = 'video'
                    elif MSG_TYPE == 'audio':
                        F_NAME = FILE_NAME
                        # duration = None
                        if IS_LINK and FILE_NAME.lower().endswith('.mp4'):
                            prev = await download_file_my(MEDIA, BOT_TID, 'mp4', MEDIA_D)
                            MEDIA = types.FSInputFile(prev)

                        file_id, file_name_video = await send_audio_my(extra_bot, BOT_TID, BOT_USERNAME, BOT_FIRSTNAME,
                                                                       OWNER_TID, MEDIA, FILE_NAME,
                                                                       BASE_D, EXTRA_D)
                        if file_name_video:
                            if os.path.exists(FILE_NAME): os.remove(FILE_NAME)
                            print(f'del {FILE_NAME=}, остался {file_name_video=}')
                            FILE_NAME = file_name_video

                        file_type = 'audio'
                        if F_NAME != FILE_NAME and os.path.exists(F_NAME): os.remove(F_NAME)
                    elif MSG_TYPE == 'voice':
                        F_NAME = FILE_NAME
                        res = await extra_bot.send_voice(OWNER_TID, MEDIA, disable_notification=True)

                        if res.voice:
                            print('is +voice')
                            file_id = res.voice.file_id
                            file_type = 'voice'
                        elif res.audio:
                            print('is +audio')
                            file_id = res.audio.file_id
                            file_type = 'audio'

                        file_id_note, file_name_video = await send_audio_my(extra_bot, BOT_TID, BOT_USERNAME,
                                                                            BOT_FIRSTNAME, OWNER_TID, MEDIA,
                                                                            FILE_NAME, BASE_D, EXTRA_D)
                        if file_name_video:
                            if os.path.exists(FILE_NAME): os.remove(FILE_NAME)
                            print(f'del {FILE_NAME=}, остался {file_name_video=}')
                            FILE_NAME = file_name_video

                        if F_NAME != FILE_NAME and os.path.exists(F_NAME): os.remove(F_NAME)
                    elif MSG_TYPE == 'sticker':
                        F_NAME = FILE_NAME
                        print(f"1 проверяем FILE_NAME {os.path.exists(FILE_NAME)=}")
                        print(f"{IS_LINK=}, {FILE_NAME=}")
                        if IS_LINK:
                            F_NAME = await download_file_my(MEDIA, BOT_TID, FILE_NAME.split(".")[-1], MEDIA_D)

                        print(f"+++++++++++++++++++")
                        print(f"{F_NAME=}")
                        if F_NAME.endswith('.mp4'):
                            file_id, _ = await item_to_dynamic_sticker(extra_bot, OWNER_TID, F_NAME, 'sticker',
                                                                       'video', False, True, False, True)

                            file_type = 'sticker'
                            if F_NAME != FILE_NAME and os.path.exists(F_NAME): os.remove(F_NAME)
                            break
                        if F_NAME.endswith('.json'):
                            tgs_file_name = await convert_json_to_tgs(F_NAME)
                            print(f"{tgs_file_name=} jsjsjsjsjso tgtgsx")
                            F_NAME = tgs_file_name
                        if F_NAME.endswith(('.png', '.jpg')):
                            print(f"endswith png")
                            image = Image.open(F_NAME)
                            image = await correct_orientation(image)
                            dt = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
                            if F_NAME and os.path.exists(F_NAME): os.remove(F_NAME)
                            F_NAME = os.path.join(MEDIA_D, str(BOT_TID), dt)
                            FILE_NAME = F_NAME
                            await asyncio.sleep(0.05)
                            image.save(F_NAME, format="webp", quality=50)
                            if os.path.getsize(F_NAME) > 1048576: return
                            MEDIA = types.FSInputFile(F_NAME)
                        else:
                            print(f"else tgs")
                            MEDIA = types.FSInputFile(F_NAME)

                        res = await extra_bot.send_sticker(OWNER_TID, MEDIA)

                        if res.sticker:
                            file_id = res.sticker.file_id
                            file_type = 'sticker'
                        elif res.document:
                            file_id = res.document.file_id
                            file_type = 'document'

                        if F_NAME.lower().endswith('.webm') and not IS_LINK:
                            POST_FNAME1, ext = os.path.splitext(F_NAME)
                            POST_FNAME_COPY = os.path.join(MEDIA_D, str(BOT_TID),
                                                           f"{os.path.basename(POST_FNAME1)}_copy.mp4")

                            cmd = [
                                "ffmpeg", "-y", "-i", F_NAME,  # Входной файл
                                "-c:v", "libx264", "-preset", "fast", "-crf", "23",  # Настройки кодирования
                                "-c:a", "aac", "-b:a", "128k",  # Кодек для аудио
                                POST_FNAME_COPY  # Выходной файл
                            ]

                            process = await asyncio.create_subprocess_exec(
                                *cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE
                            )
                            stdout, stderr = await process.communicate()

                            if process.returncode == 0:
                                print(f"Конвертация завершена: {POST_FNAME_COPY}")
                            else:
                                print(f"Ошибка: {stderr.decode()}")
                            os.remove(FILE_NAME)
                            FILE_NAME = POST_FNAME_COPY

                        print(f"{file_type=}, {file_id=}")
                        print(f"првоеряем FILE_NAME {os.path.exists(FILE_NAME)=}")
                        if F_NAME != FILE_NAME and os.path.exists(F_NAME): os.remove(F_NAME)
                    else:
                        F_NAME = FILE_NAME
                        if IS_LINK:
                            F_NAME = await download_file_my(MEDIA, BOT_TID, FILE_NAME.split(".")[-1], MEDIA_D)
                            MEDIA = types.FSInputFile(F_NAME)

                        print(f"9116, {MEDIA=}")
                        thumb = types.FSInputFile(os.path.join(EXTRA_D, 'parse.jpg'))
                        res = await extra_bot.send_document(chat_id=OWNER_TID,
                                                            document=MEDIA,
                                                            disable_content_type_detection=True,
                                                            disable_notification=True,
                                                            thumbnail=thumb)

                        if res.sticker:
                            file_id = res.sticker.file_id
                            file_type = 'sticker'
                        elif res.document:
                            file_id = res.document.file_id
                            file_type = 'document'

                        # print(f"9123, {res=}")
                        if F_NAME != FILE_NAME and os.path.exists(F_NAME): os.remove(F_NAME)

                    if res: await extra_bot.delete_message(OWNER_TID, res.message_id)
                finally:
                    await extra_bot.session.close()

                print(f"{file_id=}, {file_id_note=}, {file_type=}")
                return
            except Exception as e:
                logger.info(log_ % str(e) + " (repeat)")

                if 'restricted' in str(e).lower():
                    file_id_note = 'restricted'
                    text = l_tools_has_restricted[BOT_LZ].format(BOT_USERNAME)
                    await bot.send_message(chat_id=OWNER_TID, text=text)
                    return

                if 'Internal Server Error' not in str(e): break
                await asyncio.sleep(6)
            finally:
                cnt += 1
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return file_id, file_id_note, file_type, FILE_NAME, IS_LINK, BOT_TOKEN


async def return_file_link(bot, chat_id, FILE_NAME, KEYS_JSON, MSG_VID, MSG_TYPE, IS_LINK):
    if MSG_TYPE == 'photo':
        result = photo_jpg
    elif MSG_TYPE in ['gif', 'animation']:
        result = gif_jpg
    elif MSG_TYPE == 'video':
        result = video_jpg
    elif MSG_TYPE in ['video_note', 'telescope']:
        result = video_note_jpg
    elif MSG_TYPE == 'audio':
        result = audio_jpg
    elif MSG_TYPE == 'voice':
        result = voice_jpg
    elif MSG_TYPE == 'sticker':
        result = sticker_jpg
    elif MSG_TYPE == 'web':
        result = web_jpg
    else:
        result = document_jpg

    try:
        print(f"here {FILE_NAME=}, {IS_LINK=}")
        if IS_LINK:
            result = FILE_NAME
            print(f'IS_LINK return_file_link: {result}')
        else:
            print(f'hare ai in FILE_NAME, {MSG_TYPE=}, {result=}')
            if MSG_TYPE in ['document', 'web'] and not FILE_NAME.endswith(
                ('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webp', '.webm', '.mp3')): return

            res = await get_link_for_media(bot, MSG_VID, FILE_NAME, KEYS_JSON)
            if res:
                result = res
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def jpg_video_preview(bot, chat_id, KEYS_JSON, file_link, BOT_TID, MSG_TYPE, file_id, BASE_D, MEDIA_D, BOT_TOKEN):
    result = None
    destination = destination2 = destination3 = None
    try:
        print(f"jpg_video_preview {file_link=}, {file_id=}, {chat_id=}")
        if MSG_TYPE == 'photo':
            result = photo_jpg
        elif MSG_TYPE in ['gif', 'animation']:
            result = gif_jpg
        elif MSG_TYPE == 'video':
            result = video_jpg
        elif MSG_TYPE in ['video_note', 'telescope']:
            result = video_note_jpg
        elif MSG_TYPE == 'audio':
            result = audio_jpg
        elif MSG_TYPE == 'voice':
            result = voice_jpg
        elif MSG_TYPE == 'sticker':
            result = sticker_jpg
        elif MSG_TYPE == 'web':
            result = web_jpg
        else:
            result = document_jpg
        tmpls = [photo_jpg, gif_jpg, video_jpg, video_note_jpg, audio_jpg, voice_jpg, sticker_jpg, web_jpg,
                 document_jpg]
        if not BOT_TOKEN or not file_id or file_link in tmpls: return

        # download
        dt_ = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')
        dt_2 = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f-2.jpg')
        dt_3 = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f-3.jpg')
        destination = os.path.join(MEDIA_D, str(BOT_TID), dt_)
        destination2 = os.path.join(MEDIA_D, str(BOT_TID), dt_2)
        destination3 = os.path.join(MEDIA_D, str(BOT_TID), dt_3)

        extra_bot = Bot(token=BOT_TOKEN)
        try:
            file = await extra_bot.get_file(file_id)
            await extra_bot.download_file(file.file_path, destination)
        finally:
            await extra_bot.session.close()

        # save frame to jpg
        try:
            clip = VideoFileClip(destination)
            frame_at_second = int(clip.duration / 2)
            frame = clip.get_frame(frame_at_second)
            new_image = Image.fromarray(frame)
            new_image.save(destination2)
        except Exception as e:
            logger.info(log_ % str(e) + str(file_link))
            # await asyncio.sleep(round(random.uniform(0, 1), 2))

            async with aiohttp.ClientSession() as session:
                async with session.get(file_link) as response:
                    if response.status == 200:
                        async with aiofiles.open(destination, "wb") as f:
                            async for chunk in response.content.iter_chunked(1024):
                                await f.write(chunk)

                        print(f"{destination=}")
                        print(f"{os.path.exists(destination)=}")
                        clip = VideoFileClip(destination)
                        frame_at_second = int(clip.duration / 2)
                        frame = clip.get_frame(frame_at_second)
                        new_image = Image.fromarray(frame)
                        new_image.save(destination2)

        print(f'hmm')
        # square jpg
        img = Image.open(destination2)
        img = await correct_orientation(img)
        width, height = img.size
        min_side = width if width < height else height
        min_side = min_side if min_side < 320 else 320
        half_square_side = int(min_side / 2)
        left_x = int(width / 2 - half_square_side)
        left_y = int(height / 2 - half_square_side)
        right_x = int(width / 2 + half_square_side)
        right_y = int(height / 2 + half_square_side)
        clip_convert = img.crop((left_x, left_y, right_x, right_y))
        clip_convert.save(destination3, quality=20)

        res = await get_link_for_media(bot, chat_id, destination3, KEYS_JSON)
        if res:
            result = res
    except Exception as e:
        logger.info(log_ % str(e) + str(file_link))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if destination and os.path.exists(destination): os.remove(destination)
        if destination2 and os.path.exists(destination2): os.remove(destination2)
        if destination3 and os.path.exists(destination3): os.remove(destination3)
        return result


async def jpg_photo_preview(bot, chat_id, KEYS_JSON, file_link, BOT_TID, MSG_TYPE, MEDIA_D):
    result = file_link
    try:
        print(f"jpg_photo_preview {file_link=}, {MSG_TYPE=}")
        if MSG_TYPE == 'photo':
            result = photo_jpg
        elif MSG_TYPE in ['gif', 'animation']:
            result = gif_jpg
        elif MSG_TYPE == 'video':
            result = video_jpg
        elif MSG_TYPE in ['video_note', 'telescope']:
            result = video_note_jpg
        elif MSG_TYPE == 'audio':
            result = audio_jpg
        elif MSG_TYPE == 'voice':
            result = voice_jpg
        elif MSG_TYPE == 'sticker':
            result = sticker_jpg
        elif MSG_TYPE == 'web':
            result = web_jpg
        else:
            result = document_jpg

        tmpls = [photo_jpg, gif_jpg, video_jpg, video_note_jpg, audio_jpg, voice_jpg, sticker_jpg, web_jpg,
                 document_jpg]
        if MSG_TYPE in ['audio', 'voice', 'document'] or file_link in tmpls or MSG_TYPE in [
            'web'] and not file_link.endswith(('.jpg', '.jpeg', '.png', '.webp', '.webm', '.mp4', '.gif')): return

        dt = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.jpg')
        dt_finish = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f-2.jpg')
        file_name = os.path.join(MEDIA_D, str(BOT_TID), dt)
        file_finish = os.path.join(MEDIA_D, str(BOT_TID), dt_finish)

        async with aiohttp.ClientSession() as session:
            async with session.get(file_link) as response:
                resp = await response.read()
                async with aiofiles.open(file_name, 'wb') as f:
                    await f.write(resp)
        if not os.path.exists(file_name): return

        # square jpg
        img = Image.open(file_name)
        img = await correct_orientation(img)
        img = img.convert('RGB')
        width, height = img.size
        min_side = width if width < height else height
        min_side = min_side if min_side < 320 else 320
        print(f"jpg_photo_preview: {min_side=}")
        half_square_side = int(min_side / 2)
        left_x = int(width / 2 - half_square_side)
        left_y = int(height / 2 - half_square_side)
        right_x = int(width / 2 + half_square_side)
        right_y = int(height / 2 + half_square_side)
        clip_convert = img.crop((left_x, left_y, right_x, right_y))
        clip_convert.save(file_finish, quality=20)

        res = await get_link_for_media(bot, chat_id, file_finish, KEYS_JSON)
        result = result if res is None else res
        if os.path.exists(file_name): os.remove(file_name)
        if os.path.exists(file_finish): os.remove(file_finish)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def resize_media(file_name, basewidth=1024):
    result = file_name
    try:
        if str(file_name).lower().endswith('.png'):
            im = Image.open(file_name)
            im = await correct_orientation(im)
            rgb_im = im.convert('RGB')
            tmp_name = os.path.join(os.path.dirname(file_name), get_name_without_ext(file_name) + '.jpg')
            rgb_im.save(tmp_name)
            if os.path.exists(file_name):
                os.remove(file_name)
            result = file_name = tmp_name

        img = Image.open(file_name)
        img = await correct_orientation(img)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        img.save(file_name)
        result = file_name
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def resize_video_note(file_name, basewidth):
    result = file_name
    try:
        if not str(file_name).lower().endswith('.mp4'):
            clip = VideoFileClip(file_name)
            tmp_name = os.path.join(os.path.dirname(file_name), 'r_' + os.path.basename(file_name))
            clip.write_videofile(tmp_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                 remove_temp=True)

            if os.path.exists(file_name):
                os.remove(file_name)
            file_name = os.path.join(os.path.dirname(file_name), get_name_without_ext(file_name) + '.mp4')
            if os.path.exists(tmp_name):
                os.rename(tmp_name, file_name)
            result = file_name
        if basewidth == 440:
            clip = VideoFileClip(file_name)
            clip_convert = Crop(x1=basewidth / 2, y1=basewidth / 2, x2=basewidth / 2, y2=basewidth / 2).apply(clip)
            # clip_convert.write_videofile(filename=file_video_note, codec='libx264', audio_codec='aac',
            #                              temp_audiofile='temp-audio.m4a', remove_temp=True)
            # clip_resized = clip.resize((basewidth, basewidth))
            tmp_name = os.path.join(os.path.dirname(file_name), 'r_' + os.path.basename(file_name))
            clip_convert.write_videofile(tmp_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                         remove_temp=True)
            if os.path.exists(file_name):
                os.remove(file_name)
            if os.path.exists(tmp_name):
                os.rename(tmp_name, file_name)
            result = file_name
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def hand_video_note(MEDIA, IS_LINK, BOT_TID, MEDIA_D):
    result = MEDIA
    try:
        file_name = MEDIA
        if IS_LINK:
            async with aiohttp.ClientSession() as session:
                async with session.get(MEDIA) as response:
                    resp = await response.read()

                    dt = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.mp4')
                    file_name = os.path.join(MEDIA_D, str(BOT_TID), dt)
                    async with aiofiles.open(file_name, 'wb') as f:
                        await f.write(resp)

        if os.path.exists(file_name):
            clip = VideoFileClip(file_name)
            # clip = clip.with_subclip(0, 59) if int(clip.duration) > 59 else clip
            clip = clip.subclipped(0, 59) if int(clip.duration) > 59 else clip
            width, height = clip.size
            min_side = min(width, height, 640)
            half_square_side = int(min_side / 2)

            left_x = width / 2 - half_square_side
            left_y = height / 2 - half_square_side
            right_x = width / 2 + half_square_side
            right_y = height / 2 + half_square_side

            tmp_name = os.path.join(os.path.dirname(file_name), 'r_' + os.path.basename(file_name))
            clip_convert = Crop(x1=left_x, y1=left_y, x2=right_x, y2=right_y).apply(clip)
            clip_convert.write_videofile(filename=tmp_name, codec='libx264', audio_codec='aac',
                                         temp_audiofile='temp-audio.m4a', remove_temp=True)
            if os.path.exists(file_name):
                os.remove(file_name)
            if os.path.exists(tmp_name):
                os.rename(tmp_name, file_name)
            print(f'success: {file_name}')
            result = file_name
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def send_audio_my(extra_bot, BOT_TID, BOT_USERNAME, BOT_FIRSTNAME, OWNER_TID, MEDIA, FILE_NAME, BASE_D, EXTRA_D):
    result = file_name_video = None
    try:
        cnt = 3
        while cnt > 0:
            try:
                performer = f'@{BOT_USERNAME}'
                title = BOT_FIRSTNAME
                thumb = types.FSInputFile(os.path.join(EXTRA_D, 'img.jpg'))

                duration = None
                print(f"{duration=}, {FILE_NAME=}")
                try:
                    # from mutagen.mp3 import MP3
                    # duration = int(MP3(FILE_NAME).info.length)
                    duration = int(AudioFileClip(FILE_NAME).duration)
                    print(f"{duration=}")
                except Exception as e:
                    logger.info(log_ % str(e))
                    # await asyncio.sleep(round(random.uniform(0, 1), 2))
                print(f"{duration=}")

                res = await extra_bot.send_audio(chat_id=OWNER_TID, audio=MEDIA, thumbnail=thumb, title=title,
                                                 duration=duration,
                                                 performer=performer, disable_notification=True)
                await extra_bot.delete_message(OWNER_TID, res.message_id)
                if res.audio: result = res.audio.file_id

                if not result or os.path.getsize(FILE_NAME) < 5242880:
                    print('inside')
                    audio_ = AudioFileClip(FILE_NAME)
                    video_clip = VideoClip(lambda t: np.zeros((480, 640, 3), dtype=np.uint8), duration=audio_.duration)
                    video_clip = video_clip.with_audio(audio_)
                    file_name_video = FILE_NAME[:FILE_NAME.rfind('.')] + '.mp4'
                    video_clip.write_videofile(file_name_video, codec="libx264", audio_codec="aac", fps=24)

                    res = await extra_bot.send_audio(chat_id=OWNER_TID, audio=types.FSInputFile(file_name_video),
                                                     thumbnail=thumb, title=title, performer=performer,
                                                     duration=duration,
                                                     disable_notification=True)
                    await extra_bot.delete_message(OWNER_TID, res.message_id)
                    # if os.path.exists(file_name_video): os.remove(file_name_video)
                    if res.audio and not result: result = res.audio.file_id
                break
            except Exception as e:
                logger.info(log_ % str(e) + " (repeat)")
                if 'Internal Server Error' not in str(e): break
                await asyncio.sleep(6)
            finally:
                cnt += 1
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result, file_name_video


async def send_video_my(extra_bot, OWNER_TID, MEDIA):
    result = None
    try:
        res = await extra_bot.send_video(chat_id=OWNER_TID, video=MEDIA, supports_streaming=True,
                                         disable_notification=True)
        result = res.video.file_id
        await extra_bot.delete_message(OWNER_TID, res.message_id)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def download_file_my(MEDIA, BOT_TID, ext, MEDIA_D):
    result = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(MEDIA) as response:
                resp = await response.read()

                dt = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.{ext}')
                file_name = os.path.join(MEDIA_D, str(BOT_TID), dt)
                async with aiofiles.open(file_name, 'wb') as f:
                    await f.write(resp)
                result = file_name
                print(f'download_file_my: {result}')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def facade_get_fid(bot, chat_id, KEYS_JSON, BOT_TID, dst, MSG_VID, msg_type, IS_LINK, BASE_D, EXTRA_D, MEDIA_D):
    tmp_json = {}
    FILE_NAME = None
    try:
        print(f"------------0----------, {msg_type=}, {os.path.exists(dst)=}")
        # print(f"------------0----------")
        file_id, file_id_note, file_type, FILE_NAME, IS_LINK, BOT_TOKEN = await return_file_id(bot, BOT_TID, dst,
                                                                                               msg_type, IS_LINK,
                                                                                               BASE_D, EXTRA_D, MEDIA_D)
        print(f"{dst=}, {FILE_NAME=}")
        print(f"{dst=}, {os.path.exists(FILE_NAME)=}")
        if os.path.exists(FILE_NAME) and FILE_NAME.endswith(('.json', '.tgs')):
            print(f"01")
            if dst.endswith('.json'):
                print(f"02")
                async with aiofiles.open(FILE_NAME, 'r', encoding='utf-8') as f:
                    file_json = json.loads(await f.read())
                    print(f"1")
            else:
                print(f"03")
                converted_path = await convert_tgs_to_json(FILE_NAME)
                if converted_path:
                    async with aiofiles.open(converted_path, 'r', encoding='utf-8') as f:
                        file_json = json.loads(await f.read())
                        print(f"2 jjj")
                if converted_path and os.path.exists(converted_path): os.remove(converted_path)

            file_link = sticker_jpg
            file_link2 = sticker_jpg
        else:
            print(f"04")
            file_link = await return_file_link(bot, chat_id, FILE_NAME, KEYS_JSON, MSG_VID, msg_type, IS_LINK)
            print(f"facade_get_fid: {file_link=}")

            if file_link.endswith(('.mp4', '.gif', '.webm', '.mov', '.mp3')):
                file_link2 = await jpg_video_preview(bot, MSG_VID, KEYS_JSON, file_link, BOT_TID, msg_type, file_id,
                                                     BASE_D, MEDIA_D, BOT_TOKEN)
            else:
                file_link2 = await jpg_photo_preview(bot, MSG_VID, KEYS_JSON, file_link, BOT_TID, msg_type, MEDIA_D)
            file_json = None

        tmp_json = {
            'file_id': str(file_id),
            'file_id_note': str(file_id_note),
            'fileb_id': str(file_id),
            'fileb_id_note': str(file_id_note),
            'file_type': str(file_type),
            'file_name': os.path.basename(FILE_NAME),
            'file_link': file_link,
            'file_link2': file_link2,
            'file_json': file_json,
        }
        r = {'file_id': str(file_id),
             'file_id_note': str(file_id_note),
             'file_type': str(file_type),
             'file_name': os.path.basename(FILE_NAME),
             'file_link': file_link,
             'file_link2': file_link2}
        print(f"{r=}")
    except Exception as e:
        # logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        if FILE_NAME and os.path.exists(FILE_NAME): os.remove(FILE_NAME)
        return tmp_json


async def convert_png_to_gif(input_name, output_name):
    result = None
    try:
        image = Image.open(input_name)
        image = await correct_orientation(image)
        frames = [image.copy(), ImageOps.grayscale(image)]

        frames[0].save(output_name, save_all=True, append_images=frames[1:], duration=500, loop=0, optimize=True)
        result = output_name if os.path.exists(output_name) else None
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def convert_png_to_mp4(ENT_TID, input_name, output_name, MEDIA_D):
    result = None
    try:
        tmp_gif = os.path.join(MEDIA_D, str(ENT_TID), datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.gif'))
        tmp_gif = await convert_png_to_gif(input_name, tmp_gif)

        clip = VideoFileClip(tmp_gif)
        clip = concatenate_videoclips([clip] * 6, method="compose")
        clip.write_videofile(output_name, fps=24)
        if os.path.exists(tmp_gif): os.remove(tmp_gif)

        result = output_name if os.path.exists(output_name) else None
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def item_to_static_sticker(bot, chat_id, input_file, PACK_TYPE, PACK_KIND, is_upload=True, is_circle=False,
                                 is_rbg=False):
    result = result_upl = None
    file_jpg = input_file[:input_file.rfind('.')] + '_.jpg'
    file_png = input_file[:input_file.rfind('.')] + '_.png'
    try:
        print(f"item_to_static_sticker starting..")
        size_kb = 512000
        if PACK_KIND == 'video':
            size_kb = 256000
        elif PACK_KIND == 'animated':
            size_kb = 64000
        pixels = (100, 100) if PACK_TYPE == 'emoji' else (512, 512)
        sticker_format = 'static'
        quality = 10 if os.path.getsize(input_file) > 200000 else 75
        print(f"{os.path.getsize(input_file)=}, {quality=}")

        # region pre
        if input_file.lower().endswith('.webp') and os.path.getsize(input_file) <= size_kb:
            image = Image.open(input_file)
            width, height = image.size
            print(f"{width=}, {height=}")
            if PACK_TYPE == 'emoji' and width == 100 and height == 100:
                if width < 100 and height < 100:
                    target_width, target_height = 512, 512
                    image_ratio = image.width / image.height
                    target_ratio = target_width / target_height

                    if image_ratio > target_ratio:
                        new_width = target_width
                        new_height = int(target_width / image_ratio)
                    else:
                        new_height = target_height
                        new_width = int(target_height * image_ratio)
                    image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)

                    left = (new_width - target_width) // 2
                    top = (new_height - target_height) // 2
                    right = left + target_width
                    bottom = top + target_height
                    image = image.crop((left, top, right, bottom))
                    image.save(input_file, format="WEBP")
                    image.close()

                upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(input_file),
                                                    sticker_format=sticker_format)
                result_upl = upl.file_id

                if not is_upload:
                    result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(input_file))
                    if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
                    result = result.sticker.file_id
                return
            elif PACK_TYPE == 'sticker' and width <= 512 and height <= 512:
                if width < 512 and height < 512:
                    target_width, target_height = 512, 512
                    image_ratio = image.width / image.height
                    target_ratio = target_width / target_height

                    if image_ratio > target_ratio:
                        new_width = target_width
                        new_height = int(target_width / image_ratio)
                    else:
                        new_height = target_height
                        new_width = int(target_height * image_ratio)
                    image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)

                    left = (new_width - target_width) // 2
                    top = (new_height - target_height) // 2
                    right = left + target_width
                    bottom = top + target_height
                    image = image.crop((left, top, right, bottom))
                    image.save(input_file, format="WEBP")
                    image.close()

                upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(input_file),
                                                    sticker_format=sticker_format)
                result_upl = upl.file_id

                if not is_upload:
                    result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(input_file))
                    if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
                    result = result.sticker.file_id
                return
        elif input_file.lower().endswith('.tgs') and os.path.getsize(input_file) <= size_kb:
            upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(input_file),
                                                sticker_format=sticker_format)
            result_upl = upl.file_id

            if not is_upload:
                result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(input_file))
                if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
                result = result.sticker.file_id
            return
        # endregion

        # region pixels
        image = Image.open(input_file)
        image = await correct_orientation(image)
        width, height = image.size
        left = (width - min(width, height)) // 2
        top = (height - min(width, height)) // 2
        right = (width + min(width, height)) // 2
        bottom = (height + min(width, height)) // 2
        image = image.crop((left, top, right, bottom))
        if width < pixels[0] and height < pixels[1]:
            target_width, target_height = pixels
            image_ratio = image.width / image.height
            target_ratio = target_width / target_height

            if image_ratio > target_ratio:
                new_width = target_width
                new_height = int(target_width / image_ratio)
            else:
                new_height = target_height
                new_width = int(target_height * image_ratio)
            image = image.resize((new_width, new_height), resample=Image.Resampling.LANCZOS)
        else:
            image = image.resize(pixels, resample=Image.Resampling.LANCZOS)
        image = image.convert("RGB")
        image.save(file_jpg, format="JPEG", quality=quality, optimize=True, lossless=False, method=6)
        image.close()
        # endregion

        # region size
        quality = quality
        while quality > 0:
            img = Image.open(file_jpg)
            # img = await correct_orientation(img)
            img.save(file_jpg, format="JPEG", quality=quality)

            if os.path.getsize(file_jpg) < size_kb: break
            quality = 1 if quality == 0 else quality - 10
        if os.path.getsize(file_jpg) > size_kb: return
        # endregion

        # region is_circle
        rad = 25
        fill_ = 255
        image = Image.open(file_jpg)
        # image = await correct_orientation(image)
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)

        if is_circle:
            # draw.ellipse((0, 0, image.width, image.height), fill=255)
            left, top, right, bottom = (0, 0, image.width, image.height)
            draw.pieslice(((left, top), (right, bottom)), 0, 360, fill=fill_, outline=fill_)
        else:
            left, top, right, bottom = (0, 0, image.width, image.height)
            draw.pieslice(((left, top), (left + 2 * rad, top + 2 * rad)), 180, 270, fill=fill_, outline=fill_)
            draw.pieslice(((right - 2 * rad, top), (right, top + 2 * rad)), 270, 0, fill=fill_, outline=fill_)
            draw.pieslice(((left, bottom - 2 * rad), (left + 2 * rad, bottom)), 90, 180, fill=fill_, outline=fill_)
            draw.pieslice(((right - 2 * rad, bottom - 2 * rad), (right, bottom)), 0, 90, fill=fill_, outline=fill_)
            draw.rectangle((left + rad, top, right - rad, bottom), fill=fill_)
            draw.rectangle((left, top + rad, right, bottom - rad), fill=fill_)
        res = Image.new('RGBA', image.size, (0, 0, 0, 0))
        res.paste(image, mask=mask)
        res.save(file_png, format="PNG", quality=90, optimize=True, lossless=False, method=6)
        res.close()
        # endregion

        # region rbg
        try:
            if is_rbg:
                img = Image.open(file_png)
                # img = await correct_orientation(img)
                output_ = remove(img)
                output_.save(file_png)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        if is_upload:
            upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(file_png),
                                                sticker_format=sticker_format)
            result_upl = upl.file_id
        else:
            result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(file_png))
            result = result.sticker.file_id
        print(f"result_upl ok")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
        if 'too big' in str(e):
            await bot.send_message(chat_id=chat_id, text=l_post_sticker_toobig['en'])
    finally:
        try:
            print(f"item_to_static_sticker finishing..")
            if os.path.exists(file_jpg): os.remove(file_jpg)
            if os.path.exists(file_png): os.remove(file_png)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        return result, result_upl


async def item_to_dynamic_sticker(bot, chat_id, input_file, PACK_TYPE, PACK_KIND, is_upload=True, is_circle=False,
                                  is_rbg=False, is_del=False):
    result = result_upl = None
    file_jpg = input_file[:input_file.rfind('.')] + '_.jpg'
    file_mp4 = input_file[:input_file.rfind('.')] + '_.mp4'
    file_png = input_file[:input_file.rfind('.')] + '_.png'
    file_gray_png = input_file[:input_file.rfind('.')] + 'gray.png'
    file_webm = input_file[:input_file.rfind('.')] + '_.webm'
    spec_dir = os.path.join(os.path.dirname(input_file), 'spec')
    try:
        print(f"item_to_dynamic_sticker")

        # region data
        size_kb = 512000
        if PACK_KIND == 'video':
            size_kb = 256000
        elif PACK_KIND == 'animated':
            size_kb = 64000

        rad = 25
        fps = 30
        fill_ = 255
        bitrate = '60k'
        rounded = 'null'
        i_input_data = f'{spec_dir}/frame_%04d.png'
        os.makedirs(spec_dir, exist_ok=True, mode=0o777)
        pixels = (100, 100) if PACK_TYPE == 'emoji' else (512, 512)
        pixels_str = '100x100' if PACK_TYPE == 'emoji' else '512x512'
        side_sz = 100 if PACK_TYPE == 'emoji' else 512
        sticker_format = PACK_KIND
        quality = 20 if os.path.getsize(input_file) > 500000 else 90
        print(f"{os.path.getsize(input_file)=}, {quality=}")
        # endregion

        # region pre
        print(f"{input_file.lower().endswith('.webm')=}, {input_file=}")
        print(f"{os.path.getsize(input_file)=} , ? {size_kb=}, {PACK_TYPE=}")
        if input_file.lower().endswith('.webm') and os.path.getsize(input_file) <= size_kb:
            if PACK_TYPE == 'emoji':  # and width == 100 and height == 100 and input_file.lower().endswith('.webm'):
                upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(input_file),
                                                    sticker_format=sticker_format)
                result_upl = upl.file_id

                if not is_upload:
                    result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(input_file))
                    if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
                    result = result.sticker.file_id
                return
            elif PACK_TYPE == 'sticker':  # and width <= 512 and height <= 512 and input_file.lower().endswith('.webm'):
                print(f"here 1")
                upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(input_file),
                                                    sticker_format=sticker_format)
                result_upl = upl.file_id
                print(f"here 2")

                if not is_upload:
                    result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(input_file))
                    if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
                    result = result.sticker.file_id
                    # await bot.send_sticker(chat_id=chat_id, sticker=result)
                return
        elif input_file.lower().endswith('.tgs') and os.path.getsize(input_file) <= size_kb:
            upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(input_file),
                                                sticker_format=sticker_format)
            result_upl = upl.file_id

            if not is_upload:
                result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(input_file))
                if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
                result = result.sticker.file_id
            return
        # endregion

        if input_file.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            frames = 12
            bitrate = '100k'

            # region pixels
            print(f"pixels")
            image = Image.open(input_file)
            image = await correct_orientation(image)
            width, height = image.size
            left = (width - min(width, height)) // 2
            top = (height - min(width, height)) // 2
            right = (width + min(width, height)) // 2
            bottom = (height + min(width, height)) // 2
            image = image.crop((left, top, right, bottom))
            image = image.resize(pixels, resample=Image.Resampling.LANCZOS)
            image = image.convert("RGB")
            image.save(file_jpg, format="JPEG", quality=quality, optimize=True, lossless=False, method=6)
            image.close()
            # endregion

            # region size
            print(f"size")
            quality = quality
            while quality > 0:
                img = Image.open(file_jpg)
                img.save(file_jpg, format="JPEG", quality=quality)

                if os.path.getsize(file_jpg) < size_kb: break
                quality = 1 if quality == 0 else quality - 10
            if os.path.getsize(file_jpg) > size_kb: return
            # endregion

            # region color
            print(f"color")
            img = Image.open(file_jpg)
            img = await correct_orientation(img)
            img = img.convert("RGBA")

            img.save(file_png, format="PNG", quality=90, optimize=True, lossless=False, method=6)
            # endregion

            # region gray
            print(f"gray")
            img = Image.open(file_jpg)
            img = ImageOps.grayscale(img)
            img = img.convert("RGBA")
            img.save(file_gray_png, format="PNG", quality=90, optimize=True, lossless=False, method=6)
            img.close()
            # endregion

            for it_png in [file_png, file_gray_png]:
                try:
                    # region is_circle
                    image = Image.open(it_png)
                    mask = Image.new('L', image.size, 0)
                    draw = ImageDraw.Draw(mask)

                    if is_circle:
                        left, top, right, bottom = (0, 0, image.width, image.height)
                        draw.pieslice(((left, top), (right, bottom)), 0, 360, fill=fill_, outline=fill_)
                    else:
                        left, top, right, bottom = (0, 0, image.width, image.height)
                        draw.pieslice(((left, top), (left + 2 * rad, top + 2 * rad)), 180, 270, fill=fill_,
                                      outline=fill_)
                        draw.pieslice(((right - 2 * rad, top), (right, top + 2 * rad)), 270, 0, fill=fill_,
                                      outline=fill_)
                        draw.pieslice(((left, bottom - 2 * rad), (left + 2 * rad, bottom)), 90, 180, fill=fill_,
                                      outline=fill_)
                        draw.pieslice(((right - 2 * rad, bottom - 2 * rad), (right, bottom)), 0, 90, fill=fill_,
                                      outline=fill_)
                        draw.rectangle((left + rad, top, right - rad, bottom), fill=fill_)
                        draw.rectangle((left, top + rad, right, bottom - rad), fill=fill_)

                    res = Image.new('RGBA', image.size, (0, 0, 0, 0))
                    res.paste(image, mask=mask)
                    res.save(it_png, format="PNG", quality=90, optimize=True, lossless=False, method=6)
                    res.close()
                    # endregion

                    # region rbg
                    if is_rbg:
                        img = Image.open(it_png)
                        output_ = remove(img)
                        output_.save(it_png)  # endregion
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

            print(f"range")
            for i in range(0, frames * 2):
                it_png = file_png if i < frames else file_gray_png
                shutil.copy(it_png, f"{spec_dir}/frame_{i:04d}.png")
        else:
            try:
                if not is_circle and PACK_TYPE == 'sticker':
                    cap = cv2.VideoCapture(input_file)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    cap.release()

                    # clip = mp.VideoFileClip(input_file)
                    # width, height = clip.size

                    if width != height and (width > side_sz or height > side_sz):
                        if width > height:
                            pixels_str = f"{side_sz}x{int(side_sz * (height / width))}"
                        else:
                            pixels_str = f"{int(side_sz * (width / height))}x{side_sz}"
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

            try:
                ffmpeg_command = ['ffmpeg', '-i', input_file, '-filter_complex_threads', '2', '-r', str(fps), '-b:v',
                                  '40k', '-crf', '30', '-s', pixels_str, '-t', '3', '-an', '-y', file_mp4]
                p = await asyncio.create_subprocess_exec(*ffmpeg_command)
                await p.communicate()

                if os.path.exists(input_file): os.remove(input_file)
                input_file = file_mp4
                i_input_data = input_file
                print('end', pixels_str)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

            if is_circle:
                rounded = '[0:v]crop=ih:ih[video square];[video square]split=3[black canvas][white canvas][video square];[black canvas]setsar=1:1,drawbox=color=black@1:t=fill[black background];[white canvas]scale=w=iw*2:h=iw*2,format=yuva444p,geq=lum=\'p(X,Y)\':a=\'st(1,pow(min(W/2,H/2),2))+st(3,pow(X-(W/2),2)+pow(Y-(H/2),2));if(lte(ld(3),ld(1)),255,0)\',drawbox=color=white@1:t=fill[scaled up white circle];[scaled up white circle]scale=w=iw/2:h=iw/2[white circle];[black background][white circle]overlay[alpha mask];[video square][alpha mask]alphamerge,format=yuva420p'
            else:
                # rounded = f'split[s0][s1];[s0]pad=width={side_sz}:height={side_sz}:color=black[s2];[s1]scale={side_sz}:{side_sz}:force_original_aspect_ratio=decrease[s3];[s2][s3]overlay=W-w-1:H-h-1,setsar=1'
                # rounded = 'split[s0][s1];[s0]pad=width=512:height=512:color=black[s2];[s1]scale=512:512:force_original_aspect_ratio=decrease[s3];[s2][s3]overlay=W-w-1:H-h-1,drawbox=0:0:iw:ih:color=black@0.0[rounded]'
                print(f'here 2, {i_input_data=}, {os.path.exists(input_file)=}')

        ffmpeg_command = ['ffmpeg', '-i', i_input_data, '-filter_complex', rounded, '-filter_complex_threads', '2',
                          '-c:v', 'libvpx-vp9', '-r', str(fps), '-b:v', bitrate, '-crf', '30', '-s', pixels_str,
                          '-pix_fmt', 'yuva420p', '-t', '3', '-an', '-y', file_webm]
        print(f"{ffmpeg_command=}")
        p = await asyncio.create_subprocess_exec(*ffmpeg_command)
        await p.communicate()

        # region webm
        # images = []
        # for it_png in sorted(os.listdir(spec_dir)):
        #     images.append(np.array(Image.open(os.path.join(spec_dir, it_png))))
        # with imageio.get_writer(file_webm, mode='I', fps=fps, codec='libvpx-vp9', pixelformat='yuva420p') as writer:
        #     for image in images:
        #         try:
        #             writer.append_data(image)
        #             for _ in range(frames): writer.append_data(image)
        #         except Exception as e:
        #             logger.info(log_ % str(e))
        #             await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        if is_upload:
            upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(file_webm),
                                                sticker_format=sticker_format)
            result_upl = upl.file_id
        else:
            result = await bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(file_webm))
            if is_del: await bot.delete_message(chat_id=chat_id, message_id=result.message_id)
            result = result.sticker.file_id

            # upl = await bot.upload_sticker_file(user_id=chat_id, sticker=types.FSInputFile(file_webm),  #                                     sticker_format=sticker_format)  # result_upl = upl.file_id  #  # tmp_name = f"by_{chat_id}_{str(time.time()).split('.')[-1]}_by_{bot_username}"  # sticker = types.InputSticker(sticker=result_upl, emoji_list=['👩🏽‍💻'], format='video')  # await bot.create_new_sticker_set(user_id=chat_id,  #                                  name=tmp_name,  #                                  title=str_empty,  #                                  stickers=[sticker],  #                                  sticker_type=PACK_TYPE,  #                                  # sticker_format=sticker_format,  #                                  needs_repainting=None)  # get_sticker_set_ = await bot.get_sticker_set(name=tmp_name)  # result = await bot.send_sticker(chat_id, get_sticker_set_.stickers[0].file_id)  # await bot.delete_sticker_set(tmp_name)  # result = result.sticker.file_id
        print(f"result_upl ok")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
        if 'too big' in str(e):
            await bot.send_message(chat_id=chat_id, text=l_post_sticker_toobig['en'])
    finally:
        try:
            if os.path.exists(spec_dir): shutil.rmtree(spec_dir)
            if os.path.exists(file_mp4): os.remove(file_mp4)
            if os.path.exists(file_jpg): os.remove(file_jpg)
            if os.path.exists(file_png): os.remove(file_png)
            if os.path.exists(file_webm): os.remove(file_webm)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        return result, result_upl


async def squared_video_ffmpeg(file_name, MEDIA_D):
    result = None
    try:
        clip = VideoFileClip(file_name)
        width, height = clip.size
        min_side = width if width < height else height
        min_side = 640 if min_side > 640 else min_side
        file_name_part2 = f"{datetime.now(timezone.utc).strftime('r_%d-%m-%Y_%H-%M-%S-%f.mp4')}"
        file_video_note = os.path.join(MEDIA_D, file_name_part2)
        center_x = int(width / 2) - int(min_side / 2)
        center_y = int(height / 2) - int(min_side / 2)

        ffmpeg_command = ['ffmpeg', '-i', file_name, '-filter_complex_threads', '2', '-vf',
                          f'scale={min_side}:{min_side},setsar=1:1', '-r', '30', '-s', f'{min_side}x{min_side}', '-vf',
                          f'crop={min_side}:{min_side}:{center_x}:{center_y}', '-t', '59', '-y', file_video_note]
        p = await asyncio.create_subprocess_exec(*ffmpeg_command)
        await p.communicate()
        result = file_video_note
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


def handle_ver(emj, emj_data, entities_list):
    entities_list.append(
        {'match_start': emj_data.get('match_start'), 'match_end': emj_data.get('match_end'), 'emoji': emj})
    return str(None)


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html.strip())
    return cleantext


async def format_text_md(txt, is_web=False):
    result = txt
    try:
        if format_text == '': return
        result = result[0].upper() + result[1:]
        tmp_arr = re.split(r'\s+', result)
        entities = []
        emoji.demojize(string=tmp_arr[0], language='en', version=-1,
                       handle_version=lambda emj, emj_data: handle_ver(emj, emj_data, entities))
        distinct_list = list({e['emoji'] for e in entities})
        is_first_emoji = True if len(distinct_list) else False
        # is_first_emoji = any(unicodedata.category(c).startswith('So') for c in result)
        sym_lst = ('<', '>', '#', '$', '=', '*', '_', '|', '[', '~', '{', '`')

        if not is_first_emoji and len(tmp_arr) > 0:
            if not tmp_arr[0].startswith(sym_lst):
                result = result.replace(tmp_arr[0], f"*{tmp_arr[0]}*", 1)

        if not is_first_emoji:
            item = random.choice(emojis_)
            result = f"{item} {result}"

        tmp_arr = re.split(r'\s+', result)
        if len(tmp_arr) > 2 and not tmp_arr[1].startswith(sym_lst):
            result = result.replace(tmp_arr[1], f"*{tmp_arr[1]}*", 1)

        # italic
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'italic: {word}')
                # result = result.replace(word, f"_{word}_")
                word_pattern = re.escape(word)  # Экранируем специальные символы в слове
                result = re.sub(rf'\b{word_pattern}\b', f"_{word}_", result)
                break

        # spoiler
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'spoiler: {word}')
                # result = result.replace(word, f"||{word}||")
                word_pattern = re.escape(word)  # Экранируем специальные символы в слове
                result = re.sub(rf'\b{word_pattern}\b', f"||{word}||", result)
                break

        # under
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'under: {word}')
                # result = result.replace(word, f"__{word}__")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"__{word}__", result)
                break

        # bold
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'bold: {word}')
                # result = result.replace(word, f"*{word}*")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"*{word}*", result)
                break

        # mono
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'mono: {word}')
                # result = result.replace(word, f"`{word}`")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"`{word}`", result)
                break

        if not is_web:
            # quote
            tmp_arr = re.split(r'\s+', result)
            i = min(len(tmp_arr), 15)
            while i > 0:
                i -= 1
                r_i = random.randint(0, len(tmp_arr) - 1)
                word = tmp_arr[r_i]
                if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                        map(lambda c: c.isascii() and not c.isalnum(), word))):
                    word_pattern = re.escape(word)
                    result = re.sub(rf'\b{word_pattern}\b', f">{word}", result)
                    break

            # pre
            tmp_arr = re.split(r'\s+', result)
            i = min(len(tmp_arr), 15)
            while i > 0:
                i -= 1
                r_i = random.randint(0, len(tmp_arr) - 1)
                word = tmp_arr[r_i]
                if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                        map(lambda c: c.isascii() and not c.isalnum(), word))):
                    # print(f'quote: {word}')
                    # result = result.replace(word, f"```\n{word}```")
                    word_pattern = re.escape(word)
                    result = re.sub(rf'\b{word_pattern}\b', f"```{word}```", result)
                    break

            # py  # tmp_arr = re.split(r'\s+', result)  # i = min(len(tmp_arr), 15)  # while i > 0:  #     i -= 1  #     r_i = random.randint(0, len(tmp_arr) - 1)  #     word = tmp_arr[r_i]  #     if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(  #             sym_lst) and not any(  #         map(lambda c: c.isascii() and not c.isalnum(), word))):  #         # print(f'python: {word}')  #         # result = result.replace(word, f"```py\n{word}```")  #         word_pattern = re.escape(word)  #         result = re.sub(rf'\b{word_pattern}\b', f"```py\n{word}```", result)  #         break

        # hashtag
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'hashtag: {word}')
                # result = result.replace(word, f"#{word}")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"#{word}", result)
                break

        # tmp_arr = re.split(r'\s+', result)
        # i = min(len(tmp_arr), 15)
        # while i > 0:
        #     i -= 1
        #     r_i = random.randint(0, len(tmp_arr) - 1)
        #     word = tmp_arr[r_i]
        #     if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(
        #         sym_lst) and not any(
        #         map(lambda c: c.isascii() and not c.isalnum(), word))):
        #         print(f'cashtag: {word}')
        #         result = result.replace(word, f"${word}")
        #         break

        result = result.replace('( ', '(')
        result = result.replace(' )', ')')
        result = result.replace(' ,', ',')
    except Exception as e:
        logger.info(log_ % e)
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def format_link_md(txt):
    result = txt
    try:
        if format_text == '': return
        tmp_arr = re.split(r'\s+', result)
        arr_links = []
        arr_tlg_links = []

        for item in tmp_arr:
            if item.lower().startswith('https://t.me/') and item not in arr_tlg_links:
                arr_tlg_links.append(item)
            elif item.lower().startswith('https://') and item not in arr_links:
                arr_links.append(item)

        for tlg_link in arr_tlg_links:
            tmp1 = tlg_link.lower().split("https://t.me/")
            if len(tmp1) < 2: continue
            tmp2 = tmp1[1].split('/')
            link_name = tmp2[0].replace(',', '')
            arr_tlg_links_item = tlg_link.replace(',', '')
            result = result.replace(arr_tlg_links_item,
                                    f"[{link_name}]({arr_tlg_links_item.strip()})")  # [inline URL](http://www.example.com/)

        for link in arr_links:
            tmp1 = link.lower().split("https://")
            if len(tmp1) < 2: continue
            tmp2 = tmp1[1].split('/')
            link_name = tmp2[0]
            result = result.replace(link, f"[{link_name}]({link.strip()})")

        # if result == txt and 'https://' in txt and 'href=' in txt:  #     ix1 = str(result).find('href=')  #     ix2 = str(result).find('">', ix1)  #     tmp1 = result[ix1 + len('href="'):ix2]  #     tmp2 = tmp1.split("https://")[1].split('/')[0]  #     result = result.replace(f'>{tmp1}</a>', f'>{tmp2}</a>')
    except Exception as e:
        logger.info(log_ % e)
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def format_text(txt, is_web=False, is_color=False, is_userbot=False):
    result = txt
    try:
        if txt.strip() == '': return
        result = result[0].upper() + result[1:]
        tmp_arr = re.split(r'\s+', result)
        entities = []
        emoji.demojize(string=tmp_arr[0], language='en', version=-1,
                       handle_version=lambda emj, emj_data: handle_ver(emj, emj_data, entities))
        distinct_list = list({e['emoji'] for e in entities})
        is_first_emoji = True if len(distinct_list) else False
        # is_first_emoji = any(unicodedata.category(c).startswith('So') for c in result)
        sym_lst = ('<', '>', '#', '$', '=', 'href')

        if not is_first_emoji and len(tmp_arr) > 0:
            if not tmp_arr[0].startswith(('<', '#', '$', '=', 'href')):
                result = result.replace(tmp_arr[0], f"<b>{tmp_arr[0]}</b>", 1)

        if not is_first_emoji:
            item = random.choice(emojis_)
            result = f"{item} {result}"

        tmp_arr = re.split(r'\s+', result)
        if len(tmp_arr) > 2 and not tmp_arr[1].startswith(sym_lst):
            result = result.replace(tmp_arr[1], f"<b>{tmp_arr[1]}</b>", 1)

        # italic
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'italic: {word}')
                # result = result.replace(word, f"<i>{word}</i>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"<i>{word}</i>", result)
                break

        # spoiler
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'spoiler: {word}')
                # result = result.replace(word, f"<tg-spoiler>{word}</tg-spoiler>")
                word_pattern = re.escape(word)
                spoiler_tag = 'spoiler' if is_userbot else 'tg-spoiler'
                result = re.sub(rf'\b{word_pattern}\b', f"<{spoiler_tag}>{word}</{spoiler_tag}>", result)
                break

        # under
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'under: {word}')
                # result = result.replace(word, f"<u>{word}</u>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"<u>{word}</u>", result)
                break

        # bold
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'bold: {word}')
                # result = result.replace(word, f"<b>{word}</b>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"<b>{word}</b>", result)
                break

        # code
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'mono: {word}')
                # result = result.replace(word, f"<code>{word}</code>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"<code>{word}</code>", result)
                break

        # if not is_web:
        #     print(f"foramt {is_web=}")
        #     # quote
        #     if '\n\n' in result and '\n\n\n' not in result:
        #         from typing import List
        #         elements: List[str] = result.split('\n\n')
        #         if len(elements) > 1:
        #             elements[1] = f"<blockquote>{elements[1]}</blockquote>"
        #         result = '\n\n'.join(elements)
        #     else:
        #         tmp_arr = re.split(r'\s+', result)
        #         i = min(len(tmp_arr), 15)
        #         while i > 0:
        #             i -= 1
        #             r_i = random.randint(0, len(tmp_arr) - 1)
        #             word = tmp_arr[r_i]
        #             if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
        #                     map(lambda c: c.isascii() and not c.isalnum(), word))):
        #                 # print(f'quote: {word}')
        #                 # result = result.replace(word, f"<blockquote>{word}</blockquote>")
        #                 word_pattern = re.escape(word)
        #                 result = re.sub(rf'\b{word_pattern}\b', f"<blockquote>{word}</blockquote>", result)
        #                 break
        #
        #     # pre
        #     tmp_arr = re.split(r'\s+', result)
        #     i = min(len(tmp_arr), 15)
        #     while i > 0:
        #         i -= 1
        #         r_i = random.randint(0, len(tmp_arr) - 1)
        #         word = tmp_arr[r_i]
        #         if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
        #                 map(lambda c: c.isascii() and not c.isalnum(), word))):
        #             # print(f'python: {word}')
        #             # result = result.replace(word, f"<pre>py\n{word}</pre>")
        #             word_pattern = re.escape(word)
        #             result = re.sub(rf'\b{word_pattern}\b', f"<pre>{word}</pre>", result)
        #             break

        # pre
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'python: {word}')
                # result = result.replace(word, f"<pre>py\n{word}</pre>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"<pre>{word}</pre>", result)
                break

        # quote
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'mono: {word}')
                # result = result.replace(word, f"<code>{word}</code>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"<blockquote>{word}</blockquote>", result)
                break

        # hashtag
        tmp_arr = re.split(r'\s+', result)
        i = min(len(tmp_arr), 15)
        while i > 0:
            i -= 1
            r_i = random.randint(0, len(tmp_arr) - 1)
            word = tmp_arr[r_i]
            if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(sym_lst) and not any(
                    map(lambda c: c.isascii() and not c.isalnum(), word))):
                # print(f'hashtag: {word}')
                # result = result.replace(word, f"<span>#{word}</span>")
                word_pattern = re.escape(word)
                result = re.sub(rf'\b{word_pattern}\b', f"#{word}", result)
                break

        # tmp_arr = re.split(r'\s+', result)
        # i = min(len(tmp_arr), 15)
        # while i > 0:
        #     i -= 1
        #     r_i = random.randint(0, len(tmp_arr) - 1)
        #     word = tmp_arr[r_i]
        #     if (0 < r_i < len(tmp_arr) - 1 and len(word) >= 4 and not word.startswith(
        #         sym_lst) and not any(map(lambda c: c.isascii() and not c.isalnum(), word))):
        #         print(f'cashtag: {word}')
        #         result = result.replace(word, f"<span>${word}</span>")
        #         break

        is_color = None
        result = result.replace('( ', '(')
        result = result.replace(' )', ')')
        result = result.replace(' ,', ',')
    except Exception as e:
        logger.info(log_ % str(e) + str(is_color))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def format_link(txt):
    result = txt
    try:
        if txt.strip() == '': return
        tmp_arr = re.split(r'\s+', result)
        arr_links = []
        arr_tlg_links = []

        for item in tmp_arr:
            if item.lower().startswith('https://t.me/') and item not in arr_tlg_links:
                arr_tlg_links.append(item)
            elif item.lower().startswith('https://') and item not in arr_links:
                arr_links.append(item)

        for tlg_link in arr_tlg_links:
            tmp1 = tlg_link.lower().split("https://t.me/")
            if len(tmp1) < 2: continue
            tmp2 = tmp1[1].split('/')
            link_name = tmp2[0].replace(',', '')
            arr_tlg_links_item = tlg_link.replace(',', '')
            result = result.replace(arr_tlg_links_item, f"<a href='{arr_tlg_links_item.strip()}'>{link_name}</a>")

        for link in arr_links:
            tmp1 = link.lower().split("https://")
            if len(tmp1) < 2: continue
            tmp2 = tmp1[1].split('/')
            link_name = tmp2[0]
            result = result.replace(link, f"<a href='{link.strip()}'>{link_name}</a>")

        if result == txt and 'https://' in txt and 'href="' in txt:
            ix1 = str(result).find('href="')
            ix2 = str(result).find('">', ix1)
            tmp1 = result[ix1 + len('href="'):ix2]
            tmp2 = tmp1.split("https://")[1].split('/')[0]
            result = result.replace(f'>{tmp1}</a>', f'>{tmp2}</a>')
    except Exception as e:
        logger.info(log_ % e)
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def upper_register(txt):
    result = str(txt).replace('0', '⁰').replace('1', '¹').replace('2', '²').replace('3', '³').replace('4', '⁴').replace(
        '5', '⁵').replace('6', '⁶').replace('7', '⁷').replace('8', '⁸').replace('9', '⁹')
    try:
        if len(result) == 4:
            result = f"{result[0]}˙{result[1]}ᵏ"
        elif len(result) == 5:
            result = f"{result[0]}{result[1]}˙{result[2]}ᵏ"
        elif len(result) == 6:
            result = f"{result[0]}{result[1]}{result[2]}˙{result[3]}ᵏ"
        elif len(result) >= 7:
            result = f"{result[0]}˙{result[2]}ᴹ"
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


def upper_register_sync(txt):
    result = str(txt).replace('0', '⁰').replace('1', '¹').replace('2', '²').replace('3', '³').replace('4', '⁴').replace(
        '5', '⁵').replace('6', '⁶').replace('7', '⁷').replace('8', '⁸').replace('9', '⁹')
    try:
        if len(result) == 4:
            result = f"{result[0]}˙{result[1]}ᵏ"
        elif len(result) == 5:
            result = f"{result[0]}{result[1]}˙{result[2]}ᵏ"
        elif len(result) == 6:
            result = f"{result[0]}{result[1]}{result[2]}˙{result[3]}ᵏ"
        elif len(result) >= 7:
            result = f"{result[0]}˙{result[2]}ᴹ"
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def convert_tgmd_to_html(markdown_text):
    result = markdown_text
    try:
        # markdown_text = "👩🏽‍💻 Lorem _начало_, ыусщте  df d d\n_Это_ *пример* [link](https://t.me) текста с *жирным* и _курсивом_\n\n[Ссылка на Google](https://www.google.com)\n\n#Хэштег #markdown #HTML\n\n$Кэштег $python $coding\n\n~Этот текст будет перечеркнут~\n\n__Этот текст будет подчеркнут__\n\n`Это кодовый фрагмент`\n\n```Это тоже кодовый фрагмент```"
        markdown_text = markdown_text.replace('\n', '<br>')

        # Заменяем * на <b> (жирный) только если он окружен пробелами или не имеет соседей с символами букв и цифр
        html_text = re.sub(r'(?<![\w*])\*(?!\*)\s*(.*?)\s*\*(?!\*)(?![\w*])', r'<b>\1</b>', markdown_text)
        html_text = re.sub(r'__(.*?)__', r'<u>\1</u>', html_text)
        html_text = re.sub(r'\|\|(.*?)\|\|', r'<code>\1</code>', html_text)
        html_text = re.sub(r'_(.*?)_', r'<i>\1</i>', html_text)
        html_text = re.sub(r'~(.*?)~', r'<s>\1</s>', html_text)
        html_text = re.sub(r'```(.*?)```', r'<code>\1</code>', html_text)
        html_text = re.sub(r'`(.*?)`', r'<code>\1</code>', html_text)

        html_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_text)
        html_text = re.sub(r'#(\w+)', r'<span>#\1</span>', html_text)
        html_text = re.sub(r'\$(\w+)', r'<span>$\1</span>', html_text)

        # async with aiofiles.open("index.html", "w", encoding="utf-8") as f:
        #     await f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"UTF-8\">\n<title>Markdown to HTML</title>\n<style>\nspan {{\n    color: #007bff;\n}}\na {{\n  text-decoration: none;\n}}\n</style>\n</head>\n<body>\n{html_text}\n</body>\n</html>")
        result = html_text
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


def escape_md(*content, sep=" ") -> str:
    """
    Escape Markdown text

    E.g. for usernames

    :param content:
    :param sep:
    :return:
    """
    return markdown_decoration.quote(_join(*content, sep=sep))


async def random_text(text):
    result = text
    try:
        space_arr = []
        start_pos = 0
        for item in text:
            try:
                if item == ' ':
                    start_pos = (text.find(' ', start_pos)) + 1
                    space_arr.append(start_pos)
            except Exception:
                pass
        if len(space_arr) != 0:
            random_pos = random.choice(space_arr)
            result = f"{text[:random_pos]} {text[random_pos:]}"

        dic_char = {'В': 'B', 'М': '𐌑', 'С': 'Ϲ', 'а': 'a', 'в': 'ʙ', 'р': 'ρ', 'с': 'ϲ', 'п': 'n', 'ш': 'ɯ', 'э': '϶',
                    'к': 'κ'}  # 'и': 'ᥙ',
        arr = ['В', 'М', 'С', 'а', 'в', 'р', 'с', 'п', 'ш', 'э', 'к']  # 'и',
        random_chr = random.choice(arr)
        random_pos = arr.index(random_chr)
        for ix in range(0, random_pos):
            try:
                result = result.replace(arr[ix], dic_char[arr[ix]])
                result = f"{result}​"
            except Exception as e:
                logger.info(log_ % str(e))  # await asyncio.sleep(round(random.uniform(1, 2), 2))

        result = result[0:1023]  # result = result.replace('р', 'р')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def fun_stegano(f_name):
    result = f_name
    try:
        if not os.path.exists(f_name):
            logger.info(log_ % f"SteganoFun: no file {f_name}")
            return
        b_name = os.path.basename(f_name)
        d_name = os.path.dirname(f_name)
        random_name = os.path.join(d_name, f"{random.choice(string.ascii_letters + string.digits)}_{b_name}")
        random_len = random.randrange(5, 15)
        random_txt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random_len))

        if f_name.lower().endswith('png'):
            tmp = lsb.hide(f_name, random_txt)
            tmp.save(random_name)

            if os.path.exists(f_name):
                os.remove(f_name)
            result = random_name
        elif f_name.lower().endswith('jpeg') or f_name.lower().endswith('jpg'):
            exifHeader.hide(f_name, random_name, random_txt)

            if os.path.exists(f_name):
                os.remove(f_name)
            result = random_name
        elif f_name.lower().endswith('pdf'):
            keys = ['Title', 'Author', 'Producer', 'Creator', 'Language', 'PDFVersion', 'CreatorTool', 'DocumentID',
                    'InstanceID', 'FileModifyDate']
            for key in keys:
                try:
                    with ExifToolHelper() as et:
                        et.set_tags([f_name], tags={key: random_txt}, params=["-P", "-overwrite_original"])
                except Exception:
                    # logger.info(log_ % f"for file {f_name}: {str(e)}");  logger.debug("")
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

            try:
                with ExifToolHelper() as et:
                    et.set_tags([f_name], tags={'FilePermissions': 777777}, params=["-P", "-overwrite_original"])
            except Exception:
                # logger.info(log_ % f"for file {f_name}: {str(e)}")
                await asyncio.sleep(round(random.uniform(0, 1), 2))

            if os.path.exists(f_name):
                shutil.copyfile(f_name, random_name)
                os.remove(f_name)
            result = random_name
        elif f_name.lower().endswith('mov') or f_name.lower().endswith('mp4'):
            keys = ['Copyright', 'FileModifyDate', 'CreateDate', 'ModifyDate', 'TrackCreateDate', 'TrackModifyDate',
                    'MediaCreateDate', 'MediaModifyDate', 'MinorVersion']  # PageCount
            for key in keys:
                try:
                    with ExifToolHelper() as et:
                        random_date = (datetime.now(timezone.utc) - timedelta(hours=random.randrange(1, 23))).strftime(
                            '%Y:%m:%d %H:%M:%S+03:00')
                        et.set_tags([f_name], tags={key: random_date}, params=["-P", "-overwrite_original"])
                except Exception:
                    # logger.info(log_ % f"for file {f_name}: {str(e)}")
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

            keys = ['XResolution', 'YResolution', 'Duration']
            for key in keys:
                try:
                    with ExifToolHelper() as et:
                        random_num = random.randrange(1, 180)
                        et.set_tags([f_name], tags={key: random_num}, params=["-P", "-overwrite_original"])
                except Exception:
                    # logger.info(log_ % f"for file {f_name}: {str(e)}")
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

            if os.path.exists(f_name):
                shutil.copyfile(f_name, random_name)
                os.remove(f_name)
            result = random_name
        else:
            keys = ['FileModifyDate']
            for key in keys:
                try:
                    with ExifToolHelper() as et:
                        random_date = (datetime.now(timezone.utc) - timedelta(hours=random.randrange(1, 23))).strftime(
                            '%Y:%m:%d %H:%M:%S+03:00')
                        et.set_tags([f_name], tags={key: random_date}, params=["-P", "-overwrite_original"])
                except Exception as e:
                    logger.info(log_ % f"for file {f_name}: {str(e)}")
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

            try:
                with ExifToolHelper() as et:
                    et.set_tags([f_name], tags={'FilePermissions': 777777}, params=["-P", "-overwrite_original"])
            except Exception as e:
                logger.info(log_ % f"for file {f_name}: {str(e)}")
                await asyncio.sleep(round(random.uniform(0, 1), 2))

            if os.path.exists(f_name):
                shutil.copyfile(f_name, random_name)
                os.remove(f_name)
            result = random_name
        logger.info(log_ % f"stagano ok")
    except Exception as e:
        logger.info(log_ % f"stageno error: {str(e)}")
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def correct_tag(txt, orig_txt=''):
    result = txt
    try:
        cnt_open = cnt_close = 0
        last_ix_open = last_ix_close = 0
        for i in range(0, len(txt)):
            try:
                if txt[i] == '<' and i + 1 < len(txt) - 1 and txt[i + 1] != '/':
                    cnt_open += 1
                    last_ix_open = i
                elif txt[i] == '<' and i + 1 < len(txt) - 1 and txt[i + 1] == '/':
                    cnt_close += 1
                    last_ix_close = i
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))

        if cnt_open and cnt_close:
            flag = False
            tmp = last_ix_close
            while tmp < len(txt) - 1:
                tmp += 1
                if txt[tmp] == '>':
                    flag = True
                    break
            if not flag:
                result = f"{txt[0:last_ix_open]} {{..}}"
            elif len(txt) < len(orig_txt):
                result = f"{result} {{..}}"
        elif cnt_open and cnt_close and cnt_open != cnt_close:
            result = f"{txt[0:last_ix_open]} {{..}}"
        elif len(txt) < len(orig_txt):
            result = f"{result} {{..}}"
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


# async def photo_to_video_sticker(bot, user_id, input_file, bot_username):
#     result = None
#     file_jpg = input_file[:input_file.rfind('.')] + '_.jpg'
#     file_gif = input_file[:input_file.rfind('.')] + '.gif'
#     file_mp4 = input_file[:input_file.rfind('.')] + '.mp4'
#     file_webm = input_file[:input_file.rfind('.')] + '.webm'
#     try:
#         image = Image.open(input_file)
#         image = await correct_orientation(image)
#         width, height = image.size
#         left = (width - min(width, height)) // 2
#         top = (height - min(width, height)) // 2
#         right = (width + min(width, height)) // 2
#         bottom = (height + min(width, height)) // 2
#         image = image.crop((left, top, right, bottom))
#         image = image.resize((512, 512), resample=Image.Resampling.LANCZOS)
#         image.save(file_jpg, format="JPEG")
#
#         quality = 90
#         while quality > 0:
#             img = Image.open(file_jpg)
#             img = await correct_orientation(img)
#             img.save(file_jpg, format="JPEG", quality=quality)
#
#             if os.path.getsize(file_jpg) < 40000: break
#             quality = 1 if quality == 0 else quality - 10
#         if os.path.getsize(file_jpg) > 40000: return
#
#         image = Image.open(file_jpg)
#         image = await correct_orientation(image)
#         frames = [image.copy(), ImageOps.grayscale(image)]
#         frames[0].save(file_gif, save_all=True, append_images=frames[1:], duration=500, loop=0, optimize=True)
#         clip = mp.VideoFileClip(file_gif)
#         clip = mp.concatenate_videoclips([clip] * 4, method="compose")
#         clip.write_videofile(file_mp4, fps=30, audio_codec='none', preset='ultrafast', bitrate="500k", threads=1)
#
#         command = ['ffmpeg', '-i', file_mp4, '-c:v', 'libvpx-vp9', '-b:v', '500k', '-an', '-y', file_webm]
#         subprocess.run(command)
#
#         sticker = types.InputSticker(sticker=types.FSInputFile(file_webm), emoji_list=['❤️'])
#         name = f"by_{user_id}_{str(time.time()).split('.')[-1]}_by_{bot_username}"
#         print(f"{name=}, {len(name)}")
#         await bot.create_new_sticker_set(user_id=user_id, name=name, title=f"{user_id}", stickers=[sticker],
#                                          sticker_format='video')
#         get_sticker_set_ = await bot.get_sticker_set(name=name)
#         result = get_sticker_set_.stickers[0].file_id
#     except TelegramRetryAfter as e:
#         logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
#         await asyncio.sleep(e.retry_after + 1)
#     except Exception as e:
#         logger.info(log_ % str(e))
#         await asyncio.sleep(round(random.uniform(0, 1), 2))
#     finally:
#         if os.path.exists(file_jpg): os.remove(file_jpg)
#         if os.path.exists(file_gif): os.remove(file_gif)
#         if os.path.exists(file_mp4): os.remove(file_mp4)
#         if os.path.exists(file_webm): os.remove(file_webm)
#         return result
#
#
# async def video_to_video_sticker(bot, user_id, input_file, bot_username):
#     result = None
#     file_mp4 = input_file[:input_file.rfind('.')] + '_.mp4'
#     file_webm = input_file[:input_file.rfind('.')] + '.webm'
#     try:
#         target_size = 512
#         clip = mp.VideoFileClip(input_file)
#         top = (clip.size[1] - target_size) // 2
#         bottom = top + target_size
#         left = (clip.size[0] - target_size) // 2
#         right = left + target_size
#         cropped_clip = clip.crop(x1=left, y1=top, x2=right, y2=bottom)
#         resized_clip = cropped_clip.resize(width=target_size, height=target_size)
#         resized_clip.write_videofile(file_mp4, audio=False)
#         clip.close()
#         cropped_clip.close()
#         resized_clip.close()
#
#         command = ['ffmpeg', '-i', file_mp4, '-c:v', 'libvpx-vp9', '-b:v', '50k', '-crf', '30', '-s', '512x512', '-t',
#             '3', '-an', '-y', file_webm]
#         subprocess.run(command)
#
#         sticker = types.InputSticker(sticker=types.FSInputFile(file_webm), emoji_list=['❤️'])
#         name = f"by_{user_id}_{str(time.time()).split('.')[-1]}_by_{bot_username}"
#         print(f"{name=}, {len(name)}")
#         await bot.create_new_sticker_set(user_id=user_id, name=name, title=f"{user_id}", stickers=[sticker],
#                                          sticker_format='video')
#         get_sticker_set_ = await bot.get_sticker_set(name=name)
#         result = get_sticker_set_.stickers[0].file_id
#     except TelegramRetryAfter as e:
#         logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
#         await asyncio.sleep(e.retry_after + 1)
#     except Exception as e:
#         logger.info(log_ % str(e))
#         await asyncio.sleep(round(random.uniform(0, 1), 2))
#     finally:
#         if os.path.exists(file_mp4): os.remove(file_mp4)
#         if os.path.exists(file_webm): os.remove(file_webm)
#         return result


async def correct_link(link):
    result = link
    try:
        link = str(link)
        if len(str(link).strip()) < 4:
            result = None
            return
        link = link.strip()
        res = link.split()
        try:
            float(res[0])
            link = str(link.split()[1]).strip('@\'!')
        except:
            link = str(link.split()[0]).strip('@\'!')
        link = link.lstrip(':').rstrip('.')
        link = link.replace('@https://', 'https://').replace('@:t.me/', 'https://t.me/')

        if link.startswith('t.me/') and not ('+' in link or 'join_my_chat' in link):
            link = link.replace('t.me/', '')
        elif link.startswith('t.me/') and ('+' in link or 'join_my_chat' in link):
            link = f"https://{link}"
        elif link.endswith('.t.me'):
            link = link.replace('.t.me', '')
        else:
            if 'http://' in link:
                link = link.replace('http://', 'https://')
            link = link[len(const_url):len(link)] if const_url in link and not (
                    't.me/+' in link or 't.me/join_my_chat/' in link) else link

        if 'https://telesco.pe/' in link:
            link = link.replace('https://telesco.pe/', '')

        try:
            link = str(int(link))
        except Exception:
            link = link if 't.me/+' in str(link) or 't.me/join_my_chat/' in str(link) else f"@{link}"

        try:
            if link.split('/')[-1].isdigit():
                link = f"{link[:link.rindex('/')]}"
        except Exception:
            pass

        try:
            if '+' in link:
                link = str(int(link.split('+')[-1]))
        except Exception:
            pass

        try:
            if link.startswith('join_my_chat/'):
                link = f"t.me/{link}"
            elif link.startswith('@join_my_chat/'):
                link = link.replace('@', 't.me/')
        except Exception:
            pass

        link = link.lstrip(':-.')

        try:
            link = link.replace('@://', '')
            link = link.replace('@//', '')
            link = link.replace('@/', '')
            link = link.replace('@.me/', '')
            link = link.replace('@.', '')
            link = link.replace('@@', '')
            for el in link:
                if el not in string.ascii_letters + string.digits + "@_https://t.me/+ ":
                    link = link.replace(el, '')
        except Exception:
            pass

        if '@' in link and '/' in link: link = link[:link.index('/')]
        link = str(link).rstrip('/').rstrip('.').rstrip(':').strip()
        result = None if '@None' == link else link
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


# endregion


# region cairo
async def round_rect(context, x, y, width, height, r):
    try:
        context.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        context.arc(x + width - r, y + r, r, 3 * math.pi / 2, 0)
        context.arc(x + width - r, y + height - r, r, 0, math.pi / 2)
        context.arc(x + r, y + height - r, r, math.pi / 2, math.pi)
        context.close_path()
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def text_title(text):
    title = None
    content = text.strip()
    try:
        res = text.strip().splitlines()
        if res and len(res) >= 2 and len(res[0].strip()) < 20:
            title = res[0].strip()
            content = text.strip().replace(title, '', 1).strip()
            content = content.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return title, content


async def get_content_part(ctx, content_all, width_, original_width):
    content_part = content_all
    try:
        content_copy = content_all[::-1]
        ix = 0
        padding_coefficient = 0.1
        width_ = int(original_width - original_width * padding_coefficient)
        print(f"1 {width_=}")
        cnt = 0

        while True:
            bearing, ybearing, content_width, content_height, dx, dy = ctx.text_extents(content_copy)
            cnt += 1
            if cnt > 1000: break

            if content_width >= width_:
                space_found = False
                for i in range(len(content_copy)):
                    if ix:
                        i += 1
                        ix = 0
                    elif content_copy[i].isspace():
                        content_copy = content_copy[i:]
                        ix = i
                        space_found = True
                        break

                if not space_found:
                    break

                # Пересчитаем ширину с учетом коэффициента
                width_ = int(original_width - original_width * padding_coefficient)  # Используем исходную ширину
                print(f"2 {width_=}")
            else:
                break

        content_part = content_copy[::-1].strip()
        if '\n' in content_part:
            arr = content_part.splitlines()
            content_part = '\n'.join(arr[::-1]).strip()

        content_all = content_all.strip().replace(content_part, '', 1).strip()

        # Пересчитаем ширину после изменений
        bearing, ybearing, content_width, _, _, _ = ctx.text_extents(content_all)
        width_ = int(original_width - original_width * padding_coefficient)  # Используем исходную ширину
        print(f"3 {width_=}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return content_part, content_all, width_, original_width


async def edit_surface(title_copy, content_all_copy, cnt=1, shift=0):
    result = None
    try:
        original_width = width_ = 365
        height_ = 50
        round_num = int(height_ * 1 / (cnt - 1)) if cnt > 2 else int(height_ / 2 * 1 / cnt)
        if shift:
            height_ += shift * (cnt - 2)
        if title_copy:
            height_ += 40
        font_size = 24

        title = title_copy
        content_all = content_all_copy
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width_, int(height_ + 40))
        ctx = cairo.Context(surface)

        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.0)
        ctx.rectangle(0, 0, width_, int(height_ + 40))
        ctx.fill()

        ctx.set_source_rgba(25 / 255, 25 / 255, 30 / 255, 243 / 255)
        await round_rect(ctx, 0, 0, width_, int(height_ * 0.9), round_num)
        ctx.fill()

        # title
        start_y = 0
        if title:
            start_y = 30
            ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(font_size)
            ctx.set_source_rgb(128 / 255, 196 / 255, 255 / 255)
            ctx.move_to(20, start_y)
            ctx.show_text(title)
            ctx.stroke()

        # content
        cnt = 1
        shift = 30
        start_y = start_y + 7 if start_y else 0
        while content_all != '' and cnt < 1000:
            delta_y = start_y + shift * cnt
            cnt += 1
            ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(font_size)
            ctx.set_source_rgb(250 / 255, 250 / 255, 250 / 255)
            ctx.move_to(20, delta_y)
            content_part, content_all, width_, original_width = await get_content_part(ctx, content_all, width_,
                                                                                       original_width)
            ctx.show_text(content_part)
            ctx.stroke()

        result = surface
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result, cnt


async def text_layout(text, MEDIA_D):
    result = title = None
    try:
        title, content = await text_title(text)
        shift = 34
        surface, cnt = await edit_surface(title, content)

        if cnt > 2:
            surface, cnt = await edit_surface(title, content, cnt, shift)

        file_name = os.path.join(MEDIA_D, datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.png'))
        surface.write_to_png(file_name)
        result = file_name
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result, title


async def test_cairo(bot, MEDIA_D):
    try:
        text = 'Привет всем!\n\nя могу помочь с ответами на ваши вопросы. конечно'
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        text = 'Привет всем!\n\nя могу помочь с ответами на ваши вопросы.1. к сожалению, я не знаю, доделал ли саня домашнюю работу по алгебре. но я уверена, что ему лучше успеть ечно, я могу рассказать вам о теореме пифагора! она утверждает, что в прямоугольном треугольнике квадрат гипотенузы равен сумме квадратов катетов'
        file_png, t = await text_layout(f"{text[:256]}..", MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        text = f"""Telegram "Heieje ejoekee" (@hdhdjrjejrejrirjrnebe)!
Мы предлагаем уникальную возможность встретиться с единомышленниками и обсудить самые актуальные темы."""
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        # 👩🏽‍💻 эмоджи превращаются в квадртаики
        # text = f"""Telegram "Heieje ejoekee"\n\nМы предлагаем уникальную возможность встретиться с единомышленниками и обсудить самые актуальные темы."""
        # text = "Telegram Heieje ejo\n\nМы предлагаем уникальный шанс встретиться и обсудить самые важные темы"
        text = "Извините за\nЕсли сейчас результат правильный и не возникает проблем с отрицательными значениями, то, вероятно, предложенные изменения в цикле помогли. В таком случае, давайте проверим вашу последнюю реализацию и посмотрим, остались ли какие-либо вопросы или проблемы, которые нужно решить."
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        text = "Константин Белов\n\nFit line to width with Pango and Cairo"
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        text = "Константин Белов Fit line to width with Pango and Cairo"
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)
        #
        text = "Константин Белов"
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)
        #
        #         text = f"""She literature discovered increasing how diminution understood. Though and highly the enough
        # county for man. Of it up he still court alone widow seems. Suspected remainder rapturous my sweetness. All vanity regard sudden nor simple can. World mrs and vexed china since after often.
        #
        # Remain valley who mrs uneasy remove wooded him you. Her questions favourite him concealed. We to wife face took he. The taste begin early old why since dried can first. Prepared as or humoured formerly. Evil mrs true get post. Express village evening prudent my as ye hundred forming. Thoughts why not directly reserved packages you. Winter a silent favour of am tended mutual. """
        #         file_png, t = await text_layout(text)
        #         print(file_png, t)
        #         image = Image.open(file_png)
        #         image = await correct_orientation(image)
        #         file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        #         sticker = os.path.join(MEDIA_D, file_name_part)
        #         image.save(sticker, format="webp", quality=99)
        #         reply_id = None
        #         GROUPP_TID = -1001913792444
        #         await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
        #                                reply_to_message_id=reply_id)
        #         if os.path.exists(sticker): os.remove(sticker)
        #         if file_png and os.path.exists(file_png): os.remove(file_png)
        #
        text = f"""She literature\ndiscovered increasing how diminution understood. Though and highly the enough county for man. Of it up he still court alone widow seems. Suspected he remainder rapturous my sweetness. All vanity regard sudden nor simple can. World mrs and vexed china since after often.

Remain valley who mrs uneasy remove wooded him you. Her questions favourite him concealed. We to wife face took he. The taste begin early old why since dried can first. Prepared as or humoured formerly. Evil mrs true get post. Express village evening prudent my as ye hundred forming. Thoughts she why not directly reserved packages you. Winter an silent favour of am tended mutual. """
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        # text = "She literature discovered increasing how diminution understood. Though and highly the enough county for man"
        text = f"""She literature discovered increasing how diminution understood. Though and highly the enough county for man"""
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        text = f"""dfdfga\ndgadgadfg"""
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)

        text = f"""/Users/mark/PycharmProjects/Ferey/FereyMediaBot/Roboto-Light.ttf
👩🏽‍💻"""
        file_png, t = await text_layout(text, MEDIA_D)
        print(file_png, t)
        image = Image.open(file_png)
        image = await correct_orientation(image)
        file_name_part = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.webp')
        sticker = os.path.join(MEDIA_D, file_name_part)
        image.save(sticker, format="webp", quality=99)
        reply_id = None
        GROUPP_TID = -1001913792444
        await bot.send_sticker(chat_id=int(GROUPP_TID), sticker=types.FSInputFile(sticker),
                               reply_to_message_id=reply_id)
        if os.path.exists(sticker): os.remove(sticker)
        if file_png and os.path.exists(file_png): os.remove(file_png)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


# endregion


# region telegraph
async def tgph_select(access_token, url):
    result = telegraph_ = None
    try:
        telegraph_ = Telegraph(access_token=access_token)
        pages_ = (await telegraph_.get_page_list())['pages']

        for page_ in pages_:
            if page_['url'] == url:
                result = await telegraph_.get_page(path=page_['path'], return_content=True, return_html=False)
                return
    except Exception as e:
        if 'Flood control exceeded' in str(e):
            try:
                secs = int(str(e).split(' seconds')[0].split()[-1])
                if secs < 10: await asyncio.sleep(secs + 1)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
        elif 'All connection attempts failed' in str(e):
            await asyncio.sleep(20)
        else:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return telegraph_, result


async def tgph_change(access_token, url, json_):
    retry = 2
    while retry > 0:
        try:
            await asyncio.sleep(round(random.uniform(1, 2), 2))
            telegraph_ = Telegraph(access_token=access_token)
            pages_ = await telegraph_.get_page_list()

            for page_ in pages_['pages']:
                if page_['url'] != url: continue

                get_page_ = await telegraph_.get_page(path=page_['path'], return_content=True, return_html=False)
                try:
                    content_json = json.loads(str(get_page_['content'][0]))
                    if len(content_json) > 20: raise Exception
                except:
                    await telegraph_.edit_page(path=page_['path'], title=page_['title'], html_content='{}')
                    content_json = {}

                timestamp_ = str(utils.datetime_to_timestamp(datetime.now(timezone.utc)))
                content_json[timestamp_] = json_
                post_dumps = json.dumps(content_json, ensure_ascii=False)
                await telegraph_.edit_page(path=page_['path'], title=page_['title'], html_content=post_dumps)
                return 1
        except Exception as e:
            if 'Flood control exceeded' in str(e):
                try:
                    secs = int(str(e).split(' seconds')[0].split()[-1])
                    if secs < 10: await asyncio.sleep(secs + 1)
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(1, 2), 2))
            elif 'All connection attempts failed' in str(e):
                await asyncio.sleep(20)
            else:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
        finally:
            retry -= 1
    return 0


async def tgph_clear(access_token, url):
    retry = 2
    while retry > 0:
        try:
            await asyncio.sleep(round(random.uniform(0, 1), 2))
            telegraph_ = Telegraph(access_token=access_token)
            pages_ = await telegraph_.get_page_list()

            for page_ in pages_['pages']:
                if page_['url'] == url:
                    await telegraph_.edit_page(path=page_['path'], title=page_['title'], html_content='{}')
                return 1
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(1, 2), 2))
        finally:
            retry -= 1
    return 0


# async def get_tgph_link(file_name):
#     result = None
#     try:
#         return
#         ext = str(file_name[file_name.rfind('.'):]).lower()
#         if file_name and os.path.exists(file_name) and os.path.getsize(file_name) < 5242880 and ext in ['.jpg', '.jpeg',
#                                                                                                         '.png', '.gif',
#                                                                                                         '.mp4']:
#             cnt = 2
#             while cnt >= 0:
#                 try:
#                     telegraph_ = Telegraph()
#                     res = await telegraph_.upload_file(file_name)
#                     result = f"https://telegra.ph{res[0]['src']}"
#                     return
#                 except Exception as e:
#                     logger.info(log_ % f"Telegraph (cnt={cnt}): {str(e)}")
#                     await asyncio.sleep(round(random.uniform(6, 10), 2))
#                     cnt -= 1
#     except Exception as e:
#         logger.info(log_ % str(e))
#         await asyncio.sleep(round(random.uniform(0, 1), 2))
#     finally:
#         return result


async def is_ban_menu(chat_id):
    result = False
    try:
        telegraph_ = Telegraph(access_token=TGPH_TOKEN_MAIN)
        pages = await telegraph_.get_page_list()

        for item in pages['pages']:
            try:
                if item['path'] == 'ban-04-11-7':
                    page = await telegraph_.get_page(path=item['path'], return_content=True, return_html=True)
                    ban_ids = str(page['content']).split()

                    if str(chat_id) in ban_ids:
                        result = True
                    return
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        # telegraph_ = Telegraph(access_token=TGPH_TOKEN_MAIN)  # html_ = {'one': '1', 'two': '2'}  # html_ = json.dumps(html_, ensure_ascii=False)  # page_ = telegraph_.create_page(title='broadcasting', html_content=html_, author_name='bot_username', author_url='https://t.me/bot_username', return_content=True)  # page_url = page_['url']
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def ban_handler_menu(bot, chat_id, args):
    try:
        telegraph_ = Telegraph(access_token=TGPH_TOKEN_MAIN)
        pages = await telegraph_.get_page_list()

        if not args:
            for item in pages['pages']:
                try:
                    if item['path'] == 'ban-04-11-7':
                        page = await telegraph_.get_page(path=item['path'], return_content=True, return_html=True)
                        ban_ids = str(page['content'])
                        ban_ids = ban_ids[:4096]
                        ban_ids = ' '.join([f"<code>{it}</code>" for it in ban_ids.split()])

                        await bot.send_message(chat_id, ban_ids)
                        return
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

        prepare_ids = args.split()
        prepare_ids = [prepare_id for prepare_id in prepare_ids if prepare_id.isdigit()]
        if not len(prepare_ids): return

        for item in pages['pages']:
            try:
                if item['path'] == 'ban-04-11-7':
                    page = await telegraph_.get_page(path=item['path'], return_content=True, return_html=True)
                    ban_ids = str(page['content']).split()
                    length1 = len(ban_ids)
                    ban_ids = f"{page['content']} {' '.join(prepare_ids)}"
                    ban_ids = ban_ids.split()
                    ban_ids = list(set(ban_ids))
                    length2 = len(ban_ids)
                    modul = abs(length1 - length2)
                    await telegraph_.edit_page(path=item['path'], title="ban", html_content=' '.join(ban_ids))

                    if length1 != length2:
                        await bot.send_message(chat_id, f"👩🏽‍💻 {modul}th added to /ban (len: {length2})")
                    else:
                        await bot.send_message(chat_id, f"👩🏽‍💻 {modul}th already in /ban (len: {length2})")
                    break
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def unban_handler_menu(bot, chat_id, args):
    try:
        if not args:
            return
        else:
            prepare_ids = args.split()

        prepare_ids = [prepare_id for prepare_id in prepare_ids if prepare_id.isdigit()]
        if not len(prepare_ids): return
        telegraph_ = Telegraph(access_token=TGPH_TOKEN_MAIN)
        pages = await telegraph_.get_page_list()

        for item in pages['pages']:
            try:
                if item['path'] == 'ban-04-11-7':
                    page = await telegraph_.get_page(path=item['path'], return_content=True, return_html=True)
                    ban_ids = str(page['content']).split()
                    length1 = len(ban_ids)

                    ban_ids = [ban_id for ban_id in ban_ids if ban_id not in prepare_ids]
                    length2 = len(ban_ids)
                    ban_ids = list(set(ban_ids))
                    modul = abs(length1 - length2)
                    html_content = ' '.join(ban_ids)
                    html_content = '0' if html_content == '' else html_content
                    await telegraph_.edit_page(path=item['path'], title="ban", html_content=html_content)

                    if length1 != length2:
                        await bot.send_message(chat_id, f"👩🏽‍💻 {modul}th removed from /ban (len: {length2})")
                    else:
                        await bot.send_message(chat_id, f"👩🏽‍💻 {modul}th already deleted from /ban (len: {length2})")
                    break
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def check_tgph_posts(bot_username, BASE_D):
    try:
        arr = [k for k, v in TGPH_TOKENS.items() if bot_username in k]
        access_key = arr[0] if len(arr) else None
        if not access_key: return

        access_token = TGPH_TOKENS[access_key]
        telegraph_ = Telegraph(access_token=access_token)
        pages = await telegraph_.get_page_list()

        for item in pages['pages']:
            try:
                if item['url'] != access_key: continue
                page = await telegraph_.get_page(path=item['path'], return_content=True, return_html=False)
                try:
                    content_json = json.loads(str(page['content'][0]))
                except:
                    content_json = {}

                for OFFER_USERTID, v in content_json.items():
                    OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_BUTTON, OFFER_ISBUTTON, OFFER_TGPHLINK, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, OFFER_DT, OFFER_TZ = v

                    sql = "INSERT INTO OFFER (OFFER_USERTID, OFFER_TEXT, OFFER_MEDIATYPE, " \
                          "OFFER_FILEID, OFFER_BUTTON, OFFER_ISBUTTON, OFFER_TGPHLINK, OFFER_ISTGPH, " \
                          "OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, OFFER_DT, " \
                          "OFFER_TZ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14) ON CONFLICT DO NOTHING"
                    await db_change_pg(sql, (
                        int(OFFER_USERTID), v[OFFER_TEXT], v[OFFER_MEDIATYPE], v[OFFER_FILEID], v[OFFER_BUTTON],
                        v[OFFER_ISBUTTON], v[OFFER_TGPHLINK], v[OFFER_ISTGPH], v[OFFER_ISSPOILER], v[OFFER_ISPIN],
                        v[OFFER_ISSILENCE], v[OFFER_ISGALLERY], v[OFFER_DT], v[OFFER_TZ],), BASE_D)

                    del content_json[str(OFFER_USERTID)]
                    post_dumps = json.dumps(content_json, ensure_ascii=False)
                    await telegraph_.edit_page(path=item['path'], title=access_key, html_content=post_dumps)
                    return
            except Exception as e:
                if 'Flood control exceeded' in str(e):
                    await run_shell(f'/usr/bin/pm2 restart {bot_username}')
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def in_ban_list(tid, username=None):
    result = False
    try:
        b_ids = [68728482,  # @yagupov
                 201960795,  # @korsdp
                 6084199556,  # 👩🏽‍💻 User: Chris023, @None, 6084199556 block @FereyDemoBot
                 7227211988,  # Berto Silva
                 2066375437,  # Leslie Mccarthy
                 5105772611,  # Z Yuan
                 5438448668,  # JQ 1, en
                 6126573233,  # @icticiy, en
                 ]

        if username and username.startswith('kwprod'):
            result = True
        elif tid in b_ids:
            result = True
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def create_tgph_json_and_token(title_hash):
    ENT_TOKENTGPH = ENT_PAGETGPH = ENT_JSONTGPH = None
    try:
        telegraph_ = Telegraph()
        account_ = await telegraph_.create_account(short_name='me',
                                                   author_name='blog',
                                                   author_url="https://t.me")

        page_1 = await telegraph_.create_page(title=f"TGPH-JSON-USERS-blog",
                                              html_content="<a href='https://t.me'>@blog</a>",
                                              author_name='blog',
                                              author_url="https://t.me")
        page_2 = await telegraph_.create_page(title=f"TGPH-JSON-USERS-{title_hash}",
                                              html_content='{}')

        ENT_TOKENTGPH = account_['access_token']
        ENT_PAGETGPH = page_1['url']
        ENT_JSONTGPH = page_2['url']
        print(f"access_token = {ENT_TOKENTGPH}, ENT_PAGETGPH = {ENT_PAGETGPH}, ENT_JSONTGPH = {ENT_JSONTGPH}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH


async def generate_tgph_page(bot, title_hash, USER_ID, ENT_TID, ENT_USERNAME, ENT_FN, MEDIA_D, BASE_D,
                             entity_type='bot'):
    ENT_TOKENTGPH = ENT_PAGETGPH = ENT_JSONTGPH = tgph_ph = None
    try:
        if entity_type == 'bot':
            sql = "SELECT BOT_TOKENTGPH, BOT_PAGETGPH, BOT_JSONTGPH FROM \"BOT\" WHERE BOT_TID=$1"
            data = await db_select_pg(sql, (ENT_TID,), BASE_D)
        else:
            sql = "SELECT UB_TOKENTGPH, UB_PAGETGPH, UB_JSONTGPH FROM UB WHERE UB_TID=$1"
            data = await db_select_pg(sql, (ENT_TID,), BASE_D)

        if len(data):
            ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH = data[0]
            if ENT_TOKENTGPH and ENT_PAGETGPH and ENT_JSONTGPH: return
        print(f"{bot.id}, {USER_ID}, {MEDIA_D}, {tgph_ph}")

        # file_name = os.path.join(MEDIA_D, datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.jpeg'))
        # try:
        #     profile_photos_ = await bot.get_user_profile_photos(user_id=USER_ID, limit=1)
        #
        #     if len(profile_photos_.photos):
        #         photo_id = profile_photos_.photos[-1][-1].file_id
        #         file = await bot.get_file(photo_id)
        #         await bot.download_file(file.file_path, file_name)
        #         tgph_ph = await get_link_for_media(bot, chat_id, file_name, KEYS_JSON)
        # except Exception as e:
        #     logger.info(log_ % str(e))
        #     await asyncio.sleep(round(random.uniform(0, 1), 2))
        # finally:
        #     if file_name and os.path.exists(file_name): os.remove(file_name)
        # tgph_ph = tgph_ph if tgph_ph else bot_logo_jpeg

        tgph_ph = logo_photo
        ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH = await create_tgph_page(tgph_ph, title_hash, ENT_TID, ENT_USERNAME,
                                                                           ENT_FN, BASE_D, entity_type)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH


async def create_tgph_page(tgph_ph, title_hash, ENT_TID, ENT_USERNAME, ENT_FN, BASE_D, entity_type='bot'):
    ENT_TOKENTGPH = ENT_PAGETGPH = ENT_JSONTGPH = None
    try:
        cnt = 2
        while cnt >= 0:
            try:
                telegraph_ = Telegraph()
                title = "📰 Telegraph blog"
                author_url = f"https://t.me/{ENT_USERNAME}"
                tgph_ph = str(tgph_ph).replace('https://telegra.ph', '')
                bio = "💙 verified"

                account_ = await telegraph_.create_account(short_name=short_name, author_name=ENT_USERNAME,
                                                           author_url=author_url)
                n = f"<a href='https://t.me/{ENT_USERNAME}'>@{ENT_USERNAME}</a> <br>{ENT_FN}" if ENT_USERNAME else f"<b>{ENT_FN}</b>"
                los = "<figure><img src='{0}'/><figcaption>Photo: @{1}</figcaption></figure><blockquote>Landing <i>Telegram</i> Bot</blockquote>👩🏽‍💻 <b>Account:</b> {2}<br>[<b>id</b>=<code>{3}</code>]<br><b>Info:</b> {4}<br><aside>By</aside><aside><a href='https://t.me/{5}'>Link</a></aside>"
                html_ = los.format(tgph_ph, ENT_USERNAME, n, ENT_TID, bio, ENT_USERNAME)
                page_1 = await telegraph_.create_page(title=title, html_content=html_, author_name=ENT_USERNAME,
                                                      author_url=author_url)
                page_2 = await telegraph_.create_page(title=title_hash, html_content='{}')

                ENT_TOKENTGPH = account_['access_token']
                ENT_PAGETGPH = page_1['url']
                ENT_JSONTGPH = page_2['url']

                if entity_type == 'bot':
                    sql = "UPDATE BOT SET BOT_TOKENTGPH=$1, BOT_PAGETGPH=$2, BOT_JSONTGPH=$3 WHERE BOT_TID=$4"
                    await db_change_pg(sql, (ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH, ENT_TID,), BASE_D)
                else:
                    sql = "UPDATE UB SET UB_TOKENTGPH=$1, UB_PAGETGPH=$2, UB_JSONTGPH=$3 WHERE UB_TID=$4"
                    await db_change_pg(sql, (ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH, ENT_TID,), BASE_D)
                return
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                cnt -= 1
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return ENT_TOKENTGPH, ENT_PAGETGPH, ENT_JSONTGPH


# endregion


# region admin
async def pre_upload(bot, chat_id, media_name, media_type, EXTRA_D, BASE_D):
    result = None
    try:
        sql = "SELECT FILE_FILEID FROM \"FILE\" WHERE FILE_FILENAME=$1"
        data = await db_select_pg(sql, (media_name,), BASE_D)

        if not len(data):
            media = types.FSInputFile(str(os.path.join(EXTRA_D, media_name)))
            res = None

            if media_type == 'photo':
                res = await bot.send_photo(chat_id=chat_id, photo=media)
                result = res.photo[-1].file_id
            elif media_type == 'video':
                width = height = duration = None
                try:
                    cap = cv2.VideoCapture(str(os.path.join(EXTRA_D, media_name)))
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    duration = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))

                    print(f"{width=}, {height=}")
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

                res = await bot.send_video(chat_id=chat_id,
                                           video=media,
                                           duration=duration,
                                           width=width,
                                           height=height)
                result = res.video.file_id
            elif media_type in ['gif', 'animation']:
                res = await bot.send_animation(chat_id=chat_id, animation=media)
                result = res.animation.file_id
            elif media_type == 'audio':
                res = await bot.send_audio(chat_id=chat_id, audio=media)
                result = res.audio.file_id
            elif media_type == 'voice':
                res = await bot.send_voice(chat_id=chat_id, voice=media)
                result = res.voice.file_id
            elif media_type in ['video_note', 'telescope']:
                res = await bot.send_video_note(chat_id=chat_id, video_note=media)
                result = res.video_note.file_id
            elif media_type == 'document':
                res = await bot.send_document(chat_id=chat_id, document=media, disable_content_type_detection=True)
                result = res.document.file_id
            elif media_type == 'sticker':
                res = await bot.send_sticker(chat_id=chat_id, sticker=media)
                result = res.sticker.file_id

            if res:
                await bot.delete_message(chat_id, res.message_id)
            sql = "INSERT INTO \"FILE\" (FILE_FILEID, FILE_FILENAME) VALUES ($1, $2) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (result, media_name,), BASE_D)
            logger.info(log_ % str(f'FILE_FILEID: {result}'))
        else:
            result = data[0][0]

        if media_type == 'photo':
            await bot.send_chat_action(chat_id=chat_id, action='upload_photo')
        elif media_type == 'video':
            await bot.send_chat_action(chat_id=chat_id, action='record_video')
        elif media_type in ['video_note', 'telescope']:
            await bot.send_chat_action(chat_id=chat_id, action='record_video_note')
        elif media_type in ['gif', 'animation']:
            await bot.send_chat_action(chat_id=chat_id, action='record_video')
        elif media_type == 'audio':
            await bot.send_chat_action(chat_id=chat_id, action='upload_audio')
        elif media_type == 'voice':
            await bot.send_chat_action(chat_id=chat_id, action='record_voice')
        elif media_type == 'document':
            await bot.send_chat_action(chat_id=chat_id, action='upload_document')
        elif media_type == 'sticker':
            await bot.send_chat_action(chat_id=chat_id, action='choose_sticker')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id=1, call=None):
    try:
        sql = "SELECT OFFER_ID, OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_BUTTON, OFFER_ISBUTTON, " \
              "OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, OFFER_DT FROM OFFER"
        data_offers = await db_select_pg(sql, (), BASE_D)
        if not data_offers:
            if call: await call.message.delete()
            await bot.send_message(chat_id, l_post_text[lz], reply_markup=markupAdmin)
            await state.set_state(FsmOffer.text)
            return

        # region config
        post_id = 1 if post_id < 1 else post_id
        item = data_offers[post_id - 1]
        OFFER_ID, OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_BUTTON, OFFER_ISBUTTON, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, OFFER_DT = item
        show_offers_datetime = l_post_datetime[lz]
        show_offers_button = l_post_buttons[lz]
        show_offers_off = l_off[lz]

        extra = f"\n\n{show_offers_datetime}: {OFFER_DT if OFFER_DT else show_offers_off}\n" \
                f"{show_offers_button}: {OFFER_BUTTON if OFFER_BUTTON else show_offers_off}\n"
        OFFER_TEXT = OFFER_TEXT or ''
        OFFER_TEXT = '' if OFFER_MEDIATYPE == 'video_note' or OFFER_MEDIATYPE == 'sticker' else OFFER_TEXT
        moment = 1020 - len(OFFER_TEXT) - len(extra)
        OFFER_TEXT = await correct_tag(f"{l_post_text[0:(len(OFFER_TEXT) + moment)]}") if moment <= 0 else OFFER_TEXT

        # endregion
        # region reply_markup
        reply_markup = get_keyboard_admin(data_offers, 'offers', post_id)

        buttons = [types.InlineKeyboardButton(text=f"✅ {l_btn[lz]}" if OFFER_ISBUTTON else f"☑️ {l_btn[lz]}",
                                              callback_data=f'ofr_ispst_{OFFER_ID}_{post_id}'),
                   types.InlineKeyboardButton(text=f"✅ {l_pin[lz]}" if OFFER_ISPIN else f"☑️ {l_pin[lz]}",
                                              callback_data=f'ofr_ispin_{OFFER_ID}_{post_id}'),
                   types.InlineKeyboardButton(text=f"✅ {l_silence[lz]}" if OFFER_ISSILENCE else f"☑️ {l_silence[lz]}",
                                              callback_data=f'ofr_issilence_{OFFER_ID}_{post_id}'), ]
        reply_markup.row(*buttons)

        buttons = [types.InlineKeyboardButton(text=f"✅ {l_gallery[lz]}" if OFFER_ISGALLERY else f"☑️ {l_gallery[lz]}",
                                              callback_data=f'ofr_isgallery_{OFFER_ID}_{post_id}'),
                   types.InlineKeyboardButton(text=f"✅ {l_preview[lz]}" if OFFER_ISTGPH else f"☑️ {l_preview[lz]}",
                                              callback_data=f'ofr_ispreview_{OFFER_ID}_{post_id}'),
                   types.InlineKeyboardButton(text=f"✅ {l_spoiler[lz]}" if OFFER_ISSPOILER else f"☑️ {l_spoiler[lz]}",
                                              callback_data=f'ofr_isspoiler_{OFFER_ID}_{post_id}'), ]
        reply_markup.row(*buttons)

        buttons = [types.InlineKeyboardButton(text=l_post_new[lz], callback_data=f'ofr_new_{OFFER_ID}_{post_id}'),
                   types.InlineKeyboardButton(text=l_post_delete[lz], callback_data=f'ofr_del_{OFFER_ID}_{post_id}'),
                   types.InlineKeyboardButton(text=l_post_change[lz], callback_data=f'ofr_edit_{OFFER_ID}_{post_id}'), ]
        reply_markup.row(*buttons)

        reply_markup.row(
            types.InlineKeyboardButton(text=l_post_publish[lz], callback_data=f'ofr_publication_{OFFER_ID}_{post_id}'))

        # endregion
        # region show
        if OFFER_FILEID and '[' not in OFFER_FILEID:
            OFFER_TEXT = OFFER_TEXT + extra
            if not call:
                if OFFER_MEDIATYPE == 'photo' or OFFER_MEDIATYPE == 'text':
                    await bot.send_photo(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                         reply_markup=reply_markup.as_markup(), has_spoiler=OFFER_ISSPOILER)
                elif OFFER_MEDIATYPE in ['gif', 'animation']:
                    await bot.send_animation(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                             reply_markup=reply_markup.as_markup(), has_spoiler=OFFER_ISSPOILER)
                elif OFFER_MEDIATYPE == 'video':
                    await bot.send_video(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                         reply_markup=reply_markup.as_markup(), has_spoiler=OFFER_ISSPOILER)
                elif OFFER_MEDIATYPE == 'audio':
                    await bot.send_audio(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                         reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE == 'document':
                    await bot.send_document(chat_id=chat_id, document=OFFER_FILEID, caption=OFFER_TEXT,
                                            disable_content_type_detection=True, reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE == 'sticker':
                    await bot.send_sticker(chat_id=chat_id, sticker=OFFER_FILEID)
                    await bot.send_message(chat_id, OFFER_TEXT, reply_markup=reply_markup.as_markup(),
                                           disable_web_page_preview=True)
                elif OFFER_MEDIATYPE == 'voice':
                    if has_restricted:
                        text = l_post_has_restricted[lz].format(bot_un)
                        await bot.send_message(chat_id, text, disable_web_page_preview=True)
                        await bot.send_message(chat_id, OFFER_TEXT, reply_markup=reply_markup.as_markup(),
                                               disable_web_page_preview=True)
                    else:
                        await bot.send_voice(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                             reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE in ['video_note', 'telescope']:
                    if has_restricted:
                        text = l_post_has_restricted[lz].format(bot_un)
                        await bot.send_message(chat_id, text, disable_web_page_preview=True)
                    else:
                        await bot.send_video_note(chat_id=chat_id, video_note=OFFER_FILEID)
                    await bot.send_message(chat_id, OFFER_TEXT, reply_markup=reply_markup.as_markup(),
                                           disable_web_page_preview=True)
            else:
                if OFFER_MEDIATYPE == 'photo' or OFFER_MEDIATYPE == 'text':
                    if call.message.video_note or call.message.voice or call.message.sticker or call.message.text:
                        await bot.send_photo(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                             reply_markup=reply_markup.as_markup(), has_spoiler=OFFER_ISSPOILER)
                    else:
                        media = types.InputMediaPhoto(media=OFFER_FILEID, caption=OFFER_TEXT,
                                                      has_spoiler=OFFER_ISSPOILER)
                        await call.message.edit_media(media=media, reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE in ['gif', 'animation']:
                    if call.message.video_note or call.message.voice or call.message.sticker or call.message.text:
                        await bot.send_animation(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                                 reply_markup=reply_markup.as_markup(), has_spoiler=OFFER_ISSPOILER)
                    else:
                        media = types.InputMediaAnimation(media=OFFER_FILEID, caption=OFFER_TEXT,
                                                          has_spoiler=OFFER_ISSPOILER)
                        await call.message.edit_media(media=media, reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE == 'video':
                    if call.message.video_note or call.message.voice or call.message.sticker or call.message.text:
                        await bot.send_video(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                             reply_markup=reply_markup.as_markup(), has_spoiler=OFFER_ISSPOILER)
                    else:
                        media = types.InputMediaVideo(media=OFFER_FILEID, caption=OFFER_TEXT,
                                                      has_spoiler=OFFER_ISSPOILER)
                        await call.message.edit_media(media=media, reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE == 'audio':
                    if call.message.video_note or call.message.voice or call.message.sticker or call.message.text:
                        await bot.send_audio(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                             reply_markup=reply_markup.as_markup())
                    else:
                        media = types.InputMediaAudio(media=OFFER_FILEID, caption=OFFER_TEXT)
                        await call.message.edit_media(media=media, reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE == 'document':
                    if call.message.video_note or call.message.voice or call.message.sticker or call.message.text:
                        await bot.send_document(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                                disable_content_type_detection=True,
                                                reply_markup=reply_markup.as_markup())
                    else:
                        media = types.InputMediaDocument(media=OFFER_FILEID, caption=OFFER_TEXT,
                                                         disable_content_type_detection=True)
                        await call.message.edit_media(media=media, reply_markup=reply_markup.as_markup())
                elif OFFER_MEDIATYPE == 'sticker':
                    await bot.send_sticker(chat_id, OFFER_FILEID)
                    await bot.send_message(chat_id=chat_id, text=OFFER_TEXT, reply_markup=reply_markup.as_markup(),
                                           disable_web_page_preview=True)
                elif OFFER_MEDIATYPE in ['video_note', 'telescope']:
                    if has_restricted:
                        text = l_post_has_restricted[lz].format(bot_un)
                        await bot.send_message(chat_id, text, disable_web_page_preview=True)
                    else:
                        await bot.send_video_note(chat_id=chat_id, video_note=OFFER_FILEID)
                    await bot.send_message(chat_id, OFFER_TEXT, reply_markup=reply_markup.as_markup(),
                                           disable_web_page_preview=True)
                elif OFFER_MEDIATYPE == 'voice':
                    if has_restricted:
                        text = l_post_has_restricted[lz].format(bot_un)
                        await bot.send_message(chat_id, text, disable_web_page_preview=True)
                        await bot.send_message(chat_id, OFFER_TEXT, reply_markup=reply_markup.as_markup(),
                                               disable_web_page_preview=True)
                    else:
                        await bot.send_voice(chat_id, OFFER_FILEID, caption=OFFER_TEXT,
                                             reply_markup=reply_markup.as_markup())
        else:
            if call and str(post_id) == await get_current_page_number(call):
                await call.message.edit_reply_markup(reply_markup=reply_markup.as_markup())
            elif OFFER_FILEID:
                OFFER_FILEID = ast.literal_eval(OFFER_FILEID) if OFFER_FILEID and '[' in OFFER_FILEID else OFFER_FILEID
                OFFER_MEDIATYPE = ast.literal_eval(
                    OFFER_MEDIATYPE) if OFFER_MEDIATYPE and '[' in OFFER_MEDIATYPE else OFFER_MEDIATYPE

                media = []
                for i in range(0, len(OFFER_FILEID)):
                    caption = OFFER_TEXT if i == 0 else None

                    if OFFER_MEDIATYPE[i] == 'photo':
                        media.append(
                            types.InputMediaPhoto(media=OFFER_FILEID[i], caption=caption, has_spoiler=OFFER_ISSPOILER))
                    elif OFFER_MEDIATYPE[i] == 'video':
                        media.append(
                            types.InputMediaVideo(media=OFFER_FILEID[i], caption=caption, has_spoiler=OFFER_ISSPOILER))
                    elif OFFER_MEDIATYPE[i] == 'audio':
                        media.append(types.InputMediaAudio(media=OFFER_FILEID[i], caption=caption))
                    elif OFFER_MEDIATYPE[i] == 'document':
                        media.append(types.InputMediaDocument(media=OFFER_FILEID[i], caption=caption,
                                                              disable_content_type_detection=True))

                await bot.send_media_group(chat_id, media)
                await bot.send_message(chat_id=chat_id, text=extra, reply_markup=reply_markup.as_markup())  # endregion
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def get_current_page_number(call):
    result = '_'
    try:
        lst = call.message.reply_markup.inline_keyboard
        for items in lst:
            for it in items:
                if it.text.startswith('·'):
                    result = it.text.strip('·')
                    result = result.strip()
                    break
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def broadcast_send_admin(bot, chat_id, lz, offer_id, BASE_D, ids):
    try:
        if ids == 'me':
            user_ids = [chat_id]
        elif not ids or ids == 'all':
            sql = "SELECT USER_TID FROM USER"
            data = await db_select_pg(sql, (), BASE_D)
            user_ids = [item[0] for item in data]
        else:
            sql = "SELECT USER_TID FROM USER"
            data = await db_select_pg(sql, (), BASE_D)
            user_ids = [item[0] for item in data]
            user_ids = [item for item in user_ids if str(item) in ids]

        duration = 0 if len(user_ids) < 50 else int(len(user_ids) / 50)
        if str(chat_id) in my_tids:
            text = l_broadcast_start[lz].format(duration)
            await bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)
        all_len = len(user_ids)
        max_size = 20  # 1
        # max_size = 1  # 1
        fact_len = 0

        sql = "SELECT OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_FILEIDNOTE, OFFER_BUTTON, OFFER_ISBUTTON, " \
              "OFFER_TGPHLINK, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, " \
              "OFFER_DT FROM OFFER WHERE OFFER_ID=$1"
        data = await db_select_pg(sql, (offer_id,), BASE_D)
        if not len(data): return

        while True:
            try:
                random.shuffle(user_ids)
                await asyncio.sleep(0.05)
                tmp_user_ids = [user_ids.pop() for _ in range(0, max_size) if len(user_ids)]
                coroutines = [send_user(bot, tmp_user_id, offer_id, data[0]) for tmp_user_id in tmp_user_ids]
                results = await asyncio.gather(*coroutines)

                for result in results:
                    if result:
                        fact_len += 1

                if not len(user_ids): break
                per = int(float(len(user_ids)) / float(all_len) * 100.0)

                if str(chat_id) in my_tids:
                    text = l_broadcast_process[lz].format(100 - per)
                    await bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.info(log_ % {str(e)})
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        if str(chat_id) not in my_tids:
            sql = "DELETE FROM OFFER WHERE OFFER_ID=$1"
            await db_change_pg(sql, (offer_id,), BASE_D)

        text = l_broadcast_finish[lz].format(fact_len)
        await bot.send_message(chat_id, text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def send_user(bot, chat_id, offer_id, item, message_id=None, cur_=1):
    result = None
    try:
        OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_FILEIDNOTE, OFFER_BUTTON, OFFER_ISBUTTON, OFFER_TGPHLINK, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, OFFER_DT = item

        len_ = 1
        if OFFER_ISBUTTON:
            # reply_markup = await create_replymarkup2(bot, offer_id, OFFER_BUTTON, 'ofr')
            reply_markup = InlineKeyboardBuilder()
        else:
            reply_markup = InlineKeyboardBuilder()

        if '[' in OFFER_MEDIATYPE:
            OFFER_FILEID = ast.literal_eval(OFFER_FILEID)
            OFFER_MEDIATYPE = ast.literal_eval(OFFER_MEDIATYPE)
            OFFER_TGPHLINK = ast.literal_eval(OFFER_TGPHLINK)
            len_ = len(OFFER_FILEID)

            OFFER_FILEID = OFFER_FILEID[cur_ - 1] if message_id else OFFER_FILEID[0]
            OFFER_MEDIATYPE = OFFER_MEDIATYPE[cur_ - 1] if message_id else OFFER_MEDIATYPE[0]
            OFFER_TGPHLINK = OFFER_TGPHLINK[cur_ - 1] if message_id else OFFER_TGPHLINK[0]

        if OFFER_ISTGPH and OFFER_TGPHLINK and '[' not in OFFER_TGPHLINK:
            OFFER_MEDIATYPE = 'text'
            OFFER_TEXT = OFFER_TEXT if OFFER_TEXT and OFFER_TEXT != '' else str_empty
            OFFER_TEXT = f"<a href='{OFFER_TGPHLINK}'>​</a>{OFFER_TEXT}"

            if OFFER_ISGALLERY:
                OFFER_TEXT = '' if OFFER_TEXT == str_empty and OFFER_MEDIATYPE != 'text' else OFFER_TEXT
                buttons = [
                    types.InlineKeyboardButton(text="←", callback_data=f'pst_{chat_id}_{offer_id}_{cur_}_{len_}_prev'),
                    types.InlineKeyboardButton(text=f"{cur_}/{len_}",
                                               switch_inline_query_current_chat=f"{offer_id} ~"),
                    types.InlineKeyboardButton(text="→",
                                               callback_data=f'pst_{chat_id}_{offer_id}_{cur_}_{len_}_next'), ]
                reply_markup.row(*buttons)

        if '[' in OFFER_MEDIATYPE and not message_id:
            media = []
            for i in range(0, len(OFFER_FILEID)):
                caption = OFFER_TEXT if i == 0 else None

                if OFFER_MEDIATYPE[i] == 'photo':
                    media.append(
                        types.InputMediaPhoto(media=OFFER_FILEID[i], caption=caption, has_spoiler=OFFER_ISSPOILER))
                elif OFFER_MEDIATYPE[i] == 'video':
                    media.append(
                        types.InputMediaVideo(media=OFFER_FILEID[i], caption=caption, has_spoiler=OFFER_ISSPOILER))
                elif OFFER_MEDIATYPE[i] == 'audio':
                    media.append(types.InputMediaAudio(media=OFFER_FILEID[i], caption=caption))
                elif OFFER_MEDIATYPE[i] == 'document':
                    media.append(types.InputMediaDocument(media=OFFER_FILEID[i], caption=caption,
                                                          disable_content_type_detection=True))

            result = await bot.send_media_group(chat_id, media)
        if OFFER_MEDIATYPE == 'text':
            # await bot.send_message(chat_id=5491025132, text='OFFER_TEXT2')
            result = await bot.send_message(chat_id=chat_id, text=OFFER_TEXT, disable_web_page_preview=not OFFER_ISTGPH,
                                            disable_notification=OFFER_ISSILENCE, reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE in ['gif', 'animation']:
            result = await bot.send_animation(chat_id=chat_id, animation=OFFER_FILEID, caption=OFFER_TEXT,
                                              has_spoiler=OFFER_ISSPOILER, disable_notification=OFFER_ISSILENCE,
                                              reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE == 'photo':
            result = await bot.send_photo(chat_id=chat_id, photo=OFFER_FILEID, caption=OFFER_TEXT,
                                          has_spoiler=OFFER_ISSPOILER, disable_notification=OFFER_ISSILENCE,
                                          reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE == 'video':
            result = await bot.send_video(chat_id=chat_id, video=OFFER_FILEID, caption=OFFER_TEXT,
                                          has_spoiler=OFFER_ISSPOILER, disable_notification=OFFER_ISSILENCE,
                                          reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE == 'audio':
            result = await bot.send_audio(chat_id=chat_id, audio=OFFER_FILEID, caption=OFFER_TEXT,
                                          disable_notification=OFFER_ISSILENCE, reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE == 'voice':
            has_restricted = (await bot.get_chat(chat_id)).has_restricted_voice_and_video_messages

            if has_restricted:
                result = await bot.send_voice(chat_id=chat_id, voice=OFFER_FILEID, caption=OFFER_TEXT,
                                              disable_notification=OFFER_ISSILENCE,
                                              reply_markup=reply_markup.as_markup())
            else:
                result = await bot.send_audio(chat_id=chat_id, audio=OFFER_FILEID, caption=OFFER_TEXT,
                                              disable_notification=OFFER_ISSILENCE,
                                              reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE == 'document':
            result = await bot.send_document(chat_id=chat_id, document=OFFER_FILEID, caption=OFFER_TEXT,
                                             disable_notification=OFFER_ISSILENCE, disable_content_type_detection=True,
                                             reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE in ['video_note', 'telescope']:
            has_restricted = (await bot.get_chat(chat_id)).has_restricted_voice_and_video_messages

            if has_restricted:
                result = await bot.send_video(chat_id=chat_id, video=OFFER_FILEID, caption=OFFER_TEXT,
                                              has_spoiler=OFFER_ISSPOILER, disable_notification=OFFER_ISSILENCE,
                                              reply_markup=reply_markup.as_markup())
            else:
                result = await bot.send_video_note(chat_id=chat_id, video_note=OFFER_FILEID,
                                                   disable_notification=OFFER_ISSILENCE,
                                                   reply_markup=reply_markup.as_markup())
        elif OFFER_MEDIATYPE == 'sticker':
            result = await bot.send_sticker(chat_id=chat_id, sticker=OFFER_FILEID, disable_notification=OFFER_ISSILENCE,
                                            reply_markup=reply_markup.as_markup())

        if result and OFFER_ISPIN and not message_id and isinstance(result, list):
            await bot.pin_chat_message(chat_id=chat_id, message_id=result[0].message_id, disable_notification=False)
        elif result and OFFER_ISPIN and not message_id:
            await bot.pin_chat_message(chat_id=chat_id, message_id=result.message_id, disable_notification=False)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def generate_calendar_admin(bot, state, lz, chat_id, message_id=None, is_new=True):
    try:
        data = await state.get_data()
        shift_month = data.get('shift_month', 0)
        is_timer = data.get('is_timer', None)

        dt_ = datetime.now(timezone.utc) + timedelta(hours=0) + timedelta(days=32 * shift_month)
        if shift_month:
            dt_ = datetime(year=dt_.year, month=dt_.month, day=1)

        month_dic = {1: l_month_1[lz], 2: l_month_2[lz], 3: l_month_3[lz], 4: l_month_4[lz], 5: l_month_5[lz],
                     6: l_month_6[lz], 7: l_month_7[lz], 8: l_month_8[lz], 9: l_month_9[lz], 10: l_month_10[lz],
                     11: l_month_11[lz], 12: l_month_12[lz]}
        month = month_dic[dt_.month]

        reply_markup = InlineKeyboardBuilder()
        buttons = [types.InlineKeyboardButton(text="«", callback_data=f'calendar_left'),
                   types.InlineKeyboardButton(text=f"{month} {dt_.year}", callback_data='cb_99'),
                   types.InlineKeyboardButton(text="»", callback_data=f'calendar_right'), ]
        reply_markup.row(*buttons)

        buttons_ = [types.InlineKeyboardButton(text=l_weekday_1[lz], callback_data='cb_99'),
                    types.InlineKeyboardButton(text=l_weekday_2[lz], callback_data='cb_99'),
                    types.InlineKeyboardButton(text=l_weekday_3[lz], callback_data='cb_99'),
                    types.InlineKeyboardButton(text=l_weekday_4[lz], callback_data='cb_99'),
                    types.InlineKeyboardButton(text=l_weekday_5[lz], callback_data='cb_99'),
                    types.InlineKeyboardButton(text=l_weekday_6[lz], callback_data='cb_99'),
                    types.InlineKeyboardButton(text=l_weekday_7[lz], callback_data='cb_99'), ]
        reply_markup.row(*buttons_)

        week_first_day = datetime(year=dt_.year, month=dt_.month, day=1).weekday() + 1
        buttons_ = []
        for i in range(0, 6 * 7):
            buttons_.append(types.InlineKeyboardButton(text=" ", callback_data=f'cb_99'))

        month_days = monthrange(dt_.year, dt_.month)[1]
        for i in range(week_first_day + dt_.day - 1, month_days + week_first_day):
            cb_ = f'cb_{i - week_first_day + 1}..{dt_.month}..{dt_.year}'
            buttons_[i - 1] = types.InlineKeyboardButton(text=f"{i - week_first_day + 1}", callback_data=cb_)

        tmp = []
        for i in range(0, len(buttons_)):
            tmp.append(buttons_[i])
            if len(tmp) >= 7:
                reply_markup.row(*tmp)
                tmp = []
        text = l_post_timer[lz] if is_timer else l_post_date[lz]

        if is_new:
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup.as_markup())
        else:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                        reply_markup=reply_markup.as_markup())
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def callbacks_ofr_admin(bot, FsmOffer, call, state, BASE_D, bot_un):
    try:
        chat_id = call.from_user.id
        cmd = str(call.data.split("_")[1])
        post_id = int(call.data.split("_")[-1])
        offer_id = int(call.data.split("_")[-2])
        lz = await lz_code_pg(chat_id, call.from_user.language_code, BASE_D)
        has_restricted = (await bot.get_chat(chat_id)).has_restricted_voice_and_video_messages

        if cmd == 'new':
            await state.clear()

            await state.set_state(FsmOffer.text)

            await bot.send_message(call.from_user.id, l_post_text[lz], reply_markup=markupAdmin)
        elif cmd == 'del':
            await state.clear()

            sql = "DELETE FROM OFFER WHERE OFFER_ID=$1"
            await db_change_pg(sql, (offer_id,), BASE_D)

            await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id - 1,
                                    call)
        elif cmd == 'edit':
            await state.clear()

            await state.set_state(FsmOffer.text)
            await state.update_data(offer_id=offer_id)

            await bot.send_message(call.from_user.id, l_post_text[lz], reply_markup=markupAdmin)
        elif cmd == 'isbtn':
            sql = "SELECT OFFER_BUTTON, OFFER_ISBUTTON FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            OFFER_BUTTON, OFFER_ISBUTTON = data[0]

            if OFFER_BUTTON:
                OFFER_ISBUTTON = 0 if OFFER_ISBUTTON else 1
                sql = "UPDATE OFFER SET OFFER_ISBUTTON=$1 WHERE OFFER_ID=$2"
                await db_change_pg(sql, (OFFER_ISBUTTON, offer_id,), BASE_D)
                await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id,
                                        call)
            else:
                text = l_buttons_text[lz]
                await call.answer(text=text, show_alert=True)
        elif cmd == 'ispin':
            sql = "SELECT OFFER_ISPIN FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            OFFER_ISPIN = 0 if data[0][0] else 1
            sql = "UPDATE OFFER SET OFFER_ISPIN=$1 WHERE OFFER_ID=$2"
            await db_change_pg(sql, (OFFER_ISPIN, offer_id,), BASE_D)
            await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id, call)
        elif cmd == 'issilence':
            sql = "SELECT OFFER_ISSILENCE FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            OFFER_ISSILENCE = 0 if data[0][0] else 1
            sql = "UPDATE OFFER SET OFFER_ISSILENCE=$1 WHERE OFFER_ID=$2"
            await db_change_pg(sql, (OFFER_ISSILENCE, offer_id,), BASE_D)
            await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id, call)
        elif cmd == 'isgallery':
            sql = "SELECT OFFER_ISGALLERY, OFFER_FILEID FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            OFFER_ISGALLERY, OFFER_FILEID = data[0]

            if OFFER_FILEID and '[' in OFFER_FILEID:
                OFFER_ISGALLERY = 0 if data[0][0] else 1
                sql = "UPDATE OFFER SET OFFER_ISGALLERY=$1 WHERE OFFER_ID=$2"
                await db_change_pg(sql, (OFFER_ISGALLERY, offer_id,), BASE_D)
                await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id,
                                        call)
            else:
                text = l_gallery_text[lz]
                await call.answer(text=text, show_alert=True)
        elif cmd == 'ispreview':
            sql = "SELECT OFFER_ISTGPH, OFFER_TGPHLINK FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            OFFER_ISTGPH, OFFER_TGPHLINK = data[0]

            if not OFFER_TGPHLINK:
                text = l_preview_text[lz]
                await call.answer(text=text, show_alert=True)

            OFFER_ISTGPH = 0 if OFFER_ISTGPH else 1
            sql = "UPDATE OFFER SET OFFER_ISTGPH=$1 WHERE OFFER_ID=$2"
            await db_change_pg(sql, (OFFER_ISTGPH, offer_id,), BASE_D)
            await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id, call)
        elif cmd == 'isspoiler':
            sql = "SELECT OFFER_ISSPOILER, OFFER_MEDIATYPE FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            OFFER_ISSPOILER, OFFER_MEDIATYPE = data[0]

            if OFFER_MEDIATYPE and OFFER_MEDIATYPE in ['photo', 'animation', 'video'] or '[' in OFFER_MEDIATYPE:
                OFFER_ISSPOILER = 0 if data[0][0] else 1
                sql = "UPDATE OFFER SET OFFER_ISSPOILER=$1 WHERE OFFER_ID=$2"
                await db_change_pg(sql, (OFFER_ISSPOILER, offer_id,), BASE_D)
                await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id,
                                        call)
            else:
                text = l_spoiler_text[lz]
                await call.answer(text=text, show_alert=True)
        elif cmd == 'publication':
            await state.clear()
            await call.answer()

            reply_markup = InlineKeyboardBuilder()
            buttons = [types.InlineKeyboardButton(text=l_me[lz], callback_data=f"publication_me_{offer_id}"),
                       types.InlineKeyboardButton(text=l_all[lz], callback_data=f"publication_all_{offer_id}"),
                       types.InlineKeyboardButton(text=l_ids[lz], callback_data=f"publication_ids_{offer_id}"), ]
            reply_markup.add(*buttons).adjust(1)

            text = l_recipient[lz]
            await bot.send_message(chat_id, text, reply_markup=reply_markup.as_markup())
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def callbacks_publication_admin(bot, FsmIds, call, state, BASE_D):
    try:
        chat_id = call.from_user.id
        lz = await lz_code_pg(chat_id, call.from_user.language_code, BASE_D)
        data, option, offer_id = call.data.split('_')

        if option == 'me':
            asyncio.create_task(broadcast_send_admin(bot, chat_id, lz, offer_id, BASE_D, 'me'))
        elif option == 'all':
            asyncio.create_task(broadcast_send_admin(bot, chat_id, lz, offer_id, BASE_D, 'all'))
        elif option == 'ids':
            await state.set_state(FsmIds.start)
            await state.update_data(offer_id=offer_id)

            text = l_enter[lz]
            await bot.send_message(chat_id, text)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_ids_start_admin(bot, message, state, BASE_D):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)
        arr = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./?]', message.text)
        ids = [it for it in arr if it != '']
        data = await state.get_data()
        offer_id = data.get('offer_id')

        asyncio.create_task(broadcast_send_admin(bot, chat_id, lz, offer_id, BASE_D, ids))
        await state.clear()
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_text_admin(bot, FsmOffer, message, state, BASE_D):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)

        if message.text == '⬅️ Prev':
            await bot.send_message(chat_id, l_post_text[lz])
            await state.set_state(FsmOffer.text)
        elif message.text in ['➡️️ Next', '/Next']:
            await bot.send_message(chat_id, l_post_media[lz])
            await state.set_state(FsmOffer.media)
        else:
            if len(message.html_text) >= 1024:
                text = l_post_text_limit[lz].format(len(message.html_text))
                await bot.send_message(chat_id, text)
                return

            await state.update_data(offer_text=message.html_text)
            await bot.send_message(chat_id=chat_id, text=l_post_media[lz])
            await state.set_state(FsmOffer.media)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_album_admin(bot, FsmOffer, message, album, state, KEYS_JSON, MEDIA_D, BASE_D):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)

        offer_text = None
        offer_file_id = None
        offer_file_type = None
        offer_tgph_link = None
        file_name_part = None

        if message.text == '⬅️ Prev':
            await bot.send_message(chat_id, l_post_text[lz])
            await state.set_state(FsmOffer.text)
        elif message.text in ['➡️️ Next', '/Next']:
            if not offer_text:
                await state.update_data(offer_text=str_empty)

            await generate_calendar_admin(bot, state, lz, chat_id)
            await state.set_state(FsmOffer.date_)
        else:
            await bot.send_message(chat_id, l_post_media_wait[lz].format('album', 1))

            for obj in album:
                if obj.photo:
                    media_id = obj.photo[-1].file_id if len(obj.photo) == 1 else obj.photo[-2].file_id
                    media_type = 'photo'
                    dt_ = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.jpg')
                    file_name_part_new = f"{dt_}"
                elif obj.video:
                    media_id = obj.video.file_id
                    media_type = 'video'
                    file_name_part_new = obj.video.file_name or f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"
                elif obj.audio:
                    media_id = obj.audio.file_id
                    media_type = 'video_note'
                    file_name_part_new = obj.audio.file_name
                else:
                    media_id = obj.document.file_id
                    media_type = 'document'
                    file_name_part_new = obj.document.file_name

                file_name_part_new = file_name_part_new.replace(' ', '')
                file_name = os.path.join(MEDIA_D, file_name_part_new)
                file = await bot.get_file(media_id)
                await bot.download_file(file.file_path, file_name)

                file_link = await get_link_for_media(bot, chat_id, file_name, KEYS_JSON)
                file_link = '' if file_link is None else file_link
                if file_name and os.path.exists(file_name): os.remove(file_name)

                offer_tgph_link = (ast.literal_eval(str(offer_tgph_link)) + [file_link]) if offer_tgph_link else [
                    file_link]
                file_name_part = (ast.literal_eval(str(file_name_part)) + [file_name_part_new]) if file_name_part else [
                    file_name_part_new]
                offer_file_id = (ast.literal_eval(str(offer_file_id)) + [media_id]) if offer_file_id else [media_id]
                offer_file_type = (ast.literal_eval(str(offer_file_type)) + [media_type]) if offer_file_type else [
                    media_type]

                await state.update_data(offer_file_id=str(offer_file_id), offer_file_type=str(offer_file_type),
                                        offer_tgph_link=str(offer_tgph_link), file_name_part=str(file_name_part))
                await asyncio.sleep(0.05)

            if len(ast.literal_eval(str(offer_file_id))) < 2:
                await bot.send_message(chat_id=chat_id, text=l_post_media[lz])
                await state.set_state(FsmOffer.media)
                return

            await generate_calendar_admin(bot, state, lz, chat_id)
            await state.set_state(FsmOffer.date_)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_media_admin(bot, FsmOffer, message, state, KEYS_JSON, MEDIA_D, BASE_D, EXTRA_D):
    chat_id = message.from_user.id
    lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)

    try:
        data = await state.get_data()
        offer_text = data.get('offer_text', None)

        if message.text == '⬅️ Prev':
            await bot.send_message(chat_id, l_post_text[lz])
            await state.set_state(FsmOffer.text)
        elif message.text in ['➡️️ Next', '/Next']:
            if not offer_text:
                await state.update_data(offer_text=str_empty)

            text = l_post_button[lz].replace('XXXXX', message.chat.username) if message.chat.username else \
                l_post_button[lz].replace('XXXXX', '')
            await bot.send_message(chat_id, text)
            await state.set_state(FsmOffer.button)
        else:
            file_name = file_name_part = file_id = file_id_note = file_type = None
            file_name = ''
            if message.text:
                await bot.send_message(chat_id=chat_id, text=l_post_media[lz])
                return
            elif message.photo:
                file_id = message.photo[-1].file_id if len(message.photo) == 1 else message.photo[-2].file_id
                file_name_part = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.jpg')}"
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)
                file_type = 'photo'
            elif message.animation:
                await bot.send_message(chat_id, l_post_media_wait[lz].format('giff', 1))
                file_id = message.animation.file_id
                file_name_part = f"{message.animation.file_name}"
                file_name_part = file_name_part.replace(' ', '')
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)
                file_type = 'animation'

                if not (file_name.lower().endswith('.mp4') or file_name.lower().endswith(
                        '.gif') or file_name.lower().endswith('.giff')):
                    clip = VideoFileClip(file_name)
                    tmp_name = os.path.join(os.path.dirname(file_name), 'r_' + os.path.basename(file_name))
                    clip.write_videofile(tmp_name, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a',
                                         remove_temp=True)

                    if os.path.exists(file_name): os.remove(file_name)
                    file_name = os.path.join(os.path.dirname(file_name), get_name_without_ext(file_name) + '.mp4')
                    file_name_part = os.path.basename(file_name)
                    if os.path.exists(tmp_name): os.rename(tmp_name, file_name)
            elif message.sticker:
                if message.sticker.is_animated or message.sticker.is_video:
                    await bot.send_message(chat_id=chat_id, text=l_post_media[lz])
                    await state.set_state(FsmOffer.media)
                    return

                file_id = message.sticker.file_id
                dt_ = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.webp')
                file_name_part = f"{dt_}"
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)
                file_type = 'sticker'
            elif message.video:
                await bot.send_message(chat_id, l_post_media_wait[lz].format('video', 1))
                file_id = message.video.file_id
                file_name_part = message.video.file_name or f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"
                file_name_part = file_name_part.replace(' ', '')
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)

                clip = VideoFileClip(file_name)
                if int(clip.duration) < 60 and clip.size and clip.size[0] == clip.size[1] and clip.size[0] <= 640:
                    res = await bot.send_video_note(chat_id, types.FSInputFile(str(file_name)))
                    file_id = res.video_note.file_id
                    file_type = 'video_note'
                else:
                    file_type = 'video'
            elif message.audio:  # m4a
                file_id = message.audio.file_id
                file_name_part = f"{message.audio.file_name}"
                file_name_part = file_name_part.replace(' ', '')
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)
                file_type = 'audio'

                performer = message.from_user.username if message.from_user.username else '@performer'
                title = html.quote(message.from_user.first_name)
                thumbnail = types.InputFile(os.path.join(EXTRA_D, 'img.jpg'))
                res = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(file_name), thumbnail=thumbnail,
                                           title=title, performer=performer)
                file_id = res.audio.file_id
                await bot.delete_message(chat_id, res.message_id)
            elif message.voice:
                await bot.send_message(chat_id, l_post_media_wait[lz].format('voice', 1))
                file_id = message.voice.file_id
                dt_ = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.ogg')
                file_name_part = f"{dt_}"
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)
                file_type = 'voice'

                ogg_version = AudioSegment.from_ogg(file_name)
                ogg_version.export(file_name[:file_name.rfind('.')] + '.mp3', format="mp3")

                performer = message.from_user.username if message.from_user.username else '@performer'
                title = html.quote(message.from_user.first_name)
                thumbnail = types.InputFile(os.path.join(EXTRA_D, 'img.jpg'))
                res = await bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(file_name), thumbnail=thumbnail,
                                           title=title, performer=performer)
                file_id_note = res.audio.file_id
                await bot.delete_message(chat_id, res.message_id)
            elif message.video_note:
                file_id = message.video_note.file_id
                file_name_part = f"{datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S-%f.mp4')}"
                file_name = os.path.join(MEDIA_D, file_name_part)
                file = await bot.get_file(file_id)
                await bot.download_file(file.file_path, file_name)
                file_type = 'video_note'

                res = await bot.send_video(chat_id=chat_id, video=types.FSInputFile(file_name))
                file_id_note = res.video.file_id
                await bot.delete_message(chat_id, res.message_id)
            elif message.document:
                file_id = message.document.file_id
                file_name_part = f"{message.document.file_name}"
                file_name_part = file_name_part.replace(' ', '')
                file_type = 'document'

            offer_tgph_link = await get_link_for_media(bot, chat_id, file_name, KEYS_JSON)
            offer_tgph_link = '' if offer_tgph_link is None else offer_tgph_link
            if file_name and os.path.exists(file_name): os.remove(file_name)

            await state.update_data(offer_file_id=file_id, offer_file_id_note=file_id_note, offer_file_type=file_type,
                                    offer_tgph_link=offer_tgph_link, file_name_part=file_name_part)

            text = l_post_button[lz].replace('XXXXX', message.chat.username) if message.chat.username else \
                l_post_button[lz].replace('XXXXX', '')
            await bot.send_message(chat_id, text)
            await state.set_state(FsmOffer.button)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    # except FileIsTooBig as e:
    #     logger.info(log_ % str(e))
    #     await asyncio.sleep(round(random.uniform(0, 1), 2))
    #     await bot.send_message(chat_id, l_post_media_toobig[lz])
    except Exception as e:
        if 'too big' in str(e):
            await bot.send_message(chat_id, l_post_media_toobig[lz])
        else:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_button_admin(bot, FsmOffer, message, state, BASE_D):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)

        if message.text == '⬅️ Prev':
            await bot.send_message(message.from_user.id, l_post_media[lz])
            await state.set_state(FsmOffer.media)
        elif message.text in ['➡️️ Next', '/Next']:
            await generate_calendar_admin(bot, state, lz, chat_id)
            await state.set_state(FsmOffer.date_)
        else:
            res_ = await check_buttons(bot, chat_id, message.text.strip())
            if len(res_) == 0:
                text = l_post_button[lz].replace('XXXXX', message.chat.username) if message.chat.username else \
                    l_post_button[lz].replace('XXXXX', '')
                await bot.send_message(chat_id, text)
                await state.set_state(FsmOffer.button)
                return

            await state.update_data(offer_button=message.text.strip())
            await generate_calendar_admin(bot, state, lz, chat_id)
            await state.set_state(FsmOffer.date_)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_date_cb_admin(bot, FsmOffer, call, state, BASE_D):
    try:
        chat_id = call.from_user.id
        offer_date = call.data.split('_')[-1]
        if offer_date == '99': return
        lz = await lz_code_pg(chat_id, call.from_user.language_code, BASE_D)

        day_, month_, year_ = offer_date.split('..')
        dt_user = datetime(year=int(year_), month=int(month_), day=int(day_))
        dt_user = dt_user.strftime("%d-%m-%Y")
        await state.update_data(offer_date=offer_date)

        sql = "SELECT USER_TZ FROM USER WHERE USER_TID=$1"
        data = await db_select_pg(sql, (chat_id,), BASE_D)
        USER_TZ = data[0][0] if data[0][0] else "+00:00"
        offer_tz = USER_TZ
        await state.update_data(offer_tz=offer_tz)
        sign_ = USER_TZ[0]
        h_, m_ = USER_TZ.strip(sign_).split(':')
        dt_now = datetime.now(timezone.utc)
        if sign_ == "+":
            dt_cur = dt_now + timedelta(hours=int(h_), minutes=int(m_))
        else:
            dt_cur = dt_now - timedelta(hours=int(h_), minutes=int(m_))

        datetime_plus = (dt_cur + timedelta(hours=1)).strftime("%H:%M")
        datetime_current = dt_cur.strftime("%H:%M")

        text = l_generate_calendar_time[lz].format(dt_user, datetime_plus, datetime_current, USER_TZ)
        await bot.send_message(chat_id, text)
        await state.set_state(FsmOffer.time_)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def calendar_handler_admin(bot, call, state, BASE_D):
    try:
        chat_id = call.from_user.id
        lz = await lz_code_pg(chat_id, call.from_user.language_code, BASE_D)
        message_id = call.message.message_id
        shift = call.data.split('_')[-1]

        data = await state.get_data()
        shift_month = data.get('shift_month', 0)

        if shift == 'left':
            shift_month = 0 if shift_month == 0 else shift_month - 1
        elif shift == 'right':
            shift_month = shift_month + 1

        await state.update_data(shift_month=shift_month)
        await generate_calendar_admin(bot, state, lz, chat_id, message_id, False)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_date_admin(bot, FsmOffer, message, state, BASE_D):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)

        if message.text == '⬅️ Prev':
            text = l_post_button[lz].replace('XXXXX', message.chat.username) if message.chat.username else \
                l_post_button[lz].replace('XXXXX', '')
            await bot.send_message(chat_id, text)
            await state.set_state(FsmOffer.button)
        else:
            await bot.send_message(chat_id, l_post_finish[lz])
            await state.set_state(FsmOffer.finish)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_time_admin(bot, FsmOffer, message, state, BASE_D):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)
        text = message.text.strip()

        data = await state.get_data()
        offer_date = data.get('offer_date')
        day_, month_, year_ = offer_date.split('..')
        dt_user = datetime(year=int(year_), month=int(month_), day=int(day_))

        if message.text == '⬅️ Prev':
            await generate_calendar_admin(bot, state, lz, chat_id)
            await state.set_state(FsmOffer.date_)
        elif message.text in ['➡️️ Next', '/Next']:
            await bot.send_message(chat_id, l_post_finish[lz])
            await state.set_state(FsmOffer.finish)
        else:
            sql = "SELECT USER_TZ FROM USER WHERE USER_TID=$1"
            data = await db_select_pg(sql, (chat_id,), BASE_D)
            USER_TZ = data[0][0] if data[0][0] else "+00:00"
            offer_tz = USER_TZ
            await state.update_data(offer_tz=offer_tz)
            sign_ = USER_TZ[0]
            h_, m_ = USER_TZ.strip(sign_).split(':')
            dt_now = datetime.now(timezone.utc)
            if sign_ == "+":
                dt_cur = dt_now + timedelta(hours=int(h_), minutes=int(m_))
            else:
                dt_cur = dt_now - timedelta(hours=int(h_), minutes=int(m_))
            datetime_plus = (dt_cur + timedelta(hours=1)).strftime("%H:%M")
            datetime_current = dt_cur.strftime("%H:%M")

            try:
                arr = text.strip().split(':')
                dt_user_new = datetime(year=int(year_), month=int(month_), day=int(day_), hour=int(arr[0]),
                                       minute=int(arr[1]))
                if dt_user_new < dt_cur:
                    await message.answer(text=l_post_time_future[lz])
                    return
            except Exception as e:
                logger.info(log_ % str(e))
                text = l_generate_calendar_time[lz].format(dt_user.strftime("%d-%m-%Y"), datetime_plus,
                                                           datetime_current, USER_TZ)
                await bot.send_message(chat_id, text)
                return

            offer_dt = dt_user_new.strftime('%d-%m-%Y %H:%M')
            await state.update_data(offer_dt=offer_dt)

            await bot.send_message(chat_id, l_post_finish[lz])
            await state.set_state(FsmOffer.finish)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fsm_finish_admin(bot, FsmOffer, message, state, EXTRA_D, BASE_D, bot_un):
    try:
        chat_id = message.from_user.id
        lz = await lz_code_pg(chat_id, message.from_user.language_code, BASE_D)
        has_restricted = (await bot.get_chat(chat_id)).has_restricted_voice_and_video_messages

        if message.text == '⬅️ Prev':
            await generate_calendar_admin(bot, state, lz, chat_id)
            await state.set_state(FsmOffer.date_)
        elif message.text in ['➡️️ Next', '/Next']:
            data = await state.get_data()
            offer_id = data.get('offer_id', None)
            offer_text = data.get('offer_text', None)
            offer_file_type = data.get('offer_file_type', 'text')
            default_photo = await pre_upload(bot, chat_id, 'text.jpg', 'photo', EXTRA_D, BASE_D)
            file_name_part = data.get('file_name_part', None)
            offer_file_id = data.get('offer_file_id', default_photo)
            offer_file_id_note = data.get('offer_file_id_note')

            offer_button = data.get('offer_button', None)
            offer_isbutton = 1 if offer_button else 0
            offer_tgph_link = data.get('offer_tgph_link', None)
            if offer_tgph_link and '[' in offer_tgph_link:
                offer_istgph = 1 if len([it for it in ast.literal_eval(str(offer_tgph_link)) if it != '']) else 0
            else:
                offer_istgph = 1 if offer_tgph_link else 0

            offer_tz = data.get('offer_tz', "+00:00")
            offer_dt = data.get('offer_dt', None)

            if offer_id:
                sql = "UPDATE OFFER SET OFFER_USERTID=$1, OFFER_TEXT=$2, OFFER_MEDIATYPE=$3, OFFER_FILENAME=$4, " \
                      "OFFER_FILEID=$5, OFFER_FILEIDNOTE=$6, OFFER_BUTTON=$7, OFFER_ISBUTTON=$8, OFFER_TGPHLINK=$9, " \
                      "OFFER_ISTGPH=$10, OFFER_DT=$11, OFFER_TZ=$12, OFFER_STATUS=$13 WHERE OFFER_ID=$14"
                await db_change_pg(sql, (
                    chat_id, offer_text, offer_file_type, file_name_part, offer_file_id, offer_file_id_note,
                    offer_button, offer_isbutton, offer_tgph_link, offer_istgph, offer_dt, offer_tz, 1, offer_id,),
                                   BASE_D)
            else:
                sql = "INSERT INTO OFFER (OFFER_USERTID, OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILENAME, " \
                      "OFFER_FILEID, OFFER_FILEIDNOTE, OFFER_BUTTON, OFFER_ISBUTTON, OFFER_TGPHLINK, OFFER_ISTGPH, " \
                      "OFFER_DT, OFFER_TZ, OFFER_STATUS) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) ON CONFLICT DO NOTHING"
                await db_change_pg(sql, (
                    chat_id, offer_text, offer_file_type, file_name_part, offer_file_id, offer_file_id_note,
                    offer_button, offer_isbutton, offer_tgph_link, offer_istgph, offer_dt, offer_tz, 1,), BASE_D)

            sql = "SELECT * FROM OFFER"
            data = await db_select_pg(sql, (), BASE_D)
            items = [item[0] for item in data]
            view_post_id = items.index(offer_id) + 1 if offer_id else len(data)
            await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, view_post_id)
            await state.clear()
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


def get_keyboard_admin(data, src, post_id=1):
    row_width = len(data) if len(data) < 5 else 5
    reply_markup = InlineKeyboardBuilder()
    btns = get_numbers_with_mark(data, post_id, row_width)
    buttons = []

    for i in range(1, row_width + 1):
        arr = re.split(r'\s|[«‹·›»]', btns[i - 1])  # ('\s|(?<!\d)[,.](?!\d)', s)
        page_i = list(filter(None, arr))[0]
        page_name = f'offers_{src}_{str(int(page_i))}'
        buttons.append(types.InlineKeyboardButton(text=btns[i - 1], callback_data=page_name))
    reply_markup.add(*buttons).adjust(row_width)

    return reply_markup


async def callbacks_offers_admin(bot, FsmOffer, call, state, BASE_D, bot_un):
    try:
        chat_id = call.from_user.id
        post_id = int(call.data.split("_")[-1])
        lz = await lz_code_pg(chat_id, call.from_user.language_code, BASE_D)
        has_restricted = (await bot.get_chat(chat_id)).has_restricted_voice_and_video_messages

        await show_offers_admin(bot, FsmOffer, chat_id, lz, state, has_restricted, BASE_D, bot_un, post_id, call)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def gallery_handler_admin(bot, call, state, BASE_D):
    try:
        await state.clear()
        chat_id = call.from_user.id
        message_id = call.message.message_id
        data, option, offer_id, cur_, len_ = call.data.split("_")
        offer_id = int(offer_id)
        cur_ = int(cur_)
        len_ = int(len_)

        if option == 'prev':
            sql = "SELECT OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_FILEIDNOTE, OFFER_BUTTON, OFFER_ISBUTTON, " \
                  "OFFER_TGPHLINK, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, " \
                  "OFFER_DT FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            if not len(data): return

            cur_ = len_ if cur_ == 1 and option == 'prev' else cur_ - 1
            await send_user(bot, chat_id, offer_id, data[0], message_id, cur_)
        elif option == 'next':
            sql = "SELECT OFFER_TEXT, OFFER_MEDIATYPE, OFFER_FILEID, OFFER_FILEIDNOTE, OFFER_BUTTON, OFFER_ISBUTTON, " \
                  "OFFER_TGPHLINK, OFFER_ISTGPH, OFFER_ISSPOILER, OFFER_ISPIN, OFFER_ISSILENCE, OFFER_ISGALLERY, " \
                  "OFFER_DT FROM OFFER WHERE OFFER_ID=$1"
            data = await db_select_pg(sql, (offer_id,), BASE_D)
            if not len(data): return

            cur_ = 1 if cur_ == len_ and option == 'next' else cur_ + 1
            await send_user(bot, chat_id, offer_id, data[0], message_id, cur_)
        elif data[1] == 'cur':
            pass
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def edit_simple(bot, chat_id, post_id, message_id, cur_, BASE_D):
    result = None
    try:
        sql = "SELECT POST_TEXT, POST_MEDIATYPE, POST_FILEID, POST_FILEIDNOTE, POST_BUTTONS, POST_ISBUTTON, " \
              "POST_TGPHLINK, POST_ISTGPH, POST_ISGALLERY, POST_ISSPOILER FROM POST WHERE POST_ID=$1"
        data_posts = await db_select_pg(sql, (post_id,), BASE_D)
        if not len(data_posts): return
        item = data_posts[0]
        POST_TEXT, POST_MEDIATYPE, POST_FILEID, POST_FILEIDNOTE, POST_BUTTONS, POST_ISBUTTON, POST_TGPHLINK, POST_ISTGPH, POST_ISGALLERY, POST_ISSPOILER = item

        len_ = 0
        POST_TEXT = POST_TEXT if POST_TEXT else str_empty
        # reply_markup = await create_replymarkup2(bot, post_id,
        #                                          POST_BUTTONS) if POST_ISBUTTON else InlineKeyboardBuilder()
        reply_markup = InlineKeyboardBuilder()
        if '[' in POST_MEDIATYPE and POST_ISGALLERY:
            POST_FILEID = ast.literal_eval(POST_FILEID)
            POST_MEDIATYPE = ast.literal_eval(POST_MEDIATYPE)
            POST_TGPHLINK = ast.literal_eval(POST_TGPHLINK)

            len_ = len(POST_FILEID)
            POST_FILEID = POST_FILEID[cur_ - 1]
            POST_MEDIATYPE = POST_MEDIATYPE[cur_ - 1]
            POST_TGPHLINK = POST_TGPHLINK[cur_ - 1]

        if POST_ISTGPH and POST_TGPHLINK:
            POST_MEDIATYPE = 'text'
            POST_TEXT = POST_TEXT if POST_TEXT and POST_TEXT != '' else str_empty
            POST_TEXT = f"<a href='{POST_TGPHLINK}'>​</a>{POST_TEXT}"

        if POST_ISGALLERY:
            POST_TEXT = '' if POST_TEXT == str_empty and POST_MEDIATYPE != 'text' else POST_TEXT
            buttons = [
                types.InlineKeyboardButton(text="←", callback_data=f'pst_{chat_id}_{post_id}_0_{cur_}_{len_}_prev'),
                types.InlineKeyboardButton(text=f"{cur_}/{len_}",
                                           switch_inline_query_current_chat=f"{post_id} ~"),
                types.InlineKeyboardButton(text="→", callback_data=f'pst_{chat_id}_{post_id}_0_{cur_}_{len_}_next'), ]
            reply_markup.row(*buttons)

        if POST_MEDIATYPE == 'text':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=POST_TEXT,
                                        reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE == 'photo':
            media = types.InputMediaPhoto(media=POST_FILEID, caption=POST_TEXT, has_spoiler=POST_ISSPOILER)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,

                                         reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE in ['gif', 'animation']:
            media = types.InputMediaAnimation(media=POST_FILEID, caption=POST_TEXT, has_spoiler=POST_ISSPOILER)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE == 'video':
            media = types.InputMediaVideo(media=POST_FILEID, caption=POST_TEXT, has_spoiler=POST_ISSPOILER)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE in ['video_note', 'telescope']:
            media = types.InputMediaVideo(media=POST_FILEIDNOTE, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE == 'audio':
            media = types.InputMediaAudio(media=POST_FILEID, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE == 'voice':
            media = types.InputMediaAudio(media=POST_FILEIDNOTE, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_MEDIATYPE == 'document':
            media = types.InputMediaDocument(media=POST_FILEID, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        else:
            OFFER_FILEID = ast.literal_eval(POST_FILEID) if POST_FILEID and '[' in POST_FILEID else POST_FILEID
            OFFER_MEDIATYPE = ast.literal_eval(
                POST_MEDIATYPE) if POST_MEDIATYPE and '[' in POST_MEDIATYPE else POST_MEDIATYPE

            media = []
            POST_TEXT = None if POST_TEXT == str_empty else POST_TEXT
            for i in range(0, len(OFFER_FILEID)):
                caption = POST_TEXT if i == 0 else None

                if OFFER_MEDIATYPE[i] == 'photo':
                    media.append(
                        types.InputMediaPhoto(media=OFFER_FILEID[i], caption=caption, has_spoiler=POST_ISSPOILER))
                elif OFFER_MEDIATYPE[i] == 'video':
                    media.append(
                        types.InputMediaVideo(media=OFFER_FILEID[i], caption=caption, has_spoiler=POST_ISSPOILER))
                elif OFFER_MEDIATYPE[i] == 'audio':
                    media.append(types.InputMediaAudio(media=OFFER_FILEID[i], caption=caption))
                elif OFFER_MEDIATYPE[i] == 'document':
                    media.append(types.InputMediaDocument(media=OFFER_FILEID[i], caption=caption,
                                                          disable_content_type_detection=True))

            await bot.send_media_group(chat_id, media)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def edit_simple2(bot, chat_id, user_id, entity_id, post_id, message_id, cur_, BASE_CHN):
    result = None
    try:
        sql = "SELECT POST_ID, POST_TYPE, POST_TEXT, POST_FID, POST_FIDNOTE, POST_LNK, POST_BUTTONS, " \
              "POST_ISBUTTON, POST_ISSOUND, POST_ISSILENCE, POST_ISPIN, POST_ISPREVIEW, POST_ISSPOILER, " \
              "POST_ISGALLERY, POST_TZ, POST_DT, POST_TARGET, POST_BLOG, POST_WEB FROM POST WHERE POST_ID=$1"
        data_posts = await db_select_pg(sql, (post_id,), BASE_CHN)
        if not len(data_posts): return
        item = data_posts[0]
        POST_ID, POST_TYPE, POST_TEXT, POST_FID, POST_FIDNOTE, POST_LNK, POST_BUTTONS, POST_ISBUTTON, POST_ISSOUND, POST_ISSILENCE, POST_ISPIN, POST_ISPREVIEW, POST_ISSPOILER, POST_ISGALLERY, POST_TZ, POST_DT, POST_TARGET, POST_BLOG, POST_WEB = item

        len_ = 0
        POST_TEXT = POST_TEXT if POST_TEXT else str_empty
        # reply_markup = await create_replymarkup3(entity_id, post_id,
        #                                          POST_BUTTONS) if POST_ISBUTTON else InlineKeyboardBuilder()

        reply_markup = InlineKeyboardBuilder()
        if '[' in POST_TYPE and POST_ISGALLERY:
            POST_FID = ast.literal_eval(POST_FID)
            POST_TYPE = ast.literal_eval(POST_TYPE)
            POST_LNK = ast.literal_eval(POST_LNK)

            len_ = len(POST_FID)
            POST_FID = POST_FID[cur_ - 1]
            POST_TYPE = POST_TYPE[cur_ - 1]
            POST_LNK = POST_LNK[cur_ - 1]

        if POST_ISPREVIEW and POST_LNK:
            POST_TYPE = 'text'
            POST_TEXT = POST_TEXT if POST_TEXT and POST_TEXT != '' else str_empty
            POST_TEXT = f"<a href='{POST_LNK}'>​</a>{POST_TEXT}"

        if POST_ISGALLERY:
            button_id = 1
            sql = "SELECT CHAT_TID FROM PUSH WHERE POST_ID=$1 AND BTN_BID=$2"
            data_in = await db_select_pg(sql, (post_id, button_id,), BASE_CHN)
            if chat_id in [it[0] for it in data_in]:
                sql = "DELETE FROM PUSH WHERE CHAT_TID=$1 AND POST_ID=$2 AND BTN_BID=$3"
                await db_change_pg(sql, (chat_id, post_id, button_id,), BASE_CHN)
            else:
                sql = "INSERT INTO PUSH (CHAT_TID, CHAT_FULLNAME, CHAT_USERNAME, CHAT_ISPREMIUM, POST_ID, BTN_BID) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING"
                await db_change_pg(sql, (chat_id, 'full_name', 'username', 'is_premium', post_id, button_id,), BASE_CHN)
            sql = "SELECT BTN_BID FROM PUSH WHERE POST_ID=$1"
            data = await db_select_pg(sql, (post_id,), BASE_CHN)
            counters = {it[0]: sum(1 for x in data if x[0] == it[0]) for it in data}

            # reply_markup = await create_replymarkup3(entity_id, post_id, POST_BUTTONS,
            #                                          counters) if POST_ISBUTTON else InlineKeyboardBuilder()

            reply_markup = InlineKeyboardBuilder()
            POST_TEXT = '' if POST_TEXT == str_empty and POST_TYPE != 'text' else POST_TEXT
            if chat_id == user_id:
                middle = types.InlineKeyboardButton(text=f"{cur_}/{len_}",
                                                    switch_inline_query_current_chat=f"{entity_id} {post_id} ~")
            else:
                middle = types.InlineKeyboardButton(text=f"{cur_}/{len_}",
                                                    callback_data=f'pst_{entity_id}_{post_id}_0_{cur_}_{len_}_cur')

            buttons = [
                types.InlineKeyboardButton(text="←", callback_data=f'pst_{entity_id}_{post_id}_0_{cur_}_{len_}_prev'),
                middle, types.InlineKeyboardButton(text="→",
                                                   callback_data=f'pst_{entity_id}_{post_id}_0_{cur_}_{len_}_next'), ]
            reply_markup.row(*buttons)

        if POST_TYPE == 'text':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=POST_TEXT,
                                        reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'photo':
            media = types.InputMediaPhoto(media=POST_FID, caption=POST_TEXT, has_spoiler=POST_ISSPOILER)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,

                                         reply_markup=reply_markup.as_markup())
        elif POST_TYPE in ['gif', 'animation']:
            media = types.InputMediaAnimation(media=POST_FID, caption=POST_TEXT, has_spoiler=POST_ISSPOILER)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'video':
            media = types.InputMediaVideo(media=POST_FID, caption=POST_TEXT, has_spoiler=POST_ISSPOILER)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_TYPE in ['video_note', 'telescope']:
            media = types.InputMediaVideo(media=POST_FIDNOTE, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'audio':
            media = types.InputMediaAudio(media=POST_FID, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'voice':
            media = types.InputMediaAudio(media=POST_FIDNOTE, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'document':
            media = types.InputMediaDocument(media=POST_FID, caption=POST_TEXT)
            await bot.edit_message_media(media=media, chat_id=chat_id, message_id=message_id,
                                         reply_markup=reply_markup.as_markup())
        else:
            POST_FID = ast.literal_eval(POST_FID) if POST_FID and '[' in POST_FID else POST_FID
            POST_TYPE = ast.literal_eval(POST_TYPE) if POST_TYPE and '[' in POST_TYPE else POST_TYPE

            media = []
            POST_TEXT = None if POST_TEXT == str_empty else POST_TEXT
            for i in range(0, len(POST_FID)):
                caption = POST_TEXT if i == 0 else None

                if POST_TYPE[i] == 'photo':
                    media.append(types.InputMediaPhoto(media=POST_FID[i], caption=caption, has_spoiler=POST_ISSPOILER))
                elif POST_TYPE[i] == 'video':
                    media.append(types.InputMediaVideo(media=POST_FID[i], caption=caption, has_spoiler=POST_ISSPOILER))
                elif POST_TYPE[i] == 'audio':
                    media.append(types.InputMediaAudio(media=POST_FID[i], caption=caption))
                elif POST_TYPE[i] == 'document':
                    media.append(types.InputMediaDocument(media=POST_FID[i], caption=caption,
                                                          disable_content_type_detection=True))

            await bot.send_media_group(chat_id, media)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


# endregion


# region app
async def podcast_start_app(app, UB_TID, lz, ENT_TID, MEDIA_D, BASE_D, BOT_TOKEN_APP, PROJECT_USERNAME):
    call_py = PyTgCalls(app)
    peer_chan = None
    result = {'answer': False, 'param': ''}
    try:
        # region data
        print(f"podcast_start_app start!")
        ENT_TID = int(ENT_TID) if str(ENT_TID).startswith('-') else str(ENT_TID)
        peer = await app.resolve_peer(ENT_TID)
        try:
            get_join_as = await app.invoke(GetGroupCallJoinAs(peer=peer))
            get_join_as_lst = [it for it in get_join_as.peers if it.QUALNAME == 'types.PeerChannel']
            if not len(get_join_as_lst):
                title = f"👩🏽‍💻 Landing Channel #{random.randrange(100, 999)}"
                res = await app.create_channel(title=title, description=f"verified chan 💙{random.randrange(100, 999)}")
                peer_chan = await app.resolve_peer(res.id)
                newusername_ = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(10, 20)))
                username_chan = f"{newusername_}_{random.randrange(100, 999)}_chan"[0:31]
                _ = await app.invoke(UpdateUsername(channel=peer_chan, username=username_chan))
                print(f"@{username_chan}: {title}")
                get_join_as = await app.invoke(GetGroupCallJoinAs(peer=peer))
                get_join_as_lst = [it for it in get_join_as.peers if it.QUALNAME == 'types.PeerChannel']

            if len(get_join_as_lst):
                peer_chan = await app.resolve_peer(int(f"-100{get_join_as_lst[-1].channel_id}"))
                await app.invoke(SaveDefaultGroupCallJoinAs(peer=peer, join_as=peer_chan))
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))

        dt_ = utils.datetime_to_timestamp(datetime.now() + timedelta(minutes=1))
        call = await app.invoke(
            CreateGroupCall(peer=peer, random_id=dt_, rtmp_stream=False, title=l_podcast_start[lz], schedule_date=dt_))
        await asyncio.sleep(10)
        call = InputGroupCall(id=call.updates[0].call.id, access_hash=call.updates[0].call.access_hash)
        await app.invoke(StartScheduledGroupCall(call=call))
        await call_py.start()

        schema_name = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'BOT'
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'
        # endregion

        max_cnt = 256
        while max_cnt > 0:
            max_cnt -= 1
            # region begin of POCAST_TID
            sql = "SELECT UB_CPODCAST, UB_CPODCASTSRC, UB_CPODCASTDST FROM UB WHERE UB_TID=$1"
            data_ub = await db_select_pg(sql, (UB_TID,), BASE_D)
            print(f"{UB_TID=}, {data_ub=}")
            if not len(data_ub): return
            UB_CPODCAST, UB_CPODCASTSRC, UB_CPODCASTDST = data_ub[0]
            if not (UB_CPODCAST[0] == '☑' and UB_CPODCASTSRC and UB_CPODCASTDST): return
            try:
                POCAST_TIDs = json.loads(UB_CPODCASTSRC)
            except:
                POCAST_TIDs = []
            status_, loop_, order_ = UB_CPODCAST
            if order_ != '☑': random.shuffle(POCAST_TIDs)
            if not len(POCAST_TIDs): return
            # endregion

            for POCAST_TID in POCAST_TIDs:
                print(f"{POCAST_TIDs=}, {UB_CPODCAST=}")
                sql = f"SELECT POST_TID, POST_TYPE, POST_TEXT, POST_MEDIA FROM {schema_name}_{str(ENT_TID).replace('-', '')}.POST WHERE POST_TID=$1"
                data_post = await db_select_pg(sql, (int(POCAST_TID),), BASE_D)
                print(f"{data_post=}")
                if not len(data_post) and not len(POCAST_TIDs): return
                if not len(data_post): continue
                POST_TID, POST_TYPE, POST_TEXT, POST_MEDIA = data_post[0]

                print(f"ready: {POST_TID=}, {UB_CPODCAST=}")
                try:
                    POST_MEDIA = json.loads(POST_MEDIA)
                except:
                    POST_MEDIA = []

                for item in POST_MEDIA:
                    extra_bot = Bot(token=BOT_TOKEN_APP)
                    POST_FILENAME = '*'
                    duration = 60
                    try:
                        POST_TYPE = item['file_type']
                        POSTB_FID = item['fileb_id']
                        POST_FILENAME = os.path.join(MEDIA_D, str(UB_TID), item['file_name'])
                        print(f"{POST_TYPE=}, {POSTB_FID=}, {POST_FILENAME=}")
                        is_audio = POST_TYPE in ['document'] and POST_FILENAME.lower().endswith(('.mp3', '.ogg'))
                        is_video_ = POST_TYPE in ['document'] and POST_FILENAME.lower().endswith(('.mp4', '.mov'))

                        if POST_TYPE in ['audio', 'voice'] or is_audio:
                            file = await extra_bot.get_file(POSTB_FID)
                            await extra_bot.download_file(file.file_path, POST_FILENAME)
                            stream = MediaStream(POST_FILENAME, AudioQuality.HIGH)

                            try:
                                if POST_FILENAME.lower().endswith('.ogg'):
                                    ogg_audio = AudioSegment.from_ogg(POST_FILENAME)
                                    duration = int(len(ogg_audio) / 1000)
                                else:
                                    audio_ = AudioSegment.from_mp3(POST_FILENAME)
                                    duration = int(audio_.duration_seconds)
                            except Exception as e:
                                logger.info(log_ % str(e))
                                await asyncio.sleep(round(random.uniform(0, 1), 2))
                        elif POST_TYPE in ['video', 'video_note'] or is_video_:
                            file = await extra_bot.get_file(POSTB_FID)
                            await extra_bot.download_file(file.file_path, POST_FILENAME)
                            # stream = MediaStream(POST_FILENAME, AudioQuality.HIGH, VideoQuality.HD_720p)
                            # stream = MediaStream(POST_FILENAME, AudioQuality.MEDIUM, VideoQuality.SD_480p)
                            stream = MediaStream(POST_FILENAME, AudioQuality.LOW, VideoQuality.SD_360p)

                            try:
                                cap = cv2.VideoCapture(POST_FILENAME)
                                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                                fps = cap.get(cv2.CAP_PROP_FPS)
                                duration = frame_count / fps
                            except Exception as e:
                                logger.info(log_ % str(e))
                                await asyncio.sleep(round(random.uniform(0, 1), 2))
                        elif POST_TYPE in ['photo', 'animation', 'gif']:
                            file = await extra_bot.get_file(POSTB_FID)
                            await extra_bot.download_file(file.file_path, POST_FILENAME)
                            stream = MediaStream(POST_FILENAME)
                        else:
                            extract_links_ = await extract_links(POST_TEXT)
                            print(f"{extract_links_=}")
                            if not len(extract_links_):
                                continue
                            else:
                                stream = MediaStream(extract_links_[0])
                        if not stream: continue
                        logger.info(log_ % f"podcast_start_app starting... {ENT_TID=}, {POST_FILENAME=}, {duration=}")
                        # await tgcalls_app(app, lz, ENT_TID, stream, duration)

                        duration = 7200 if duration > 7200 else duration
                        await call_py.play(chat_id=ENT_TID, stream=stream,
                                           config=GroupCallConfig(join_as=peer_chan, auto_start=True))
                        await asyncio.sleep(duration)
                        logger.info(log_ % f"podcast_start_app finishing... {item=}")
                    except Exception as e:
                        logger.info(log_ % str(e))
                        await asyncio.sleep(round(random.uniform(0, 1), 2))
                    finally:
                        if POST_FILENAME and os.path.exists(POST_FILENAME): os.remove(POST_FILENAME)
                        await extra_bot.session.close()

            # region loop
            status_, loop_, order_ = UB_CPODCAST
            if loop_ != '☑':
                sql = "SELECT UB_CPODCAST FROM UB WHERE UB_TID=$1"
                data_config = await db_select_pg(sql, (UB_TID,), BASE_D)
                UB_CPODCAST = data_config[0][0]

                if len(UB_CPODCAST) > 0: UB_CPODCAST = f"☐{UB_CPODCAST[1:]}"
                print(f"loop: {UB_CPODCAST=}")
                sql = "UPDATE UB SET UB_CPODCAST=$1 WHERE UB_TID=$2"
                await db_change_pg(sql, (UB_CPODCAST, UB_TID), BASE_D)
                result = {'answer': 'loop', 'param': UB_CPODCAST}
                return
            # endregion
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        try:
            await call_py.leave_call(chat_id=ENT_TID)
        except:
            pass
        return result


async def tgcalls_app(app, lz, ENT_TID, stream, duration):
    result = peer_chan = None
    username_chan = title = ''
    try:
        duration = 7200 if duration > 7200 else duration
        ENT_TID = int(ENT_TID) if str(ENT_TID).startswith('-') else str(ENT_TID)
        peer = await app.resolve_peer(ENT_TID)

        try:
            get_join_as = await app.invoke(GetGroupCallJoinAs(peer=peer))
            get_join_as_lst = [it for it in get_join_as.peers if it.QUALNAME == 'types.PeerChannel']
            if not len(get_join_as_lst):
                title = f"👩🏽‍💻 Landing Channel #{random.randrange(100, 999)}"
                res = await app.create_channel(title=title, description=f"verified chan 💙{random.randrange(100, 999)}")
                peer_chan = await app.resolve_peer(res.id)
                newusername_ = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(10, 20)))
                username_chan = f"{newusername_}_{random.randrange(100, 999)}_chan"[0:31]
                _ = await app.invoke(UpdateUsername(channel=peer_chan, username=username_chan))
                print(f"@{username_chan}: {title}")
                get_join_as = await app.invoke(GetGroupCallJoinAs(peer=peer))
                get_join_as_lst = [it for it in get_join_as.peers if it.QUALNAME == 'types.PeerChannel']

            if len(get_join_as_lst):
                peer_chan = await app.resolve_peer(int(f"-100{get_join_as_lst[-1].channel_id}"))
                await app.invoke(SaveDefaultGroupCallJoinAs(peer=peer, join_as=peer_chan))
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))

        dt_ = utils.datetime_to_timestamp(datetime.now() + timedelta(minutes=1))
        call = await app.invoke(
            CreateGroupCall(peer=peer, random_id=dt_, rtmp_stream=False, title=l_podcast_start[lz], schedule_date=dt_))
        await asyncio.sleep(10)
        call = InputGroupCall(id=call.updates[0].call.id, access_hash=call.updates[0].call.access_hash)
        await app.invoke(StartScheduledGroupCall(call=call))

        call_py = PyTgCalls(app)
        await call_py.start()
        await call_py.play(chat_id=ENT_TID, stream=stream, config=GroupCallConfig(join_as=peer_chan, auto_start=True))
        await asyncio.sleep(duration)
        await call_py.play(chat_id=ENT_TID, stream=stream, config=GroupCallConfig(join_as=peer_chan, auto_start=True))
        await asyncio.sleep(duration)
        result = True
        await call_py.leave_call(chat_id=ENT_TID)
        print(f"@{username_chan}: {title} finish....")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


# endregion


# region pyrogram
async def get_session(SESSION_TID, SESSION_D, BASE_S, EXTRA_D, CONF_P, is_proxy=False):
    res = proxy = None
    try:
        sql = "SELECT SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_PHONE FROM SESSION WHERE SESSION_TID = ?"
        data = await db_select_pg(sql, (SESSION_TID,), BASE_S)
        if not len(data): return
        SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_PHONE = data[0]

        if is_proxy:
            proxy = await get_proxy(SESSION_TID, EXTRA_D, CONF_P)

        res = Client(name=str(os.path.join(SESSION_D, SESSION_NAME)), api_id=SESSION_APIID, api_hash=SESSION_APIHASH,
                     phone_number=SESSION_PHONE, proxy=proxy)
    finally:
        return res


async def is_my_chat(bot, chat_id, link, SESSIONS_D, EXTRA_D, CONF_P, BASE_S, BASE_E, is_history=False):
    result = None
    get_chat_history_count = 0
    try:
        sql = "SELECT SESSION_TID,SESSION_STATUS FROM SESSION WHERE SESSION_SPAM IS NOT '*' LIMIT 10"
        data = await db_select_pg(sql, (), BASE_S)
        random.shuffle(data)
        for item in data:
            SESSION_TID, SESSION_STATUS = item
            if not (await check_session_flood(SESSION_TID, BASE_S) and (
                    SESSION_STATUS == '' or SESSION_STATUS is None)): continue
            try:
                link = await correct_link(link)
                if not link: return

                # process
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (f'isChat', SESSION_TID,), BASE_S)

                async with await get_session(SESSION_TID, SESSIONS_D, BASE_S, EXTRA_D, CONF_P, False) as app:
                    try:
                        r = await join_my_chat(bot, app, chat_id, link, SESSION_TID, BASE_S)
                        if r is None:
                            logger.info(log_ % f"{link} is None")
                            return
                        txt_ = f"👩🏽‍💻 Администратор закрытой группы не принял заявки на вступление"
                        if r == -1:
                            await bot.send_message(chat_id, txt_)
                            return
                        if 'id' in r:
                            result = await app.get_chat(r.id)

                        if is_history and 'id' in r:
                            try:
                                get_chat_history_count = await app.get_chat_history_count(r.id)
                            except Exception as e:
                                logger.info(log_ % str(e))
                                await asyncio.sleep(round(random.uniform(0, 1), 2))
                    finally:
                        await leave_my_chat(app, result, link)
                break
            except (FloodWait, SlowmodeWait) as e:
                # wait_ = f"Wait: {datetime.fromtimestamp(e.value + 1, tz=timezone.utc).strftime('%H:%M:%S')}"
                wait_ = f"Wait: {datetime.fromtimestamp(e.value + 1, tz=timezone.utc).strftime('%H:%M:%S')}"
                logger.info(log_ % wait_)
                await asyncio.sleep(round(random.uniform(5, 10), 2))

                till_time = (datetime.now() + timedelta(seconds=e.value + 1)).strftime("%d-%m-%Y_%H-%M")
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                SESSION_STATUS = f'Wait {till_time}'
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
            except (UserDeactivatedBan, UserDeactivated, AuthKeyInvalid, AuthKeyUnregistered, AuthKeyDuplicated,
                    SessionExpired, SessionRevoked) as e:
                logger.info(log_ % f"{SESSION_TID} deactivated: {str(e)}")
                await asyncio.sleep(round(random.uniform(5, 10), 2))
                await delete_account(bot, SESSION_TID, SESSIONS_D, CONF_P, BASE_S)
            except Exception as e:
                logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(1, 2), 2))
            finally:
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
    except Exception as e:
        logger.info(log_ % str(e) + f"{BASE_E}")
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result, get_chat_history_count


async def is_invite_chat(bot, chat_id, link, SESSIONS_D, EXTRA_D, CONF_P, BASE_S, BASE_E):
    result = r = None
    try:
        sql = "SELECT SESSION_TID,SESSION_STATUS FROM SESSION WHERE SESSION_SPAM IS NOT '*'"
        data = await db_select_pg(sql, (), BASE_S)
        random.shuffle(data)
        for item in data:
            SESSION_TID, SESSION_STATUS = item
            if not (await check_session_flood(SESSION_TID, BASE_S) and (
                    SESSION_STATUS == '' or SESSION_STATUS is None)): continue
            try:
                link = await correct_link(link)
                if not link: continue

                # process
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (f'isChat', SESSION_TID,), BASE_S)

                async with await get_session(SESSION_TID, SESSIONS_D, BASE_S, EXTRA_D, CONF_P) as app:
                    try:
                        r = await join_my_chat(bot, app, chat_id, link, SESSION_TID, BASE_S)

                        # get_chat https://t.me/+KO7_fV4aGKZkYTUy
                        if r == -1 or r is None: return
                        r = await app.get_chat(r.id)
                        logger.info(log_ % f"{SESSION_TID} get_chat {r.id}")

                        if not (r.type.value in ['group', 'supergroup']):
                            text = "🚶 Вставь ссылку на группу, а не канал"
                            await bot.send_message(chat_id, text)
                        elif hasattr(r.permissions, 'can_invite_users') and not r.permissions.can_invite_users:
                            text = "🚶 Зайди в «Разрешения» группы и включи <i>участникам группы</i> возможность: " \
                                   "«Добавление участников»"
                            await bot.send_message(chat_id, text)
                        else:
                            text = "🚶 Начинаем проверку группы..\n#длительность 2мин"
                            await bot.send_message(chat_id, text)
                            # await asyncio.sleep(r_conf('AWAIT_JOIN'))

                            try:
                                get_chat_member = await app.get_chat_member(chat_id=r.id, user_id=int(SESSION_TID))
                                result = True if get_chat_member and get_chat_member.status.value == 'member' else False
                            except Exception as e:
                                logger.info(log_ % str(e))
                                await asyncio.sleep(round(random.uniform(1, 2), 2))

                    finally:
                        await leave_my_chat(app, r, link)
                break
            except (FloodWait, SlowmodeWait) as e:
                wait_ = f"Wait: {datetime.fromtimestamp(e.value + 1, tz=timezone.utc).strftime('%H:%M:%S')}"
                logger.info(log_ % wait_)
                await asyncio.sleep(round(random.uniform(5, 10), 2))

                till_time = (datetime.now() + timedelta(seconds=e.value + 1)).strftime("%d-%m-%Y_%H-%M")
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                SESSION_STATUS = f'Wait {till_time}'
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
            except (UserDeactivatedBan, UserDeactivated, AuthKeyInvalid, AuthKeyUnregistered, AuthKeyDuplicated,
                    SessionExpired, SessionRevoked) as e:
                logger.info(log_ % f"{SESSION_TID} deactivated: {str(e)}")
                await asyncio.sleep(round(random.uniform(5, 10), 2))
                await delete_account(bot, SESSION_TID, SESSIONS_D, CONF_P, BASE_S)
            except Exception as e:
                logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(1, 2), 2))
            finally:
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
    except Exception as e:
        logger.info(log_ % str(e) + f"{BASE_E}")
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def join_my_chat(bot, app, chat_id, link, SESSION_TID, BASE_S):
    result = None
    try:
        if 't.me/c/' in str(link):
            try:
                tmp = link.strip('https://t.me/c/').split('/')[0]
                peer_channel = await app.resolve_peer(int(f"-100{tmp}"))
                result = await app.invoke(functions.channels.JoinChannel(channel=peer_channel))
            except Exception as e:
                logger.info(log_ % str(e))
        else:
            result = await app.join_chat(link)
        await asyncio.sleep(1)
    except (FloodWait, SlowmodeWait) as e:
        text = log_ % f"Wait: {datetime.fromtimestamp(e.value + 1, tz=timezone.utc).strftime('%H:%M:%S')}"
        logger.info(text)
        await asyncio.sleep(round(random.uniform(5, 10), 2))

        till_time = (datetime.now() + timedelta(seconds=e.value + 1)).strftime("%d-%m-%Y_%H-%M")
        sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
        SESSION_STATUS = f'Wait {till_time}'
        await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
    except UserAlreadyParticipant as e:
        logger.info(log_ % f"UserAlreadyParticipant {link}: {str(e)}")
        try:
            result = await app.get_chat(link)
        except Exception:
            pass
    except (InviteHashExpired, InviteHashInvalid) as e:
        logger.info(log_ % str(e))
        try:
            result = await app.join_chat(link)
        except Exception:
            await bot.send_message(chat_id, f"️👩🏽‍💻 Link {link} is invalid or try later")
    except (UsernameInvalid, UsernameNotOccupied, ChannelBanned) as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
        await bot.send_message(chat_id, f"️👩🏽‍💻 Link {link} is invalid or try later")
    except BadRequest as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(2, 3), 2))

        try:
            result = await app.join_chat(link)
        except Exception:
            result = -1
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def leave_my_chat(app, r, link):
    try:
        if not r: return
        chat_id = r.id if r and ('t.me/+' in str(link) or 'join_my_chat/' in str(link)) else link
        # like_names_res = is_names(r.title)
        if r.username and f'ferey' in r.username: return

        await app.leave_chat(chat_id, True)  # logger.info(log_ % f"\t{link} leave chat")
    except (FloodWait, SlowmodeWait) as e:
        wait_ = f"Wait: {datetime.fromtimestamp(e.value + 1, tz=timezone.utc).strftime('%H:%M:%S')}"
        logger.info(log_ % wait_)
        await asyncio.sleep(e.value + 1)
    except Exception:
        # logger.info(log_ % f"leave_my_chat_error: {link} {str(e)}")
        await asyncio.sleep(round(random.uniform(5, 10), 2))


async def get_chat_members(bot, chat_id, link, SESSIONS_D, EXTRA_D, CONF_P, BASE_S, BASE_E):
    result = []
    r = None
    try:
        text = f"🚶 Проверяем участников группы..\n#длительность 1мин"
        await bot.send_message(chat_id, text)
        sql = "SELECT SESSION_TID,SESSION_STATUS FROM SESSION WHERE SESSION_SPAM IS NOT '*'"
        data = await db_select_pg(sql, (), BASE_S)
        random.shuffle(data)
        for item in data:
            tmp_members = []
            SESSION_TID, SESSION_STATUS = item
            if not (await check_session_flood(SESSION_TID, BASE_S) and (
                    SESSION_STATUS == '' or SESSION_STATUS is None)): continue
            try:
                link = await correct_link(link)
                if not link: continue

                # process
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (f'getChatMembers', SESSION_TID,), BASE_S)

                async with await get_session(SESSION_TID, SESSIONS_D, BASE_S, EXTRA_D, CONF_P) as app:
                    try:
                        r = await join_my_chat(bot, app, chat_id, link, SESSION_TID, BASE_S)

                        # get members
                        sql = "SELECT SESSION_TID FROM SESSION"
                        data_ = await db_select_pg(sql, (), BASE_S)
                        data_ = [str(item[0]) for item in data_]
                        try:
                            async for member in app.get_chat_members(r.id, filter=enums.ChatMembersFilter.SEARCH):
                                if member.user.username and not member.user.is_bot and not member.user.is_deleted and not member.user.is_scam and not member.user.is_fake and not member.user.is_support and str(
                                        member.user.id) not in data_:
                                    tmp_members.append(member.user.username)
                        except ChatAdminRequired as e:
                            logger.info(log_ % str(e))
                            await bot.send_message(chat_id, f"🔺 Требуются права админа")
                            return
                        except Exception as e:
                            logger.info(log_ % str(e))
                    finally:
                        await leave_my_chat(app, r, link)

                    result = tmp_members
                    break
            except (FloodWait, SlowmodeWait) as e:
                wait_ = f"Wait: {datetime.fromtimestamp(e.value + 1, tz=timezone.utc).strftime('%H:%M:%S')}"
                logger.info(log_ % wait_)
                await asyncio.sleep(round(random.uniform(5, 10), 2))

                till_time = (datetime.now() + timedelta(seconds=e.value + 1)).strftime("%d-%m-%Y_%H-%M")
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                SESSION_STATUS = f'Wait {till_time}'
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
            except (UserDeactivatedBan, UserDeactivated, AuthKeyInvalid, AuthKeyUnregistered, AuthKeyDuplicated,
                    SessionExpired, SessionRevoked) as e:
                logger.info(log_ % f"{SESSION_TID} deactivated: {str(e)}")
                await asyncio.sleep(round(random.uniform(5, 10), 2))
                await delete_account(bot, SESSION_TID, SESSIONS_D, CONF_P, BASE_S)
            except Exception as e:
                logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(1, 2), 2))
            finally:
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
    except Exception as e:
        logger.info(log_ % str(e) + f"{BASE_E}")
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def delete_account(bot, SESSION_TID, SESSIONS_D, CONF_P, BASE_S):
    try:
        sql = "SELECT SESSION_NAME FROM SESSION WHERE SESSION_TID=$1"
        data = await db_select_pg(sql, (SESSION_TID,), BASE_S)
        if not data:
            await bot.send_message(my_tid, f"✅ Account {SESSION_TID} doesnt exist")
            return
        SESSION_NAME = os.path.join(SESSIONS_D, f'{data[0][0]}.session')

        sql = "DELETE FROM SESSION WHERE SESSION_TID = ?"
        await db_change_pg(sql, (SESSION_TID,), BASE_S)

        sql = "DELETE FROM COMPANY WHERE COMPANY_FROMUSERTID = ?"
        await db_change_pg(sql, (SESSION_TID,), BASE_S)

        if os.path.exists(SESSION_NAME):
            os.remove(SESSION_NAME)
        await bot.send_message(my_tid, f"✅ deleteAccount {SESSION_TID} ok")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        await log(e, CONF_P)
        await asyncio.sleep(round(random.uniform(1, 2), 2))


async def delete_invalid_chat(chat, BASE_E):
    sql = "DELETE FROM CHANNEL WHERE CHANNEL_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    sql = "DELETE FROM CHAT WHERE CHAT_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    sql = "DELETE FROM USER WHERE USER_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    sql = "DELETE FROM \"BOT\" WHERE BOT_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    chat = chat.strip('@')

    sql = "DELETE FROM CHANNEL WHERE CHANNEL_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    sql = "DELETE FROM CHAT WHERE CHAT_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    sql = "DELETE FROM USER WHERE USER_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    sql = "DELETE FROM \"BOT\" WHERE BOT_USERNAME=$1"
    await db_change_pg(sql, (chat,), BASE_E)

    # chat = chat if 'https://' in chat else f"@{chat}"  # await send_to_admins(f"deleteInvalidChat {chat}")


async def check_session_flood(SESSION_TID, BASE_S):
    result = SESSION_TID
    try:
        sql = "SELECT SESSION_STATUS FROM SESSION WHERE SESSION_TID = ?"
        data = await db_select_pg(sql, (SESSION_TID,), BASE_S)
        if not data: return

        t_t = str(data[0][0]).split()
        if len(t_t) == 2:
            date_ = t_t[1].split('_')[0]
            time_ = t_t[1].split('_')[1]

            day = int(date_.split('-')[0])
            month = int(date_.split('-')[1])
            year = int(date_.split('-')[2])
            hour = int(time_.split('-')[0])
            minute = int(time_.split('-')[1])

            diff = datetime.now() - datetime(year=year, month=month, day=day, hour=hour, minute=minute)

            if diff.days >= 0:
                sql = "UPDATE SESSION SET SESSION_STATUS = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (None, SESSION_TID,), BASE_S)
                result = SESSION_TID
            else:
                result = None
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def check_session_limit(SESSION_TID, LIMIT_NAME, LIMIT, BASE_S):
    result = SESSION_TID
    try:
        sql = f"SELECT {LIMIT_NAME} FROM SESSION WHERE SESSION_TID = ?"
        data = await db_select_pg(sql, (SESSION_TID,), BASE_S)
        if not data: return

        t_t = str(data[0][0]).split()
        if len(t_t) == 2:
            msg_by_day = int(t_t[0])
            date_ = t_t[1].split('-')

            day = int(date_[0])
            month = int(date_[1])
            year = int(date_[2])

            diff = datetime.now() - datetime(year=year, month=month, day=day)

            if diff.days > 0:
                result = f"0 {datetime.now().strftime('%d-%m-%Y')}"
                sql = f"UPDATE SESSION SET {LIMIT_NAME} = ? WHERE SESSION_TID = ?"
                await db_change_pg(sql, (result, SESSION_TID,), BASE_S)
            elif msg_by_day < LIMIT:
                result = SESSION_TID
            else:
                result = None
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def check_inviteday(CONF_P, BASE_S, threshold=0):
    result = 0
    try:
        sql = "SELECT SESSION_TID,SESSION_INVITEDAY FROM SESSION WHERE SESSION_SPAM IS NOT '*'"
        data = await db_select_pg(sql, (), BASE_S)
        for item in data:
            try:
                SESSION_TID, SESSION_INVITEDAY = item
                INVITEDAY_LIMIT_ = r_conf('INVITEDAY_LIMIT', CONF_P)
                checkSessionLimit_ = await check_session_limit(SESSION_TID, 'SESSION_INVITEDAY', INVITEDAY_LIMIT_,
                                                               BASE_S)
                if SESSION_INVITEDAY == '' or SESSION_INVITEDAY is None:
                    result += INVITEDAY_LIMIT_
                elif await check_session_flood(SESSION_TID, BASE_S) and checkSessionLimit_:
                    result += r_conf('INVITEDAY_LIMIT', CONF_P) - int(SESSION_INVITEDAY.split()[0])
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))

        result = int(result * 0.6)
        if threshold:
            result = result if result < threshold else threshold
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def set_privacy(app):
    try:
        keys = [InputPrivacyKeyAddedByPhone(), InputPrivacyKeyChatInvite(), InputPrivacyKeyForwards(),
                InputPrivacyKeyPhoneCall(), InputPrivacyKeyPhoneNumber(), InputPrivacyKeyProfilePhoto(),
                InputPrivacyKeyStatusTimestamp(), InputPrivacyKeyVoiceMessages()]
        for key in keys:
            try:
                if key.QUALNAME == InputPrivacyKeyPhoneNumber().QUALNAME:
                    await app.invoke(SetPrivacy(key=key, rules=[InputPrivacyValueDisallowAll()]))
                elif key.QUALNAME == InputPrivacyKeyVoiceMessages().QUALNAME:
                    await app.invoke(SetPrivacy(key=key, rules=[InputPrivacyValueAllowAll()]))
                elif key.QUALNAME == InputPrivacyKeyProfilePhoto().QUALNAME:
                    await app.invoke(SetPrivacy(key=key, rules=[InputPrivacyValueAllowAll()]))
                else:
                    await app.invoke(SetPrivacy(key=key, rules=[InputPrivacyValueAllowContacts()]))
            except Exception as e:
                logger.info(log_ % f"{str(e)}")
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        try:
            await app.invoke(SetAccountTTL(ttl=AccountDaysTTL(days=365)))
            await app.invoke(SetAuthorizationTTL(authorization_ttl_days=365))
        except Exception as e:
            logger.info(log_ % f"{str(e)}")
            await asyncio.sleep(round(random.uniform(0, 1), 2))
    except (SlowmodeWait, FloodWait) as e:
        # await set_karma(e)
        await asyncio.sleep(e.value + 1)
    except Exception as e:
        logger.info(log_ % f"{str(e)}")
        await asyncio.sleep(round(random.uniform(0, 1), 2))


# endregion


# region apiGoogle
async def api_sync_all(value_many, spreadsheet_id, CONF_P, EXTRA_D, range_many='A2', sheet_id='Sheet1',
                       value_input_option='USER_ENTERED', major_dimension="ROWS"):
    scopes = r_conf('scopes', CONF_P)
    credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
    http_auth = credentials.authorize(httplib2.Http())
    sheets_service = build('sheets', 'v4', http=http_auth, cache_discovery=False)

    convert_value = []
    for item in value_many:
        convert_value.append(list(item))

    await api_write_cells(sheets_service, convert_value, range_many, spreadsheet_id, sheet_id, value_input_option,
                          major_dimension)


async def api_sync_update(value_many, spreadsheet_id, range_many, CONF_P, EXTRA_D, sheet_id='Sheet1',
                          value_input_option='USER_ENTERED', major_dimension="ROWS"):
    try:
        if range_many is None:
            logger.info(log_ % 'range_many is None')
            return
        scopes = r_conf('scopes', CONF_P)
        credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
        httpAuth = credentials.authorize(httplib2.Http())
        sheets_service = build('sheets', 'v4', http=httpAuth, cache_discovery=False)

        convert_value = []
        for item in value_many:
            convert_value.append(list(item))

        await api_write_cells(sheets_service, convert_value, range_many, spreadsheet_id, sheet_id, value_input_option,
                              major_dimension)
    except Exception as e:
        logger.info(log_ % str(e))


async def api_find_row_by_tid(USER_TID, CONF_P, EXTRA_D, sheet_id='Sheet1'):
    result = None
    try:
        scopes_ = r_conf('scopes', CONF_P)
        credential_file_ = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
        credentials_ = ServiceAccountCredentials.from_json_keyfile_name(credential_file_, scopes_)
        http_auth = credentials_.authorize(httplib2.Http())
        sheets_service = build('sheets', 'v4', http=http_auth, cache_discovery=False)
        spreadsheet_id = (r_conf('db_file_id', CONF_P))[0]

        values_list = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_id,
                                                                 fields='values').execute().get('values', [])

        row = 0
        for ix, item in enumerate(values_list):
            if str(USER_TID) in item:
                row = ix + 1
                break
        result = 'A' + str(row)
    finally:
        return result


async def api_write_cells(sheets_service, value_many, range_many, spreadsheet_id, sheet_id, valueInputOption,
                          majorDimension="ROWS"):
    result = False
    try:
        result = sheets_service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                                    body={"valueInputOption": valueInputOption,
                                                                          "data": [{"range": f"{sheet_id}!{range_many}",
                                                                                    "majorDimension": majorDimension,
                                                                                    "values": value_many, }]}).execute()
        logger.info(log_ % 'write to db ok')
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def api_append_cells(sheets_service, value_many, spreadsheet_id, valueInputOption):
    result = True
    try:
        sheets_service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range='A1',
                                                      valueInputOption=valueInputOption,
                                                      body={"values": value_many}).execute()

        logger.info(log_ % 'write to db ok')
    except Exception as e:
        logger.info(log_ % str(e))
        result = False
    return result


async def api_read_cells(sheets_service, range_many, spreadsheet_id, sheet_id='Sheet1'):
    result = None
    try:
        r = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id,
                                                            ranges=f"{sheet_id}!{range_many}").execute()

        result = r.get('valueRanges', [])[0]['values'] if len(r.get('valueRanges', [])) > 0 else None
        logger.info(log_ % 'read from db ok')
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


def get_random_color():
    """
    Создаю случайный цвет с альфа каном
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/other#Color
    :return:
    """
    return {"red": randrange(0, 255) / 255, "green": randrange(0, 255) / 255, "blue": randrange(0, 255) / 255,
            "alpha": randrange(0, 10) / 10  # 0.0 - прозрачный
            }


def api_create_file_or_folder(drive_service, mime_type, name, parent_id):
    creation_id = None
    try:
        body = {'name': name, 'mimeType': mime_type, 'parents': [parent_id],
                'properties': {'title': 'titleSpreadSheet', 'locale': 'ru_RU'}, 'locale': 'ru_RU'}
        result_folder = drive_service.files().create(body=body, fields='id').execute()
        creation_id = result_folder['id']
    finally:
        return creation_id


async def table_init(TABLE_API_JSON, CELL_NAMES, EXTRA_D, CONF_P, INI_D):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(EXTRA_D, TABLE_API_JSON),
                                                                       r_conf('scopes', CONF_P))
        httpAuth = credentials.authorize(httplib2.Http())
        drive_service = build('drive', 'v3', http=httpAuth, cache_discovery=False)
        file_list_dic = await api_get_file_list(drive_service, (r_conf('share_folder_id', CONF_P))[0], {})

        files = []
        db_file_name = 'db'
        files = await is_need_for_create(file_list_dic, files, 'application/vnd.google-apps.spreadsheet', db_file_name,
                                         CONF_P, INI_D)
        for i in range(0, len(files)):
            creation_id = api_create_file_or_folder(drive_service, 'application/vnd.google-apps.spreadsheet',
                                                    db_file_name, (r_conf('share_folder_id', CONF_P))[0])
            w_conf(get_new_key_config(files[i], CONF_P, INI_D), [creation_id], CONF_P, INI_D)
            await api_sync_all([CELL_NAMES], (r_conf('db_file_id', CONF_P))[0], CONF_P, EXTRA_D, 'A1')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def send_my_copy(bot, cnt, USER_TID, USER_USERNAME, result):
    try:
        # USER_TID = 5150111687
        await bot.copy_message(chat_id=int(USER_TID), from_chat_id=result.chat.id, message_id=result.message_id,
                               reply_markup=result.reply_markup)
        cnt += 1
        logger.info(log_ % f"\t{cnt}. send to user {USER_TID}-{USER_USERNAME} ok")
        await asyncio.sleep(0.05)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        logger.info(log_ % f"\tsend to user {USER_TID}-{USER_USERNAME} error")
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return cnt


async def api_get_file_list(drive_service, folder_id, tmp_dic=None, parent_name='', is_file=False):
    if tmp_dic is None:
        tmp_dic = {} or None
    if is_file:
        file = drive_service.files().get(fileId=folder_id, fields="id, name, size, modifiedTime, mimeType").execute()
        tmp_dic[file['id']] = [file['name'], file['mimeType'], parent_name, file['modifiedTime']]
        return tmp_dic
    q = "\'" + folder_id + "\'" + " in parents"
    fields = "nextPageToken, files(id, name, size, modifiedTime, mimeType)"
    results = drive_service.files().list(pageSize=1000, q=q, fields=fields).execute()
    items = results.get('files', [])
    for item in items:
        try:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                tmp_dic[item['id']] = [item['name'], item['mimeType'], parent_name, item['modifiedTime']]
                await api_get_file_list(drive_service, item['id'], tmp_dic, item['name'])
            else:
                tmp_dic[item['id']] = [item['name'], item['mimeType'], parent_name, item['modifiedTime']]
        except Exception as e:
            logger.info(log_ % str(e))

    tmp_dic_2 = {}
    for k, v in reversed(tmp_dic.items()):
        tmp_dic_2[k] = v

    return tmp_dic_2


async def upload_file(drive_service, name, post_media_name, folder_id):
    result = None
    try:
        if name == 'нет' or name is None: return

        request_ = drive_service.files().create(media_body=MediaFileUpload(filename=post_media_name, resumable=True),
                                                body={'name': name, 'parents': [folder_id]})
        response = None
        while response is None:
            status, response = request_.next_chunk()
            if status: logger.info(log_ % "Uploaded %d%%." % int(status.progress() * 100))
        logger.info(log_ % "Upload Complete!")
        # if os.path.exists(post_media_name):
        #     os.remove(post_media_name)
        result = True
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def api_dl_file(drive_service, id_, name, gdrive_mime_type, MEDIA_D):
    save_mime_type = None
    file_name = add = ''

    if gdrive_mime_type.endswith('document') and not (name.endswith('doc') or name.endswith('docx')):
        save_mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    elif gdrive_mime_type.endswith('sheet') and not (name.endswith('xls') or name.endswith('xlsx')):
        save_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif gdrive_mime_type.endswith('presentation') and not (name.endswith('ppt') or name.endswith('pptx')):
        save_mime_type = 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    elif gdrive_mime_type == 'application/vnd.google-apps.folder':
        return ''

    if save_mime_type:
        request_ = drive_service.files().export_media(fileId=id_, mimeType=save_mime_type)
    else:
        request_ = drive_service.files().get_media(fileId=id_)

    if request_:
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request_)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.info(log_ % "Download %d%%." % int(status.progress() * 100))

        if gdrive_mime_type.endswith('.spreadsheet'):
            add = '.xlsx'
        elif gdrive_mime_type.endswith('.document'):
            add = '.docx'
        elif gdrive_mime_type.endswith('.presentation'):
            add = '.pptx'
        file_name = return_cutted_filename(name, add, MEDIA_D)
        with io.open(file_name, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        await asyncio.sleep(1)
    return file_name


def return_cutted_filename(name, add, MEDIA_D):
    file_name = f'{MEDIA_D}/{name}{add}'
    l_ = len(file_name)
    diff = 255 - l_
    if diff <= 0:
        ext = get_ext(name)
        name = name[0:len(name) - 1 - abs(diff) - len(ext)] + ext
        file_name = f'{MEDIA_D}/{name}{add}'
    return file_name


def get_name_without_ext(file_name):
    name = file_name
    try:
        ext = get_ext(name)
        if ext != '':
            index_ext = str(name).rindex(ext)
            index_slash = str(name).rindex('/') + 1 if '/' in name else 0
            name = name[index_slash:index_ext]
    finally:
        return name


def get_ext(name):
    ext = ''
    try:
        index = str(name).rindex('.')
        ext = name[index:len(name)]
        if len(ext) > 5:
            ext = ''
    finally:
        return ext


async def is_need_for_create(file_list_dic, unit, mime_type, name, CONF_P, INI_D):
    flag = False
    for k, v in file_list_dic.items():
        if v[0] == name and v[1] == mime_type:
            flag = True
            w_conf(get_new_key_config(name, CONF_P, INI_D), [k], CONF_P, INI_D)
            break
    if not flag: unit.append(name)
    return unit


def is_exists_google_id(file_list_dic, mime_type, name, parent_name):
    result = None
    for k, v in file_list_dic.items():
        if v[0] == name and v[1] == mime_type and v[2] == parent_name:
            return k
    return result


def get_new_key_config(value, CONF_P, INI_D):
    new_key = ""
    try:
        CONF_P.read(INI_D)
        for k, v in CONF_P.items('CONFIG'):
            if value == ast.literal_eval(v)[0]:
                arr = str(k).split('_')
                new_key = f'{arr[0]}_{arr[1]}_id'
                break
    finally:
        return new_key


async def api_init(CONF_P, INI_D, EXTRA_D, fields_0):
    scopes = r_conf('scopes', CONF_P)
    credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
    httpAuth = credentials.authorize(httplib2.Http())
    drive_service = build('drive', 'v3', http=httpAuth, cache_discovery=False)
    file_list_dic = await api_get_file_list(drive_service, (r_conf('share_folder_id', CONF_P))[0], {})

    subflders = []
    mimeType_folder = 'application/vnd.google-apps.folder'
    static_folder_name = (r_conf('static_folder_name', CONF_P))[0]
    dynamic_folder_name = (r_conf('dynamic_folder_name', CONF_P))[0]
    subflders = await is_need_for_create(file_list_dic, subflders, mimeType_folder, static_folder_name, CONF_P, INI_D)
    subflders = await is_need_for_create(file_list_dic, subflders, mimeType_folder, dynamic_folder_name, CONF_P, INI_D)
    for i in range(0, len(subflders)):
        share_folder_id = (r_conf('share_folder_id', CONF_P))[0]
        creation_id = api_create_file_or_folder(drive_service, mimeType_folder, subflders[i], share_folder_id)
        w_conf(get_new_key_config(subflders[i], CONF_P, INI_D), [creation_id], CONF_P, INI_D)

    files = []
    mimeType_sheet = 'application/vnd.google-apps.spreadsheet'
    db_file_name = (r_conf('db_file_name', CONF_P))[0]
    files = await is_need_for_create(file_list_dic, files, mimeType_sheet, db_file_name, CONF_P, INI_D)
    for i in range(0, len(files)):
        db_file_name = (r_conf('db_file_name', CONF_P))[0]
        mimeType_sheet = 'application/vnd.google-apps.spreadsheet'
        share_folder_id = (r_conf('share_folder_id', CONF_P))[0]
        creation_id = api_create_file_or_folder(drive_service, mimeType_sheet, db_file_name, share_folder_id)
        w_conf(get_new_key_config(files[i], CONF_P, INI_D), [creation_id], CONF_P, INI_D)
        value_many = [fields_0]
        spreadsheetId = (r_conf('db_file_id', CONF_P))[0]
        await api_sync_all(value_many, spreadsheetId, CONF_P, EXTRA_D, 'A1')
    logger.info(log_ % 'api init ok')


async def get_cell_dialog(range_many, CONF_P, EXTRA_D):
    scopes = r_conf('scopes', CONF_P)
    credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
    http_auth = credentials.authorize(httplib2.Http())
    sheets_service = build('sheets', 'v4', http=http_auth, cache_discovery=False)
    spreadsheet_id = '1sQWH3NpJAh8t4QDmP-8vvc7XaCTx4Uflc6LADA9zvN8'
    sheet_id = 'Лист1'

    result = None
    try:
        ranges = f"{sheet_id}!{range_many}"
        r = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=ranges).execute()
        if ':' in range_many:
            result = r.get('valueRanges', [])[0]['values'] if len(r.get('valueRanges', [])) > 0 else None
            result = [item[0] for item in result]
        else:
            result = r.get('valueRanges', [])[0]['values'][0][0] if len(r.get('valueRanges', [])) > 0 else None
        logger.info(log_ % 'read from db ok')
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def get_list_of_send_folder(CONF_P, EXTRA_D):
    scopes = r_conf('scopes', CONF_P)
    credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
    httpAuth = credentials.authorize(httplib2.Http())
    drive_service = build('drive', 'v3', http=httpAuth, cache_discovery=False)

    tmp = []
    file_list_dic = await api_get_file_list(drive_service, (r_conf('dynamic_folder_id', CONF_P))[0], {})
    for k, v in file_list_dic.items():
        try:
            parent_folder = v[2]
            name_folder = v[0]
            datetime_ = datetime.now()
            if parent_folder == '' and datetime_ < datetime.strptime(name_folder, "%d-%m-%Y %H:%M").replace(
                    tzinfo=timezone.utc):
                tmp.append([name_folder, k])
        except Exception as e:
            logger.info(log_ % str(e))

    return tmp


async def save_post_to_google_drive(CONF_P, EXTRA_D, post_txt, post_btn, post_url, post_media_name, post_media_type,
                                    post_pin, post_time, post_media_options, post_users='*'):
    try:
        scopes = r_conf('scopes', CONF_P)
        credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
        httpAuth = credentials.authorize(httplib2.Http())
        drive_service = build('drive', 'v3', http=httpAuth, cache_discovery=False)
        file_list_dic = await api_get_file_list(drive_service, (r_conf('dynamic_folder_id', CONF_P))[0], {})

        mime_type_folder = 'application/vnd.google-apps.folder'
        id_time_folder = is_exists_google_id(file_list_dic, mime_type_folder, post_time.strftime("%d-%m-%Y %H:%M"), '')
        if id_time_folder is None:
            id_time_folder = api_create_file_or_folder(drive_service, 'application/vnd.google-apps.folder',
                                                       post_time.strftime("%d-%m-%Y %H:%M"),
                                                       (r_conf('dynamic_folder_id', CONF_P))[0])

        mime_type_sheet = 'application/vnd.google-apps.spreadsheet'
        id_InfoXlsx = is_exists_google_id(file_list_dic, mime_type_sheet, 'info', post_time.strftime("%d-%m-%Y %H:%M"))
        if id_InfoXlsx is None:
            mime_type_sheet = 'application/vnd.google-apps.spreadsheet'
            id_InfoXlsx = api_create_file_or_folder(drive_service, mime_type_sheet, 'info', id_time_folder)
            v_m = [["текст", "кнопка(имя)", "кнопка(ссылка)", "медиа", "медиа тип", "закрепить(pin)", "пользователи"]]
            spreadsheet_id = id_InfoXlsx
            await api_sync_all(value_many=v_m, spreadsheet_id=spreadsheet_id, CONF_P=CONF_P, EXTRA_D=EXTRA_D,
                               range_many='A1', major_dimension="COLUMNS")

        name = os.path.basename(post_media_name) if post_media_name else 'нет'
        if post_media_type == 'poll':
            post_txt = post_media_name
            name = str(post_media_options)
        else:
            await upload_file(drive_service, name, post_media_name, id_time_folder)

        v_m = [[post_txt, post_btn if post_btn else 'no', post_url if post_url else 'no', name,
                post_media_type if post_media_type else 'no', 'yes' if post_pin else 'no', post_users]]
        spreadsheet_id = id_InfoXlsx
        await api_sync_all(value_many=v_m, spreadsheet_id=spreadsheet_id, CONF_P=CONF_P, EXTRA_D=EXTRA_D,
                           range_many='B1', major_dimension="COLUMNS")
        logger.info(log_ % 'save to google ok')
    except Exception as e:
        logger.info(log_ % str(e))


# endregion


# region pay
async def update_subscribe(bot, BASE_D, BOT_TOKEN_E18B):
    result = []
    try:
        dt_ = datetime.now(timezone.utc)
        if not (dt_.hour % 2 == 0 and dt_.minute % 2 == 0 and dt_.second % 2 == 0): return
        sql = "SELECT USER_TID, USER_LZ, USER_DTPAID, USER_ISPAID FROM USER"
        data = await db_select_pg(sql, (), BASE_D)

        for item in data:
            try:
                USER_TID, USER_LZ, USER_DTPAID, USER_ISPAID = item

                if USER_ISPAID == 1 and USER_DTPAID and (
                        dt_ - datetime.strptime(USER_DTPAID, '%d-%m-%Y_%H-%M-%S').replace(
                    tzinfo=timezone.utc)).days > 31:
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
                    get_ = await bot.get_chat(chat_id=USER_TID)
                    chan_private_donate = channel_library_ru if USER_LZ == 'ru' else channel_library_en
                    extra_bot = Bot(token=BOT_TOKEN_E18B)
                    get_chat_member_ = await extra_bot.get_chat_member(chat_id=chan_private_donate, user_id=USER_TID)
                    await extra_bot.session.close()

                    if get_chat_member_.status in ['member', 'administrator', 'creator']:
                        USER_DTPAID = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S')
                        sql = "UPDATE USER SET USER_ISPAID=1, USER_USERNAME=$1, USER_FULLNAME=$2, USER_DTPAID=$3 " \
                              "WHERE USER_TID=$4"
                        await db_change_pg(sql, (get_.username, get_.full_name, USER_DTPAID, USER_TID,), BASE_D)
                    else:
                        sql = "UPDATE USER SET USER_ISPAID=0, USER_USERNAME=$1, USER_FULLNAME=$2 WHERE USER_TID=$3"
                        await db_change_pg(sql, (get_.username, get_.full_name, USER_TID,), BASE_D)
                elif USER_ISPAID == -1 and USER_DTPAID and (
                        dt_ - datetime.strptime(USER_DTPAID, '%d-%m-%Y_%H-%M-%S').replace(
                    tzinfo=timezone.utc)).days > 31:
                    result.append(
                        item)  # else:  #     sql = "UPDATE USER SET USER_USERNAME=$1, USER_FULLNAME=$2 WHERE USER_TID=$3"  #     await db_change_pg(sql, (get_.username, get_.full_name, USER_TID,), BASE_D)
            except TelegramRetryAfter as e:
                logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
                await asyncio.sleep(e.retry_after + 1)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def convert_domain_to_currency(domain):
    result = 'EUR'
    try:
        if domain == 'ae':
            result = 'AED'
        elif domain == 'af':
            result = 'AFN'
        elif domain == 'al':
            result = 'AFN'
        elif domain == 'am':
            result = 'AMD'
        elif domain == 'ar':
            result = 'ARS'
        elif domain == 'au':
            result = 'AUD'
        elif domain == 'az':
            result = 'AZN'
        elif domain == 'ba':
            result = 'BAM'
        elif domain == 'bd':
            result = 'BDT'
        elif domain == 'bg':
            result = 'BGN'
        elif domain == 'bn':
            result = 'BND'
        elif domain == 'bo':
            result = 'BOB'
        elif domain == 'br':
            result = 'BRL'
        elif domain == 'by':
            result = 'BYN'
        elif domain == 'ca':
            result = 'CAD'
        elif domain == 'ch':
            result = 'CHF'
        elif domain == 'cl':
            result = 'CLP'
        elif domain == 'cn':
            result = 'CNY'
        elif domain == 'co':
            result = 'COP'
        elif domain == 'cr':
            result = 'CRC'
        elif domain == 'cz':
            result = 'CZK'
        elif domain == 'dk':
            result = 'DKK'
        elif domain == 'do':
            result = 'DOP'
        elif domain == 'dz':
            result = 'DZD'
        elif domain == 'eg':
            result = 'EGP'
        elif domain == 'et':
            result = 'ETB'
        elif domain == 'uk':
            result = 'GBP'
        elif domain == 'ge':
            result = 'GEL'
        elif domain == 'gt':
            result = 'GTQ'
        elif domain == 'hk':
            result = 'HKD'
        elif domain == 'hh':
            result = 'HNL'
        elif domain == 'hr':
            result = 'HRK'
        elif domain == 'hu':
            result = 'HUF'
        elif domain == 'id':
            result = 'IDR'
        elif domain == 'il':
            result = 'ILS'
        elif domain == 'in':
            result = 'INR'
        elif domain == 'is':
            result = 'ISK'
        elif domain == 'jm':
            result = 'JMD'
        elif domain == 'ke':
            result = 'KES'
        elif domain == 'kg':
            result = 'KGS'
        elif domain == 'kr':
            result = 'KRW'
        elif domain == 'kz':
            result = 'KZT'
        elif domain == 'lb':
            result = 'LBP'
        elif domain == 'lk':
            result = 'LKR'
        elif domain == 'ma':
            result = 'MAD'
        elif domain == 'md':
            result = 'MDL'
        elif domain == 'mn':
            result = 'MNT'
        elif domain == 'mu':
            result = 'MUR'
        elif domain == 'mv':
            result = 'MVR'
        elif domain == 'mx':
            result = 'MXN'
        elif domain == 'my':
            result = 'MYR'
        elif domain == 'mz':
            result = 'MZN'
        elif domain == 'ng':
            result = 'NGN'
        elif domain == 'ni':
            result = 'NIO'
        elif domain == 'no':
            result = 'NOK'
        elif domain == 'np':
            result = 'NPR'
        elif domain == 'nz':
            result = 'NZD'
        elif domain == 'pa':
            result = 'PAB'
        elif domain == 'pe':
            result = 'PEN'
        elif domain == 'ph':
            result = 'PHP'
        elif domain == 'pk':
            result = 'PKR'
        elif domain == 'pl':
            result = 'PLN'
        elif domain == 'py':
            result = 'PYG'
        elif domain == 'qa':
            result = 'QAR'
        elif domain == 'ro':
            result = 'RON'
        elif domain == 'rs':
            result = 'RSD'
        elif domain == 'ru':
            result = 'RUB'
        elif domain == 'sa':
            result = 'SAR'
        elif domain == 'se':
            result = 'SEK'
        elif domain == 'sg':
            result = 'SGD'
        elif domain == 'th':
            result = 'THB'
        elif domain == 'tj':
            result = 'TJS'
        elif domain == 'tr':
            result = 'TRY'
        elif domain == 'tt':
            result = 'TTD'
        elif domain == 'tw':
            result = 'TWD'
        elif domain == 'tz':
            result = 'TZS'
        elif domain == 'ua':
            result = 'UAH'
        elif domain == 'ug':
            result = 'UGX'
        elif domain == 'us':
            result = 'USD'
        elif domain == 'uy':
            result = 'UYU'
        elif domain == 'uz':
            result = 'UZS'
        elif domain == 'vn':
            result = 'VND'
        elif domain == 'ye':
            result = 'YER'
        elif domain == 'za':
            result = 'ZAR'
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def create_invoice_link_my(BOT_TID, BOT_LC, msg_text, msg_btns, POST_LNK, BASE_D):
    result = None
    try:
        sql = "SELECT BOT_TOKEN, BOT_TOKENPAY FROM \"BOT\" WHERE BOT_TID=$1"
        data = await db_select_pg(sql, (BOT_TID,), BASE_D)
        if not len(data): return
        BOT_TOKEN, BOT_TOKENPAY = data[0]

        btn_name = msg_btns[0]['lbl'].encode('utf-16', 'surrogatepass').decode('utf-16')
        # msg_text = await replace_user_vars(chat_id, msg_text)
        msg_text = msg_text if msg_text and msg_text != '' else btn_name
        soup = BeautifulSoup(msg_text, 'html.parser')
        msg_text = soup.get_text()

        currency = await convert_domain_to_currency(BOT_LC)
        price = msg_btns[0]['lnk']
        amount = int(price.replace('.', '').replace(',', '')) if '.' in price or ',' in price else int(
            f"{msg_btns[0]['lnk']}")
        prices = [types.LabeledPrice(label=btn_name, amount=amount)]

        print(f"{POST_LNK=}")
        if POST_LNK:
            if '[' in POST_LNK:
                urls = ast.literal_eval(POST_LNK)
                photo_url = next((url for url in urls if str(url).endswith(('.png', '.jpg', '.jpeg'))), None)
            else:
                photo_url = POST_LNK if str(POST_LNK).endswith(('.png', '.jpg', '.jpeg')) else None
            print(f"{photo_url=}")
        else:
            photo_url = None
        print(f"{photo_url=}")

        msg_media = {'title': btn_name, 'description': msg_text, 'payload': f"{BOT_TID}_{amount}",
                     'provider_token': BOT_TOKENPAY, 'currency': currency, 'prices': prices, 'max_tip_amount': amount,
                     'suggested_tip_amounts': [amount], 'photo_url': photo_url}
        print(f'msg_media = {msg_media}')

        extra_bot = Bot(token=BOT_TOKEN)
        # result = await extra_bot.create_invoice_link(title=msg_media['title'], description=msg_media['description'],
        #                                              payload=msg_media['payload'],
        #                                              provider_token=msg_media['provider_token'],
        #                                              currency=msg_media['currency'], prices=msg_media['prices'],
        #                                              max_tip_amount=msg_media['max_tip_amount'],
        #                                              suggested_tip_amounts=msg_media['suggested_tip_amounts'])
        result = await extra_bot.create_invoice_link(title=msg_media['title'],
                                                     description=msg_media['description'],
                                                     payload=msg_media['payload'], currency='XTR',
                                                     prices=[LabeledPrice(label="XTR", amount=amount)],
                                                     photo_url=msg_media['photo_url'])

        await extra_bot.session.close()
        print(f'invoice_link = {result}')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def check_sub_pay(chat_id, lz, BOT_TOKEN_E18B, BASE_D):
    is_paid = False
    till_paid = ''
    try:
        USER_ISPAID = 0
        USER_DTPAID = ''
        dt_now = datetime.now(timezone.utc)
        USER_DT = dt_now.strftime('%d-%m-%Y_%H-%M-%S')
        extra_bot = None
        try:
            lib_id = channel_library_ru if lz == 'ru' else channel_library_en
            extra_bot = Bot(token=BOT_TOKEN_E18B)
            member_ = await extra_bot.get_chat_member(chat_id=lib_id, user_id=chat_id)
            if member_.status in ['member', 'administrator', 'creator']: is_paid = True
            print(f"check_sub_pay {is_paid=}")
        except Exception as e:
            logger.info(log_ % str(e))
        finally:
            if extra_bot: await extra_bot.session.close()

        sql = "SELECT USER_ISPAID, USER_DTPAID, USER_TYPAID, USER_DT, USER_LZ FROM USER WHERE USER_TID=$1"
        data_usr = await db_select_pg(sql, (chat_id,), BASE_D)

        if not len(data_usr):
            sql = "INSERT INTO USER (USER_TID, USER_DT) VALUES ($1, $2) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (chat_id, USER_DT,), BASE_D)
        else:
            USER_ISPAID, USER_DTPAID, USER_TYPAID, USER_DT, lz = data_usr[0]

        if is_paid:
            sql = "UPDATE USER SET USER_ISPAID=1, USER_DTPAID='', USER_TYPAID='all' WHERE USER_TID=$1"
            await db_change_pg(sql, (chat_id,), BASE_D)
        elif USER_ISPAID and USER_DTPAID:
            till_paid = dt_now.strptime(USER_DTPAID, "%d-%m-%Y_%H-%M-%S").replace(tzinfo=timezone.utc)
            print(f"{till_paid=}")

            if dt_now > till_paid:
                sql = "UPDATE USER SET USER_ISPAID=0, USER_DTPAID='', USER_TYPAID='' WHERE USER_TID=$1"
                await db_change_pg(sql, (chat_id,), BASE_D)
                till_paid = ''
            else:
                is_paid = True
                till_paid = till_paid.strftime('%d.%m.%Y')
        else:
            sql = "UPDATE USER SET USER_ISPAID=0, USER_DTPAID='', USER_TYPAID='' WHERE USER_TID=$1"
            await db_change_pg(sql, (chat_id,), BASE_D)
        print(f"check_sub_pay {is_paid=}, {till_paid=}")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return is_paid, till_paid


# endregion


# region web
async def check_webapp_hash(init_data, TOKEN_BOT, BOT_TOKEN_MAIN=None, extra=None):
    result = None
    try:
        if extra: print(f"{extra=}")
        parsed_data = dict(parse_qsl(init_data))  # return k/v, but not dict!
        if "auth_date" not in parsed_data: return
        auth_date = utils.timestamp_to_datetime(int(parsed_data['auth_date']))  # web_app opened seconds
        # print(f'seconds {(datetime.now() - auth_date).seconds}', init_data)
        # if (datetime.now() - auth_date).seconds > 2000 or "hash" not in parsed_data: return
        if (datetime.now() - auth_date).seconds > 20000 or "hash" not in parsed_data: return
        # какой смысл не делать с BOT_TOKEN_MAIN, если он используется в srv_bot_add и srv_app_upd

        hash_ = parsed_data.pop("hash")
        data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0)))

        BOT_TOKEN_MAIN = TOKEN_BOT if BOT_TOKEN_MAIN is None or BOT_TOKEN_MAIN == '' else BOT_TOKEN_MAIN
        # print(f"{BOT_TOKEN_MAIN=}")
        secret_key = hmac.new(key=b"WebAppData", msg=BOT_TOKEN_MAIN.encode(), digestmod=hashlib.sha256)
        calculated_hash = hmac.new(key=secret_key.digest(), msg=data_check_string.encode(),
                                   digestmod=hashlib.sha256).hexdigest()

        if calculated_hash != hash_:
            secret_key = hmac.new(key=b"WebAppData", msg=TOKEN_BOT.encode(), digestmod=hashlib.sha256)
            calculated_hash = hmac.new(key=secret_key.digest(), msg=data_check_string.encode(),
                                       digestmod=hashlib.sha256).hexdigest()
            if calculated_hash != hash_: return

        res = {}
        for key, value in parse_qsl(init_data):
            if (value.startswith("[") and value.endswith("]")) or (value.startswith("{") and value.endswith("}")):
                value = json.loads(value)
            res[key] = value

        result = res
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_vars_web_main(chat_id, username, full_name, lc, is_premium, utm_web, BASE_D, BOT_TOKEN_E18B):
    is_paid = False
    till_paid = ''
    lz = 'en'
    try:
        dt = lz = utm = None
        pays = []

        sql = "SELECT USER_TID, USER_LZ, USER_DT, USER_UTM, USER_PAY FROM \"USER\" WHERE USER_TID=$1"
        data_user = await db_select_pg(sql, (chat_id,), BASE_D)
        if len(data_user): USER_TID, lz, dt, utm, pays = data_user[0]

        if not dt:
            dt = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S')
        if not utm:
            utm = utm_web
        if not lz:
            if lc in ['zh', 'zh-chs', 'zh-cht', 'ja', 'ko', 'zh-CN', 'zh-TW', 'th', 'vi', 'tw', 'sg']:
                lz = 'zh'
            # arabic    # ir, af
            elif lc in ['ar-XA', 'ar', 'tr', 'ur', 'fa', 'tj', 'dz', 'eg', 'iq', 'sy', 'ae', 'sa', 'tn', 'ir', 'af']:
                lz = 'ar'
            # spanish   # portugal: 'pt', 'br', 'ao', 'mz'
            elif lc in ['es', 'ar', 'cl', 'co', 'cu', 've', 'bo', 'pe', 'ec', 'pt', 'br', 'ao', 'mz']:
                lz = 'es'
            # french
            elif lc in ['fr', 'ch', 'be', 'ca']:
                lz = 'fr'
            # europe
            elif lc in ['ru', 'kz', 'kg', 'uz', 'tm', 'md', 'am', 'uk-UA', 'uk', 'kk', 'tk', 'ky']:
                lz = 'ru'
            else:
                lz = 'en'

        if utm_web not in ['@FereyPostBot', '']:
            sql = """
                    INSERT INTO "USER" (USER_TID, USER_USERNAME, USER_FULLNAME, USER_LZ, USER_LC, USER_UTM, USER_ISPREMIUM, USER_DT) 
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (USER_TID) 
                    DO UPDATE SET 
                        USER_USERNAME = EXCLUDED.USER_USERNAME, 
                        USER_FULLNAME = EXCLUDED.USER_FULLNAME, 
                        USER_LZ = EXCLUDED.USER_LZ, 
                        USER_LC = EXCLUDED.USER_LC, 
                        USER_UTM = EXCLUDED.USER_UTM, 
                        USER_ISPREMIUM = EXCLUDED.USER_ISPREMIUM,
                        USER_DT = EXCLUDED.USER_DT
                """
            await db_change_pg(sql, (chat_id, username, full_name, lz, lc, utm, is_premium, dt,), BASE_D)

        try:
            print(f"{pays=}")
            if not pays: pays = '[]'
            pays = json.loads(pays)
        except Exception as e:
            logger.info(log_ % str(e))
            pays = []

        print(f"{pays=}")
        for pay in pays:
            try:
                if not (pay.get('TYPE', '') == 'SUB' and pay.get('DT_END', '')): continue
                DT_END = datetime.strptime(pay.get('DT_END'), '%d-%m-%Y_%H-%M-%S').replace(tzinfo=timezone.utc)
                print(f"{DT_END=}")
                if datetime.now(timezone.utc) <= DT_END:
                    is_paid = True
                    till_paid = DT_END.strftime('%d.%m.%Y')
            except Exception as e:
                logger.info(log_ % str(e))
                pass

        if not is_paid:
            extra_bot = None
            try:
                lib_id = channel_library_ru if lz == 'ru' else channel_library_en
                print(f"{channel_library_ru=}, {channel_library_en=}")
                extra_bot = Bot(token=BOT_TOKEN_E18B)
                member_ = await extra_bot.get_chat_member(chat_id=lib_id, user_id=chat_id)
                if member_.status in ['member', 'administrator', 'creator']: is_paid = True
                print(f"get_vars_web_main -> get_chat_member {is_paid=}")
            except Exception as e:
                logger.info(log_ % str(e))
            finally:
                if extra_bot: await extra_bot.session.close()
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return is_paid, till_paid, lz


# endregion


# region notes
# sys.path.append('../hub')
# print("In module products sys.path[0], __package__ ==", sys.path[-1], __package__)
# from .. .hub import xtra
# dp.register_chosen_inline_handler(chosen_inline_handler_fun, lambda chosen_inline_result: True)
# dp.register_inline_handler(inline_handler_main, lambda inline_handler_main_: True)
# channel_post_handler
# edited_channel_post_handler
# poll_handler - а это получается реакция на размещение опроса
# poll_answer_handler - реакция на голосование
# chat_join_request_handler
# errors_handler
# current_state

# apt install redis -y
# nano /etc/redis/redis.conf
# systemctl restart redis.service
# systemctl status redis
# redis-cli
# netstat -lnp | grep redis

# apt update && apt upgrade -y
# curl -fsSL https://deb.nodesource.com/setup_current.x | sudo -E bash -
# apt install -y nodejs build-essential nginx yarn
# npm install -g npm pm2@latest -g
# ufw allow 'Nginx Full'
# curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /usr/share/keyrings/yarnkey.gpg >/dev/null
# echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | tee /etc/apt/sources.list.d/yarn.list
# node -v
# nginx -v
# yarn -v

# systemctl restart nginx
# systemctl reload nginx
# snap install core;  snap refresh core
# apt remove python3-certbot-nginx certbot -y
# rm -rf /etc/letsencrypt/renewal/
# rm -rf /etc/letsencrypt/archive/
# rm -rf /etc/letsencrypt/live/
# rm -rf /opt/letsencrypt
# rm -rf /etc/letsencrypt
# snap install --classic certbot
# ln -s /snap/bin/certbot /usr/bin/certbot
# endregion


# region pst
async def ch_games(USER_GAMES, game, condition, balls=-1):
    try:
        dt = datetime.now(timezone.utc)
        dt_ = dt.strftime('%d-%m-%Y_%H-%M-%S')

        print(f"Текущее время: {dt_}")
        print(f"Игровые данные: {USER_GAMES}")
        print(f"Игра: {game}, Условие: {condition}, Баллы: {balls}")

        if condition:
            # if game not in USER_GAMES:
            #     USER_GAMES[game] = {'date': datetime.now(timezone.utc)}
            # dt_game = USER_GAMES[game].get('date')
            # print(f"Дата игры: {dt_game}")

            if game not in USER_GAMES or not USER_GAMES[game].get('date', None):
                print("Нет даты, устанавливаем новую")
                USER_GAMES[game] = {'date': dt_, 'balls': balls}
                print(f"Добавлена новая игра: {USER_GAMES[game]}")
            else:
                dt_game = USER_GAMES[game].get('date')
                dt_game = datetime.strptime(dt_game, "%d-%m-%Y_%H-%M-%S").replace(tzinfo=timezone.utc)
                print(f"Дата игры в datetime: {dt_game}")

                if (dt - dt_game).days >= 1 or balls == -1:
                    print("Прошел день, обновляем данные")
                    USER_GAMES[game]['date'] = dt_
                    USER_GAMES[game]['balls'] = balls
                else:
                    print("День не прошел, данные не меняем")
        else:
            print("Условие не выполнено, обнуляем баллы")
            if isinstance(USER_GAMES.get(game), dict):
                USER_GAMES[game]['balls'] = 0
            else:
                USER_GAMES[game] = {'date': dt_, 'balls': 0}
    except Exception as e:
        logger.info(log_ % str(e))
        print(f"Ошибка: {e}")
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        print(f"Финальные данные: {USER_GAMES}")
        return USER_GAMES


# async def ch_games(USER_GAMES, game, condition, balls=1):
#     try:
#         dt = datetime.now(timezone.utc)
#         dt_ = dt.strftime('%d-%m-%Y_%H-%M-%S')
#
#         if condition:
#             dt_game = USER_GAMES[game].get('date')
#
#             if not dt_game:
#                 USER_GAMES[game]['date'] = dt_
#                 USER_GAMES[game]['balls'] = balls
#             else:
#                 dt_game = datetime.strptime(dt_game, "%d-%m-%Y_%H-%M-%S").replace(tzinfo=timezone.utc)
#                 if (dt - dt_game).days >= 1:
#                     USER_GAMES[game]['date'] = dt_
#                     USER_GAMES[game]['balls'] = balls
#         else:
#             USER_GAMES[game]['balls'] = 0
#     except Exception as e:
#         logger.info(log_ % str(e))
#         await asyncio.sleep(round(random.uniform(0, 1), 2))
#     finally:
#         return USER_GAMES


async def get_user_vars(PROJECT_USERNAME, BASE_P, ENT_TID, chat_id, lc, username, full_name, is_premium=False, usr_hash='',
                        page=''):
    USER_TID = chat_id
    USER_VARS = json.loads(USER_VARS_)
    USER_LSTS = json.loads(USER_LSTS_)
    USER_GAMES = {}
    print(f"start get usernv a, {USER_LSTS=}")
    try:
        schema_name = 'USER'
        balls = 1
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'BOT'
            balls = -1
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'

        sql = f"SELECT USER_TID, USER_GAMES, USER_VARS, USER_LSTS FROM {schema_name}_{str(ENT_TID).replace('-', '')}.USER WHERE USER_TID=$1"
        data_user = await db_select_pg(sql, (chat_id,), BASE_P)
        print(f"{data_user=}")
        if len(data_user):
            USER_TID, USER_GAMES, USER_VARS, USER_LSTS = data_user[0]
            USER_GAMES = json.loads(USER_GAMES)
            USER_VARS = json.loads(USER_VARS)
            USER_LSTS = json.loads(USER_LSTS)
            if page in ['msg', 'pst']: USER_GAMES = await ch_games(USER_GAMES, 'web', True, balls)

            # region lz
            if lc:
                USER_VARS['USER_LC'] = lc
                lz = 'en'
                if lc in ['zh', 'zh-chs', 'zh-cht', 'ja', 'ko', 'zh-CN', 'zh-TW', 'th', 'vi', 'tw', 'sg']:
                    lz = 'zh'
                # arabic    # ir, af
                elif lc in ['ar-XA', 'ar', 'tr', 'ur', 'fa', 'tj', 'dz', 'eg', 'iq', 'sy', 'ae', 'sa', 'tn', 'ir',
                            'af']:
                    lz = 'ar'
                # spanish   # portugal: 'pt', 'br', 'ao', 'mz'
                elif lc in ['es', 'ar', 'cl', 'co', 'cu', 've', 'bo', 'pe', 'ec', 'pt', 'br', 'ao', 'mz']:
                    lz = 'es'
                # french
                elif lc in ['fr', 'ch', 'be', 'ca']:
                    lz = 'fr'
                # europe
                elif lc in ['ru', 'kz', 'kg', 'uz', 'tm', 'md', 'am', 'uk-UA', 'uk', 'kk', 'tk', 'ky']:
                    lz = 'ru'
                USER_VARS['USER_LZ'] = lz
            # endregion
            print(f"{USER_VARS=}, {lc=}")
        USER_VARS['USER_HASH'] = usr_hash
        USER_VARS['USER_ISPREMIUM'] = is_premium

        sql = f""" 
        INSERT INTO {schema_name}_{str(ENT_TID).replace('-', '')}.USER (
            USER_TID, USER_USERNAME, USER_FULLNAME, USER_GAMES, USER_VARS, USER_LSTS
        )
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (USER_TID) DO UPDATE
        SET 
            USER_USERNAME = EXCLUDED.USER_USERNAME,
            USER_FULLNAME = EXCLUDED.USER_FULLNAME,
            USER_GAMES = EXCLUDED.USER_GAMES,
            USER_VARS = EXCLUDED.USER_VARS,
            USER_LSTS = EXCLUDED.USER_LSTS
        """
        await db_change_pg(sql, (USER_TID, username, full_name,
                                 json.dumps(USER_GAMES, ensure_ascii=False),
                                 json.dumps(USER_VARS, ensure_ascii=False),
                                 json.dumps(USER_LSTS, ensure_ascii=False),), BASE_P)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return USER_TID, username, full_name, USER_GAMES, USER_VARS, USER_LSTS


async def get_user_vars2(chat_id, ENT_TID, BASE_D, PROJECT_USERNAME):
    USER_GAMES = {}
    USER_VARS = {}
    USER_ISPAID = 0
    try:
        schema_name = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'BOT'
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'

        sql = f"SELECT USER_GAMES, USER_VARS, USER_ISPAID FROM {schema_name}_{str(ENT_TID).replace('-', '')}.USER WHERE USER_TID=$1"
        data_usr = await db_select_pg(sql, (chat_id,), BASE_D)
        if not len(data_usr) or not data_usr[0][0]:
            if not len(data_usr):
                dt_now = datetime.now(timezone.utc).strftime('%d-%m-%Y_%H-%M-%S')
                sql = f"INSERT INTO {schema_name}_{str(ENT_TID).replace('-', '')}.USER (USER_TID, USER_DT) VALUES ($1, $2) ON CONFLICT DO NOTHING"
                await db_change_pg(sql, (chat_id, dt_now,), BASE_D)
        else:
            USER_GAMES, USER_VARS, USER_ISPAID = data_usr[0]
            USER_GAMES = json.loads(USER_GAMES) if USER_GAMES else {}
            USER_VARS = json.loads(USER_VARS) if USER_VARS else {}
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return USER_GAMES, USER_VARS, USER_ISPAID


async def post_save(bot, data_user, data_web, MEDIA_D, BASE_P, KEYS_JSON, PROJECT_USERNAME, PROJECT_TYPE, is_paid=False):
    result = {'result': True, 'bot': True, 'post': data_web['post']}
    try:
        chat_id = int(data_user['user']['id'])
        username = data_user.get('user', {}).get('username', None)
        is_premium = data_user.get('user', {}).get('is_premium', None)

        print(f"{data_web=}")
        lz = data_web['lz']
        post = data_web['post']
        ENT_TID = str(data_web['ENT_TID'])
        tid_tmp = str(ENT_TID).replace('-', '')
        ENT_TOKEN = data_web['ENT_TOKEN'] if 'ENT_TOKEN' in data_web else None
        ENT_FIRSTNAME = data_web['ENT_FIRSTNAME'] if 'ENT_FIRSTNAME' in data_web else str_empty
        ENT_USERNAME = data_web['ENT_USERNAME'] if 'ENT_USERNAME' in data_web else str_empty
        os.makedirs(os.path.join(MEDIA_D, str(ENT_TID)), exist_ok=True, mode=0o777)
        EXTRA_D = os.path.join(os.path.dirname(MEDIA_D), "EXTRA")

        POST_TID = post['POST_TID']
        POST_TYPE = post['POST_TYPE']
        POST_TEXT = post['POST_TEXT'].strip()
        POST_MEDIA = post['POST_MEDIA']
        POST_BUTTONS = post['POST_BUTTONS']
        POST_CHKBOX = post['POST_CHKBOX']
        POST_BLOG = await region_blog2(bot, ENT_TID, POST_TYPE, POST_TEXT, POST_MEDIA, BASE_P, PROJECT_TYPE)

        POST_ISPAY = POST_CHKBOX['POST_ISPAY'] if 'POST_ISPAY' in POST_CHKBOX else False
        POST_STARS = POST_CHKBOX['POST_STARS'] if 'POST_STARS' in POST_CHKBOX else '1'
        POST_ISWATER = POST_CHKBOX['POST_ISWATER'] if 'POST_ISWATER' in POST_CHKBOX else False
        POST_WATER = POST_CHKBOX['POST_WATER'] if 'POST_WATER' in POST_CHKBOX else ''

        POST_APPTOKEN = post['POST_APPTOKEN'] if 'POST_APPTOKEN' in post else ''
        POST_TARGETTYPE = post['POST_TARGETTYPE'] if 'POST_TARGETTYPE' in post else 'me'
        POST_TARGET = post['POST_TARGET'] if 'POST_TARGET' in post else ''
        POST_ISPRIVATE = post['POST_ISPRIVATE'] if 'POST_ISPRIVATE' in post else 0

        POST_LZ = data_web['lz']
        POST_TZ = await get_tz(data_web['dateTime'])

        POST_DT = post['POST_DT'] if 'POST_DT' in post else ''
        POST_DT = await get_utc_from_local(POST_DT, POST_TZ)
        POST_DT = datetime.strptime(POST_DT, "%Y-%m-%dT%H:%M") if POST_DT else None

        POST_TR = post['POST_TR'] if 'POST_TR' in post else ''
        POST_TR = await get_utc_from_local(POST_TR, POST_TZ)
        POST_TR = datetime.strptime(POST_TR, "%Y-%m-%dT%H:%M") if POST_TR else None
        print(f"{POST_DT=}, {POST_TARGET=}, {ENT_TOKEN=}")

        if PROJECT_USERNAME == 'FereyPostBot':
            HASH_STR = f"pst-{ENT_TID}-{POST_TID}"
            HASH_VAL = hashlib.blake2b(HASH_STR.encode('utf-8'), digest_size=8).hexdigest()
            sql = "INSERT INTO \"HASH\" (HASH_STR, HASH_VAL) VALUES ($1, $2) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (HASH_STR, HASH_VAL,), BASE_P)
            POST_WEB = f"https://t.me/{PROJECT_USERNAME}/web?startapp=pst-{HASH_VAL}&mode=fullscreen"
        else:
            web_val = f"pst-{tid_tmp}-{POST_TID}"
            print(f"{web_val=}")
            HASH_VAL = hashlib.blake2b(web_val.encode('utf-8'), digest_size=8).hexdigest()
            POST_WEB = f"https://t.me/{PROJECT_USERNAME}/web?startapp=pst-{HASH_VAL}-{tid_tmp}&mode=fullscreen"

        print(f"{result=}, {POST_APPTOKEN=}")
        if ENT_TOKEN and len(POST_MEDIA):
            # region need start
            if PROJECT_USERNAME in ['FereyChannelBot', 'FereyGroupBot']:
                extra_bot = Bot(token=ENT_TOKEN)
                try:
                    if not ENT_USERNAME: ENT_USERNAME = (await extra_bot.get_me()).username
                    print(f"{chat_id=}, {ENT_USERNAME=}, {ENT_TOKEN=}")
                    r = await extra_bot.send_message(chat_id=chat_id, text=str_empty, disable_notification=True)
                    await extra_bot.delete_message(chat_id=chat_id, message_id=r.message_id)
                    member_ = await extra_bot.get_chat_member(chat_id=int(ENT_TID), user_id=chat_id)

                    print(f'{member_=}')
                    if member_.status not in ['administrator', 'creator']:
                        await bot.send_message(chat_id=chat_id,
                                               text=l_chn_no_rights_for_media[lz].format(PROJECT_USERNAME))
                        await bot.leave_chat(ENT_TID)
                        result['bot'] = False
                except Exception as e:
                    logger.info(log_ % str(e))
                    await bot.send_message(chat_id, l_bot_need_start_add[lz].format(ENT_USERNAME))
                finally:
                    await extra_bot.session.close()
            # endregion

            print(f"before {POST_ISWATER=}, {POST_WATER=}, {ENT_TOKEN=}, {POST_MEDIA=}")
            if POST_TYPE == 'photo' and POST_ISWATER and POST_WATER and ENT_TOKEN:
                for it in POST_MEDIA:
                    if 'filew_id' in it: continue
                    POST_FNAME = os.path.join(MEDIA_D, str(ENT_TID), it['file_name'])
                    POST_FNAME1, ext = os.path.splitext(it['file_name'])
                    POST_FNAME_COPY = os.path.join(MEDIA_D, str(ENT_TID), f"{os.path.basename(POST_FNAME1)}_c{ext}")

                    print(f'{it=}')
                    extra_bot = Bot(token=ENT_TOKEN)
                    try:
                        file = await extra_bot.get_file(it['fileb_id'])
                        await extra_bot.download_file(file.file_path, POST_FNAME)

                        POST_FNAME_COPY = await add_water_to_photo(POST_FNAME, POST_FNAME_COPY, POST_WATER, EXTRA_D)
                        if not POST_FNAME_COPY: continue

                        r_ = await extra_bot.send_photo(chat_id=chat_id,
                                                        photo=types.FSInputFile(POST_FNAME_COPY),
                                                        disable_notification=True)
                        await extra_bot.delete_message(chat_id, r_.message_id)

                        print(f"sooo ")
                        filew_id = r_.photo[-1].file_id
                        print(f"sooo {filew_id=}")
                        it['filew_id'] = filew_id
                    finally:
                        if os.path.exists(POST_FNAME): os.remove(POST_FNAME)
                        if os.path.exists(POST_FNAME_COPY): os.remove(POST_FNAME_COPY)
                        await extra_bot.session.close()

            print(f"--------------------------------------------------------")
            print(f"--------------------------------------------------------")
            print(f"--------------------------------------------------------")
            print(f"--------------------------------------------------------")
            print(f"after {POST_MEDIA=}")

        # region pay
        for button in POST_BUTTONS:
            try:
                if button['knd'] == 'web':
                    web_val = f"pst-{tid_tmp}-{button['lnk']}"
                    web_hash = hashlib.blake2b(web_val.encode('utf-8'), digest_size=8).hexdigest()
                    button['web'] = web_hash
                elif button['knd'] == 'nft':
                    web_val = f"nft-{tid_tmp}-{POST_TID}"
                    web_hash = hashlib.blake2b(web_val.encode('utf-8'), digest_size=8).hexdigest()
                    button['web'] = web_hash
                elif button['knd'] == 'pay' and ENT_TOKEN:
                    try:
                        amount = int(button['lnk'])
                    except:
                        amount = 1

                    extra_bot = Bot(token=ENT_TOKEN)
                    prices = [LabeledPrice(label="XTR", amount=amount)]
                    payload = f"PST_{ENT_TID}_{POST_TID}_{button['bid']}"
                    pay_lnk = await extra_bot.create_invoice_link(title=button['lbl'],
                                                                  description=f"@{ENT_USERNAME}",
                                                                  payload=payload,
                                                                  currency='XTR',
                                                                  prices=prices)
                    button['web'] = pay_lnk
                    await extra_bot.session.close()
            except TelegramRetryAfter as e:
                logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
                await asyncio.sleep(e.retry_after + 1)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                await bot.send_message(chat_id, l_bot_need_restart_extra_bot[lz].format(ENT_USERNAME))
            print(f"res {POST_BUTTONS=}")

        POST_PAY = POST_INVOICE = ''
        if POST_ISPAY and POST_STARS and ENT_TOKEN:
            try:
                extra_bot = Bot(token=ENT_TOKEN)
                try:
                    amount = int(POST_STARS)
                except:
                    amount = 1
                prices = [LabeledPrice(label="XTR", amount=amount)]
                POST_INVOICE = await extra_bot.create_invoice_link(title=ENT_FIRSTNAME,
                                                               description=f"@{ENT_USERNAME}",
                                                               payload=f"PST_{ENT_TID}_{POST_TID}_0",
                                                               currency='XTR',
                                                               prices=prices)

                prf = 'p' if PROJECT_USERNAME in ['FereyBotBot'] else ''
                web_val = f"{prf}pay-{tid_tmp}-{POST_TID}-{POST_STARS}-{tid_tmp}"
                HASH_VAL = hashlib.blake2b(web_val.encode('utf-8'), digest_size=8).hexdigest()
                POST_PAY = f"https://t.me/{PROJECT_USERNAME}/web?startapp={prf}pay-{HASH_VAL}-{tid_tmp}"

                await extra_bot.session.close()
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                await bot.send_message(chat_id, l_bot_need_restart_extra_bot[lz].format(ENT_USERNAME))

        if ENT_TOKEN:
            print(f" = = = = = =  ={ENT_TOKEN=}")
            if PROJECT_USERNAME == 'FereyChannelBot':
                sql = "UPDATE \"CHANNEL\" SET CHANNEL_CPAYTOKEN=$1 WHERE CHANNEL_TID=$2"
                await db_change_pg(sql, (ENT_TOKEN, str(ENT_TID),), BASE_P)
            elif PROJECT_USERNAME == 'FereyGroupBot':
                sql = "UPDATE \"GROUPP\" SET GROUPP_CPAYTOKEN=$1 WHERE GROUPP_TID=$2"
                await db_change_pg(sql, (ENT_TOKEN, str(ENT_TID),), BASE_P)
        print(f"{POST_PAY=}, {POST_STARS=}")
        # endregion

        # region nft
        POST_NFT = ''
        if any(item['knd'] == 'nft' for item in POST_BUTTONS):
            HASH_STR = f"nft-{tid_tmp}-{POST_TID}"
            HASH_VAL = hashlib.blake2b(HASH_STR.encode('utf-8'), digest_size=8).hexdigest()
            POST_NFT = f'https://t.me/{PROJECT_USERNAME}/web?startapp=nft-{HASH_VAL}-{tid_tmp}'
        print(f"{POST_NFT=}")
        # endregion

        # region priority
        POST_PRIORITY = 0
        if is_premium:
            POST_PRIORITY = 1
        if is_paid:
            POST_PRIORITY = 2
        # endregion

        # region db
        schema_prefix = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_prefix = 'BOT'
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_prefix = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_prefix = 'GROUPP'

        print(f"{ENT_TID=}, {POST_TID=}, {schema_prefix=}")
        sql = f"DELETE FROM {schema_prefix}_{tid_tmp}.LANG WHERE POST_TID=$1"
        await db_change_pg(sql, (POST_TID,), BASE_P)

        sql = f"SELECT POST_TID, POST_MEDIA FROM {schema_prefix}_{tid_tmp}.POST WHERE POST_TID=$1"
        data_media = await db_select_pg(sql, (POST_TID,), BASE_P)
        if len(data_media):
            POST_TID, POST_MEDIA_OLD = data_media[0]
            print(f"{POST_MEDIA_OLD=}")
            if POST_MEDIA_OLD:
                try:
                    POST_MEDIA_OLD = json.loads(POST_MEDIA_OLD)
                except:
                    POST_MEDIA_OLD = []

                old_ids = {media["file_id"] for media in POST_MEDIA_OLD}
                new_ids = {media["file_id"] for media in POST_MEDIA}
                to_delete = old_ids - new_ids
                print(f"{old_ids=}, {new_ids=}, {to_delete=}")

                for file_id in to_delete:
                    print(f"{file_id=}")
                    await delete_from_ipfs(file_id, KEYS_JSON)

        result['post'] = {
            'POST_TID': post['POST_TID'], 'POST_USERTID': chat_id, 'POST_USERTUN': username,
            'POST_TYPE': post['POST_TYPE'], 'POST_TEXT': unescape(POST_TEXT),
            'POST_MEDIA': POST_MEDIA, 'POST_BUTTONS': POST_BUTTONS, 'POST_CHKBOX': post['POST_CHKBOX'],
            'POST_TARGETTYPE': POST_TARGETTYPE, 'POST_TARGET': POST_TARGET,
            'POST_WEB': POST_WEB, 'POST_PAY': POST_PAY, 'POST_INVOICE': POST_INVOICE, 'POST_NFT': POST_NFT,
            'POST_BLOG': POST_BLOG,
            'POST_LZ': POST_LZ, 'POST_TZ': POST_TZ,
            'POST_DT': POST_DT.strftime("%Y-%m-%dT%H:%M") if POST_DT else None,
            'POST_TR': POST_TR.strftime("%Y-%m-%dT%H:%M") if POST_TR else None,
        }
        POST_MEDIA = json.dumps(POST_MEDIA, ensure_ascii=False)
        POST_BUTTONS = json.dumps(POST_BUTTONS, ensure_ascii=False)
        POST_CHKBOX = json.dumps(POST_CHKBOX, ensure_ascii=False)

        sql = f""" 
            INSERT INTO {schema_prefix}_{tid_tmp}.POST (
                POST_TID, POST_CHATTID, POST_USERTID, POST_USERTUN, POST_TARGETTYPE, POST_TARGET,
                POST_TYPE, POST_TEXT, POST_MEDIA, POST_BUTTONS, POST_CHKBOX, 
                POST_WEB, POST_PAY, POST_INVOICE, POST_NFT, POST_BLOG, POST_ISPRIVATE, 
                POST_LZ, POST_TZ, POST_DT, POST_TR, POST_PRIORITY
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22)
            ON CONFLICT (POST_TID) DO UPDATE
            SET 
                POST_CHATTID = EXCLUDED.POST_CHATTID,
                POST_USERTID = EXCLUDED.POST_USERTID,
                POST_USERTUN = EXCLUDED.POST_USERTUN,
                POST_TARGETTYPE = EXCLUDED.POST_TARGETTYPE,
                POST_TARGET = EXCLUDED.POST_TARGET,

                POST_TYPE = EXCLUDED.POST_TYPE,
                POST_TEXT = EXCLUDED.POST_TEXT,
                POST_MEDIA = EXCLUDED.POST_MEDIA,
                POST_BUTTONS = EXCLUDED.POST_BUTTONS,
                POST_CHKBOX = EXCLUDED.POST_CHKBOX,
                
                POST_WEB = EXCLUDED.POST_WEB,
                POST_PAY = EXCLUDED.POST_PAY,
                POST_INVOICE = EXCLUDED.POST_INVOICE,
                POST_NFT = EXCLUDED.POST_NFT,
                POST_BLOG = EXCLUDED.POST_BLOG,
                POST_ISPRIVATE = EXCLUDED.POST_ISPRIVATE,
                
                POST_LZ = EXCLUDED.POST_LZ,
                POST_TZ = EXCLUDED.POST_TZ,
                POST_DT = EXCLUDED.POST_DT,
                POST_TR = EXCLUDED.POST_TR,
                POST_PRIORITY = EXCLUDED.POST_PRIORITY
        """
        await db_change_pg(sql, (
            POST_TID, str(ENT_TID), chat_id, username, POST_TARGETTYPE, POST_TARGET,
            POST_TYPE, POST_TEXT, POST_MEDIA, POST_BUTTONS, POST_CHKBOX,
            POST_WEB or None, POST_PAY or None, POST_INVOICE or None, POST_NFT or None, POST_BLOG, POST_ISPRIVATE,
            POST_LZ or 'en', POST_TZ, POST_DT, POST_TR, POST_PRIORITY
        ), BASE_P)
        # endregion
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def post_pub(bot, lz, chat_id, ENT_TID, post, MEDIA_D, BASE_S, BASE_D, PROJECT_USERNAME, is_private=True, is_paid=False):
    result = False
    try:
        # region data
        POST_ID, POST_TID, POST_MSGID, POST_CHATTID, POST_USERTID, POST_USERTUN, \
            POST_TARGETTYPE, POST_TARGET, POST_TYPE, POST_TEXT, POST_MEDIA, POST_BUTTONS, \
            POST_CHKBOX, POST_WEB, POST_NFT, POST_PAY, POST_INVOICE, POST_BLOG, POST_ISMINTED, \
            POST_MINTLINK, POST_ISPRIVATE, POST_TZ, POST_DT, POST_TR, POST_STATUS = post

        cur_ = 1
        len_ = 1
        index = 0
        POST_MEDIA = json.loads(POST_MEDIA)
        POST_BUTTONS = json.loads(POST_BUTTONS)
        POST_CHKBOX = json.loads(POST_CHKBOX)
        POST_MEDIA_COPY = copy.deepcopy(POST_MEDIA)
        EXTRA_D = os.path.join(os.path.dirname(MEDIA_D), "EXTRA")

        POST_ISTAG = POST_CHKBOX['POST_ISTAG'] if 'POST_ISTAG' in POST_CHKBOX else False
        POST_ISCOLLAPSE = POST_CHKBOX['POST_ISCOLLAPSE'] if 'POST_ISCOLLAPSE' in POST_CHKBOX else False
        POST_ISGALLERY = POST_CHKBOX['POST_ISGALLERY'] if 'POST_ISGALLERY' in POST_CHKBOX else False

        POST_ISWATER = POST_CHKBOX['POST_ISWATER'] if 'POST_ISWATER' in POST_CHKBOX else False
        POST_WATER = POST_CHKBOX['POST_WATER'] if 'POST_WATER' in POST_CHKBOX else ''
        POST_ISPAY = POST_CHKBOX['POST_ISPAY'] if 'POST_ISPAY' in POST_CHKBOX else False
        POST_STARS = POST_CHKBOX['POST_STARS'] if 'POST_STARS' in POST_CHKBOX else 1

        if not is_private:
            chat_id = int(ENT_TID)
            POST_CHKBOX['POST_EFFECT'] = None
        if len(POST_MEDIA) > 1 and POST_ISGALLERY: len_ = len(POST_MEDIA)

        schema_name = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'BOT'
            for it in POST_MEDIA:
                it['file_id'] = it['fileb_id']
                it['file_id_note'] = it['fileb_id_note']
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'

        reply_markup = InlineKeyboardBuilder()
        # endregion

        # region txt
        POST_TEXT = await correct_txt_tags_for_tg(POST_TEXT)
        if POST_ISTAG and POST_TEXT and len(POST_TEXT) < 900:
            sql = f"SELECT USER_TID FROM {schema_name}_{str(ENT_TID).replace('-', '')}.USER"
            data_rnd = await db_select_pg(sql, (), BASE_D)
            if len(data_rnd):
                data_rnd = [it[0] for it in data_rnd]
                random.shuffle(data_rnd)
                data_rnd = data_rnd[:1]

                for it in data_rnd:
                    if len(POST_TEXT) > 900: break
                    POST_TEXT = f"{POST_TEXT}<a href='tg://user?id={it}'>{str_empty}</a>"
        if isinstance(POST_MEDIA, list) and not len(POST_MEDIA): POST_TYPE = 'text'
        if POST_TYPE != 'text': POST_TEXT = POST_TEXT[0:1024]
        print(f"{is_paid=}, {POST_TEXT=}")
        # endregion

        # region pay
        print(f"region pay {POST_ISPAY=}, {POST_TYPE=}")
        if not is_paid and POST_ISPAY and POST_PAY and POST_TYPE not in ['photo', 'video']:
            print(f"{POST_PAY=}")
            reply_markup.row(types.InlineKeyboardButton(text=l_bot_pub_with_payment[lz], url=POST_PAY))
            # lp_options = LinkPreviewOptions(is_disabled=False, url=post_photo, prefer_small_media=True)
            result = await bot.send_message(chat_id=chat_id,
                                            text=str_empty,
                                            # link_preview_options=lp_options,
                                            reply_markup=reply_markup.as_markup())

            if PROJECT_USERNAME in ['FereyChannelBot', 'FereyGroupBot'] and not is_private:
                sql = f"UPDATE {schema_name}_{str(ENT_TID).replace('-', '')}.POST SET POST_MSGID=$1 WHERE POST_TID=$2"
                await db_change_pg(sql, (result.message_id, POST_TID,), BASE_D)
            return
        # endregion

        # region reply_markup
        print(f"========================")
        if len(POST_MEDIA) > 1 and POST_ISGALLERY and not POST_ISCOLLAPSE and not POST_ISPAY and POST_TYPE not in ['sticker']:
            POST_TEXT = '' if POST_TEXT == str_empty and POST_TYPE != 'text' else POST_TEXT

            buttons = [
                types.InlineKeyboardButton(text="←", callback_data=f'pst_{ENT_TID}_{POST_TID}_0_{cur_}_{len_}_prev'),
                types.InlineKeyboardButton(text=f"{cur_}/{len_}", callback_data=f'pst_{ENT_TID}_{POST_TID}_0_{cur_}_{len_}_cur'),
                types.InlineKeyboardButton(text="→", callback_data=f'pst_{ENT_TID}_{POST_TID}_0_{cur_}_{len_}_next'), ]
            reply_markup.row(*buttons)

        if POST_ISCOLLAPSE and not POST_ISPAY:
            reply_markup.row(types.InlineKeyboardButton(text="ᴿᵁᴺ", callback_data=f'pst_{ENT_TID}_{POST_TID}_0_1_1_run'))
        else:
            reply_markup = await get_ent_rm(chat_id, reply_markup, ENT_TID, POST_USERTUN, POST_TID, POST_BUTTONS, BASE_D, PROJECT_USERNAME)
        # endregion

        # region send
        print(f"send ======================== {chat_id=}, {POST_TYPE=}")
        if not is_paid and POST_ISPAY and POST_TYPE in ['photo', 'video']:
            if PROJECT_USERNAME in ['FereyChannelBot']:
                sql = f"SELECT CHANNEL_CPAYTOKEN FROM \"CHANNEL\" WHERE CHANNEL_TID=$1"
                data_ent = await db_select_pg(sql, (str(ENT_TID),), BASE_D)
                if not len(data_ent): return
                ENT_TOKEN = data_ent[0][0]
            elif PROJECT_USERNAME == 'FereyGroupBot':
                sql = f"SELECT GROUPP_CPAYTOKEN FROM \"GROUPP\" WHERE GROUPP_TID=$1"
                data_ent = await db_select_pg(sql, (str(ENT_TID),), BASE_D)
                if not len(data_ent): return
                ENT_TOKEN = data_ent[0][0]
            else:
                sql = f"SELECT BOT_TOKEN FROM \"BOT\" WHERE BOT_TID=$1"
                data_ent = await db_select_pg(sql, (int(ENT_TID),), BASE_D)
                if not len(data_ent): return
                ENT_TOKEN = data_ent[0][0]

            media = []
            print(f"POST_ISPAY {chat_id=}, {ENT_TOKEN=}, {POST_MEDIA=}")

            for i in range(0, len(POST_MEDIA)):
                try:
                    if POST_MEDIA[i]['file_type'] == 'photo':
                        media.append(types.InputPaidMediaPhoto(media=POST_MEDIA[i]['fileb_id']))
                    elif POST_MEDIA[i]['file_type'] == 'video':
                        media.append(types.InputPaidMediaVideo(media=POST_MEDIA[i]['fileb_id']))
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

            if ENT_TOKEN:
                try:
                    extra_bot = Bot(token=ENT_TOKEN)
                    result = await extra_bot.send_paid_media(chat_id=chat_id,
                                                             star_count=int(POST_STARS),
                                                             media=media,
                                                             caption=POST_TEXT,
                                                             payload=f'PST_{ENT_TID}_{POST_TID}_0',

                                                             parse_mode=ParseMode.HTML,
                                                             show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                                             disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                                             protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                                             reply_markup=reply_markup.as_markup())
                    await extra_bot.session.close()
                except Exception as e:
                    logger.info(log_ % str(e))
                    # await asyncio.sleep(round(random.uniform(0, 1), 2))
                    await bot.send_message(chat_id=int(POST_USERTID), text=l_payment_check_token[lz])
                    return
        elif len(POST_MEDIA) > 1 and not POST_ISGALLERY:
            media = []
            for i in range(0, len(POST_MEDIA)):
                caption = POST_TEXT if i == 0 else None
                if caption: caption = caption if caption not in ['', str_empty] else None

                if POST_MEDIA[i]['file_type'] == 'photo':
                    media.append(types.InputMediaPhoto(media=POST_MEDIA[i]['file_id'], caption=caption,
                                                       parse_mode=ParseMode.HTML,
                                                       show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                                       has_spoiler=POST_CHKBOX['POST_ISSPOILER']))
                elif POST_MEDIA[i]['file_type'] == 'video':
                    media.append(types.InputMediaVideo(media=POST_MEDIA[i]['file_id'], caption=caption,
                                                       parse_mode=ParseMode.HTML,
                                                       show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                                       has_spoiler=POST_CHKBOX['POST_ISSPOILER']))
                elif POST_MEDIA[i]['file_type'] == 'audio':
                    media.append(types.InputMediaAudio(media=POST_MEDIA[i]['file_id'], parse_mode=ParseMode.HTML,
                                                       caption=caption))
                elif POST_MEDIA[i]['file_type'] == 'document':
                    media.append(types.InputMediaDocument(media=POST_MEDIA[i]['file_id'], caption=caption,
                                                          parse_mode=ParseMode.HTML,
                                                          disable_content_type_detection=True))

            result = await bot.send_media_group(chat_id=chat_id, media=media,
                                                disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                                protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                                message_effect_id=POST_CHKBOX['POST_EFFECT'])
        elif POST_TYPE == 'text':
            POST_TEXT = POST_TEXT or str_empty
            result = await bot.send_message(chat_id=chat_id, text=POST_TEXT, parse_mode=ParseMode.HTML,
                                            link_preview_options=LinkPreviewOptions(is_disabled=not POST_CHKBOX['POST_ISPREVIEW']),
                                            disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                            protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                            disable_web_page_preview=not POST_CHKBOX['POST_ISPREVIEW'],
                                            message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                            reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'photo':
            print(f"here {POST_MEDIA=}")

            file_id = POST_MEDIA[index]['file_id']
            print(f"before {file_id=}, {POST_ISWATER=}, {POST_WATER=}")
            if POST_ISWATER and POST_WATER:
                if 'filew_id' not in POST_MEDIA[index]:
                    BOT_TOKEN = None
                    if PROJECT_USERNAME == 'FereyBotBot':
                        sql = f"SELECT BOT_TOKEN FROM \"BOT\" WHERE BOT_TID=$1"
                        data_ent = await db_select_pg(sql, (ENT_TID,), BASE_D)
                        if len(data_ent): BOT_TOKEN = data_ent[0][0]

                    if BOT_TOKEN:
                        os.makedirs(os.path.join(MEDIA_D, str(ENT_TID)), exist_ok=True, mode=0o777)
                        POST_FNAME = os.path.join(MEDIA_D, str(ENT_TID), POST_MEDIA[index]['file_name'])
                        POST_FNAME1, ext = os.path.splitext(POST_MEDIA[index]['file_name'])
                        POST_FNAME_COPY = os.path.join(MEDIA_D, str(ENT_TID), f"{os.path.basename(POST_FNAME1)}_c{ext}")

                        extra_bot = Bot(token=BOT_TOKEN)
                        try:
                            file = await extra_bot.get_file(file_id)
                            await extra_bot.download_file(file.file_path, POST_FNAME)

                            POST_FNAME_COPY = await add_water_to_photo(POST_FNAME, POST_FNAME_COPY, POST_WATER, EXTRA_D)

                            r_ = await extra_bot.send_photo(chat_id, types.FSInputFile(POST_FNAME_COPY))
                            await extra_bot.delete_message(chat_id, r_.message_id)

                            print(f"sooo ")
                            file_id = r_.photo[-1].file_id
                            print(f"sooo {file_id=}")
                            POST_MEDIA_COPY[index]['filew_id'] = file_id
                            print(f"sooo {POST_MEDIA_COPY=}")

                            sql = f"UPDATE {schema_name}_{str(ENT_TID).replace('-', '')}.POST SET POST_MEDIA=$1 WHERE POST_TID=$2"
                            await db_change_pg(sql, (
                                json.dumps(POST_MEDIA_COPY, ensure_ascii=False),
                                POST_TID,
                            ), BASE_D)
                        finally:
                            if os.path.exists(POST_FNAME): os.remove(POST_FNAME)
                            if os.path.exists(POST_FNAME_COPY): os.remove(POST_FNAME_COPY)
                            await extra_bot.session.close()
                else:
                    file_id = POST_MEDIA[index]['filew_id']

            print(f"after {file_id=}")
            result = await bot.send_photo(chat_id=chat_id, photo=file_id, caption=POST_TEXT,
                                          parse_mode=ParseMode.HTML,
                                          show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                          has_spoiler=POST_CHKBOX['POST_ISSPOILER'],
                                          disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                          protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                          message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                          reply_markup=reply_markup.as_markup())
        elif POST_TYPE in ['animation', 'gif']:
            print(f"sova")
            try:
                print(f"sova1, {POST_MEDIA[index]['file_id']=}")
                result = await bot.send_animation(chat_id=chat_id, animation=POST_MEDIA[index]['file_id'],
                                                  caption=POST_TEXT, parse_mode=ParseMode.HTML,
                                                  show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                                  has_spoiler=POST_CHKBOX['POST_ISSPOILER'],
                                                  disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                                  protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                                  message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                                  reply_markup=reply_markup.as_markup())
            except:
                print(f"sova2, {POST_MEDIA[index]['file_id']=}")
                result = await bot.send_document(chat_id=chat_id, document=POST_MEDIA[index]['file_id'],
                                                 caption=POST_TEXT,
                                                 parse_mode=ParseMode.HTML,
                                                 disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                                 protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                                 message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                                 disable_content_type_detection=True,
                                                 reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'video':
            print(f"video {POST_MEDIA[index]['file_id']=}")
            result = await bot.send_video(chat_id=chat_id,
                                          video=POST_MEDIA[index]['file_id'],
                                          caption=POST_TEXT,
                                          parse_mode=ParseMode.HTML,
                                          show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                          has_spoiler=POST_CHKBOX['POST_ISSPOILER'],
                                          disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                          protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                          message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                          reply_markup=reply_markup.as_markup())
        elif POST_TYPE in ['video_note', 'telescope']:
            try:
                result = await bot.send_video_note(chat_id=chat_id, video_note=POST_MEDIA[index]['file_id'],
                                                   disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                                   protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                                   message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                                   reply_markup=reply_markup.as_markup())
            except Exception as e:
                logger.info(log_ % str(e))

                result = await bot.send_video(chat_id=chat_id,
                                              video=POST_MEDIA[index]['file_id_note'],
                                              caption=POST_TEXT,
                                              parse_mode=ParseMode.HTML,
                                              show_caption_above_media=POST_CHKBOX['POST_ISPREVIEW'],
                                              has_spoiler=POST_CHKBOX['POST_ISSPOILER'],
                                              disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                              protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                              message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                              reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'audio':
            result = await bot.send_audio(chat_id=chat_id, audio=POST_MEDIA[index]['file_id'], caption=POST_TEXT,
                                          parse_mode=ParseMode.HTML,
                                          disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                          protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                          message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                          reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'voice':
            try:
                result = await bot.send_voice(chat_id=chat_id, voice=POST_MEDIA[index]['file_id'], caption=POST_TEXT,
                                              parse_mode=ParseMode.HTML,
                                              disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                              protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                              message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                              reply_markup=reply_markup.as_markup())
            except Exception as e:
                logger.info(log_ % str(e))

                result = await bot.send_audio(chat_id=chat_id, audio=POST_MEDIA[index]['file_id_note'],
                                              caption=POST_TEXT,
                                              parse_mode=ParseMode.HTML,
                                              disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                              protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                              message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                              reply_markup=reply_markup.as_markup())
        elif POST_TYPE == 'sticker':
            result = await bot.send_sticker(chat_id=chat_id, sticker=POST_MEDIA[index]['file_id'],
                                            disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                            protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                            message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                            reply_markup=reply_markup.as_markup())
        else:
            POST_FNAME = None
            is_sended = False
            if POST_MEDIA and POST_MEDIA[0]['file_name'].endswith(('.webp', '.webm', '.tgs')):
                try:
                    print(f"{POST_MEDIA=}")
                    ext_ = 'webp'
                    if POST_MEDIA[0]['file_name'].endswith('webm'):
                        ext_ = 'webm'
                    elif POST_MEDIA[0]['file_name'].endswith('tgs'):
                        ext_ = 'tgs'

                    POST_FNAME = datetime.now(timezone.utc).strftime(f'%d-%m-%Y_%H-%M-%S-%f.{ext_}')
                    print(f"{POST_MEDIA=}, {POST_FNAME=}")
                    file = await bot.get_file(POST_MEDIA[0]['file_id'])
                    await bot.download_file(file.file_path, POST_FNAME)

                    result = await bot.send_sticker(
                        chat_id=chat_id,
                        sticker=types.FSInputFile(POST_FNAME),
                        message_effect_id=POST_CHKBOX['POST_EFFECT'],
                        disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                        protect_content=POST_CHKBOX['POST_ISPROTECT'],
                        reply_markup=reply_markup.as_markup()
                    )
                    is_sended = True
                except Exception as e:
                    logger.info(log_ % f"{chat_id}: {str(e)}")
                finally:
                    if POST_FNAME and os.path.exists(POST_FNAME): os.remove(POST_FNAME)

            if not is_sended:
                result = await bot.send_document(chat_id=chat_id, document=POST_MEDIA[index]['file_id'],
                                                 caption=POST_TEXT,
                                                 parse_mode=ParseMode.HTML,
                                                 disable_notification=not POST_CHKBOX['POST_ISSOUND'],
                                                 protect_content=POST_CHKBOX['POST_ISPROTECT'],
                                                 message_effect_id=POST_CHKBOX['POST_EFFECT'],
                                                 disable_content_type_detection=True,
                                                 reply_markup=reply_markup.as_markup())
        # endregion

        # region msgid
        print(chat_id, ENT_TID)
        if result and (int(chat_id) == int(ENT_TID) or PROJECT_USERNAME in ['FereyChannelBot', 'FereyGroupBot'] and not is_private):
            print('indeid')
            if isinstance(result, list):
                POST_MSGID = ' '.join([str(it.message_id) for it in result if it.message_id])
            else:
                POST_MSGID = str(result.message_id)
            print(f'res: POST_MSGID = {POST_MSGID}')
            sql = f"UPDATE {schema_name}_{str(ENT_TID).replace('-', '')}.POST SET POST_MSGID=$1 WHERE POST_TID=$2"
            await db_change_pg(sql, (POST_MSGID, POST_TID,), BASE_D)
        # endregion

        # region story
        try:
            if result and BASE_S and POST_TYPE == 'text' and POST_CHKBOX.get('POST_ISSTORY', False) and int(chat_id) == int(
                    ENT_TID):
                member_ = await bot.get_chat_member(chat_id=int(ENT_TID), user_id=bot.id)

                if member_.can_post_stories and member_.can_promote_members:
                    asyncio.create_task(
                        story_start(bot, lz, POST_USERTID, ENT_TID, POST_TYPE, POST_TEXT, POST_MEDIA[0]['file_id'],
                                    POST_MEDIA[0]['file_name'], POST_CHKBOX, False, MEDIA_D, BASE_D, BASE_S))
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        # region podcast
        try:
            if result and BASE_S and result.chat.username and POST_CHKBOX.get('POST_ISPODCAST', False) and int(chat_id) == int(
                    ENT_TID) and len(POST_MEDIA):
                member_ = await bot.get_chat_member(chat_id=int(ENT_TID), user_id=bot.id)

                if member_.can_manage_video_chats and member_.can_promote_members:
                    print(f"member_ can and promote")
                    is_paid, till_paid, lz = await get_vars_web_main(chat_id, '', '', lz, '', '', BASE_D, '')

                    asyncio.create_task(
                        podcast_start(bot, POST_USERTID, lz, ENT_TID, POST_TID, POST_TYPE, POST_TEXT,
                                      POST_MEDIA[0]['file_id'], POST_MEDIA[0]['file_name'], is_paid, BASE_S,
                                      MEDIA_D, BASE_D, PROJECT_USERNAME))
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        # region reac
        try:
            if result and POST_CHKBOX['POST_REACTION']:
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                reactions = [ReactionTypeEmoji(emoji=POST_CHKBOX['POST_REACTION'])]
                msg_id = result[0].message_id if isinstance(result, list) else result.message_id
                await bot.set_message_reaction(chat_id=chat_id, message_id=msg_id, reaction=reactions, is_big=True)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion

        # region pin
        try:
            if result and POST_CHKBOX['POST_ISPIN']:
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                msg_id = result[0].message_id if isinstance(result, list) else result.message_id
                await bot.pin_chat_message(chat_id=chat_id, message_id=msg_id,
                                           disable_notification=False,
                                           # disable_notification=not POST_CHKBOX['POST_ISSOUND']
                                           )
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
        # endregion
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        print("post pub finish")
        return result


async def region_blog2(bot, ENT_TID, POST_TYPE, POST_TEXT, POST_MEDIA, BASE_D, PROJECT_TYPE='bot', ENT_USERNAME=''):
    result = None
    try:
        # if PROJECT_TYPE in ['post']: return
        cnt = 0
        POST_MEDIA = json.loads(POST_MEDIA) if isinstance(POST_MEDIA, str) else POST_MEDIA
        print(f"bb {POST_TEXT=}")
        POST_TEXT = POST_TEXT if POST_TEXT else str_empty
        POST_TEXT = POST_TEXT.replace('<tg-spoiler>', '').replace('</tg-spoiler>', '').replace('<pre>py\n', '').replace(
            '<pre>', '').replace('</pre>', '').replace('<br>', '')
        POST_TEXT = POST_TEXT.replace('<span style="caret-color: var(--tg-theme-hint-color);">', '')
        POST_TEXT = POST_TEXT.replace('&nbsp;', '')
        POST_TEXT = re.sub(r'<span style="background-color: rgba\(0, 123, 247, 0\.7\);">(.*?)<\/span>', r'\1',
                           POST_TEXT)
        POST_TEXT = re.sub(r'<span style="background-color: gray;">(.*?)<\/span>', r'\1', POST_TEXT)
        POST_TEXT = re.sub(r'<span style="background-color: rgba\(0, 123, 247, 0\.8\);">(.*?)<\/span>', r'\1',
                           POST_TEXT)
        # POST_TEXT = re.sub(r'</?div>', '\n', POST_TEXT)
        POST_TEXT = re.sub(r'</?div[^>]*>', '\n', POST_TEXT)
        POST_TEXT = re.sub(r'<span[^>]*>.*?</span>', '', POST_TEXT)
        POST_TEXT = POST_TEXT.replace('<strike>', '<s>').replace('</strike>', '</s>')
        POST_TEXT = POST_TEXT.strip()
        POST_TEXT = POST_TEXT or str_empty
        print(f"aa {POST_TEXT=}")
        ENT_NAME = ENT_TID

        print(f"{PROJECT_TYPE=}")
        while cnt >= 0:
            try:
                if PROJECT_TYPE == 'bot':
                    print(f"1")
                    sql = "SELECT BOT_USERNAME, BOT_FIRSTNAME FROM \"BOT\" WHERE BOT_TID=$1"
                    data_bot = await db_select_pg(sql, (int(ENT_TID),), BASE_D)
                    if not len(data_bot): return
                    BOT_USERNAME, BOT_FIRSTNAME = data_bot[0]

                    # get_chat_ = await bot.get_me()
                    ENT_USERNAME = f"@{BOT_USERNAME}"
                    ENT_NAME = BOT_FIRSTNAME
                    ENT_LINK = f"https://t.me/{BOT_USERNAME}"
                    print(f"2 15997")
                elif PROJECT_TYPE == 'user':
                    sql = "SELECT UB_USERNAME, UB_FIRSTNAME, UB_BOTUSERNAME, UB_CHANNELLINK FROM UB WHERE UB_TID=$1"
                    data_bot = await db_select_pg(sql, (int(ENT_TID),), BASE_D)
                    UB_USERNAME, UB_FIRSTNAME, UB_BOTUSERNAME, UB_CHANNELLINK = data_bot[0]

                    if UB_USERNAME:
                        ENT_USERNAME = f"@{UB_USERNAME}"
                        ENT_LINK = f"https://t.me/{UB_USERNAME.strip('@')}"
                    else:
                        ENT_USERNAME = UB_FIRSTNAME
                        ENT_LINK = f"https://t.me/"
                elif PROJECT_TYPE == 'post':
                    ENT_USERNAME = '@FereyPostBot'
                    ENT_NAME = '🫧 Ferey Post App'
                    ENT_LINK = 'https://t.me/FereyPostBot'
                else:
                    get_chat_ = await bot.get_chat(int(ENT_TID))
                    ENT_USERNAME = get_chat_.title
                    ENT_NAME = ENT_USERNAME
                    ENT_LINK = f"https://t.me/{get_chat_.username}" if get_chat_.username else 'https://t.me'

                figure_html = ''
                telegraph_ = Telegraph()
                await telegraph_.create_account(short_name=short_name, author_name=ENT_USERNAME, author_url=ENT_LINK)
                print(f"16022б {POST_MEDIA=}")

                for item in POST_MEDIA:
                    print(f"16025 {item=}")
                    if not isinstance(item, dict): continue

                    print(f"ffkfkfkf  {item=}")
                    tgph_ph = str(item['file_link']).replace('https://telegra.ph', '')
                    if str(item['file_type']) in ['video', 'video_note']:
                        figure_html = f'{figure_html}<figure><video src="{tgph_ph}" preload="auto" autoplay="autoplay" loop="loop" muted="muted"></video><figcaption>Video: {ENT_LINK}</figcaption></figure>'
                    else:
                        figure_html = f'{figure_html}<figure><img src="{tgph_ph}"/><figcaption>Photo: {ENT_LINK}</figcaption></figure>'

                print(f"{figure_html=}")
                # figure_html = '<figure><img src="https://ddejfvww7sqtk.cloudfront.net/user-media/08-09-2024/75565/1041116.jpg"/><figcaption>Photo: {ENT_LINK}</figcaption></figure>'
                p_html = ''
                if POST_TEXT and POST_TEXT != '':
                    POST_TEXT = POST_TEXT.strip()
                    if '\n' in POST_TEXT:
                        POST_TEXTS = POST_TEXT.split('\n')
                        for i in range(len(POST_TEXTS)):
                            if POST_TEXTS[i] == '': continue

                            if len(POST_TEXTS) > 2 and i == 1 and random.choice([True, False]):
                                p_html = f"{p_html}<p><blockquote>{POST_TEXTS[i]}</blockquote></p>"
                            elif len(POST_TEXTS) > 4 and i == 4 and random.choice([True, False]):
                                p_html = f"{p_html}<p><aside>{POST_TEXTS[i]}</aside></p>"
                            else:
                                p_html = f"{p_html}<p>{POST_TEXTS[i]}</p>"
                    else:
                        p_html = f"<p>{POST_TEXT}</p>"
                html_ = f"{figure_html}{p_html}"
                page_blog = await telegraph_.create_page(title=f"📰 {ENT_NAME}", html_content=html_,
                                                         author_name=str(ENT_USERNAME), author_url=ENT_LINK)

                print(f"{html_=}")
                result = page_blog['url']
                logger.info(log_ % f"{ENT_TID}: {result}")
                return
            except Exception as e:
                logger.info(log_ % str(e) + f"{POST_TEXT=}")
                await asyncio.sleep(round(random.uniform(3, 5), 2))
                cnt -= 1
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def update_media(bot, chat_id, lz, ENT_TID, BOT_TOKEN, POST_MEDIA, MEDIA_D, PROJECT_USERNAME, is_check=True):
    result = [POST_MEDIA, False]
    try:
        print('check -======= pay')
        os.makedirs(os.path.join(MEDIA_D, str(ENT_TID)), exist_ok=True, mode=0o777)
        BOT_USERNAME = ''
        if is_check and PROJECT_USERNAME in ['FereyChannelBot']:
            extra_bot = Bot(token=BOT_TOKEN)
            try:
                BOT_USERNAME = (await extra_bot.get_me()).username
                r = await extra_bot.send_message(chat_id=chat_id, text=str_empty)
                await extra_bot.delete_message(chat_id=chat_id, message_id=r.message_id)
                member_ = await extra_bot.get_chat_member(chat_id=int(ENT_TID), user_id=chat_id)

                print(f'{member_=}')
                if member_.status not in ['administrator', 'creator']:
                    await bot.send_message(chat_id=chat_id, text=l_chn_no_rights_for_media[lz].format(PROJECT_USERNAME))
                    shutil.rmtree(os.path.join(MEDIA_D, str(ENT_TID)))
                    await bot.leave_chat(ENT_TID)
            except Exception as e:
                logger.info(log_ % str(e))
                await bot.send_message(chat_id, l_bot_need_start_add[lz].format(BOT_USERNAME))
                return
            finally:
                await extra_bot.session.close()

        try:
            media = []
            for media in POST_MEDIA:
                file_name = r = None
                extra_bot = Bot(token=BOT_TOKEN)
                try:
                    file = await bot.get_file(media['file_id'])
                    file_name = str(os.path.join(MEDIA_D, str(ENT_TID), media['file_name']))
                    await bot.download_file(file.file_path, file_name)

                    if media['file_type'] == 'photo':
                        r = await extra_bot.send_photo(chat_id=chat_id, photo=types.FSInputFile(file_name))
                        media['fileb_id'] = r.photo[-1].file_id
                    elif media['file_type'] == 'video':
                        r = await extra_bot.send_video(chat_id=chat_id, video=types.FSInputFile(file_name))
                        media['fileb_id'] = r.video.file_id
                    elif media['file_type'] in ['gif', 'animation']:
                        r = await extra_bot.send_animation(chat_id=chat_id, animation=types.FSInputFile(file_name))
                        media['fileb_id'] = r.animation.file_id
                    elif media['file_type'] in ['video_note', 'telescope']:
                        r = await extra_bot.send_video_note(chat_id=chat_id, video_note=types.FSInputFile(file_name))
                        media['fileb_id'] = r.video_note.file_id
                        r = await extra_bot.send_video(chat_id=chat_id, video=types.FSInputFile(file_name))
                        media['fileb_id_note'] = r.video.file_id
                    elif media['file_type'] == 'voice':
                        r = await extra_bot.send_voice(chat_id=chat_id, voice=types.FSInputFile(file_name))
                        media['fileb_id'] = r.voice.file_id
                        r = await extra_bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(file_name))
                        media['fileb_id_note'] = r.audio.file_id
                    elif media['file_type'] == 'audio':
                        r = await extra_bot.send_audio(chat_id=chat_id, audio=types.FSInputFile(file_name))
                        media['fileb_id'] = r.audio.file_id
                    elif media['file_type'] == 'sticker':
                        r = await extra_bot.send_sticker(chat_id=chat_id, sticker=types.FSInputFile(file_name))
                        media['fileb_id'] = r.sticker.file_id
                    elif media['file_type'] == 'document':
                        r = await extra_bot.send_document(chat_id=chat_id, document=types.FSInputFile(file_name))
                        media['fileb_id'] = r.document.file_id

                    if r and r.message_id:
                        await extra_bot.delete_message(chat_id=chat_id, message_id=r.message_id)
                except TelegramRetryAfter as e:
                    logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
                    await asyncio.sleep(e.retry_after + 1)
                except Exception as e:
                    logger.info(log_ % str(e))
                    await asyncio.sleep(round(random.uniform(0, 1), 2))
                finally:
                    if file_name and os.path.exists(file_name): os.remove(file_name)
                    await extra_bot.session.close()

            print(f"{media=}")
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))

        result = [POST_MEDIA, True]
        print(f"{POST_MEDIA=}")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_ent_rm(chat_id, reply_markup, ENT_TID, POST_USERTUN, POST_TID, POST_BUTTONS, BASE_D, PROJECT_USERNAME,
                     cur_='1'):
    try:
        schema_name = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'Bot'
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'

        if POST_BUTTONS and len(POST_BUTTONS):
            sql = f"SELECT BTN_BID FROM {schema_name}_{str(ENT_TID).replace('-', '')}.PUSH WHERE ENT_VID=$1"
            data = await db_select_pg(sql, (POST_TID,), BASE_D)
            counters = {str(it[0]): sum(1 for x in data if x[0] == it[0]) for it in data}
        else:
            counters = {}
        print(f"{counters=}")
        sorted_buttons = sorted(POST_BUTTONS, key=lambda x: x['ind'])
        print(f"{sorted_buttons=}")
        rows = {}

        for button in sorted_buttons:
            try:
                print(f"{button=}")
                ind = button['ind']
                row_index = (ind - 1) // 3
                if row_index not in rows:
                    rows[row_index] = []

                if button['knd'] == 'button_in':
                    cb_ = f"pst_{ENT_TID}_{POST_TID}_{button['bid']}_{cur_}_1_btn"
                    counter = '⁰' if button['bid'] not in counters else await upper_register(counters[button['bid']])
                    btn = types.InlineKeyboardButton(text=f"{counter} {button['lbl']}", callback_data=cb_)
                    rows[row_index].append(btn)
                elif button['knd'] == 'like':
                    cb_ = f"pst_{ENT_TID}_{POST_TID}_{button['bid']}_1_1_{button['knd']}"
                    counter = '⁰' if button['bid'] not in counters else await upper_register(counters[button['bid']])
                    btn = types.InlineKeyboardButton(text=f"{counter} {button['lbl']}", callback_data=cb_)
                    rows[row_index].append(btn)
                elif button['knd'] == 'link':
                    if button['lnk'].split('/')[-1] == str(POST_USERTUN):
                        url = f"tg://user?id={chat_id}"
                    else:
                        url = button['lnk']

                    btn = types.InlineKeyboardButton(text=button['lbl'], url=url)
                    rows[row_index].append(btn)
                elif button['knd'] in ['pay', 'payment']:
                    if button['web'] != '':
                        btn = types.InlineKeyboardButton(text=button['lbl'], url=button['web'])
                        rows[row_index].append(btn)
                elif button['knd'] == 'boost':
                    if str(ENT_TID).startswith(prefix_100):
                        url = f"https://t.me/boost?c={str(ENT_TID)[len(prefix_100):]}"
                    else:
                        url = f"https://t.me/boost?c={str(ENT_TID)}"

                    btn = types.InlineKeyboardButton(text=button['lbl'], url=url)
                    rows[row_index].append(btn)
                elif button['knd'] == 'share':
                    # get_chat_ = await bot.get_chat(int(ENT_TID))
                    # get_link_ = f"https://t.me/{get_chat_.username}" if get_chat_.username else get_chat_.invite_link
                    # txt = urllib.parse.quote(button['lnk'].strip(), safe="")
                    # url = f"https://t.me/share/url?url={get_link_}&text={txt}"
                    #
                    # btn = types.InlineKeyboardButton(text=button['lbl'], url=url)
                    # rows[row_index].append(btn)

                    print(f"===============================")
                    print(f"===============================")
                    print(f"===============================")
                    print(f"{button=}")
                    # выключить инлайн режим и проверить без него
                    btn = types.InlineKeyboardButton(text=button['lbl'], switch_inline_query=f"{ENT_TID} {str(POST_TID)} ~")
                    rows[row_index].append(btn)
                elif button['knd'] == 'web':
                    print(f"{button['lnk']=}")
                    NEXT_POST_TID = button['lnk']
                    if button['lnk'].strip() == '':
                        NEXT_POST_TID = POST_TID
                        # sql = f"SELECT POST_TID FROM {schema_name}_{str(ENT_TID).replace('-', '')}.POST"
                        # data_post = await db_select_pg(sql, (), BASE_D)
                        # if len(data_post) and data_post[0][0]:
                        #     NEXT_POST_TID = data_post[0][0]
                        # else:
                        #     continue

                    print(f"{NEXT_POST_TID=}")
                    HASH_STR = f"pst-{str(ENT_TID).replace('-', '')}-{str(NEXT_POST_TID).replace('-', '')}"
                    HASH_VAL = hashlib.blake2b(HASH_STR.encode('utf-8'), digest_size=8).hexdigest()
                    # if PROJECT_USERNAME == 'FereyPostBot':
                    #     sql = "INSERT INTO \"HASH\" (HASH_STR, HASH_VAL) VALUES ($1, $2) ON CONFLICT DO NOTHING"
                    #     await db_change_pg(sql, (HASH_STR, HASH_VAL,), BASE_D)

                    post_fix = '' if PROJECT_USERNAME == 'FereyPostBot' else f"-{str(ENT_TID).replace('-', '')}"
                    url = f'https://t.me/{PROJECT_USERNAME}/web?startapp=pst-{HASH_VAL}{post_fix}&mode=fullscreen'
                    btn = types.InlineKeyboardButton(text=button['lbl'], url=url)
                    rows[row_index].append(btn)
                elif button['knd'] == 'nft':
                    HASH_STR = f"nft-{str(ENT_TID).replace('-', '')}-{POST_TID}"
                    HASH_VAL = hashlib.blake2b(HASH_STR.encode('utf-8'), digest_size=8).hexdigest()

                    url = f'https://t.me/{PROJECT_USERNAME}/web?startapp=nft-{HASH_VAL}-{str(ENT_TID).replace('-', '')}'
                    btn = types.InlineKeyboardButton(text=button['lbl'], url=url)
                    rows[row_index].append(btn)
                elif button['knd'] == 'copy':
                    copy_text = CopyTextButton(text=button['lnk'])
                    btn = types.InlineKeyboardButton(text=button['lbl'], copy_text=copy_text)
                    rows[row_index].append(btn)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        for row in rows.values():
            reply_markup.row(*row)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return reply_markup


async def podcast_start(bot, chat_id, lz, ENT_TID, POST_ID, POST_TYPE, POST_TEXT, POST_FID, POST_FILENAME, USER_ISPAID,
                        BASE_S, MEDIA_D, BASE_D, PROJECT_USERNAME):
    file_name = os.path.join(MEDIA_D, str(ENT_TID), POST_FILENAME)
    SESSION_D = os.path.dirname(BASE_S)
    r = None
    cnt = 1
    duration = 60
    try:
        print(f"{POST_TYPE=}")

        if POST_TYPE in ['audio', 'voice'] or (
                POST_TYPE in ['document'] and file_name.lower().endswith(('.mp3', '.ogg'))):
            file = await bot.get_file(POST_FID)
            await bot.download_file(file.file_path, file_name)
            stream = MediaStream(file_name, AudioQuality.HIGH)

            try:
                if file_name.lower().endswith('.ogg'):
                    ogg_audio = AudioSegment.from_ogg(file_name)
                    duration = int(len(ogg_audio) / 1000)
                else:
                    audio_ = AudioSegment.from_mp3(file_name)
                    duration = int(audio_.duration_seconds)
            except:
                pass
        elif POST_TYPE in ['video', 'video_note'] or (
                POST_TYPE in ['document'] and file_name.lower().endswith(('.mp4', '.mov'))):
            file = await bot.get_file(POST_FID)
            await bot.download_file(file.file_path, file_name)
            stream = MediaStream(file_name, AudioQuality.HIGH, VideoQuality.HD_720p)

            try:
                # with VideoFileClip(file_name) as clip:
                #     duration = int(clip.duration)

                cap = cv2.VideoCapture(file_name)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                duration = frame_count / fps
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))
        elif POST_TYPE in ['photo', 'animation', 'gif']:
            file = await bot.get_file(POST_FID)
            await bot.download_file(file.file_path, file_name)
            stream = MediaStream(file_name)
        else:
            extract_links_ = await extract_links(POST_TEXT)
            print(f"{extract_links_=}")
            if not len(extract_links_):
                return
            else:
                stream = MediaStream(extract_links_[0])

        duration = duration if duration < 200 else 200
        if not USER_ISPAID: duration = duration if duration < 60 else 60

        sql = "SELECT SESSION_TID, SESSION_STATUS FROM SESSION"
        data = await db_select_pg(sql, (), BASE_S)
        random.shuffle(data)

        for _ in data[:10]:
            sql = "SELECT SESSION_TID, SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_STATUS FROM SESSION"
            data_ = await db_select_pg(sql, (), BASE_S)
            random.shuffle(data_)
            SESSION_TID, SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_STATUS = data_[0]
            if SESSION_STATUS is not None: continue

            try:
                sql = "UPDATE SESSION SET SESSION_STATUS=$1 WHERE SESSION_TID=$2"
                await db_change_pg(sql, (f'podcast_start', SESSION_TID,), BASE_S)
                get_chat_ = await bot.get_chat(ENT_TID)
                link = f'@{get_chat_.username}' if get_chat_.username else get_chat_.invite_link

                try:
                    await bot.unban_chat_member(chat_id=int(ENT_TID), user_id=SESSION_TID)
                except Exception as e:
                    logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

                name_ = str(os.path.join(SESSION_D, SESSION_NAME))
                async with Client(name=name_, api_id=SESSION_APIID, api_hash=SESSION_APIHASH) as app:
                    # async with await get_session(SESSION_TID, SESSION_D, BASE_S, EXTRA_D, CONF_P) as app:
                    try:
                        r = await join_my_chat(bot, app, my_tid, link, SESSION_TID, BASE_S)
                        if not r.username: return
                        promote_ = await bot.promote_chat_member(chat_id=int(ENT_TID), user_id=int(SESSION_TID),
                                                                 can_manage_video_chats=True)
                        if not promote_: raise Exception

                        result = await py_tg_calls_fun(bot, app, chat_id, lz, r, POST_ID, ENT_TID, stream, duration,
                                                       BASE_D, PROJECT_USERNAME)
                        print(f"{result=}")
                        await bot.promote_chat_member(chat_id=int(ENT_TID), user_id=SESSION_TID, is_anonymous=False,
                                                      can_manage_chat=False, can_delete_messages=False,
                                                      can_manage_video_chats=False, can_restrict_members=False,
                                                      can_promote_members=False, can_change_info=False,
                                                      can_invite_users=False, can_post_stories=False,
                                                      can_edit_stories=False, can_delete_stories=False,
                                                      can_post_messages=False, can_edit_messages=False,
                                                      can_pin_messages=False, can_manage_topics=False)

                    except Exception as e:
                        logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                        await asyncio.sleep(round(random.uniform(0, 1), 2))
                    finally:
                        await leave_my_chat(app, r, link)

                    cnt += 1
                    if result or cnt > 2: break
            except (
                    UserDeactivatedBan, UserDeactivated, AuthKeyInvalid, AuthKeyUnregistered, AuthKeyDuplicated,
                    SessionExpired,
                    SessionRevoked) as e:
                logger.info(log_ % f"deactivated {SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(5, 10),
                                          2))  # await delete_account(bot, SESSION_TID, SESSION_D, CONF_P, BASE_S)
            except Exception as e:
                logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                sql = "UPDATE CHANNEL SET CHANNEL_ISPROMOTED=0 WHERE CHANNEL_TID=$1"
                await db_change_pg(sql, (ENT_TID,), BASE_D)
            finally:
                sql = "UPDATE SESSION SET SESSION_STATUS=$1 WHERE SESSION_TID=$2"
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
        if file_name and os.path.exists(file_name): os.remove(file_name)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        await delete_msg_media_file(file_name)


async def py_tg_calls_fun(bot, app, chat_id, lz, r, POST_ID, ENT_TID, stream, duration, BASE_D, PROJECT_USERNAME):
    result = peer_chan = None
    try:
        # print('duration', duration)
        peer = await app.resolve_peer(ENT_TID)

        try:
            get_join_as = await app.invoke(GetGroupCallJoinAs(peer=peer))
            get_join_as_lst = [it for it in get_join_as.peers if it.QUALNAME == 'types.PeerChannel']
            if not len(get_join_as_lst):
                title = f"👩🏽‍💻 Landing Channel #{random.randrange(100, 999)}"
                res = await app.create_channel(title=title, description=f"verified chan 💙{random.randrange(100, 999)}")
                peer_chan = await app.resolve_peer(res.id)
                newusername_ = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(10, 20)))
                username_chan = f"{newusername_}_{random.randrange(100, 999)}_chan"[0:31]
                _ = await app.invoke(UpdateUsername(channel=peer_chan, username=username_chan))
                print(f"@{username_chan}: {title}")
                get_join_as = await app.invoke(GetGroupCallJoinAs(peer=peer))
                get_join_as_lst = [it for it in get_join_as.peers if it.QUALNAME == 'types.PeerChannel']

            if len(get_join_as_lst):
                peer_chan = await app.resolve_peer(int(f"-100{get_join_as_lst[-1].channel_id}"))
                await app.invoke(SaveDefaultGroupCallJoinAs(peer=peer, join_as=peer_chan))
        except:
            pass

        dt_ = utils.datetime_to_timestamp(datetime.now() + timedelta(minutes=1))
        call = await app.invoke(
            CreateGroupCall(peer=peer, random_id=dt_, rtmp_stream=False, title=l_podcast_start[lz], schedule_date=dt_))
        await asyncio.sleep(10)
        call = InputGroupCall(id=call.updates[0].call.id, access_hash=call.updates[0].call.access_hash)
        await app.invoke(StartScheduledGroupCall(call=call))

        call_py = PyTgCalls(app)

        # @call_py.on_participants_change()
        @call_py.on_update()
        async def participant_handler(_: PyTgCalls, update: Update):
            try:
                if not getattr(update, 'participant', None): return
                if update.participant.action != GroupCallParticipant.Action.JOINED: return

                if not str(update.participant.user_id).startswith('-100'):
                    await add_to_push_podcast(bot, app, update.participant.user_id, POST_ID, BASE_D, PROJECT_USERNAME)
            except Exception as exc:
                logger.info(log_ % str(exc))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        await call_py.start()
        await call_py.play(chat_id=ENT_TID, stream=stream, config=GroupCallConfig(join_as=peer_chan, auto_start=True))
        if r.username: await bot.send_message(chat_id=chat_id, text=f'https://t.me/{r.username}?livestream')
        await asyncio.sleep(duration)
        result = True

        participants = await call_py.get_participants(chat_id=ENT_TID)
        for participant in participants:
            if str(participant.user_id).startswith('-100'): continue
            await add_to_push_podcast(bot, app, participant.user_id, POST_ID, BASE_D, PROJECT_USERNAME)
        # await call_py.leave_group_call(chat_id=ENT_TID)
        await call_py.leave_call(chat_id=ENT_TID)
        print(f"@{username_chan}: {title} finish....")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def add_to_push_podcast(bot, app, user_id, ENT_TID, POST_ID, BASE_D, PROJECT_USERNAME):
    result = None
    try:
        schema_name = 'USER'
        if PROJECT_USERNAME == 'FereyBotBot':
            schema_name = 'BOT'
        elif PROJECT_USERNAME == 'FereyChannelBot':
            schema_name = 'CHANNEL'
        elif PROJECT_USERNAME == 'FereyGroupBot':
            schema_name = 'GROUPP'

        try:
            result = await bot.get_chat(user_id)
            user_id = result.id
            full_name = result.full_name
            username = result.username
            sql = f"INSERT INTO {schema_name}_{str(ENT_TID).replace('-', '')}.PUSH (CHAT_TID, CHAT_FULLNAME, CHAT_USERNAME, POST_ID, BTN_BID) VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (user_id, full_name, username, POST_ID, -1,), BASE_D)
            print('user_id get_chat ', user_id)
        except TelegramRetryAfter as e:
            logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
            await asyncio.sleep(e.retry_after + 1)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))

        if result: return

        try:
            get_users_ = await app.get_users([user_id])
            if not len(get_users_): return
            user_id = get_users_[0].id
            first_name = get_users_[0].first_name
            last_name = get_users_[0].last_name if get_users_[0].last_name else ''
            full_name = f"{first_name} {last_name}".strip()
            username = get_users_[0].username
            is_premium = get_users_[0].is_premium
            lc = get_users_[0].language_code
            sql = f"INSERT INTO {schema_name}_{str(ENT_TID).replace('-', '')}.PUSH (CHAT_TID, CHAT_FULLNAME, CHAT_USERNAME, CHAT_ISPREMIUM, CHAT_LC, POST_ID, BTN_BID) VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (user_id, full_name, username, is_premium, lc, POST_ID, -1,), BASE_D)
            print('user_id get_users_ ', user_id)
        except (FloodWait, SlowmodeWait) as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(e.value + 1)
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(0, 1), 2))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def story_start(bot, lz, chat_id, ENT_TID, POST_TYPE, POST_TEXT, POST_FID, POST_FILENAME, POST_CHKBOX,
                      USER_ISPAID, MEDIA_D, BASE_D, BASE_S):
    file_name = os.path.join(MEDIA_D, str(ENT_TID), POST_FILENAME)
    SESSION_D = os.path.dirname(BASE_S)
    r = None
    cnt = 1
    duration = 60
    try:
        POST_TEXT = str(POST_TEXT.strip()) if POST_TEXT.strip() else None

        if POST_TYPE in ['video', 'video_note'] or (
                POST_TYPE in ['document'] and file_name.lower().endswith(('.mp4', '.mov'))):
            file = await bot.get_file(POST_FID)
            await bot.download_file(file.file_path, file_name)

            try:
                with VideoFileClip(file_name) as clip:
                    duration = int(clip.duration)
            except:
                pass

            duration = duration if duration < 60 else 60
        elif POST_TYPE in ['photo']:
            file = await bot.get_file(POST_FID)
            await bot.download_file(file.file_path, file_name)
            duration = 7
        else:
            return

        sql = "SELECT SESSION_TID, SESSION_PHONE, SESSION_STATUS FROM SESSION"
        data = await db_select_pg(sql, (), BASE_S)
        random.shuffle(data)

        for _ in data[:10]:
            sql = "SELECT SESSION_TID, SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_PHONE, SESSION_STATUS FROM SESSION WHERE SESSION_PHONE NOT LIKE '79%'"
            data_ = await db_select_pg(sql, (), BASE_S)
            print(f"{len(data_)=}")
            print(f"{data_=}")
            random.shuffle(data_)
            SESSION_TID, SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_PHONE, SESSION_STATUS = data_[0]
            if SESSION_STATUS is not None or str(SESSION_PHONE).startswith('79'): continue

            try:
                sql = "UPDATE SESSION SET SESSION_STATUS=$1 WHERE SESSION_TID=$2"
                await db_change_pg(sql, (f'story_start', SESSION_TID,), BASE_S)
                get_chat_ = await bot.get_chat(ENT_TID)
                link = f'@{get_chat_.username}' if get_chat_.username else get_chat_.invite_link

                try:
                    await bot.unban_chat_member(chat_id=int(ENT_TID), user_id=SESSION_TID)
                except Exception as e:
                    logger.info(log_ % f"{SESSION_TID}: {str(e)}")  # PARTICIPANT_ID_INVALID
                    await asyncio.sleep(round(random.uniform(0, 1), 2))

                name_ = str(os.path.join(SESSION_D, SESSION_NAME))
                async with Client(name=name_, api_id=SESSION_APIID, api_hash=SESSION_APIHASH) as app:
                    # async with await get_session(SESSION_TID, SESSION_D, BASE_S, EXTRA_D, CONF_P) as app:
                    try:
                        r = await join_my_chat(bot, app, my_tid, link, SESSION_TID, BASE_S)
                        promote_ = await bot.promote_chat_member(ENT_TID, SESSION_TID, can_post_stories=True)
                        if not promote_: raise Exception

                        result = await app.send_story(chat_id=int(ENT_TID), media=file_name, caption=POST_TEXT,
                                                      period=None, duration=duration,
                                                      # for video, but for photo always 7 sec
                                                      pinned=POST_CHKBOX['POST_ISPIN'],
                                                      protect_content=POST_CHKBOX['POST_ISPROTECT'])
                        print(f"{result=}")

                        await bot.promote_chat_member(chat_id=int(ENT_TID), user_id=SESSION_TID, is_anonymous=False,
                                                      can_manage_chat=False, can_delete_messages=False,
                                                      can_manage_video_chats=False, can_restrict_members=False,
                                                      can_promote_members=False, can_change_info=False,
                                                      can_invite_users=False, can_post_stories=False,
                                                      can_edit_stories=False, can_delete_stories=False,
                                                      can_post_messages=False, can_edit_messages=False,
                                                      can_pin_messages=False, can_manage_topics=False)

                        print(f"if public channel: {result.link=}")
                        if result.link: await bot.send_message(chat_id=chat_id, text=result.link)
                    except Exception as e:
                        logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                        await asyncio.sleep(round(random.uniform(0, 1), 2))

                        if 'BOOSTS_REQUIRED' in str(e):
                            stat_boosts = await app.get_boosts_status(chat_id=int(ENT_TID))
                            print(f"{stat_boosts=}")
                            need_boosts = stat_boosts.next_level_boosts - stat_boosts.current_level_boosts
                            await bot.send_message(chat_id=chat_id,
                                                   text=l_chn_need_boost_for_story[lz].format(need_boosts))
                            return
                    finally:
                        await leave_my_chat(app, r, link)

                    cnt += 1
                    if result or cnt > 2: break
            except (UserDeactivatedBan, UserDeactivated, AuthKeyInvalid, AuthKeyUnregistered, AuthKeyDuplicated,
                    SessionExpired, SessionRevoked) as e:
                logger.info(log_ % f"deactivated {SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(5, 10),
                                          2))  # await delete_account(bot, SESSION_TID, SESSION_D, CONF_P, BASE_S)
            except Exception as e:
                logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(0, 1), 2))
                sql = "UPDATE CHANNEL SET CHANNEL_ISPROMOTED=0 WHERE CHANNEL_TID=$1"
                await db_change_pg(sql, (ENT_TID,), BASE_D)
            finally:
                sql = "UPDATE SESSION SET SESSION_STATUS=$1 WHERE SESSION_TID=$2"
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
        if file_name and os.path.exists(file_name): os.remove(file_name)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        await delete_msg_media_file(file_name)


async def pst_inline(chat_id, POST_TID, data_bot, BASE_P, PROJECT_USERNAME, is_main_bot=False):
    result = []
    try:
        (
            BOT_ID, BOT_TID, OWNER_TID, SESSION_TID, BOT_STATUS, BOT_PID, BOT_USERNAME,
            BOT_FIRSTNAME, BOT_PHOTO, BOT_TOKEN, BOT_CRYPTOPAY, BOT_TOKENPAY, BOT_ISPAID,
            BOT_TOKENTGPH, BOT_PAGETGPH, BOT_JSONTGPH, BOT_CBAN, BOT_CTRANSLATE, BOT_CPAY,
            BOT_CPAYCHANNEL, BOT_CPAYCHANNELTID, BOT_CPAYGROUP, BOT_CPAYGROUPTID, BOT_CPAYPRICE,
            BOT_OWNERADDRESS, BOT_CPAYCOLLECTION, BOT_CPAYMASTER, BOT_CPAYAMOUNT,
            BOT_CPAYCURRENCY, BOT_CPAYPERIOD, BOT_CINTEGRATION, BOT_CINTEGRATIONDST,
            BOT_CNOTIFICATION, BOT_CUSER, BOT_CADMIN, BOT_CADMINDST, BOT_VARS, BOT_LSTS,
            BOT_USERCNT, BOT_HASH, BOT_IP, BOT_PORT, BOT_ISNFTUSERNAME, BOT_STAGES, BOT_TZ,
            BOT_COLLECTIONADDRESS, BOT_COLLECTIONPRIVATE, BOT_CPAYDONCNT
        ) = data_bot[0]

        sql = f"""
            SELECT POST_ID, POST_TID, POST_MSGID, POST_CHATTID, POST_USERTID, POST_USERTUN, 
                   POST_TARGETTYPE, POST_TARGET, POST_TYPE, POST_TEXT, POST_MEDIA, POST_BUTTONS, 
                   POST_CHKBOX, POST_WEB, POST_PAY, POST_NFT, POST_BLOG, POST_ISMINTED, 
                   POST_MINTLINK, POST_ISPRIVATE, POST_TZ, POST_DT, POST_TR, POST_STATUS 
            FROM BOT_{BOT_TID}.POST 
            WHERE POST_TID=$1
        """
        data_post = await db_select_pg(sql, (POST_TID,), BASE_P)
        if not len(data_post): return
        POST_ID, POST_TID, POST_MSGID, POST_CHATTID, POST_USERTID, POST_USERTUN, \
            POST_TARGETTYPE, POST_TARGET, POST_TYPE, POST_TEXT, POST_MEDIA, POST_BUTTONS, \
            POST_CHKBOX, POST_WEB, POST_PAY, POST_NFT, POST_BLOG, POST_ISMINTED, \
            POST_MINTLINK, POST_ISPRIVATE, POST_TZ, POST_DT, POST_TR, POST_STATUS = data_post[0]
        print(f"===============================================")
        print(f"pst_inline")
        print(f"===============================================")

        try:
            POST_MEDIA = json.loads(POST_MEDIA)
        except:
            POST_MEDIA = []
        try:
            POST_BUTTONS = json.loads(POST_BUTTONS)
        except:
            POST_BUTTONS = []
        try:
            POST_CHKBOX = json.loads(POST_CHKBOX)
        except:
            POST_CHKBOX = {}

        PST_TEXT = await correct_txt_tags_for_tg(POST_TEXT)
        # we don't know from that button
        # if len(lnk) + len(PST_TEXT) < 1024: PST_TEXT = f"{PST_TEXT}\n\n<blockquote>{lnk}</blockquote>"

        reply_markup = InlineKeyboardBuilder()
        if POST_CHKBOX['POST_ISGALLERY'] and len(POST_MEDIA) > 1:
            len_ = len(POST_MEDIA)

            # msg_markup = copy.deepcopy(reply_markup_.as_markup())
            # for items in msg_markup.inline_keyboard:
            #     cnt = 0
            #     for i, item in enumerate(items):
            #         if getattr(item, 'text', None):
            #             if i == 0 and '←' in item.text:
            #                 cnt += 1
            #             elif i == 1 and '/' in item.text:
            #                 cnt += 1
            #             elif i == 2 and '→' in item.text:
            #                 cnt += 1
            # if reply_markup_ and reply_markup_ != InlineKeyboardBuilder():
            #     msg_markup = copy.deepcopy(reply_markup_.as_markup())
            #     for items in msg_markup.inline_keyboard:
            #         cnt = 0
            #         for i, item in enumerate(items):
            #             if getattr(item, 'text', None):
            #                 if i == 0 and '←' in item.text:
            #                     cnt += 1
            #                 elif i == 1 and '/' in item.text:
            #                     cnt += 1
            #                 elif i == 2 and '→' in item.text:
            #                     cnt += 1
            #         if cnt == 3:
            #             for item in items:
            #                 if getattr(item, 'text', None) and '←' in item.text:
            #                     tmp = item.callback_data.split('_')
            #                     item.callback_data = f"{tmp[0]}_{ix + 1}_{tmp[2]}_{tmp[3]}"
            #                 elif getattr(item, 'text', None) and '/' in item.text:
            #                     tmp = item.text.split('/')
            #                     item.text = f"{ix + 1}/{tmp[-1]}"
            #                 elif getattr(item, 'text', None) and '→' in item.text:
            #                     tmp = item.callback_data.split('_')
            #                     item.callback_data = f"{tmp[0]}_{ix + 1}_{tmp[2]}_{tmp[3]}"
            # else:
            #     msg_markup = None
            # index = cur_ - 1
            cur_ = '1'

            buttons = [
                types.InlineKeyboardButton(text="←", callback_data=f'pst_{BOT_TID}_{POST_TID}_0_{cur_}_{len_}_prev'),
                types.InlineKeyboardButton(text=f"{cur_}/{len_}", callback_data=f'pst_{BOT_TID}_{POST_TID}_0_{cur_}_{len_}_cur'),
                types.InlineKeyboardButton(text="→", callback_data=f'pst_{BOT_TID}_{POST_TID}_0_{cur_}_{len_}_next')
            ]
            reply_markup.row(*buttons)
        reply_markup = await get_ent_rm(chat_id, reply_markup, BOT_TID, POST_USERTUN, POST_TID, POST_BUTTONS, BASE_P, PROJECT_USERNAME)

        if POST_TYPE == 'text':
            input_message_content = InputTextMessageContent(message_text=PST_TEXT)
            article = types.InlineQueryResultArticle(id=str(uuid4()),
                                             title=BOT_FIRSTNAME,
                                             description=f"@{BOT_USERNAME}",
                                             input_message_content=input_message_content,
                                             reply_markup=reply_markup.as_markup())
            result.append(article)
            return

        print(f"{POST_MEDIA=}")
        for media in POST_MEDIA:
            try:
                article = None
                POST_FID = media['file_id'] if is_main_bot else media['fileb_id']
                POST_TYPE = media['file_type']
                POST_LNK = media['file_link']
                print(f"{is_main_bot=}")

                if POST_TYPE == 'photo':
                    # if POST_LNK and POST_LNK != '':
                    #     article = types.InlineQueryResultPhoto(id=str(uuid4()),
                    #                                            thumbnail_url=POST_LNK,
                    #                                            photo_url=POST_LNK,
                    #                                            caption=POST_TEXT,
                    #                                            title=f"post #{post_id}: {html.quote(POST_TEXT.strip()[0:16])}",
                    #                                            description=f"Date: {POST_DT}, type: {POST_TYPE}",
                    #                                            parse_mode=ParseMode.HTML,
                    #                                            reply_markup=msg_markup
                    #                                            )
                    # else:
                    article = types.InlineQueryResultCachedPhoto(id=str(uuid4()),
                                                                 photo_file_id=POST_FID,
                                                                 caption=PST_TEXT,
                                                                 title=BOT_FIRSTNAME,
                                                                 description=f"@{BOT_USERNAME}",
                                                                 parse_mode=ParseMode.HTML,
                                                                 reply_markup=reply_markup.as_markup())
                elif POST_TYPE in ['animation', 'gif']:
                    # if POST_LNK and POST_LNK != '':
                    #     article = types.InlineQueryResultGif(id=str(uuid4()),
                    #                                          thumbnail_url=POST_LNK,
                    #                                          gif_url=POST_LNK,
                    #                                          caption=POST_TEXT,
                    #                                          title=f"post #{post_id}: {html.quote(POST_TEXT.strip()[0:16])}",
                    #                                          description=f"Date: {POST_DT}, type: {POST_TYPE}",
                    #                                          parse_mode=ParseMode.HTML,
                    #                                          reply_markup=msg_markup)
                    # else:
                    article = types.InlineQueryResultCachedGif(id=str(uuid4()),
                                                               gif_file_id=POST_FID,
                                                               caption=PST_TEXT,
                                                               title=BOT_FIRSTNAME,
                                                               # description=f"Date: {POST_DT}, type: {POST_TYPE}",
                                                               parse_mode=ParseMode.HTML,
                                                               reply_markup=reply_markup.as_markup())
                elif POST_TYPE == 'video':
                    # if POST_LNK and POST_LNK != '':
                    #     article = types.InlineQueryResultVideo(id=str(uuid4()),
                    #                                            thumbnail_url=POST_LNK,
                    #                                            mime_type='video/mp4',
                    #                                            video_url=POST_LNK,
                    #                                            caption=POST_TEXT,
                    #                                            title=f"post #{post_id}: {html.quote(POST_TEXT.strip()[0:16])}",
                    #                                            description=f"Date: {POST_DT}, type: {POST_TYPE}",
                    #                                            parse_mode=ParseMode.HTML,
                    #                                            reply_markup=msg_markup)
                    # else:
                    article = types.InlineQueryResultCachedVideo(id=str(uuid4()),
                                                                 video_file_id=POST_FID,
                                                                 caption=PST_TEXT,
                                                                 title=BOT_FIRSTNAME,
                                                                 description=f"@{BOT_USERNAME}",
                                                                 parse_mode=ParseMode.HTML,
                                                                 reply_markup=reply_markup.as_markup())
                elif POST_TYPE == 'audio':
                    # if POST_LNK and POST_LNK != '':
                    #     article = types.InlineQueryResultAudio(id=str(uuid4()),
                    #                                            audio_url=POST_LNK,
                    #                                            caption=POST_TEXT,
                    #                                            title=f"post #{post_id}: {html.quote(POST_TEXT.strip()[0:16])}",
                    #                                            # description=f"Date: {POST_DT}, type: {POST_TYPE}",
                    #                                            parse_mode=ParseMode.HTML,
                    #                                            reply_markup=msg_markup)
                    # else:
                    article = types.InlineQueryResultCachedAudio(id=str(uuid4()),
                                                                 audio_file_id=POST_FID,
                                                                 caption=PST_TEXT,
                                                                 parse_mode=ParseMode.HTML,
                                                                 reply_markup=reply_markup.as_markup())
                elif POST_TYPE == 'voice':
                    # if POST_LNK and POST_LNK != '':
                    #     article = types.InlineQueryResultVoice(id=str(uuid4()),
                    #                                            voice_url=POST_LNK,
                    #                                            caption=POST_TEXT,
                    #                                            title=f"post #{post_id}: {html.quote(POST_TEXT.strip()[0:16])}",
                    #                                            parse_mode=ParseMode.HTML,
                    #                                            reply_markup=msg_markup)
                    # else:
                    article = types.InlineQueryResultCachedVoice(id=str(uuid4()),
                                                                 voice_file_id=POST_FID,
                                                                 caption=PST_TEXT,
                                                                 title=BOT_FIRSTNAME,
                                                                 parse_mode=ParseMode.HTML,
                                                                 reply_markup=reply_markup.as_markup())
                elif POST_TYPE in ['video_note', 'telescope']:
                    print(f"{POST_LNK=}")
                    # article = types.InlineQueryResultVideo(id=str(uuid4()),
                    #                                        title=BOT_FIRSTNAME,
                    #                                        description=f"@{BOT_USERNAME}",
                    #                                        mime_type='video/mp4',
                    #                                        thumbnail_url=POST_LNK,
                    #                                        caption=None,
                    #                                        # works only with telesco - old info!
                    #                                        # video_url='https://telesco.pe//45',
                    #                                        video_url=POST_LNK,
                    #                                        parse_mode=ParseMode.HTML,
                    #                                        reply_markup=reply_markup.as_markup())
                    # all works now fine !

                    article = types.InlineQueryResultVideo(id=str(uuid4()),
                                                       title=BOT_FIRSTNAME,
                                                       mime_type='video/mp4',
                                                       thumbnail_url=POST_LNK,
                                                       video_url=POST_FID,
                                                       reply_markup=reply_markup.as_markup())
                elif POST_TYPE == 'sticker':
                    article = types.InlineQueryResultCachedSticker(id=str(uuid4()),
                                                                   sticker_file_id=POST_FID,
                                                                   reply_markup=reply_markup.as_markup())
                elif POST_TYPE == 'document':
                    article = types.InlineQueryResultCachedDocument(id=str(uuid4()),
                                                                    document_file_id=POST_FID,
                                                                    caption=PST_TEXT,
                                                                    title=BOT_FIRSTNAME,
                                                                    description=f"@{BOT_USERNAME}",
                                                                    parse_mode=ParseMode.HTML,
                                                                    reply_markup=reply_markup.as_markup())

                if article:
                    result.append(article)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result
# endregion


# region fun
async def every_media_url(file_name):
    try:
        print(f"every_media_url {file_name=}")
        await asyncio.sleep(round(random.uniform(40, 60), 2))

        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"every_media_url done")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def delete_msg_media_file(msg_media):
    try:
        if msg_media and os.path.exists(msg_media):
            os.remove(msg_media)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def get_tz(dt_client):
    result = '+00:00'
    try:
        minutes = int(dt_client.lstrip('-'))
        sign_ = '+' if dt_client[0] == '-' else '-'
        h_orig = int(minutes / 60)
        h_ = str(h_orig) if h_orig >= 10 else f'0{h_orig}'
        m_ = minutes - h_orig * 60
        m_ = str(m_) if m_ >= 10 else f'0{m_}'
        result = f"{sign_}{h_}:{m_}"
        print('tz_ ', result)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_utc_from_local(POST_DT, POST_TZ):
    result = POST_DT
    try:
        if str(POST_DT) in ['', 'None']: return
        sign_ = POST_TZ[0]
        h_, m_ = POST_TZ.strip(sign_).split(':')
        h_, m_ = int(h_), int(m_)
        delta = timedelta(hours=h_, minutes=m_)
        dt = datetime.strptime(POST_DT, "%Y-%m-%dT%H:%M")
        dt = dt - delta if sign_ == '+' else dt + delta
        result = dt.strftime("%Y-%m-%dT%H:%M")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


def is_all_latin(text):
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.?!;:()\"'-—")

    for char in text:
        if char not in allowed_chars:
            return False
    return True


async def txt_moderate(txt):
    result = txt
    try:
        txt = txt.replace('mef', '')
        print(f"{txt=}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def bot_middleware(app, handler):
    async def middleware_handler(request):
        request['bot'] = app['bot']
        return await handler(request)

    return middleware_handler


async def getgems_set(bot, message, EXTRA_D):
    result = False
    try:
        chat_id = message.from_user.id
        if message.text and 80 < len(message.text) < 90 and '_C-' in message.text and str(chat_id) in my_tids:
            f_n = next(
                (os.path.join(root, f) for root, _, files in os.walk(EXTRA_D) for f in files if f.endswith('.getgems')),
                None)
            print(f"{f_n=}")
            if f_n:
                file_dir, file_name = os.path.split(f_n)
                current_date = datetime.now(timezone.utc).strftime('%d-%m-%Y')
                print(f"{current_date=} (он уже сущ)")
                new_file_path = os.path.join(file_dir, f'{current_date}.getgems')
                os.rename(f_n, new_file_path)
            else:
                current_date = datetime.now(timezone.utc).strftime('%d-%m-%Y')
                new_file_path = os.path.join(EXTRA_D, f'{current_date}.getgems')

            async with aiofiles.open(new_file_path, 'w') as file:
                await file.write(message.text)

            await bot.send_message(chat_id, f"👩🏽‍💻 <b>Token</b>: <code>{message.text}</code>")
            result = True
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def getgems_get(EXTRA_D):
    result = None
    try:
        f_n = next(
            (os.path.join(root, f) for root, _, files in os.walk(EXTRA_D) for f in files if f.endswith('.getgems')),
            None)
        if f_n:
            async with aiofiles.open(f_n, 'r') as file:
                result = (await file.read()).strip()

        print(f"{result=}")
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def correct_orientation(image):
    try:
        exif = image.getexif()
        if exif:
            orientation_key = None
            for key, value in ExifTags.TAGS.items():
                if value == 'Orientation':
                    orientation_key = key
                    break

            if orientation_key is not None:
                orientation = exif.get(orientation_key)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return image


async def extract_links(text):
    result = []
    try:
        tmp_arr = re.split(r'\s+', text)

        for item in tmp_arr:
            try:
                if ('https://' in item.lower() or 'http://' in item.lower()) and (
                        '.mp4' in item.lower() or '.jpg' in item.lower() or '.jpeg' in item.lower() or '.png' in item.lower() or '.mp3' in item.lower() or '.ogg' in item.lower()):
                    ix_start = item.lower().find('https://') if 'https://' in item.lower() else item.lower().find(
                        'http://')
                    ix_finish = -1

                    if '.mp4' in item.lower():
                        ix_finish = item.lower().find('.mp4') + len('.mp4')
                    elif '.jpg' in item.lower():
                        ix_finish = item.lower().find('.jpg') + len('.jpg')
                    elif '.jpeg' in item.lower():
                        ix_finish = item.lower().find('.jpeg') + len('.jpeg')
                    elif '.png' in item.lower():
                        ix_finish = item.lower().find('.png') + len('.png')
                    elif '.mp3' in item.lower():
                        ix_finish = item.lower().find('.mp3') + len('.mp3')
                    elif '.ogg' in item.lower():
                        ix_finish = item.lower().find('.ogg') + len('.ogg')

                    if ix_finish == -1: continue
                    print(item.lower()[ix_start:ix_finish])
                    result.append(item.lower()[ix_start:ix_finish])
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(0, 1), 2))

        if len(result):
            result = list(set(result))
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def is_member_in_channel(bot, chat_id, lz):
    result = False
    try:
        # бот дб добавлен в канал предварительно
        channel_id = ferey_channel_en
        if lz == 'ru':
            channel_id = ferey_channel_europe
        elif lz == 'es':
            channel_id = ferey_channel_es
        elif lz == 'fr':
            channel_id = ferey_channel_fr
        elif lz == 'ar':
            channel_id = ferey_channel_ar
        elif lz == 'zh':
            channel_id = ferey_channel_zh

        get_chat_member_ = await bot.get_chat_member(chat_id=channel_id, user_id=chat_id)
        if get_chat_member_.status in ['member', 'administrator', 'creator']:
            result = True
        else:
            text = l_subscribe_channel_for_post[lz].format(get_tg_channel(lz))
            await bot.send_message(chat_id, text)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def get_lz_by_entity_id(ENTITY_TID, BASE_D):
    result = 'en'
    try:
        sql = "SELECT OWNER_TID FROM CHANNEL WHERE CHANNEL_TID=$1"
        data = await db_select_pg(sql, (ENTITY_TID,), BASE_D)
        if not len(data): return
        OWNER_TID = data[0][0]

        sql = "SELECT USER_LZ FROM USER WHERE USER_TID=$1"
        data = await db_select_pg(sql, (OWNER_TID,), BASE_D)
        if not len(data): return
        result = data[0][0]
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def run_shell(cmd):
    result = None
    try:
        proc = await asyncio.create_subprocess_shell(cmd, stderr=asyncio.subprocess.PIPE,
                                                     stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()

        logger.info(log_ % f'[{cmd!r} exited with {proc.returncode}]')
        if stdout:
            logger.info(log_ % f'{stdout.decode()}')
            result = f'[stdout]\n{stdout.decode()}'
        if stderr:
            logger.info(log_ % f'{stderr.decode()}')
            result = f'[stderr]\n{stderr.decode()}'
        else:
            result = str(proc.returncode)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


def _join(*content, sep=" "):
    return sep.join(map(str, content))


async def get_chat_channel(bot, link, SESSION_D, BASE_S):
    result = r = None
    try:
        sql = "SELECT SESSION_TID, SESSION_STATUS FROM SESSION"
        data = await db_select_pg(sql, (), BASE_S)
        random.shuffle(data)

        for _ in data:
            sql = "SELECT SESSION_TID, SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_STATUS FROM SESSION"
            data = await db_select_pg(sql, (), BASE_S)
            random.shuffle(data)
            SESSION_TID, SESSION_NAME, SESSION_APIID, SESSION_APIHASH, SESSION_STATUS = data[0]
            if SESSION_STATUS is not None: continue

            try:
                sql = "UPDATE SESSION SET SESSION_STATUS=$1 WHERE SESSION_TID=$2"
                await db_change_pg(sql, (f'get_chat_channel', SESSION_TID,), BASE_S)

                logger.info(log_ % f"{SESSION_TID} {SESSION_NAME}")
                name_ = str(os.path.join(SESSION_D, SESSION_NAME))
                async with Client(name=name_, api_id=SESSION_APIID, api_hash=SESSION_APIHASH) as app:
                    try:
                        r = await join_my_chat(bot, app, my_tid, link, SESSION_TID, BASE_S)
                        result = await bot.get_chat(r.id)
                    finally:
                        await leave_my_chat(app, r, link)
                        break
            except (UserDeactivatedBan, UserDeactivated, AuthKeyInvalid, AuthKeyUnregistered, AuthKeyDuplicated,
                    SessionExpired, SessionRevoked) as e:
                logger.info(log_ % f"{SESSION_TID} deactivated: {str(e)}")
                await asyncio.sleep(round(random.uniform(5, 10), 2))
            except Exception as e:
                logger.info(log_ % f"{SESSION_TID}: {str(e)}")
                await asyncio.sleep(round(random.uniform(0, 1), 2))
            finally:
                sql = "UPDATE SESSION SET SESSION_STATUS=$1 WHERE SESSION_TID=$2"
                await db_change_pg(sql, (SESSION_STATUS, SESSION_TID,), BASE_S)
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


async def auto_destroy_msg(bot, telegram_bot, chat_id, text, message_id, type_='text', sec=5):
    result = None
    try:
        if not random.choice([0, 1, 1]): return

        step = 1
        by = f"<a href='https://t.me/{ferey_telegram_demo_bot}'>by</a>"
        text = f"{text}\n\n{by} @{telegram_bot} <b>{sec}</b>sec"
        ix_sec = text.rfind('</b>sec')
        while text[ix_sec] != '>': ix_sec -= 1

        while sec > 0:
            try:
                text = text.replace(f"<b>{sec}</b>sec", f"<b>{sec - 1}</b>sec")
                sec -= step
                if type_ == 'text':
                    await bot.edit_message_text(chat_id=chat_id, text=text, message_id=message_id,
                                                disable_web_page_preview=True)
                else:
                    await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=text)
                await asyncio.sleep(1)
            except TelegramRetryAfter as e:
                logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
                await asyncio.sleep(e.retry_after + 1)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
                break
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(e)
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        await bot.delete_message(chat_id, message_id)
        return result


async def log_old(txt, LOG_DEFAULT, colour=92):
    try:
        logging.info(f'\033[{colour}m%s\033[0m' % (str(txt)))
        async with aiofiles.open(LOG_DEFAULT, 'a') as f:
            await f.write(str(txt) + '\n')
    except Exception as e:
        logger.info(f'\033[{95}m%s\033[0m' % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))


async def log(txt, color=21):
    try:
        '''DESC
21 - underscore     !
30 - black          !
90 - grey
91 - red            !
92 - green          !
93 - yellow         
94 - blue
95 - purple         !
96 - cyan           !
97 - white
---------------------
100 - grey bg
101 - red bg
102 - green bg
103 - yellow bg
104 - blue bg
105 - purple bg
106 - cyan bg
107 - white bg
'''

        logger.info(f'\033[{color}m%s\033[0m' % str(txt))
    except Exception:
        await asyncio.sleep(round(random.uniform(0, 1), 2))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def fun_empty(txt):
    try:
        txt = str(txt)
        if '%' in txt:
            print(txt)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))


async def lz_code(chat_id, lan, BASE_D):
    result = 'en'
    try:
        sql = "SELECT USER_LZ FROM USER WHERE USER_TID=$1"
        data = await db_select_pg(sql, (chat_id,), BASE_D)

        # first enter before DB
        if not len(data) or not data[0][0]:
            # chinese
            if lan in ['zh', 'zh-chs', 'zh-cht', 'ja', 'ko', 'zh-CN', 'zh-TW', 'th', 'vi', 'tw', 'sg']:
                result = 'zh'
            # arabic    # ir, af
            elif lan in ['ar-XA', 'ar', 'tr', 'ur', 'fa', 'tj', 'dz', 'eg', 'iq', 'sy', 'ae', 'sa', 'tn', 'ir', 'af']:
                result = 'ar'
            # spanish   # portugal: 'pt', 'br', 'ao', 'mz'
            elif lan in ['es', 'ar', 'cl', 'co', 'cu', 've', 'bo', 'pe', 'ec', 'pt', 'br', 'ao', 'mz']:
                result = 'es'
            # french
            elif lan in ['fr', 'ch', 'be', 'ca']:
                result = 'fr'
            # europe
            elif lan in ['ru', 'kz', 'kg', 'uz', 'tm', 'md', 'am', 'uk-UA', 'uk', 'kk', 'tk', 'ky']:
                result = 'ru'

            sql = "UPDATE USER SET USER_LZ=$1 WHERE USER_TID=$2"
            await db_change_pg(sql, (result, chat_id,), BASE_D)
        else:
            result = data[0][0]
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def lz_code_pg(chat_id, lan, BASE_D):
    result = 'en'
    try:
        sql = "SELECT USER_LZ FROM \"USER\" WHERE USER_TID=$1"
        data = await db_select_pg(sql, (chat_id,), BASE_D)

        # first enter before DB
        if not len(data) or not data[0][0]:
            # chinese
            if lan in ['zh', 'zh-chs', 'zh-cht', 'ja', 'ko', 'zh-CN', 'zh-TW', 'th', 'vi', 'tw', 'sg']:
                result = 'zh'
            # arabic    # ir, af
            elif lan in ['ar-XA', 'ar', 'tr', 'ur', 'fa', 'tj', 'dz', 'eg', 'iq', 'sy', 'ae', 'sa', 'tn', 'ir', 'af']:
                result = 'ar'
            # spanish   # portugal: 'pt', 'br', 'ao', 'mz'
            elif lan in ['es', 'ar', 'cl', 'co', 'cu', 've', 'bo', 'pe', 'ec', 'pt', 'br', 'ao', 'mz']:
                result = 'es'
            # french
            elif lan in ['fr', 'ch', 'be', 'ca']:
                result = 'fr'
            # europe
            elif lan in ['ru', 'kz', 'kg', 'uz', 'tm', 'md', 'am', 'uk-UA', 'uk', 'kk', 'tk', 'ky']:
                result = 'ru'

            sql = "UPDATE \"USER\" SET USER_LZ=$1 WHERE USER_TID=$2"
            await db_change_pg(sql, (result, chat_id,), BASE_D)
        else:
            result = data[0][0]
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def check_sub_pay_pg(chat_id, lz, BOT_TOKEN_E18B, BASE_D):
    is_paid = False
    till_paid = ''
    try:
        USER_ISPAID = 0
        USER_DTPAID = ''
        dt_now = datetime.now(timezone.utc)
        USER_DT = dt_now.strftime('%d-%m-%Y_%H-%M-%S')
        extra_bot = None
        try:
            lib_id = channel_library_ru if lz == 'ru' else channel_library_en
            extra_bot = Bot(token=BOT_TOKEN_E18B)
            member_ = await extra_bot.get_chat_member(chat_id=lib_id, user_id=chat_id)
            if member_.status in ['member', 'administrator', 'creator']: is_paid = True
            print(f"check_sub_pay {is_paid=}")
        except Exception as e:
            logger.info(log_ % str(e))
        finally:
            if extra_bot: await extra_bot.session.close()

        sql = "SELECT USER_ISPAID, USER_DTPAID, USER_TYPAID, USER_DT, USER_LZ FROM \"USER\" WHERE USER_TID=$1"
        data_usr = await db_select_pg(sql, (chat_id,), BASE_D)

        if not len(data_usr):
            sql = "INSERT INTO \"USER\" (USER_TID, USER_DT) VALUES ($1, $2) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (chat_id, USER_DT,), BASE_D)
        else:
            USER_ISPAID, USER_DTPAID, USER_TYPAID, USER_DT, lz = data_usr[0]

        if is_paid:
            sql = "UPDATE \"USER\" SET USER_ISPAID=1, USER_DTPAID='', USER_TYPAID='all' WHERE USER_TID=$1"
            await db_change_pg(sql, (chat_id,), BASE_D)
        elif USER_ISPAID and USER_DTPAID:
            till_paid = dt_now.strptime(USER_DTPAID, "%d-%m-%Y_%H-%M-%S").replace(tzinfo=timezone.utc)
            print(f"{till_paid=}")

            if dt_now > till_paid:
                sql = "UPDATE \"USER\" SET USER_ISPAID=0, USER_DTPAID='', USER_TYPAID='' WHERE USER_TID=$1"
                await db_change_pg(sql, (chat_id,), BASE_D)
                till_paid = ''
            else:
                is_paid = True
                till_paid = till_paid.strftime('%d.%m.%Y')
        else:
            sql = "UPDATE \"USER\" SET USER_ISPAID=0, USER_DTPAID='', USER_TYPAID='' WHERE USER_TID=$1"
            await db_change_pg(sql, (chat_id,), BASE_D)
        print(f"check_sub_pay {is_paid=}, {till_paid=}")
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}")
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return is_paid, till_paid


async def no_war_text(txt):
    result = txt
    try:
        pass  # result = txt.replace('а', 'ä').replace('А', 'Ä').replace('в', 'ʙ').replace('В', 'B').replace('г', 'ґ')  # .replace('Г', 'Ґ').replace('е', 'é').replace('Е', 'É').replace('ж', 'җ').replace('Ж', 'Җ').replace('з', 'з́')  # .replace('З', 'З́').replace('й', 'ҋ').replace('Й', 'Ҋ').replace('к','қ').replace('К', 'Қ').replace('М', 'M')  # .replace('Н','H').replace('о', 'ô').replace('О', 'Ô').replace('р', 'p').replace('Р', 'P').replace('с', 'č')  # .replace('С', 'Č').replace('т', 'ҭ').replace('Т', 'Ҭ').replace('у', 'ў').replace('У', 'Ў').replace('х', 'x')  # .replace('Х', 'X').replace('э', 'є').replace('Э', 'Є')  # result = txt.replace('А', 'Ä').replace('в', 'ʙ').replace('В', 'B').replace('г', 'ґ').replace('Г', 'Ґ').  # replace('Е', 'É').replace('ж', 'җ').replace('Ж', 'Җ').replace('й', 'ҋ').replace('К', 'Қ').replace('М', 'M')  # .replace('Н', 'H').replace('о', 'ô').replace('О', 'Ô').replace('р', 'p').replace('Р', 'P').replace('С', 'Č')  # .replace('Т', 'Ҭ').replace('У', 'Ў').replace('х', 'x').replace('Х', 'X').replace('э', 'є')
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def get_from_media(CONF_P, EXTRA_D, MEDIA_D, BASE_D, src, re_write=False, basewidth=1024):
    result = None
    try:
        is_link = await is_url(src)
        file_id = await get_fileid_from_src(src, is_link, BASE_D)
        if is_link and 'drive.google.com' not in src:
            result = src
        elif src is None:
            result = None
        elif file_id and re_write is False:
            result = file_id
        else:
            if os.path.basename(src) in os.listdir(MEDIA_D) and re_write is False:
                # tmp = os.path.join(MEDIA_D, os.path.basename(src))
                result = os.path.join(MEDIA_D, os.path.basename(src))
            else:
                scopes = r_conf('scopes', CONF_P)
                credential_file = os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0])
                credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
                http_auth = credentials.authorize(httplib2.Http())
                drive_service = build('drive', 'v3', http=http_auth, cache_discovery=False)

                if is_link:
                    docid = get_doc_id_from_link(src)
                    file_list_dic = await api_get_file_list(drive_service, docid, {}, is_file=True)
                else:
                    file_list_dic = await api_get_file_list(drive_service, (r_conf('share_folder_id', CONF_P))[0], {})

                for k, v in file_list_dic.items():
                    if is_link:
                        result = await api_dl_file(drive_service, k, v[0], v[1], MEDIA_D)
                        break
                    elif str(v[0]).lower() == str(os.path.basename(src)).lower():
                        result = await api_dl_file(drive_service, k, v[0], v[1], MEDIA_D)
                        break

            if await is_image(result):
                result = await resize_media(result, basewidth)
            elif await is_video(result):
                result = await resize_video_note(result, basewidth)
            logger.info(log_ % 'dl media ok')
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def is_url(url):
    status = False
    try:
        if url and '://' in url:  # and requests.get(url).status_code == 200:
            status = True
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return status


async def get_fileid_from_src(src, is_link, BASE_D):
    data = None
    try:
        if is_link:
            sql = "SELECT FILE_FILEID FROM \"FILE\" WHERE FILE_FILELINK=$1"
        else:
            sql = "SELECT FILE_FILEID FROM \"FILE\" WHERE FILE_FILENAME=$1"
        data = await db_select_pg(sql, (src,), BASE_D)
        if not data:
            return None
        data = data[0][0]
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return data


async def is_image(file_name):
    im = None
    try:
        if str(file_name).lower().endswith('.docx') or str(file_name).lower().endswith('.pdf') or str(
                file_name).lower().endswith('.mp4'):
            return False
        im = Image.open(file_name)
    except Exception as e:
        logger.info(log_ % 'isImage: ' + str(e))
    finally:
        return im


async def is_video(file_name):
    vi = None
    try:
        vi = True if str(mimetypes.guess_type(file_name)[0]).startswith('video') else False
    except Exception as e:
        logger.info(log_ % 'isVideo: ' + str(e))
    finally:
        return vi


async def get_thumb(MEDIA_D, file_name, sz_thumbnail=32):
    size = sz_thumbnail, sz_thumbnail
    result = ''
    try:
        name = get_name_without_ext(file_name)
        im = Image.open(file_name)
        im = await correct_orientation(im)
        im.thumbnail(size, Image.Resampling.LANCZOS)
        result = f'{MEDIA_D}/"thumbnail_"{name}'
        im.save(result, "JPEG")
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def check_username(username):
    result = True
    try:
        if str(username).isdigit():
            result = False
        elif len(username) < 4 or len(username) > 31:
            result = False
        elif username.startswith('_') or username.endswith('_'):
            result = False
        elif '@' in username and not username.startswith('@'):
            result = False
        else:
            for it in username:
                if it not in string.ascii_letters + string.digits + "@_":
                    result = False
                    return
    except TelegramRetryAfter as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))
    finally:
        return result


def touch(path):
    if not os.path.exists(path):
        with open(path, 'a'):
            os.utime(path,
                     None)  # async with aiofiles.open(path, 'a'):  #     await asyncio.to_thread(os.utime, path, None)


def get_numbers_with_mark(data, id_, row_width=5):
    btns = []
    middle = int(row_width / 2 + 1)
    length = 5 if len(data) < 5 else len(data)

    if id_ == 1 or id_ == 2 or id_ == 3:
        btns.insert(0, f'1')
        btns.insert(1, f'2')
        btns.insert(2, f'3')
        btns.insert(3, f'4›')
        btns.insert(4, f'{length}»')

        btns[id_ - 1] = f'· {id_} ·'
    elif middle < id_ < length - middle + 1:  # 4
        btns.insert(0, f'«1')
        btns.insert(1, f'‹{id_ - 1}')
        btns.insert(2, f'· {id_} ·')
        btns.insert(3, f'{id_ + 1}›')
        btns.insert(4, f'{length}»')
    elif id_ == length or id_ == length - 1 or id_ == length - 2:
        btns.insert(0, f'«1')
        btns.insert(1, f'‹{length - 3}')
        btns.insert(2, f'{length - 2}')
        btns.insert(3, f'{length - 1}')
        btns.insert(4, f'{length}')

        btns[(row_width - (length - id_)) - 1] = f'· {id_} ·'

    if id_ == 4 and len(data) == 4:
        btns = ['«1', '‹2', '3', '· 4 ·', '5']

    return btns


def get_keyboard(data, src, post_id=1, chat_id=''):
    result = InlineKeyboardBuilder()

    row_width = len(data) if len(data) < 5 else 5
    btns = get_numbers_with_mark(data, post_id, row_width)
    buttons = []

    for i in range(1, row_width + 1):
        arr = re.split(r'\s|[«‹·›»]', btns[i - 1])  # ('\s|(?<!\d)[,.](?!\d)', s)
        page_i = list(filter(None, arr))[0]
        page_name = f'page_{src}_{chat_id}_{str(int(page_i))}'
        buttons.append(types.InlineKeyboardButton(text=btns[i - 1], callback_data=page_name))
    result.row(*buttons).adjust(row_width)
    return result


async def save_fileid(message, src, BASE_D):
    if message is None: return
    file_id = usr_id = ''
    if message.photo:
        file_id = message.photo[-1].file_id
    elif message.animation:  # giff
        file_id = message.animation.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:  # m4a
        file_id = message.audio.file_id
    elif message.voice:
        file_id = message.voice.file_id
    elif message.video_note:
        file_id = message.video_note.file_id
    elif message.document:
        file_id = message.document.file_id
    elif message.poll:
        file_id = message.poll.id

    if await is_url(src):
        sql = f"INSERT INTO \"FILE\" (FILE_FILEID, FILE_FILELINK) VALUES ($1, $2) ON CONFLICT DO NOTHING"
    else:
        sql = "INSERT INTO \"FILE\" (FILE_FILEID, FILE_FILENAME) VALUES ($1, $2)  ON CONFLICT DO NOTHING"
    if not await is_exists_filename_or_filelink(src, BASE_D):
        usr_id = await db_change_pg(sql, (file_id, src,), BASE_D)
    return usr_id


async def is_exists_filename_or_filelink(src, BASE_D):
    sql = "SELECT * FROM \"FILE\""
    data = await db_select_pg(sql, (), BASE_D)
    for item in data:
        if src in item:
            return True
    return False


async def check_email(content):
    # Email-check regular expression
    result = None
    try:
        if not content: return
        parts = content.split()
        for part in parts:
            USER_EMAIL = re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", part)
            if len(USER_EMAIL) != 0:
                result = USER_EMAIL[0]
                break
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def check_phone(content):
    result = None
    try:
        for phone in content.split():
            if phone and (str(phone).startswith('+') or str(phone).startswith('8') or str(phone).startswith('9') or str(
                    phone).startswith('7')) and len(str(phone)) >= 10:
                result = phone
                break
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


async def get_photo_file_id(bot, chat_id, file_id_text, BASE_D):
    result = None
    try:
        sql = "SELECT FILE_FILEID FROM \"FILE\" WHERE FILE_FILENAME='text.jpg'"
        data2 = await db_select_pg(sql, (), BASE_D)
        if not len(data2):
            res = await bot.send_photo(chat_id, text_jpeg)
            result = res.photo[-1].file_id
            sql = "INSERT INTO \"FILE\" (FILE_FILEID, FILE_FILENAME) VALUES ($1, $2) ON CONFLICT DO NOTHING"
            await db_change_pg(sql, (file_id_text, 'text.jpg',), BASE_D)
        else:
            result = data2[0][0]
    except Exception as e:
        logger.info(log_ % str(e))
    finally:
        return result


def is_yes_not(msg):
    result = False
    try:
        if msg and str(msg).lower().strip() in ['y', 'yes', 'да', 'д', 'lf', 'l', '1']:
            result = True
    finally:
        return result


def w_conf(key, val, CONF_P, INI_D):
    try:
        CONF_P.read(INI_D)
        CONF_P.set(SECTION, key, str(val))

        with open(INI_D, 'w') as configfile:
            CONF_P.write(configfile)
    except Exception as e:
        print(e, 95)


def r_conf(key, CONF_P):
    result = None
    try:
        s = CONF_P.get(SECTION, key)
        result = ast.literal_eval(s)
        if len(result) == 0:
            result = None
    finally:
        return result


def get_doc_id_from_link(link):
    try:
        begin = link[0:link.rindex('/')].rindex('/') + 1
        end = link.rindex('/')
        link = link[begin:end]
    finally:
        return link


def get_tg_channel(lan):
    result = 'ferey_channel_en'
    try:
        # chinese
        if lan in ['zh', 'zh-chs', 'zh-cht', 'ja', 'ko', 'zh-CN', 'zh-TW', 'th', 'vi', 'tw', 'sg']:
            result = 'ferey_channel_zh'
        # arabic    # ir, af
        elif lan in ['ar-XA', 'ar', 'tr', 'ur', 'fa', 'tj', 'dz', 'eg', 'iq', 'sy', 'ae', 'sa', 'tn', 'ir', 'af']:
            result = 'ferey_channel_ar'
        # spanish   # portugal: 'pt', 'br', 'ao', 'mz'
        elif lan in ['es', 'ar', 'cl', 'co', 'cu', 've', 'bo', 'pe', 'ec', 'pt', 'br', 'ao', 'mz']:
            result = 'ferey_channel_es'
        # french
        elif lan in ['fr', 'ch', 'be', 'ca']:
            result = 'ferey_channel_fr'
        # europe
        elif lan in ['ru', 'kz', 'kg', 'uz', 'tm', 'md', 'am', 'uk-UA', 'uk', 'kk', 'tk', 'ky']:
            result = 'ferey_channel_europe'
    except Exception as e:
        logger.info(e)
    finally:
        return result


def get_tg_group(lan):
    result = 'ferey_group_english'
    try:
        # chinese
        if lan in ['zh', 'zh-chs', 'zh-cht', 'ja', 'ko', 'zh-CN', 'zh-TW', 'th', 'vi', 'tw', 'sg']:
            result = 'ferey_group_chinese'
        # arabic    # ir, af
        elif lan in ['ar-XA', 'ar', 'tr', 'ur', 'fa', 'tj', 'dz', 'eg', 'iq', 'sy', 'ae', 'sa', 'tn', 'ir', 'af']:
            result = 'ferey_group_arabic'
        # spanish   # portugal: 'pt', 'br', 'ao', 'mz'
        elif lan in ['es', 'ar', 'cl', 'co', 'cu', 've', 'bo', 'pe', 'ec', 'pt', 'br', 'ao', 'mz']:
            result = 'ferey_group_spanish'
        # french
        elif lan in ['fr', 'ch', 'be', 'ca']:
            result = 'ferey_group_french'
        # europe
        elif lan in ['ru', 'kz', 'kg', 'uz', 'tm', 'md', 'am', 'uk-UA', 'uk', 'kk', 'tk', 'ky']:
            result = 'ferey_group_europe'
    except Exception as e:
        logger.info(e)
    finally:
        return result


async def send_to_admins(bot, CONF_P, txt):
    try:
        for admin_id in r_conf('admin_id', CONF_P):
            try:
                await bot.send_message(chat_id=int(admin_id), text=txt)
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
        logger.info(log_ % txt)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))


async def template_sender(CONF_P, EXTRA_D, MEDIA_D):
    # post_media_id = None
    post_media_options = None

    # 1
    post_txt = f'''
🍃 Через 1 час в 20:00 я проведу прямой эфир!

Подключайся и смотри все самые интересные моменты!

🍂 Не пропусти возможность!
Переходи по моей ссылке, встроенной в кнопку.
'''
    post_btn = '🎥 Прямой эфир в instagram'
    post_url = 'https://www.instagram.com'
    post_media_type = 'photo'
    post_media_name = os.path.join(MEDIA_D, (r_conf('logo_name', CONF_P))[0])
    post_pin = False
    tmp_date = datetime.now() + timedelta(days=3)
    post_time = datetime(tmp_date.year, tmp_date.month, tmp_date.day, hour=20, minute=0)
    await save_post_to_google_drive(CONF_P, EXTRA_D, post_txt, post_btn, post_url, post_media_name, post_media_type,
                                    post_pin, post_time, post_media_options)

    # 2
    post_txt = f'''
🔥 Как тебе прямой эфир? 
Расскажи об этом. 
Ниже я прикреплю Google-форму обратной связи

При заполнении, пришлю тебе Чек-лист по твоему запросу
'''
    post_btn = '⚠️ Google-форма обратной связи'
    post_url = 'https://docs.google.com/forms/d/e/1FAIpQLSehCkXuL9nCgRvPEdddgTnC99SMW-d_qTPzDjBzbASTAnX_lg/viewform'
    post_media_type = 'photo'
    post_media_name = os.path.join(MEDIA_D, (r_conf('logo_name', CONF_P))[0])
    post_pin = True
    tmp_date = datetime.now() + timedelta(days=4)
    post_time = datetime(tmp_date.year, tmp_date.month, tmp_date.day, hour=20, minute=0)
    await save_post_to_google_drive(CONF_P, EXTRA_D, post_txt, post_btn, post_url, post_media_name, post_media_type,
                                    post_pin, post_time, post_media_options)

    # 3
    post_txt = post_btn = post_url = post_pin = None
    post_media_name = os.path.join(MEDIA_D, (r_conf('logo_name', CONF_P))[0])
    post_media_type = 'video_note'
    tmp_date = datetime.now(timezone.utc) + timedelta(days=5)
    post_time = datetime(tmp_date.year, tmp_date.month, tmp_date.day, hour=20, minute=0)
    await save_post_to_google_drive(CONF_P, EXTRA_D, post_txt, post_btn, post_url, post_media_name, post_media_type,
                                    post_pin, post_time, post_media_options)


async def api_update_send_folder(CONF_P, EXTRA_D, INI_D):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(EXTRA_D, (r_conf('credential_file', CONF_P))[0]), r_conf('scopes', CONF_P))
    httpAuth = credentials.authorize(httplib2.Http())
    drive_service = build('drive', 'v3', http=httpAuth, cache_discovery=False)
    dynamic_folder_name = (r_conf('dynamic_folder_id', CONF_P))[0]
    file_list_dic = await api_get_file_list(drive_service, dynamic_folder_name, {})

    tmp = {}
    for k, v in file_list_dic.items():
        try:
            if v[1] == 'application/vnd.google-apps.folder':
                # google_folder.append(v[0])
                tmp[k] = v[0]  # google_key.append(v[2])
        except Exception as e:
            logger.info(log_ % str(e))
            await asyncio.sleep(round(random.uniform(1, 2), 2))

    tmp = dict(sorted(tmp.items(), key=lambda para: para[-1], reverse=False))
    google_folder = []
    google_key = []
    for k, v in tmp.items():
        google_key.append(k)
        google_folder.append(v)

    # google_folder.sort()
    w_conf('google_folder', google_folder, CONF_P, INI_D)
    w_conf('google_key', google_key, CONF_P, INI_D)
    logger.info(log_ % google_folder)


async def scheduled_hour(part_of_hour, CONF_P, EXTRA_D, INI_D):
    logger.info(log_ % 'scheduled_hour ok')
    # await templateSender()
    await api_update_send_folder(CONF_P, EXTRA_D, INI_D)
    await asyncio.sleep(part_of_hour + 200)
    while True:
        logger.info(log_ % f'start sending...{str(datetime.now())}')
        await api_update_send_folder(CONF_P, EXTRA_D, INI_D)
        await asyncio.sleep(one_hour - (datetime.now()).minute * 60 + 200)


async def read_likes(BASE_D, POST_ID=1):
    cnt = '⁰'
    try:
        sql = "SELECT USER_ID FROM \"LIKE\" WHERE POST_ID=$1"
        data_likes = await db_select_pg(sql, (POST_ID,), BASE_D)
        # print(f"{data_likes=}")
        cnt = str(0 + len(data_likes))
        cnt = cnt.replace('0', '⁰').replace('1', '¹').replace('2', '²').replace('3', '³').replace('4', '⁴').replace('5',
                                                                                                                    '⁵').replace(
            '6', '⁶').replace('7', '⁷').replace('8', '⁸').replace('9', '⁹')
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return cnt


async def db_has_like(user_id, post_id, BASE_D):
    data = True
    try:
        sql = "SELECT LIKE_ID FROM \"LIKE\" WHERE USER_ID=$1 AND POST_ID=$2"
        data = await db_select_pg(sql, (user_id, post_id,), BASE_D)
        data = True if data else False
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return data


def is_tid(item):
    result = False
    try:
        result = int(item)
    except Exception:
        # logger.info(log_ % str(e))
        pass
    finally:
        return result


async def create_replymarkup(bot, owner_id, chat_id, offer_id, OFFER_BUTTON, BASE_D, COLUMN_OWNER="OFFER_CHATTID"):
    result = InlineKeyboardBuilder()
    try:
        if OFFER_BUTTON is None or OFFER_BUTTON == '': return
        tmp = []
        dic_btns = await check_buttons(bot, None, OFFER_BUTTON)
        buttons = []
        offer_id = int(offer_id)
        for k, v in dic_btns.items():
            try:
                if v[0]:
                    sql = f"SELECT * FROM OFFER WHERE {COLUMN_OWNER}=$1"
                    data = await db_select_pg(sql, (owner_id,), BASE_D)
                    items = [item[0] for item in data]
                    view_post_id = items.index(offer_id) + 1 if offer_id else len(data)

                    if len(tmp) > 0 and tmp[-1] is None:
                        result.add(*buttons)
                        if 'ᴵ' in v[0]:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat='')]
                        elif str(v[1]).startswith('pst_'):
                            buttons = [types.InlineKeyboardButton(text=str(v[0]),
                                                                  callback_data=f"{v[1]}_{chat_id}_{view_post_id}")]
                        else:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), url=v[1])]
                    else:
                        if 'ᴵ' in v[0]:
                            buttons.append(
                                types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat=''))
                        elif str(v[1]).startswith('pst_'):
                            buttons.append(types.InlineKeyboardButton(text=str(v[0]),
                                                                      callback_data=f"{v[1]}_{chat_id}_{view_post_id}"))
                        else:
                            buttons.append(types.InlineKeyboardButton(text=str(v[0]), url=v[1]))
                tmp.append(v[0])
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
        if len(buttons) > 0:
            result.add(*buttons)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result.as_markup()


async def create_replymarkup_bot(ent_id, post_id, POST_BUTTONS, reply_markup, cur_, len_, counters=None, is_spo=False):
    if counters is None:
        counters = {}
    result = reply_markup
    try:
        if POST_BUTTONS is None or POST_BUTTONS == '': return
        tmp = []
        btn_ix = 0
        buttons = []
        post_id = int(post_id)
        dic_btns = await check_buttons2(POST_BUTTONS, False)

        for k, v in dic_btns.items():
            try:
                if v[0]:
                    if len(tmp) > 0 and tmp[-1] is None:
                        result.row(*buttons)
                        if 'ᴵ' in v[0]:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat='')]
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_{cur_}_{len_}_like"
                            if is_spo:
                                cb_ = f"pspoiler_{cb_}"
                                is_spo = not is_spo

                            buttons = [types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_)]
                            btn_ix += 1
                        else:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), url=v[1])]
                            btn_ix += 1
                    else:
                        if 'ᴵ' in v[0]:
                            buttons.append(
                                types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat=''))
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            # cb_ = f"pst_{post_id}_{btn_ix}"
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_{cur_}_{len_}_like"
                            if is_spo:
                                cb_ = f"pspoiler_{cb_}"
                                is_spo = not is_spo

                            buttons.append(types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_))
                            btn_ix += 1
                        else:
                            buttons.append(types.InlineKeyboardButton(text=str(v[0]), url=v[1]))
                            btn_ix += 1
                tmp.append(v[0])
            except Exception as e:
                logger.info(log_ % str(e))
                pass
        if len(buttons) > 0:
            result.row(*buttons)
    except Exception as e:
        logger.info(log_ % str(e))
        pass
    finally:
        return result


async def create_replymarkup4(ent_id, post_id, POST_BUTTONS, reply_markup, counters=None):
    if counters is None:
        counters = dict()
    result = reply_markup
    try:
        if POST_BUTTONS is None or POST_BUTTONS == '': return
        tmp = []
        btn_ix = 0
        buttons = []
        post_id = int(post_id)
        dic_btns = await check_buttons2(POST_BUTTONS, False)

        for k, v in dic_btns.items():
            try:
                if v[0]:
                    if len(tmp) > 0 and tmp[-1] is None:
                        result.row(*buttons)
                        if 'ᴵ' in v[0]:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat='')]
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_1_1_btn"

                            buttons = [types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_)]
                            btn_ix += 1
                        else:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), url=v[1])]
                            btn_ix += 1
                    else:
                        if 'ᴵ' in v[0]:
                            buttons.append(
                                types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat=''))
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_1_1_btn"

                            buttons.append(types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_))
                            btn_ix += 1
                        else:
                            buttons.append(types.InlineKeyboardButton(text=str(v[0]), url=v[1]))
                            btn_ix += 1
                tmp.append(v[0])
            except Exception as e:
                logger.info(log_ % str(e))
                pass
        if len(buttons) > 0:
            result.row(*buttons)
    except Exception as e:
        logger.info(log_ % str(e))
        pass
    finally:
        return result


async def create_replymarkup5(ent_id, post_id, POST_BUTTONS, reply_markup, counters=None, is_spo=False):
    if counters is None:
        counters = {}
    result = reply_markup
    try:
        if POST_BUTTONS is None or POST_BUTTONS == '': return
        tmp = []
        btn_ix = 0
        buttons = []
        post_id = int(post_id)
        dic_btns = await check_buttons2(POST_BUTTONS, False)

        for k, v in dic_btns.items():
            try:
                if v[0]:
                    if len(tmp) > 0 and tmp[-1] is None:
                        result.row(*buttons)
                        if 'ᴵ' in v[0]:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat='')]
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_1_1_btn"
                            if is_spo:
                                cb_ = f"pspoiler_{cb_}"
                                is_spo = not is_spo

                            buttons = [types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_)]
                            btn_ix += 1
                        else:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), url=v[1])]
                            btn_ix += 1
                    else:
                        if 'ᴵ' in v[0]:
                            buttons.append(
                                types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat=''))
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_1_1_btn"
                            if is_spo:
                                cb_ = f"pspoiler_{cb_}"
                                is_spo = not is_spo

                            buttons.append(types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_))
                            btn_ix += 1
                        else:
                            buttons.append(types.InlineKeyboardButton(text=str(v[0]), url=v[1]))
                            btn_ix += 1
                tmp.append(v[0])
            except Exception as e:
                logger.info(log_ % str(e))
                pass
        if len(buttons) > 0:
            result.row(*buttons)
    except Exception as e:
        logger.info(log_ % str(e))
        pass
    finally:
        return result


async def create_replymarkup6(ent_id, post_id, POST_BUTTONS, reply_markup, counters=None):
    if counters is None:
        counters = dict()
    result = reply_markup
    try:
        if POST_BUTTONS is None or POST_BUTTONS == '': return
        tmp = []
        btn_ix = 0
        buttons = []
        post_id = int(post_id)
        print(f"{POST_BUTTONS=}")

        # for item in POST_BUTTONS:

        dic_btns = await check_buttons2(POST_BUTTONS, False)
        for k, v in dic_btns.items():
            try:
                if v[0]:
                    if len(tmp) > 0 and tmp[-1] is None:
                        result.row(*buttons)
                        if 'ᴵ' in v[0]:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat='')]
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_1_1_btn"

                            buttons = [types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_)]
                            btn_ix += 1
                        else:
                            buttons = [types.InlineKeyboardButton(text=str(v[0]), url=v[1])]
                            btn_ix += 1
                    else:
                        if 'ᴵ' in v[0]:
                            buttons.append(
                                types.InlineKeyboardButton(text=str(v[0]), switch_inline_query_current_chat=''))
                            btn_ix += 1
                        elif str(v[1]).startswith("pst_"):
                            counter = '⁰' if btn_ix not in counters else await upper_register(counters[btn_ix])
                            cb_ = f"pst_{ent_id}_{post_id}_{btn_ix}_1_1_btn"

                            buttons.append(types.InlineKeyboardButton(text=f"{counter} {str(v[0])}", callback_data=cb_))
                            btn_ix += 1
                        else:
                            buttons.append(types.InlineKeyboardButton(text=str(v[0]), url=v[1]))
                            btn_ix += 1
                tmp.append(v[0])
            except Exception as e:
                logger.info(log_ % str(e))
                pass
        if len(buttons) > 0:
            result.row(*buttons)
    except Exception as e:
        logger.info(log_ % str(e))
        pass
    finally:
        return result


async def check_buttons(bot, chat_id, txt, is_counter=False):
    result = {}
    txt = txt.strip()
    try:
        start_ = []
        finish_ = []
        for ix in range(0, len(txt)):
            try:
                if txt[ix] == '[':
                    start_.append([ix, '['])
                elif txt[ix] == ']':
                    finish_.append([ix, ']'])
                elif txt[ix] == '\n':
                    start_.append([ix, '\n'])
                    finish_.append([ix, '\n'])
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))

        if len(start_) != len(finish_): return

        for ix in range(0, len(start_)):
            try:
                if start_[ix][-1] == '\n':
                    result[ix] = [None, None]
                else:
                    tmp = txt[start_[ix][0] + 1: finish_[ix][0]]
                    split_btn = tmp.strip().split('|')
                    if len(split_btn) > 1:
                        btn_name = split_btn[0].strip() if len(split_btn) > 1 else "🔗 Go"
                        btn_link = split_btn[-1].strip()
                        if not await is_url(btn_link):
                            await bot.send_message(chat_id, f"🔗 {btn_link}: invalid")
                            return
                    else:
                        btn_name = f"⁰{split_btn[0]}" if is_counter else split_btn[0]
                        # btn_link = cleanhtml(split_btn[0])[:20]
                        # btn_link = f"pst_{btn_link.encode('utf-8').hex()}"
                        btn_link = f"pst_"

                    result[ix] = [btn_name, btn_link]
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}", 95)
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


async def check_buttons2(txt, is_counter=False):
    result = {}
    try:
        if not txt: return
        txt = txt.strip()
        start_ = []
        finish_ = []
        for ix in range(0, len(txt)):
            try:
                if txt[ix] == '[':
                    start_.append([ix, '['])
                elif txt[ix] == ']':
                    finish_.append([ix, ']'])
                elif txt[ix] == '\n':
                    start_.append([ix, '\n'])
                    finish_.append([ix, '\n'])
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))

        if len(start_) != len(finish_): return

        for ix in range(0, len(start_)):
            try:
                if start_[ix][-1] == '\n':
                    result[ix] = [None, None]
                else:
                    tmp = txt[start_[ix][0] + 1: finish_[ix][0]]
                    split_btn = tmp.strip().split('|')
                    if len(split_btn) > 1:
                        btn_name = split_btn[0].strip() if len(split_btn) > 1 else "🔗 Go"
                        btn_link = split_btn[-1].strip()
                        if not await is_url(btn_link):
                            return
                    else:
                        btn_name = f"⁰{split_btn[0]}" if is_counter else split_btn[0]
                        btn_link = f"pst_"

                    result[ix] = [btn_name, btn_link]
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
    except TelegramRetryAfter as e:
        logger.info(log_ % f"TelegramRetryAfter {e.retry_after}", 95)
        await asyncio.sleep(e.retry_after + 1)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


def get_post_of_dict(dicti_, pos=1):
    tmp = 1
    for k, v in dicti_.items():
        if tmp == pos:
            return k, v
        tmp += 1
    return None, None


async def del_extra_files(UNKNOWN_ERRORS_TXT, EXTRA_D):
    try:
        if os.path.exists(UNKNOWN_ERRORS_TXT): os.remove(UNKNOWN_ERRORS_TXT)
        UNKNOWN_ERRORS_TXT2 = os.path.join(os.path.dirname(os.path.dirname(UNKNOWN_ERRORS_TXT)), 'unknown_errors.txt')
        if os.path.exists(UNKNOWN_ERRORS_TXT2): os.remove(UNKNOWN_ERRORS_TXT2)

        max_dt = datetime(2020, 1, 1, tzinfo=timezone.utc)
        arr = [it for it in os.listdir(EXTRA_D) if it.startswith('debug.') and it != 'debug.log']

        for item in arr:
            parts = item.split('.')
            if len(parts) <= 2: continue
            parts_dt = parts[1].split('_')
            cur_dt = datetime.strptime(f"{parts_dt[0]}_{parts_dt[1]}", '%Y-%m-%d_%H-%M-%S').replace(tzinfo=timezone.utc)

            if cur_dt > max_dt:
                max_dt = cur_dt

        for item in arr:
            file_item = os.path.join(EXTRA_D, item)
            parts = item.split('.')
            if len(parts) <= 2: continue
            parts_dt = parts[1].split('_')
            cur_dt = datetime.strptime(f"{parts_dt[0]}_{parts_dt[1]}", '%Y-%m-%d_%H-%M-%S').replace(tzinfo=timezone.utc)

            if cur_dt < max_dt and os.path.exists(file_item):
                os.remove(file_item)
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(0, 1), 2))


async def get_proxy(identifier, EXTRA_D, CONF_P, server=None):
    result = None
    try:
        if r_conf('proxy', CONF_P) == 0: return

        async with aiofiles.open(os.path.join(EXTRA_D, "proxy.txt"), "r") as f:
            lines = await f.readlines()
        random.shuffle(lines)

        for line in lines:
            try:
                hostname, port, username, password = line.strip().split('..')
                # logger.info(log_ % f"proxy ({identifier}): {hostname}")
                result = {"scheme": "socks5", "hostname": hostname, "port": int(port), "username": username,
                          "password": password}
                break
            except Exception as e:
                logger.info(log_ % str(e))
                await asyncio.sleep(round(random.uniform(1, 2), 2))
    except Exception as e:
        logger.info(log_ % f"{str(e)}, {identifier}, {server}")
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


def is_names(phrase):
    # (?s)\bhello\b.*?\b
    keywords = ['names', 'сотка', 'скорость', 'like', 'концентрат', 'aяз', 'чит-код', "сборная", 'ск-', 'капитан',
                'лагерь']
    for keyword in keywords:
        if keyword.lower() in phrase.lower():
            return True
    return False


async def haversine(lon1, lat1, lon2, lat2):
    result = None
    try:
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6372
        result = c * r * 1000.0
    except Exception as e:
        logger.info(log_ % str(e))
        await asyncio.sleep(round(random.uniform(1, 2), 2))
    finally:
        return result


# endregion


def main():
    pass


if __name__ == "__main__":
    main()
