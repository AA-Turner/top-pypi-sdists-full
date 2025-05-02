from .functions import (extract_text_from_image,
                        logger,
                        Counter,
                        spacy,
                        kw_model,
                        summarizer,
                        LEDTokenizer,
                        LEDForConditionalGeneration)
nlp = spacy.load("en_core_web_sm")
def generate_with_bigbird(text: str, task: str = "title", model_dir: str = "allenai/led-base-16384") -> str:
    try:
        tokenizer = LEDTokenizer.from_pretrained(model_dir)
        model = LEDForConditionalGeneration.from_pretrained(model_dir)
        prompt = (
            f"Generate a concise, SEO-optimized {task} for the following content: {text[:1000]}"
            if task in ["title", "caption", "description"]
            else f"Summarize the following content into a 100-150 word SEO-optimized abstract: {text[:4000]}"
        )
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(
            inputs["input_ids"],
            max_length=200 if task in ["title", "caption"] else 300,
            num_beams=5,
            early_stopping=True
        )
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error in BigBird processing: {e}")
        return ""
def generate_media_url(fs_path: str,domain=None,repository_dir=None) -> str | None:
    fs_path = os.path.abspath(fs_path)
    if not fs_path.startswith(repository_dir):
        return None
    rel_path = fs_path[len(repository_dir):]
    rel_path = quote(rel_path.replace(os.sep, '/'))
    ext = os.path.splitext(fs_path)[1].lower()
    prefix = EXT_TO_PREFIX.get(ext, 'repository')
    return f"{domain}/{prefix}/{rel_path}"
def get_keybert(full_text,
                keyphrase_ngram_range=None,
                top_n=None,
                stop_words=None,
                use_mmr=None,
                diversity=None):
    keyphrase_ngram_range = keyphrase_ngram_range or (1,3),
    top_n = top_n or 10,
    stop_words = stop_words or "english",
    use_mmr = use_mmr or True,
    diversity = diversity or 0.5
    keybert = kw_model.extract_keywords(
        full_text,
        keyphrase_ngram_range=keyphrase_ngram_range,
        stop_words=stop_words,
        top_n=top_n,
        use_mmr=use_mmr,
        diversity=diversity
    )
    return keybert
def extract_keywords_nlp(text, top_n=10):
    if not isinstance(text,str):
        logger.info(f"this is not a string: {text}")
    doc = nlp(str(text))
    word_counts = Counter(token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2)
    entity_counts = Counter(ent.text.lower() for ent in doc.ents if len(ent.text.split()) > 1)
    top_keywords = [word for word, _ in (word_counts + entity_counts).most_common(top_n)]
    return top_keywords

def refine_keywords(keywords,
                    full_text,
                     keyphrase_ngram_range=None,
                     top_n=None,
                     stop_words=None,
                     use_mmr=None,
                     diversity=None,
                    info_data={}):
    info_data['keywords'] =  keywords or extract_keywords_nlp(full_text, top_n=top_n)
    keybert = get_keybert(full_text,
                keyphrase_ngram_range=keyphrase_ngram_range,
                top_n=top_n,
                stop_words=stop_words,
                use_mmr=use_mmr,
                diversity=diversity)
    info_data['combined_keywords'] = list({kw for kw,_ in keybert} | set(info_data['keywords']))[:10]
    info_data['keyword_density'] = calculate_keyword_density(full_text, info_data['combined_keywords'])
    return info_data
def calculate_keyword_density(text, keywords):
    words = text.lower().split()
    return {kw: (words.count(kw.lower()) / len(words)) * 100 for kw in keywords if len(words) > 0}

def chunk_summaries(chunks,
                    max_length=None,
                    min_length=None,
                    truncation=False):

    max_length = max_length or 160
    min_length = min_length or 40
    summaries = []
    for idx, chunk in enumerate(chunks):
       
            out = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                truncation=truncation  # >>> explicitly drop over‑long parts if still above model limit
            )
            summaries.append(out[0]["summary_text"])
   
    return summaries

def split_to_chunk(full_text,max_words=None):
    # split into sentence-ish bits
    max_words = max_words or 300
    sentences = text.split(". ")
    chunks, buf = [], ""
    for sent in sentences:
        # +1 for the “. ” we removed
        if len((buf + sent).split()) <= max_words:
            buf += sent + ". "
        else:
            chunks.append(buf.strip())
            buf = sent + ". "
    if buf:
        chunks.append(buf.strip())
    return chunks
def get_summary(full_text,
                keywords=None,
                info_data={},
                max_words=None,
                max_length=None,
                min_length=None,
                truncation=False):
    info_data["summary"] = None
    if full_text and summarizer:
        chunks = split_to_chunk(full_text,max_words=max_words)
        summaries = chunk_summaries(chunks,
                        max_length=max_length,
                        min_length=min_length,
                        truncation=truncation)
        # stitch back together
        info_data["summary"] = " ".join(summaries).strip()

    return info_data


