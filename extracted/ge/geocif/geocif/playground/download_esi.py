import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# URL of the directory listing
url = "https://nssrgeo.ndc.nasa.gov/team/crh/"

# Directory to save downloaded files
save_dir = "downloads"
os.makedirs(save_dir, exist_ok=True)

def download_file(file_url, save_path):
    """
    Downloads a file from the given URL if it does not already exist locally.
    """
    if os.path.exists(save_path):
        return f"Skipped (exists): {os.path.basename(save_path)}"
    try:
        response = requests.get(file_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return f"Downloaded: {os.path.basename(save_path)}"
    except Exception as e:
        return f"Failed: {os.path.basename(save_path)} ({e})"

def fetch_file_list(url):
    """
    Fetches the list of files containing 'avhrr_esi' from the directory listing.
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        files = [
            link.get("href")
            for link in soup.find_all("a")
            if "avhrr_esi" in link.get("href") and link.get("href").endswith(".tar")
        ]
        return files
    else:
        raise Exception(f"Failed to fetch directory listing: {url}")

def download_files_in_parallel(file_urls, base_url):
    """
    Downloads files in parallel using ThreadPoolExecutor with a progress bar.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        tasks = [
            executor.submit(download_file, os.path.join(base_url, file), os.path.join(save_dir, file))
            for file in file_urls
        ]
        for future in tqdm(tasks, desc="Downloading files", unit="file"):
            results.append(future.result())
    return results

if __name__ == "__main__":
    try:
        file_list = fetch_file_list(url)
        if not file_list:
            print("No files found matching 'avhrr_esi'.")
        else:
            print(f"Found {len(file_list)} files to download.")
            results = download_files_in_parallel(file_list, url)
            for result in results:
                print(result)
    except Exception as e:
        print(f"Error: {e}")
