import os
import pefile

def process_file(file_path):
    try:
        pe = pefile.PE(file_path)
        memory_mapped_image = pe.get_memory_mapped_image()
        print(f"{file_path}: {len(memory_mapped_image)} bytes")
    except pefile.PEFormatError:
        pass

def find_files(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(".dmp"):
                file_path = os.path.join(root, file)
                result = process_file(file_path)
                if result:
                    results.append(result)
    return results

if __name__ == "__main__":
    directory = "./tests/test_files"
    results = find_files(directory)
