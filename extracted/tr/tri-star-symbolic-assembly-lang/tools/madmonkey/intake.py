from tools.crawler.madmonkey_crawler import crawl_and_inject_to_madmonkey


def dispatch_chaos(seed="src/tsal"):
    results = crawl_and_inject_to_madmonkey(seed)
    with open("memory/madmonkey_intake.log", "w") as log:
        for file, result in results:
            log.write(f"{file} → {result}\n")
    print(f"✅ Dispatched {len(results)} chaos entries to MadMonkey.")
