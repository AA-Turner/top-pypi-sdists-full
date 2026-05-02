# __main__.py

try:
    from .encryption import *
    from .stream import *
except ImportError:
    from encryption import *
    from stream import *

from arg_parser import *
import os


def main():
    reg = Register()
    reg.add(Command("--simple-encrypt", "Encrypts a string with a (given) key", ["-s"], ["-k", "-of"]))
    reg.add(Command("--se", "....", ["-s"], ["-k", "-of"]))
    reg.add(Parameter("-s", "String to de-/encrypt"))
    reg.add(Parameter("-k", "Key for de-/encryption"))
    reg.add(Parameter("-of", "File to write the decrypted string in"))

    reg.add(Command("--simple-decrypt", "Decrypts a string with a key", ["-s", "-k"], ["-of"]))
    reg.add(Command("--sd", "....", ["-s", "-k"], ["-of"]))

    reg.add(Command("--encrypt-file", "Encrypts a file with a given or random key", ["-p"], ["-k, -r", "-pr"]))
    reg.add(Command("--ef", "....", ["-p"], ["-k, -r", "-pr"]))
    reg.add(Parameter("-p", "Path to the file to de-/encrypt"))
    reg.add(Parameter("-r", "Register-file for storing the keys, 'def' for default register."))
    reg.add(Parameter("-pr", "Prompts for a key. Useful in batch of shell scripts.", True))

    reg.add(Command("--decrypt-file", "Decrypts a file with a given key the decypters key or a register", None,
                    ["-p", "-k", "-r", "-pr"]))
    reg.add(Command("--df", "....", None, ["-p", "-k", "-r", "-pr"]))

    reg.add(Command("--connect", "Connects to a server and creates an encrypted chat-session",
                    ["-ip", "-port", "-k"]))
    reg.add(Parameter("-ip", "IP to connect to v4 or v6"))
    reg.add(Parameter("-port", "Port to connect to or to listen on"))

    reg.add(Command("--host", "Starts an encrypted server hosting a chat-session", ["-ip", "-port"], ["-k"]))

    reg.add(Command("--config", "Edit config values", None, ["-pa", "-v", "-sh"]))
    reg.add(Parameter("-pa", "Parameter to edit"))
    reg.add(Parameter("-v", "New value of parameter"))
    reg.add(Parameter("-sh", "Show config parameters", True))

    parser = Parser(reg, os.path.realpath(__file__))

    encryptor = Encryptor()
    decrypter = Decrypter()

    @parser("--simple-encrypt", "--se")
    def simple_encrypt(opts: dict):
        key = None if not opts.__contains__("-k") else opts["-k"]
        key, value = encryptor.encrypt(opts["-s"], key)
        if not opts.__contains__("-of"):
            value = value.replace("\"", "\\\"").replace("\'", "\\'")
            print(f"Key: {key}\nEncrypted: {value}")
        else:
            with open(opts["-of"], "w") as f:
                f.write("Key: " + key.string + "\nEncrypted: " + value)
                f.close()
                log("Encryption", f"Info: Wrote encrypted string to {opts['-of']}")

    @parser("--simple-decrypt", "--sd")
    def simple_decrypt(opts: dict):
        key = None if not opts.__contains__("-k") else opts["-k"]
        decrypted = decrypter.decrypt(opts["-s"], key)
        if not opts.__contains__("-of"):
            print(decrypted)
        else:
            with open(opts["-of"], "wb") as f:
                f.write(decrypted.encode("utf-8"))
                f.close()
                log("Decryption", f"Info: Wrote decrypted string to {opts['-of']}")

    @parser("--encrypt-file", "--ef")
    def encrypt_file(opts: dict):
        key = None if "-k" not in opts else opts["-k"]
        register = None if "-r" not in opts else opts["-r"]
        if "-pr" in opts:
            key = input("Key: ")
        key = encryptor.encrypt_file(opts["-p"], key)
        if register:
            encryptor.add_to_register(opts["-r"], opts["-p"], key)

    @parser("--decrypt-file", "--df")
    def decrypt_file(opts: dict):
        key = None if "-k" not in opts else opts["-k"]
        register = None if "-r" not in opts else opts["-r"]
        if "-pr" in opts:
            key = input("Key: ")
        if register:
            decrypter.decrypt_with_register(opts["-r"])
        else:
            decrypter.decrypt_file(opts["-p"], key)

    @parser("--connect")
    def connect(opts: dict):
        stream = Stream_Client(ip=opts["-ip"], port=int(opts["-port"]), key=opts["-k"])
        stream.connect()

    @parser("--host")
    def host(opts: dict):
        stream = Stream_Host(ip=opts["-ip"], port=int(opts["-port"]), key=None if not opts.__contains__("-k") else
        opts["-k"])
        stream.listen()

    @parser("--config")
    def config(opts: dict):
        if opts.__contains__("-sh"):
            print("Config parameters:")
            for param in encryptor.cfg.cfg:
                print(" " * 4 + param + " " * (30 - len(param)) + encryptor.cfg[param])
        elif opts.__contains__("-pa") and opts.__contains__("-v"):
            if encryptor.cfg.cfg.__contains__(opts["-pa"]):
                encryptor.cfg[opts["-pa"]] = opts["-v"]
                encryptor.cfg.write_cfg()
                log("Config", f"Changed param '{opts['-pa']}' to '{opts['-v']}'")
            else:
                raise Exception(f"Couldn't find param '{opts['-pa']}'")
        else:
            print("You executed command --config the wrong way. Use '-sh' to show all parameters and '-pa'"
                  " and '-v' to edit parameters.", end="\n\n")
            parser.print_usage()


if __name__ == "__main__":
    main()
