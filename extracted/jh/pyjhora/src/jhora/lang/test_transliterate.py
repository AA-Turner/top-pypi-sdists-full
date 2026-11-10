import re, json, os
from aksharamukha import transliterate
import shutil, os

def safe_convert(convert_fn, path, script):
    bak = path + ".bak"
    if not os.path.exists(bak):          # keep the first backup only
        shutil.copy2(path, bak)
    src = bak                            # always convert from the Devanagari backup
    convert_fn(src, path, script)

DEVA = re.compile(r"[\u0900-\u097F\u200C\u200D]+")   # includes danda

def conv(text, script):
    return DEVA.sub(lambda m: transliterate.process("Devanagari", script, m.group(0)), text)

def convert_txt(src, dst, script):
    out = []
    for raw in open(src, encoding="utf-8-sig", newline="").read().splitlines(keepends=True):
        body = raw.rstrip("\r\n"); eol = raw[len(body):]
        if not body.strip() or body.lstrip().startswith("#") or "=" not in body:
            out.append(raw); continue
        k, v = body.split("=", 1)
        out.append(f"{k}={conv(v, script)}{eol}")
    open(dst, "w", encoding="utf-8", newline="").write("".join(out))

def convert_json(src, dst, script):
    def walk(x, depth=0):
        if isinstance(x, dict):
            return {(conv(k, script) if depth > 0 and "_" not in k and not k.strip().isdigit() and k.lower() != "source" else k):
                    (v if depth > 0 and k.lower() == "source" else walk(v, depth + 1)) for k, v in x.items()}
        if isinstance(x, list): return [walk(i, depth + 1) for i in x]
        if isinstance(x, str):  return conv(x, script)
        return x
    data = json.load(open(src, encoding="utf-8-sig"))
    json.dump(walk(data), open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

if __name__ == "__main__":
    from jhora import const
    files = ["amsa_rulers_mai.json", "prediction_msgs_mai.json", "yoga_msgs_mai.json", "dosha_msgs_mai.json",
             "raja_yoga_msgs_mai.json"]
    for file in files:
        print(f"Processing {file} ...")
        safe_convert(convert_json, const._LANGUAGE_PATH + file, "Tirhuta")
