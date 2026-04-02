"""App Settings"""

# Django
from django.conf import settings

# Set Naming on Auth Hook
KILLSTATS_APP_NAME = getattr(settings, "KILLSTATS_APP_NAME", "Killstats")

# zKillboard - https://zkillboard.com/
ZKILLBOARD_BASE_URL = "https://zkillboard.com/"
ZKILLBOARD_API_URL = "https://zkillboard.com/api/"
ZKILLBOARD_R2Z2_URL = "https://r2z2.zkillboard.com/ephemeral/"
ZKILLBOARD_R2Z2_SEQUENCE_URL = "https://r2z2.zkillboard.com/ephemeral/sequence.json"

ZKILLBOARD_BASE_URL_REGEX = r"^http[s]?:\/\/zkillboard\.com\/"
ZKILLBOARD_KILLMAIL_URL_REGEX = r"^http[s]?:\/\/zkillboard\.com\/kill\/\d+\/"

# Caching Key for Caching System
STORAGE_BASE_KEY = "killstats_storage_"

# Max lifetime of killmails in temporary storage in seconds
KILLSTATS_STORAGE_LIFETIME = getattr(
    settings, "KILLSTATS_STORAGE_LIFETIME", 3_600 * 24 * 3
)

KILLSTATS_BULK_BATCH_SIZE = getattr(settings, "KILLSTATS_BULK_BATCH_SIZE", 500)

# Max lifetime of API Cache (10 min)
KILLSTATS_API_CACHE_LIFETIME = getattr(settings, "KILLSTATS_API_CACHE_LIFETIME", 10)

# Tasks max time limit in seconds
KILLSTATS_TASKS_TIME_LIMIT = getattr(settings, "KILLSTATS_TASKS_TIME_LIMIT", 1800)
# Tasks hard timeout
KILLSTATS_TASKS_TIMEOUT = getattr(settings, "KILLSTATS_TASKS_TIMEOUT", 600)

# Rate limiting for zKillboard RedisQ requests
# Max seconds to wait trying to acquire a rate slot (0 = don't wait)
KILLSTATS_ZKB_RATE_TIMEOUT = getattr(settings, "KILLSTATS_ZKB_RATE_TIMEOUT", 10)
# Maximum allowed requests per second across all workers/processes
KILLSTATS_MAX_ZKB_PER_SEC = getattr(settings, "KILLSTATS_MAX_ZKB_PER_SEC", 2)
