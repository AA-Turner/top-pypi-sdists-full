import os
import shutil

def delete_create_folder(folder_path, family):
    """
    Deletes a folder and its contents recursively & Creates a new folder at the specified path.

    Args:
        folder_path (str): The path to the folder to be deleted.
        family (str): The name of the subfolder to create within the given path.

    Returns:
        bool: True if the folder was successfully deleted and created, False otherwise.
    """
    try:
        # Construct the full path for the folder
        full_folder_path = os.path.join(folder_path, family)

        # Delete the folder if it exists
        if os.path.exists(full_folder_path):
            shutil.rmtree(full_folder_path)
            print(f"Folder {full_folder_path} deleted successfully along with its contents.")

        # Create the folder
        os.makedirs(full_folder_path)
        print(f"Folder {full_folder_path} created successfully.")

        return True

    except OSError as e:
        print(f"Error: {e}")
        return False
