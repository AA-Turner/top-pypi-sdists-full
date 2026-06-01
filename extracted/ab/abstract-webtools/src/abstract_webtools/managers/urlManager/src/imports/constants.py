from .imports import *
import re
load()  # load once
DEFINITIION_ALIAS = {
    "text":{"alias":["text","post","content","tweet","thread","body"],"description":"The main text."},
    "url":{"alias":["url","u","link","site","domain","intentUrl","link_address","address","canonical",'path'],"description":"A URL to include in the post."},
    "via":{"alias":["via","username","user","@","uploader","author"],"description":"A username to attribute the post to."},
    "hashtags":{"alias":["hashtags","hashtag","tag","tags"],"description":"Comma-separated hashtags (without the # symbol)."},
    "related":{"alias":["related","contributor","credit","cc","bcc"],"description":"Comma-separated related accounts."},
    "subject":{"alias":["title","subject","heading","header"],"description":"The email subject."},
    "body":{"alias":["text","post","content","tweet","thread","body"],"description":"The email body."},
    "cc":{"alias":["related","contributor","credit","cc","bcc"],"description":"Additional email addresses."},
    "bcc":{"alias":["related","contributor","credit","cc","bcc"],"description":"Additional email addresses."}
}
def get_alias_params(string):
    return DEFINITIION_ALIAS.get(string)
SOCIAL_SHARE_PARAMS={
    "x":{
        "url":"https://twitter.com/intent/tweet",
        "params":{
            "text":get_alias_params("text"),
            "url":get_alias_params("url"),
            "via":get_alias_params("via"),
            "hashtags":get_alias_params("hashtags"),
            "related":get_alias_params("related")
            },
        "characters":{"limit":280,"optimal":100,"mobile_cutoff":150,"url_len":30},
        "alias":["x","twitter","x.com","tweet","twitter.com"],
        "hash_symbol":False
        },
     "facebook":{
         "url":"http://facebook.com/sharer.php",
         "params":{
             "u":get_alias_params("url")
             },
         "characters":{"limit":63206,"optimal":50,"mobile_cutoff":150,"url_len":None},
         "alias":["facebook","fb","facebook.com","meta","meta.com"],
         "hash_symbol":True
         },
    
     "threads":{
         "url":"https://www.threads.net/intent/post",
         "params":{
             "text":get_alias_params("text")
             },
         "characters":{"limit":500,"optimal":150,"mobile_cutoff":150,"url_len":None},
         "alias":["threads","@","threads.com","@.com"],
         "hash_symbol":True
         },
    "mailto":{
        "url":"mailto:",
        "params":{
             "subject":get_alias_params("subject"),
             "body":get_alias_params("body"),
             "cc":get_alias_params("cc"),
             "bcc":get_alias_params("bcc")
             },
        "characters":{"limit":None,"optimal":None,"mobile_cutoff":None},
        "alias":["mailto","mail","email","email.com","mail.com"],
        "hash_symbol":True
        },
    "minds":{
        "url":"https://www.minds.com/newsfeed/subscriptions/latest",
        "params":{
            "intentUrl":get_alias_params("url")
            },
        "characters":{"limit":500,"optimal":125,"mobile_cutoff":150,"url_len":None},
        "alias":["minds","mindscollective","collective"],
        "hash_symbol":True
        }
             
    }

META_VARS = {
    "title": {"min": [20, 30], "max": [50,60]},
    "description": {"min": [70, 100], "max": [150, 160]},
    "alt": {"min": [10, 20], "max": [100, 125]},
    "context": {"min": [20, 30], "max": [70, 100]},
    "keywords": {"min": [10, 20], "max": [200, 250]}
}
ATTR_RE = re.compile(r'([a-zA-Z0-9:_-]+)\s*=\s*([\'"`])([^\'"`]+)\2')
TAG_OPEN_RE = re.compile(r'<\s*([a-zA-Z0-9:_-]+)')
TAG_CONTENT_RE = re.compile(r'<\s*([a-zA-Z0-9:_-]+)[^>]*>(.*?)</\s*\1\s*>', re.DOTALL)

EXTENTIONS=['.ac', '.academy', '.accountant', '.actor', '.agency', '.ai', '.airforce', '.am',
            '.apartments', '.archi', '.army', '.art', '.asia', '.associates', '.at', '.attorney',
            '.auction', '.audio', '.baby', '.band', '.bar', '.bargains', '.be', '.beer', '.berlin',
            '.best', '.bet', '.bid', '.bike', '.bingo', '.bio', '.biz', '.black', '.blackfriday',
            '.blog', '.blue', '.boston', '.boutique', '.br.com', '.build', '.builders', '.business',
            '.buzz', '.buz', '.ca', '.cab', '.cafe', '.camera', '.camp', '.capital', '.cards', '.care',
            '.careers', '.casa', '.cash', '.casino', '.catering', '.cc', '.center', '.ceo', '.ch', '.charity',
            '.chat', '.cheap', '.christmas', '.church', '.city', '.claims', '.cleaning', '.click', '.clinic',
            '.clothing', '.cloud', '.club', '.cn.com', '.co', '.co.com', '.co.in', '.co.nz', '.co.uk', '.coach',
            '.codes', '.coffee', '.college', '.com', '.com.co', '.com.mx', '.com.tw', '.community', '.company',
            '.computer', '.condos', '.construction', '.consulting', '.contact', '.contractors', '.cooking',
            '.cool', '.coupons', '.courses', '.credit', '.creditcard', '.cricket', '.cruises', '.cymru',
            '.cz', '.dance', '.date', '.dating', '.de', '.de.com', '.deals', '.degree', '.delivery',
            '.democrat', '.dental', '.dentist', '.desi', '.design', '.diamonds', '.diet', '.digital',
            '.direct', '.directory', '.discount', '.doctor', '.dog', '.domains', '.download', '.earth',
            '.eco', '.education', '.email', '.energy', '.engineer', '.engineering', '.enterprises',
            '.equipment', '.estate', '.eu', '.eu.com', '.events', '.exchange', '.expert', '.exposed',
            '.express', '.fail', '.faith', '.family', '.fans', '.farm', '.fashion', '.film', '.finance',
            '.financial', '.fish', '.fishing', '.fit', '.fitness', '.flights', '.florist', '.flowers', '.fm',
            '.football', '.forsale', '.foundation', '.fun', '.fund', '.furniture', '.futbol', '.fyi', '.gallery',
            '.games', '.garden', '.gay', '.gift', '.gifts', '.gives', '.glass', '.global', '.gmbh', '.gold',
            '.golf', '.graphics', '.gratis', '.green', '.gripe', '.group', '.gs', '.guide', '.guitars', '.guru',
            '.haus', '.healthcare', '.help', '.hiphop', '.hn', '.hockey', '.holdings', '.holiday', '.horse',
            '.host', '.hosting', '.house', '.how', '.immo', '.in', '.industries', '.info', '.ink', '.institue',
            '.insure', '.international', '.investments', '.io', '.irish', '.it', '.jetzt', '.jewelry', '.jp',
            '.jpn.com', '.juegos', '.kaufen', '.kim', '.kitchen', '.kiwi', '.la', '.land', '.lawyer', '.lease',
            '.legal', '.lgbt', '.li', '.life', '.lighting', '.limited', '.limo', '.link', '.live', '.llc', '.loan',
            '.loans', '.lol', '.london', '.love', '.ltd', '.luxury ', '.maison', '.managment', '.market', '.marketing',
            '.mba', '.me', '.me.uk', '.media', '.memorial', '.men', '.menu', '.miami', '.mobi', '.moda', '.moe', '.money',
            '.monster', '.mortgage', '.mx', '.nagoya', '.navy', '.net', '.net.co', '.network', '.news', '.ngo', '.ninja',
            '.nl', '.nyc', '.okinawa', '.one', '.ong', '.online', '.org', '.org.in', '.org.uk', '.partners', '.parts',
            '.party', '.pet', '.ph', '.photo', '.photography', '.photos', '.physio', '.pics', '.pictures', '.pink',
            '.pizza', '.pl', '.place', '.plumbing', '.plus', '.poker', '.press', '.pro', '.productions', '.promo',
            '.properties', '.property', '.pub', '.qpon', '.quebec', '.racing', '.realty', '.recipes', '.red', '.rehab',
            '.reisen', '.rent', '.rentals', '.repair', '.report', '.republican', '.rest', '.restaurant', '.review',
            '.reviews', '.rip', '.rocks', '.rodeo', '.run', '.sa.com', '.sale', '.sarl', '.sc', '.school', '.schule',
            '.science', '.se.net', '.services', '.sexy', '.sg', '.shiksha', '.shoes', '.shop', '.shopping', '.show',
            '.singles', '.site', '.ski', '.soccer', '.social', '.software', '.solar', '.solutions', '.soy', '.space',
            '.srl', '.store', '.stream', '.studio', '.study', '.style', '.supplies', '.supply', '.support', '.surf',
            '.surgery', '.systems', '.tattoo', '.tax', '.taxi', '.team', '.tech', '.technology', '.tel', '.tennis',
            '.theater', '.tienda', '.tips', '.today', '.tokyo', '.tools', '.tours', '.town', '.toys', '.trade', '.training',
            '.tv', '.tw', '.uk', '.uk.com', '.university', '.uno', '.us', '.us.com', '.vacations', '.vc', '.vegas',
            '.ventures', '.vet', '.viajes', '.video', '.villas', '.vip', '.vision', '.vodka', '.vote', '.voting',
            '.voyage', '.watch', '.webcam', '.website', '.wedding', '.wiki', '.win', '.wine', '.work', '.works',
            '.world', '.ws', '.wtf', '.xyz', '.yoga', '.za.com', '.zone']
POPULAR_EXTENTIONS = [
    '.com','.io','.ai','.net','.org','.co','.us'
    ]
ALL_EXTENTIONS = list(set(POPULAR_EXTENTIONS+EXTENTIONS))
ALL_URL_KEYS = {
    'scheme':['https','http'],
    'netloc':{
        "www":[True,False],
        "extentions":[POPULAR_EXTENTIONS,ALL_EXTENTIONS]
        }
    }
EXTENSIONS = EXTENTIONS
POPULAR_EXTENSIONS = POPULAR_EXTENTIONS
ALL_EXTENSIONS = ALL_EXTENTIONS
INVERSE_HTTP = {'http': 'https', 'https': 'http'}
INVERSE_BOOL = {True:False,False:True}

ENC = tiktoken.get_encoding("cl100k_base")
