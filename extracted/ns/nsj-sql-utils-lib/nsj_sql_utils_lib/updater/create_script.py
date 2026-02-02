import os
import getpass
from datetime import datetime
import argparse
    
def create_script(filename, path):
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")

    user_name = getpass.getuser()

    filename = f"{current_time}-{filename}.sql"

    if path.strip() == "":
        file_path = f"./database/scripts/{filename}"
    else:
        file_path = f"{path}/{filename}"

    with open(file_path, 'w') as file:
        file.write(f"-- Criado por: {user_name}\n")
        file.write(f"-- Data e Hora: {datetime.now()}\n")

    os.chmod(file_path, 0o777)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--filename", help="Filename of file")
    parser.add_argument("--scriptspath", help="Path for scripts folder")
    args=vars(parser.parse_args())
    filename = args['filename'] if args['filename'] is not None else input("Informe o nome do arquivo: ")
    path  = args['scriptspath'] if args['scriptspath'] is not None else ''
    
    create_script(filename, path)
    
    

    
