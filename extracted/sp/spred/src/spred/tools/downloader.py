import os
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'resource', 'ref')

def download_with_resume(url, local_path):
    # Check if part of the file has been downloaded
    downloaded = 0
    if os.path.exists(local_path):
        downloaded = os.path.getsize(local_path)

    req = urllib.request.Request(url)
    if downloaded > 0:
        req.add_header('Range', f'bytes={downloaded}-')  # resume from where left off

    try:
        with urllib.request.urlopen(req) as response:
            # 服务器可能返回 206 或 200 状态码，需计算总大小
            content_length = response.headers.get('Content-Length')
            if content_length is None:
                total_size = None
            else:
                total_size = int(content_length) + downloaded

            mode = 'ab' if downloaded > 0 else 'wb'
            print(f"Starting download: {url}")
            print(f"Saving to: {local_path}")
            print(f"Resuming from byte {downloaded}..." if downloaded > 0 else "Starting fresh download...")

            with open(local_path, mode) as out_file:
                block_size = 8192
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    out_file.write(buffer)
                    downloaded += len(buffer)
                    if total_size:
                        done = int(50 * downloaded / total_size)
                        print(f"\r[{'█' * done}{'.' * (50 - done)}] {downloaded / total_size:.2%}", end='')

            print("\nDownload completed.")
    except Exception as e:
        print(f"\nDownload failed: {e}")
        if os.path.exists(local_path):
            print(f"Deleting incomplete file: {local_path}")
            os.remove(local_path)

def get_annotation_file(species, reference_source):
    if species.lower() not in ['mouse', 'human']:
        print("The species should be Mouse or Human")
        return None

    if reference_source.lower() not in ['gencode', 'ncbi']:
        print("The reference source should be 'gencode' or 'ncbi'")
        return None

    if species.lower() == 'mouse':
        if reference_source.lower() == 'gencode':
            LOCAL_FILENAME = os.path.join(DATA_DIR, 'GRCm39_M36/transcript_gene_info.tsv.gz')
            ANNOTATION_URL = 'https://github.com/ZhengCQ/SpReD/releases/download/v1.0.0/GRCm39_M36.transcript_gene_info.tsv.gz'
        elif reference_source.lower() == 'ncbi':
            LOCAL_FILENAME = os.path.join(DATA_DIR, 'NCBI_Mm10/transcript_gene_info.tsv.gz')
            ANNOTATION_URL = ''  # fill in URL if available
    elif species.lower() == 'human':
        if reference_source.lower() == 'gencode':
            LOCAL_FILENAME = os.path.join(DATA_DIR, 'GRCh38_V42/transcript_gene_info.tsv.gz')
            ANNOTATION_URL = 'https://github.com/ZhengCQ/SpReD/releases/download/v1.0.0/GRCh38_v42.transcript_gene_info.tsv.gz'
        elif reference_source.lower() == 'ncbi':
            LOCAL_FILENAME = os.path.join(DATA_DIR, 'NCBI_Hg38/transcript_gene_info.tsv.gz')
            ANNOTATION_URL = ''  # fill in URL if available

    if not ANNOTATION_URL:
        print(f"No URL specified for {species} - {reference_source}.")
        return None

    if not os.path.exists(LOCAL_FILENAME):
        os.makedirs(os.path.dirname(LOCAL_FILENAME), exist_ok=True)
        download_with_resume(ANNOTATION_URL, LOCAL_FILENAME)

    return LOCAL_FILENAME


