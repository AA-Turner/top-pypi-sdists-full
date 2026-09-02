from datetime import datetime
from pathlib import Path
from typing import Literal
from elevenlabs import stream as play_stream
from matrx_ai.providers.eleven_labs.client import get_elevenlabs_client
import asyncio
from matrx_utils import vcprint, clear_terminal

from matrx_ai._ext import get_ext

def _audio_dir() -> Path:
    """The host's audio temp dir, resolved LAZILY at first use.

    Reading ``get_ext("settings")`` at import time made this module
    un-importable on a standalone install (ExtNotConfiguredError before any
    capability was requested). The package must import cleanly with no host.
    """
    path = get_ext("settings").temp_dir / "audio"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _unique_audio_path(stem: str = "dialogue") -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return _audio_dir() / f"{stem}_{timestamp}.mp3"


def save_audio(audio_bytes: bytes, output_path: str | Path | None = None) -> Path:
    path = Path(output_path) if output_path else _unique_audio_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        f.write(audio_bytes)
    print(f"Saved {len(audio_bytes)} bytes to {path}")
    return path


MAX_CHARS = 4800  # stay safely under the 5000-char API limit


def _chunk_inputs(dialogue_inputs: list[dict]) -> list[list[dict]]:
    """Split dialogue turns into batches whose combined text stays under MAX_CHARS."""
    batches: list[list[dict]] = []
    current: list[dict] = []
    current_len = 0
    for turn in dialogue_inputs:
        turn_len = len(turn.get("text", ""))
        if current and current_len + turn_len > MAX_CHARS:
            batches.append(current)
            current = []
            current_len = 0
        current.append(turn)
        current_len += turn_len
    if current:
        batches.append(current)
    return batches


def _collect_stream(audio_stream) -> bytes:
    audio_bytes = b""
    for chunk in audio_stream:
        if isinstance(chunk, bytes):
            audio_bytes += chunk
    return audio_bytes


async def get_audio_bytes(dialogue_inputs: list[dict]) -> bytes:
    client = get_elevenlabs_client()
    batches = _chunk_inputs(dialogue_inputs)
    all_bytes = b""
    for i, batch in enumerate(batches):
        print(f"Requesting batch {i + 1}/{len(batches)} ({sum(len(t.get('text','')) for t in batch)} chars)")
        audio_stream = client.text_to_dialogue.stream(inputs=batch, model_id="eleven_v3")
        all_bytes += _collect_stream(audio_stream)
    return all_bytes


def stream_audio(dialogue_inputs: list[dict]) -> bytes:
    client = get_elevenlabs_client()
    batches = _chunk_inputs(dialogue_inputs)
    all_bytes = b""
    for i, batch in enumerate(batches):
        print(f"Streaming batch {i + 1}/{len(batches)} ({sum(len(t.get('text','')) for t in batch)} chars)")
        audio_stream = client.text_to_dialogue.stream(inputs=batch, model_id="eleven_v3")
        batch_bytes = b""

        def tee_stream(source):
            nonlocal batch_bytes
            for chunk in source:
                if isinstance(chunk, bytes):
                    batch_bytes += chunk
                    yield chunk

        play_stream(tee_stream(audio_stream))
        all_bytes += batch_bytes
    return all_bytes


async def main(play_type: Literal["real_time", "save_to_file"] = "save_to_file", dialogue_inputs: list[dict] = None) -> None:
    if play_type == "real_time":
        audio_bytes = stream_audio(dialogue_inputs)
        save_audio(audio_bytes)
    elif play_type == "save_to_file":
        audio_bytes = await get_audio_bytes(dialogue_inputs)
        save_audio(audio_bytes)


sample_dialogue_inputs = [
    {   # Clemens Hartmann 4 – Breaking News
        "text": "ده هزار خانه مسکونی ویران شده. صدها غیرنظامی کشته شدن.",
        "voice_id": "gnF5qCDI1EmWwqRYMHxn",
    },
    {   # Vidya – Famous News Personality
        "text": "و در همین حال، رئیس‌جمهور آمریکا در یک مصاحبه می‌گه شاید جزیره خارگ رو فقط برای تفریح بمباران کنیم.",
        "voice_id": "HSdLdxNgP1KF3yQK3IkB",
    },
    {   # JC – Energetic News Broadcaster
        "text": "امروز پانزده مارس دو هزار و بیست و شش است و ابعاد این جنگ داره از هر چیزی که تصور می‌کردیم وحشتناک‌تر می‌شه",
        "voice_id": "4XUsiqPDK4UACIM2BILe",
    },
    {   # Nazli – Formal and Assertive News Anchor
        "text": "لحن ترامپ واقعاً تکان‌دهنده‌ست، اما بیا اول روی واقعیت‌های میدانی تمرکز کنیم.",
        "voice_id": "I8PntRGWO35zIGM4lnWO",
    },
    {   # Walter – Serious News Anchor
        "text": "ما الان با یک کمپین نظامی بی‌سابقه روبه‌رو هستیم. آمریکا و اسرائیل تا الان بیش از پانزده هزار هدف رو در ایران زدن.",
        "voice_id": "9ZbFvrGBxO3uSmsw6wdI",
    },
    {   # Mira – Seasoned News Anchor
        "text": "استفاده از بمب‌افکن‌های استراتژیک بی-پنجاه‌ودو روی اصفهان و کشته شدن سرتیپ عبدالله جلالی‌نسب نشون می‌ده که هدف فقط تضعیف نیست،",
        "voice_id": "CaT0A6YBELRBgT6Qa2lH",
    },
    {   # Jonathan – News Anchor
        "text": "بلکه فلج کردنِ کاملِ سیستم فرماندهی نظامی ایرانه.",
        "voice_id": "QC3gSHMyKh8m20lGyUNZ",
    },
]

sample_2 = [
  {
    "text": "[excited] به پادکست امروز خوش اومدید. امروز یکشنبه، ۱۵ مارس ۲۰۲۶ است و خاورمیانه در یکی از ملتهب‌ترین روزهای تاریخ مدرن خودش قرار داره. من آرش هستم و امروز با تیم کامل اینجا جمع شدیم تا ابعاد این بحران رو باز کنیم. [short pause] سینا، سارا... لطفاً نقشه راه امروز رو به ما بدید. تیترها چیه؟",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[serious] تیتر اول: حملات گسترده آمریکا و اسرائیل با استفاده از بمب‌افکن‌های استراتژیک بی‌۵۲ به زیرساخت‌های نظامی ایران، به ویژه در اصفهان. حداقل ۱۵ نفر از جمله سرتیپ عبدالله جلالی‌نسب کشته شدند. مقامات ایران می‌گویند ۱۰ هزار خانه مسکونی تا امروز آسیب دیده، در حالی که پیت هگست، وزیر دفاع آمریکا، اعلام کرده بیش از ۱۵ هزار هدف تا الان منهدم شده.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[serious] تیتر دوم: سپاه پاسداران موج پنجاهم حملات تلافی‌جویانه خودش رو آغاز کرد. آژیرهای خطر در مرکز اسرائیل به صدا درآمده، و با وجود رهگیری پرتابه‌ها توسط امارات، عربستان و قطر، پایگاه هوایی احمد الجابر و فرودگاه بین‌المللی کویت هدف قرار گرفته و چند سرباز مجروح شدند.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[serious] تیتر سوم: عباس عراقچی، وزیر خارجه ایران، ادعا کرده آمریکا از پایگاه‌های امارات در دبی و راس‌الخیمه برای حمله به جزیره خارگ استفاده کرده. ایران تهدید کرده که تاسیسات غیرآمریکایی در امارات رو هدف قرار می‌ده.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[serious] و تیتر آخر: دونالد ترامپ پیشنهاد آتش‌بس ایران رو رد کرد و گفت شرایط هنوز به اندازه کافی خوب نیست. او همچنین گفت شاید فقط برای تفریح دوباره به خارگ حمله کنیم و از چین و ژاپن خواست برای بازگشایی تنگه هرمز یک ائتلاف دریایی تشکیل بدن.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[exhales sharply] ممنون از هر دو. خب... حجم اتفاقات واقعاً سرگیجه‌آوره. بیاید از تیتر اول شروع کنیم. ۱۵ هزار هدف منهدم شده و روزی هزار حمله هوایی. نیکا... تو همیشه روی هزینه‌های انسانی تاکید داری. نابودی ۱۰ هزار خانه مسکونی یعنی چی؟",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[angry] یعنی یک فاجعه مطلق آرش! این دیگه یک جنگ نقطه‌زن نیست. وقتی بی‌۵۲ وارد میدان می‌شه و ده‌ها هزار خونه ویران می‌شن، ما داریم درباره آوارگی صدها هزار انسان بی‌گناه، تعطیلی کامل مدارس و زندگی روزمره حرف می‌زنیم. این یک مجازات دسته‌جمعیه.",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[thoughtful] من درد و رنج غیرنظامیان رو انکار نمی‌کنم نیکا... [short pause] اما از زاویه عمل‌گرایانه، زیرساخت‌های نظامی داخل بافت شهری تنیده شدند. آمریکا داره روزی ده‌ها میلیون دلار فقط هزینه لجستیک این هزار حمله در روز می‌کنه تا توان موشکی رو فلج کنه.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[serious] و دقیقاً به همین دلیل سرتیپ جلالی‌نسب رو در اصفهان هدف قرار دادن. حذف رهبران ارشد نظامی، سیستم فرماندهی رو مختل می‌کنه. اما یک واقعیت تلخ وجود داره... تهران از این ویرانی‌ها برای تحریک احساسات ضدجنگ در داخل و مظلوم‌نمایی در سطح بین‌المللی استفاده می‌کنه.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[sarcastic] دقیقاً فرهاد. دولت ایران عاشق این آمارهاست. هرچی خونه بیشتر خراب بشه، بلندگوهای تبلیغاتی‌شون بلندتر می‌شه. در واقع، این ویرانی‌ها تنها کارت برنده‌ایه که برای خریدن همدردی جهانی براشون باقی مونده.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[appalled] سامان، چطور می‌تونی این‌قدر سرد درباره مرگ صدها نفر صحبت کنی؟ اینها عدد نیستن، انسان‌هایی هستن که زیر بمباران گیر افتادن و هیچ سودی از این جنگ نمی‌برن!",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[calm] من سرد نیستم نیکا، من دارم منطقِ بی‌رحمانهٔ قدرت رو تحلیل می‌کنم. احساسات، استراتژی نظامی رو تغییر نمی‌ده.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[clears throat] بسیار خب، بیاید روی همین استراتژی تمرکز کنیم. ایران موج پنجاهم حملاتش رو آغاز کرده. سینا، سارا... جزئیات برخوردها در خلیج فارس چی بود؟",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[serious] سیستم‌های دفاعی امارات، عربستان و قطر پرتابه‌ها رو رهگیری کردن. اما در کویت، موشک‌ها از سیستم عبور کردن و رادارهای پایگاه احمد الجابر آسیب دیدند.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[serious] و باید اضافه کنم که امارات رسماً ادعای عراقچی مبنی بر استفاده آمریکا از حریم هوایی و پایگاه‌های دبی و راس‌الخیمه رو تکذیب کرده.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[thoughtful] این یک بازی خطرناکه. ایران با کشوندن همسایگان خلیج فارس به وسط درگیری، داره پیام می‌ده که اگر ما بسوزیم، کل منطقه می‌سوزه. این یعنی گسترش عامدانهٔ میدان جنگ.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[curious] ولی از نظر نظامی هوشمندانه‌ست! ایران داره با پهپادهای ارزون‌قیمت، اسرائیل و کشورهای عربی رو مجبور می‌کنه موشک‌های رهگیر چند میلیون دلاری رو مصرف کنن. این یک جنگ فرسایشیه.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[annoyed] هوشمندانه؟ سامان، تهدید کردن بنادر امارات و دبی یعنی بازی با اقتصاد جهانی. این کار باعث فرار فوری سرمایه می‌شه. امارات الان در لبه تیغ حرکت می‌کنه... هم باید شراکتش رو با آمریکا حفظ کنه، هم مراقب باشه زیرساخت‌های حیاتی‌ش نابود نشن.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[serious] درسته تارا. اما این فشار روی آمریکا هم هست. اگر کویت تلفات بده و امارات احساس ناامنی کنه، ممکنه آزادی عمل نظامی آمریکا رو محدود کنن تا از خودشون محافظت کنن.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[sighs] و این ما رو می‌رسونه به شوکه‌کننده‌ترین بخش اخبار امروز. مصاحبه ترامپ. سارا، دقیقاً چی گفت؟",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[serious] رئیس‌جمهور ترامپ گفت که طرح صلح پیشنهادی ایران رو رد کرده چون به گفته او شرایط هنوز به اندازه کافی خوب نیست. او اضافه کرد که شاید فقط برای تفریح دوباره به جزیره خارگ حمله کنند.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[angry] فقط برای تفریح؟! —",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[serious] و همچنین از چین و ژاپن خواست که برای بازگشایی تنگه هرمز، یک ائتلاف دریایی تشکیل دهند.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[angry] ممنون سینا! همونطور که می‌گفتم... فقط برای تفریح؟! این ادبیات یک رهبر جهانیه؟ مردم دارن می‌میرن، یک پنجم نفت جهان متوقف شده، و او این رو مثل یک برنامه ריאلیتی‌شو می‌بینه! این لحن تمام متحدان آمریکا رو منزجر می‌کنه.",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[laughs] نیکا، به عصر بازدارندگی مدرن خوش اومدی. این ادبیات ممکنه زمخت باشه، اما غیرقابل پیش‌بینی بودن، خودش یک سلاحه. ترامپ داره به تهران می‌گه هیچ خط قرمزی وجود نداره.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[sighs] مشکل اینه که این رویکرد، هزینه‌های آمریکا رو بالا می‌بره. رد کردن آتش‌بس یعنی طولانی‌تر شدن جنگی که روزانه میلیاردها دلار خرج داره. و درخواست از چین و ژاپن؟ این یک کابوس دیپلماتیکه.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[thoughtful] تارا دقیقاً دست گذاشت روی نقطه اصلی. چین و ژاپن به شدت به نفت تنگه هرمز وابسته‌اند. ترامپ عملاً داره به پکن و توکیو می‌گه: نفت شماست، دردسر شماست. بیاید خودتون ناوگانتون رو اسکورت کنید.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[serious] ولی آیا ژاپن حاضره کشتی‌های نظامی‌ش رو در خط مستقیم آتش قرار بده؟ ورود ائتلاف دریایی جدید یعنی یک جرقه بزرگ‌تر در تنگه هرمز.",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[curious] دقیقاً! و اینجاست که بازی شطرنج پیچیده می‌شه. اگر چین وارد بشه، آیا با ایران درگیر می‌شه یا به عنوان میانجی عمل می‌کنه؟ ترامپ داره با یک بلوف بزرگ، بارِ تامین امنیت انرژی رو از دوش آمریکا برمی‌داره.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[short pause] چیزی که مشخصه اینه که هیچ‌کس در این معادله برنده نیست. خاورمیانه در حال تبدیل شدن به یک زمین سوخته است، و هر روزی که آتش‌بس به تاخیر می‌افته، بازگشت به شرایط عادی ناممکن‌تر می‌شه.",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[thoughtful] موافقم. اقتصاد منطقه داره تاوان سنگینی می‌ده و هر موشکی که شلیک می‌شه، سال‌ها توسعه رو به عقب میندازه. این هزینه واقعی جنگه.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[exhales sharply] مکالمه فوق‌العاده‌ای بود. از اصفهان تا کویت، و از واشنگتن تا پکن... امواج این جنگ داره تمام دنیا رو در بر می‌گیره. آیا دیپلماسی در نهایت پیروز می‌شه یا منافع اقتصادی در تنگه هرمز مسیر جنگ رو تغییر می‌ده؟ ما اینجا هستیم تا هر روز این تحولات رو برای شما موشکافی کنیم. ممنون که به ما گوش دادید.",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  }
]

english_sample =   [
    {
    "text": "[excited] Welcome to the podcast. Today is Sunday, March 15, 2026, and the Middle East is facing one of the most volatile days in its modern history. I am Aaron, and we have the full panel here today to unpack every angle of this crisis. [short pause] Samuel, Sarah... please give us the roadmap. What are the headlines?",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[serious] Headline one. The US and Israel conducted extensive airstrikes utilizing B-52 strategic bombers against Iranian military infrastructure, heavily targeting Isfahan. At least fifteen people were killed, including senior military figure Brigadier-General Abdullah Jalali Nasab. Iranian authorities report up to ten thousand residential homes have been damaged or destroyed since the conflict began, while US Defense Secretary Pete Hegseth claims over fifteen thousand targets have been struck overall.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[serious] Headline two. The Islamic Revolutionary Guard Corps launched its fiftieth wave of retaliatory strikes against Israel and Gulf nations. Sirens sounded in central Israel, and while the UAE, Saudi Arabia, and Qatar intercepted multiple projectiles, strikes successfully hit Kuwait's Ahmad al-Jaber airbase and international airport, wounding soldiers and damaging radar systems.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[serious] Headline three. Iranian Foreign Minister Abbas Araghchi claimed the US utilized bases in the UAE, specifically near Ras Al-Khaimah and Dubai, to launch strikes against the Kharg Island oil terminal. Iran has threatened to target non-US civilian ports and assets in the UAE in retaliation.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[serious] And the final headline. President Donald Trump rejected an Iranian ceasefire proposal, stating the terms quote aren't good enough yet. He suggested the US might strike Kharg Island again quote just for fun, and called on allies including China and Japan to form a naval coalition to force open the Strait of Hormuz.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[exhales sharply] Thank you both. Alright... the sheer scale of these developments is dizzying. Let us start with that first headline. Fifteen thousand targets destroyed and over a thousand strikes a day. Natalie... you always focus on the human cost. What does the destruction of ten thousand residential homes actually look like?",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[angry] It looks like an absolute catastrophe, Aaron! This is not a surgical operation anymore. When you bring B-52s into the theater and ten thousand homes are leveled, we are talking about massive displacement. Schools are entirely virtual, daily life is completely paralyzed. Hundreds of civilians have died. It is collective punishment.",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[thoughtful] I am not denying the civilian suffering, Natalie... [short pause] But from a purely pragmatic standpoint, military infrastructure is deeply embedded in these urban areas. The US is facing enormous financial and logistical costs executing a thousand strikes a day just to degrade these missile systems.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[serious] And that is exactly why they targeted Brigadier-General Jalali Nasab in Isfahan. Taking out top-tier military leadership completely disrupts their command and control. But there is a harsh geopolitical reality here... Tehran is going to leverage every single one of those civilian casualties to rally anti-war sentiment domestically and internationally.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[sarcastic] Exactly, Frank. The Iranian government thrives on those statistics. The more homes that get destroyed, the louder their propaganda megaphones get. Frankly, that destruction is the only card they have left to buy any global sympathy.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[appalled] Sean, how can you be so incredibly cold about the deaths of hundreds of people? These are not numbers or propaganda cards! They are human beings trapped under bombardment with absolutely nothing to gain from this war!",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[calm] I am not being cold, Natalie, I am analyzing the brutal logic of power. Emotional outrage does not change military strategy.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[clears throat] Alright, let us pivot to that exact military strategy. Iran just launched its fiftieth wave of strikes. Samuel, Sarah... what were the specific fallout details in the Gulf?",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[serious] Defense systems in the UAE, Saudi Arabia, and Qatar successfully intercepted incoming projectiles. However, in Kuwait, missiles bypassed the screens, hitting the Ahmad al-Jaber airbase and causing direct casualties among soldiers.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[serious] I should also add that the UAE has firmly denied any involvement in the US strikes on Kharg Island, directly contradicting Foreign Minister Araghchi's claims.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[thoughtful] This is an incredibly dangerous game of escalation. By dragging neighboring Gulf states into the crossfire, Iran is signaling that if they burn, the whole region burns with them. It is a deliberate expansion of the theater.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[curious] But militarily, it is pretty smart! Iran is rapidly depleting its own stockpiles, sure, but they are forcing Israel and Gulf nations to expend highly expensive interceptor missiles. It projects strength and drains their adversaries.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[annoyed] Smart? Sean, threatening civilian ports in the UAE and major global hubs like Dubai means playing with the global economy. It causes immediate capital flight. The UAE is walking a tightrope right now... trying to remain an indispensable US partner while avoiding the physical destruction of their own infrastructure.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[serious] Taylor is right. And this puts immense diplomatic pressure on the United States. If Kuwait is taking casualties and the UAE feels unsafe, these regional allies might restrict US operational freedom and airspace just to protect their own territories.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[sighs] Which brings us to perhaps the most shocking part of today's news cycle. The President's interview. Sarah, what were his exact words again?",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[serious] President Trump stated he rejected Iran's peace plan because quote the terms aren't good enough yet. He then added that the US might strike Kharg Island again quote just for fun.",
    "voice_id": "HSdLdxNgP1KF3yQK3IkB"
  },
  {
    "text": "[angry] Just for fun?! —",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[serious] He also called on international allies, specifically mentioning China and Japan, to form a naval coalition to reopen the Strait of Hormuz.",
    "voice_id": "gnF5qCDI1EmWwqRYMHxn"
  },
  {
    "text": "[angry] Thank you, Samuel! As I was saying... JUST FOR FUN?! Is this how a world leader speaks? People are dying, a fifth of the world's traded oil is paralyzed, and he treats this like a reality TV show! That dismissive rhetoric completely alienates the international community.",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[laughs] Natalie, welcome to modern deterrence. The rhetoric might be crass, but sheer unpredictability is a weapon itself. Trump is signaling to Tehran that there are absolutely zero red lines left.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[sighs] The problem is that this approach prolongs the financial drain on the US. Rejecting a ceasefire keeps the meter running. And asking China and Japan to step in? That is a massive diplomatic gamble.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[thoughtful] Taylor hits the nail on the head. China and Japan are heavily reliant on the Strait of Hormuz. Trump is essentially telling Beijing and Tokyo... it is your oil, so it is your problem. Come secure it yourselves.",
    "voice_id": "9ZbFvrGBxO3uSmsw6wdI"
  },
  {
    "text": "[serious] But is Japan really willing to put its naval vessels in the direct line of fire? Joining an escort coalition requires an incredibly high bar of military commitment.",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  },
  {
    "text": "[curious] Exactly! And that is where the geopolitical chess gets fascinating. If China brings its navy in, do they actually engage Iran, or do they force a mediation? Trump is trying to shift the burden of global energy transit onto a broader group of nations.",
    "voice_id": "QC3gSHMyKh8m20lGyUNZ"
  },
  {
    "text": "[short pause] What is undeniably clear is that nobody is winning this equation. The Middle East is turning into scorched earth, and every day a ceasefire is rejected, a return to normalcy becomes more impossible.",
    "voice_id": "CaT0A6YBELRBgT6Qa2lH"
  },
  {
    "text": "[thoughtful] Agreed. The regional economy is taking devastating damage. Every missile fired sets development back by years. That is the true long-term cost.",
    "voice_id": "I8PntRGWO35zIGM4lnWO"
  },
  {
    "text": "[exhales sharply] Incredible conversation today. From Isfahan to Kuwait, and from Washington to Beijing... the ripples of this conflict are touching every corner of the globe. Will diplomacy finally break through, or will the economic chokehold in the Strait of Hormuz dictate the path of this war? We will be here to analyze it all. Thanks for listening.",
    "voice_id": "4XUsiqPDK4UACIM2BILe"
  }
]


if __name__ == "__main__":
    clear_terminal()
    asyncio.run(main(play_type="real_time", dialogue_inputs=english_sample))
