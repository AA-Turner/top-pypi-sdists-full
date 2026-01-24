from .imports import *
logger = logging.getLogger("FlanManager")

class FlanManager(BaseModelManager):
    """
    Managed interface for google/flan-t5-xl (text2text generation).
    Loads once per process, reuses shared TorchEnvManager context.
    """

    def __init__(self, model_dir=None, use_quantization=None):
        # BaseModelManager handles singleton setup and environment resolution
        super().__init__(modrl_name="flan", model_dir=model_dir, use_quantization=use_quantization)
        self.lock = threading.Lock()
    # ------------------------------------------------------------------
    # Model + tokenizer loading (overrides BaseModelManager)
    # ------------------------------------------------------------------
    def _load_model_and_tokenizer(self):
        AutoTokenizer = get_AutoTokenizer()
        AutoModelForSeq2SeqLM = get_AutoModelForSeq2SeqLM()

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_dir).to(self.device)

        logger.info(f"Flan model loaded on {self.device} ({self.torch_dtype})")


    # ------------------------------------------------------------------
    # Custom summarization wrapper
    # ------------------------------------------------------------------
    def summarize(
        self,
        text: str,
        max_chunk: int = None,
        min_length: int = None,
        max_length: int = None,
        do_sample: bool = False,
    ) -> str:
        
        if not self.pipeline:
            self._safe_preload()
        max_chunk = zero_or_default(max_chunk,default=512)
        if not max_length and not min_length:
            min_length = zero_or_default(min_length,default=100)
            max_length = zero_or_default(max_length,default=512)
        elif not is_number(max_length) and is_number(min_length):
            max_length = int(min_length*(512/100))
        elif is_number(max_length) and not is_number(min_length):
            min_length = int(max_length*(100/512))
        elif is_number(max_length) and is_number(min_length) and max_length < min_length:
            min_length = int(max_length*(100/512))
        prompt = (
            "You are a highly observant assistant tasked with summarizing long, unscripted video monologues.\n\n"
            f"TEXT:\n{text}\n\n"
            "INSTRUCTIONS:\n"
            "Summarize the speaker’s core points and tone as if describing the monologue "
            "to someone who hasn’t heard it. Group related ideas together. Highlight interesting "
            "or unusual claims. Use descriptive language. Output a full narrative paragraph (or two), not bullet points."
        )

        result = self.pipeline(
            prompt,
            max_length=max_length,
            min_length=min_length,
            do_sample=do_sample,
            num_return_sequences=1,
        )[0]["generated_text"]

        return result.strip()

    # ------------------------------------------------------------------
    # Generate concise document title (PDF or raw text)
    # ------------------------------------------------------------------
    def generate_title(self, source: str | Path, from_pdf: bool = True, max_chars: int = 1200) -> str:
        """
        Generate a short, meaningful title (5–12 words) for text or PDF content.
        Uses the same Flan pipeline already loaded in this manager.
        """
        if not self.pipeline:
            self._safe_preload()

        # --- extract text ---
        if from_pdf:
            pdf_path = Path(source)
            text = ""
            try:
                with fitz.open(pdf_path) as doc:
                    for page in doc[:2]:
                        text += page.get_text("text") + "\n"
                        if len(text) > max_chars:
                            break
            except Exception as e:
                logger.error(f"PDF read failed for {pdf_path}: {e}")
                text = str(pdf_path.stem)
        else:
            text = str(source)

        text = text.strip()[:max_chars]

        # --- build title prompt ---
        prompt = (
            "You are a precise titler. "
            "Generate a clear, original, and informative title (5–12 words, no punctuation at the end) "
            "for the following document excerpt:\n\n"
            f"{text}\n\nTitle:"
        )

        # --- generate ---
        result = self.pipeline(
            prompt,
            max_length=24,
            min_length=5,
            do_sample=False,
            num_return_sequences=1,
        )[0]["generated_text"]

        # --- postprocess ---
        title = re.sub(r"^Title[:\- ]+", "", result.strip(), flags=re.I)
        title = re.sub(r"\s+", " ", title).strip(" -:;,.")
        title = title.title()

        # fallback: if it's empty or looks like the first line repeated
        if not title or title.lower() in text.lower()[:120]:
            title = text.split("\n")[0].strip().title()

        logger.info(f"Generated title: {title}")
        return title


    def get_flan_summary(
        self,
        text: str,
        max_chunk: int = None,
        min_length: int = None,
        max_length: int = None,
        do_sample: bool = None
    ) -> str:
        prompt = f"""
You are a highly observant assistant tasked with summarizing long, unscripted video monologues.

TEXT:
{text}

INSTRUCTIONS:
Summarize the speaker’s core points and tone as if describing the monologue to someone who hasn’t heard it.
Group related ideas together. Highlight interesting or unusual claims. Use descriptive language.
Output a full narrative paragraph (or two), not bullet points.
"""

        do_sample = do_sample or False
        return self.summarizer(prompt,
                          max_length=max_length,
                          min_length=min_length,
                          do_sample=do_sample)[0]['generated_text']
