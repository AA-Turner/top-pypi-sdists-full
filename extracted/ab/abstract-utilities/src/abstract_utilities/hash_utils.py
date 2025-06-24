import hashlib
def generate_data_hash(insertName,value):
    # Combine values to create a unique reference
    data_string = f"{insertName}_{value}"
    return hashlib.md5(data_string.encode()).hexdigest()
