# TODO: Root folder is a folder that cnvrg adds to each data owner.
#  A bug was found in the server function that lists folders.
#  The function is data_commit.rb:data_trees and probably also commit.rb:trees
#  Those functions return the root directory ONLY if state_saved is true.
#  Since Those parts should go through a refactor pretty soon (11.2022), it wasn't fixed,
#  and the root folder is added here to the filter list. Once those functions are no more in use,
#  please re-check if the root folder can be removed.

CNVRG_METADATA_PATHS = [".cnvrgignore", "/"]


def clean_cnvrg_metadata_files_and_folders(original_generator):
    """
    For test purpose ONLY!
    Removes files and folders created by cnvrg from the given generator
    @param original_generator: Generator containing files and folders to clean
    @return: A filtered generator
    """
    return filter(lambda asset: asset.fullpath not in CNVRG_METADATA_PATHS, original_generator)
