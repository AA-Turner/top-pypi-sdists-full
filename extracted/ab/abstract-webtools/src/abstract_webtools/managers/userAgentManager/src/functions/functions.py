from ..imports import *
def classify_user_agents(user_agents):
    classified = {}

    for ua in user_agents:
        # Detect OS
        os = None
        if "Windows" in ua:
            os = "Windows"
        elif "Macintosh" in ua:
            os = "Macintosh"
        # ... Add other OS checks here

        # Detect browser and version
        browser = None
        version = None
        if "Chrome/" in ua:
            browser = "Chrome"
            version = re.search(r"Chrome/([\d.]+)", ua)
            version = version.group(1) if version else None
        elif "Firefox/" in ua:
            browser = "Firefox"
            version = re.search(r"Firefox/([\d.]+)", ua)
            version = version.group(1) if version else None
        # ... Add other browser checks here

        if os and browser and version:
            if os not in classified:
                classified[os] = {}
            if browser not in classified[os]:
                classified[os][browser] = {}
            classified[os][browser][version] = ua

    return classified
def randomChoice(db):
    if isinstance(db,dict):
        db = list(db.values())
    return random.choice(db)
def getRandomValues(db,key):
    return db.get(key) or randomChoice(db)
def pickUserAgentVars(val, options):
    if not val: return options[0]
    if val in options: return val
    l = val.lower()
    for o in options:
        if l in o.lower():
            return o
    return options[0]
