from .imports import *
from .paths import *
from .urls import *
def get_save_page_path(url, output_dir):
    """
    Save HTML page to local directory.
    """
    parsed_url = urlparse(url)
    page_path = parsed_url.path.lstrip('/')

    if not page_path or page_path.endswith('/'):
        page_path = os.path.join(page_path, 'index.html')
    elif not os.path.splitext(page_path)[1]:
        page_path += '.html'

    page_full_path = os.path.join(output_dir, page_path)
    return page_full_path
def save_page(url, content,output_dir):
    page_full_path = get_save_page_path(url=url,
                                        output_dir=output_dir)
    page_full_path = currate_full_path(page_full_path)
    if page_full_path:
        dirname = os.path.dirname(page_full_path)
        

        with open(page_full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved page: {page_full_path}")
def get_asset_path(asset_url,
                   base_url,
                   output_dir,
                   downloaded_assets=None,
                   session=None):
    """
    Download and save assets like images, CSS, JS files.
    """
    session=requests.Session()
    downloaded_assets = downloaded_assets or set()
    asset_url = normalize_url(asset_url, base_url)
    if asset_url in list(downloaded_assets):
        return
    downloaded_assets.add(asset_url)

    parsed_url = urlparse(asset_url)
    asset_path = parsed_url.path.lstrip('/')
    if not asset_path:
        return  # Skip if asset path is empty

    asset_full_path = os.path.join(output_dir, asset_path)
    return asset_full_path
def save_asset(asset_url,
               base_url,
               output_dir,
               downloaded_assets=None,
               session=None):
    asset_full_path = get_asset_path(asset_url=asset_url,
                                     base_url=base_url,
                                     output_dir=output_dir,
                                     downloaded_assets=downloaded_assets,
                                     session=session)
    if asset_full_path:
        os.makedirs(os.path.dirname(asset_full_path), exist_ok=True)

        try:
            response = session.get(asset_url, stream=True)
            response.raise_for_status()
            with open(asset_full_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Saved asset: {asset_full_path}")
        except Exception as e:
            print(f"Failed to save asset {asset_url}: {e}")
        return downloaded_assets
