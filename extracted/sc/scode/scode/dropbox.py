def dropbox_upload_file(src_file_path, destination_path, ACCESS_TOKEN):
    """
    It takes a file path, uploads it to Dropbox, and returns the file path of the uploaded file
    
    :param src_file_path: The path to the file you want to upload
    :param destination_path: The path to the folder where you want to upload the file
    :param ACCESS_TOKEN: The access token you got from the Dropbox API console
    """
    import dropbox
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    destination_path = destination_path.replace('\\', '/')
    src_file_path = src_file_path.replace('\\', '/')
    if destination_path[-1] == '/':
        destination_path = destination_path[:-1]
    if '.' not in destination_path.split('/')[-1]:
        destination_path += "/" + src_file_path.split('/')[-1]
    with open(src_file_path, "rb") as f:
        dbx.files_upload(f.read(), destination_path, mode=dropbox.files.WriteMode.overwrite)

def dropbox_upload_folder(folder_path, destination_path, ACCESS_TOKEN):
    """
    It takes a folder path, a destination path, and an access token, and uploads the folder to the
    destination path on Dropbox
    
    :param folder_path: The path to the folder you want to upload
    :param destination_path: The path to the folder in Dropbox where you want to upload the file
    :param ACCESS_TOKEN: The access token for your Dropbox account
    """
    import os
    import glob
    folder_path = folder_path.replace('\\', '/')
    if folder_path[-1] == '/':
        folder_path = folder_path[:-1]
    destination_path = destination_path.replace('\\', '/')
    if destination_path[-1] == '/':
        destination_path = destination_path[:-1]
    file_list = glob.glob(f'{folder_path}/**')
    for file_path in file_list:
        filename = file_path.split('\\')[-1]
        if os.path.isdir(file_path):
            dropbox_upload_folder(file_path, f"{destination_path}/{filename}", ACCESS_TOKEN)
        else:
            dropbox_upload_file(file_path, f'{destination_path}/{filename}', ACCESS_TOKEN)
