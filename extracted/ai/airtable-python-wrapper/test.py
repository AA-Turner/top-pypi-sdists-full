from airtable import Table
import backoff
from requests.exceptions import ConnectTimeout

# key = os.environ["AIRTABLE_KEY"]
# table = Airtable("tbl14MDsKoB0VqI8G", "entries", api_key=key)
table = Table("appNtnZ99fkL1cByn", "entries", timeout=1)


get_with_backoff = backoff.on_exception(backoff.expo, ConnectTimeout, max_tries=10)(
    table.get_all
)

get_with_backoff()
