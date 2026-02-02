from abstract_utilities import get_logFile
from abstract_solcatcher import call_solcatcher_ts,async_call_solcatcher_ts,async_call_solcatcher_py,call_solcatcher_py
import traceback
logger = get_logFile('meta_data')
async def insert_meta_data(mint, metaData, uri=None):
    """
    Insert or update the metadata in DB through the TS-based endpoint.
    """
    # If your TS endpoint expects `metaData`, `uri`, and `mint`, pass them as a dict or separate params:
    # e.g. `payload={'metaData': metaData, 'uri': uri, 'mint': mint}`
    return await async_call_solcatcher_ts(
        'insert-meta',
        metaData=metaData,
        uri=uri,
        mint=mint
    )

async def call_meta_data(mint, url=None):
    """
    Python function that calls the TS endpoint `call-meta`,
    or directly calls your Solana logic if you prefer.
    """
    if not mint:
        logger.warning(f"call_meta_data called with no mint!")
        return {}
    payload = {"endpoint":'call-meta',"url": url, "mint": mint}

    # Example: call your TypeScript endpoint "call-meta"
    response = await async_call_solcatcher_py('make_limited_ts_call',payload=payload)
    # If the result is a dictionary with 'result', unwrap it
    if response and hasattr(response, 'get'):
        return response.get('result', response)
    return response

async def fetch_metaData(mint, url=None):
    """
    Higher-level function that tries up to 5 times to fetch metadata (call_meta_data),
    then inserts it via `insert_meta_data` if found.
    """
    if not mint:
        logger.error("No mint provided to fetch_metaData.")
        return {}

    for attempt in range(1, 6):
        try:
            # Generate URL from rate limiter
            if url == None:
                if attempt == 5:
                    url1 = 'https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370'
                else:
                    url1 = await async_call_solcatcher_py('getUrl1',method='fetch-meta')
            else:
                url1=url
            payload = {"endpoint":'fetch-meta',"url": url1, "mint": mint}

            # Actually fetch the metadata from your TS or Solana endpoint
            meta_data = await async_call_solcatcher_py('make_limited_ts_call',payload=payload)
            if not meta_data:
                logger.warning(
                    f"Attempt {attempt} of 5: No metadata returned for {mint} "
                )
                continue

            # Insert the metadata
            ##insert_result = await insert_meta_data(mint, meta_data)
            logger.info(f"[fetch_metaData] Inserted metadata for {mint}")
            return insert_result

        except Exception as e:
            logger.error(f"[fetch_metaData] Attempt {attempt} failed for {mint}: {e}")

    logger.warning(f"[fetch_metaData] All 5 attempts failed for {mint}")
    return {}
async def async_get_or_fetch_meta_data(mint=None,meta_id=None,pair_id=None,url_1_only=None,url_2_only=None):
    url = "http://api.mainnet-beta.solana.com"
    if url_2_only:
        url = 'https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370'
    return await async_call_solcatcher_ts('get-or-fetch-metadata',mint=mint,url=url)

def get_or_fetch_meta_data(mint=None,meta_id=None,pair_id=None,url=None,url_1_only=None,url_2_only=None):
    url = url or "http://api.mainnet-beta.solana.com"
    if url_2_only:
        url = 'https://rpc.ankr.com/solana/c3b7fd92e298d5682b6ef095eaa4e92160989a713f5ee9ac2693b4da8ff5a370'
    return call_solcatcher_ts('get-or-fetch-metadata',mint=mint,url=url,umi=None)
