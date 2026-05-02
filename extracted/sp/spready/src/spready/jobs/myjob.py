from spready import sproute

@sproute(path="/client/a")
def execute(): 
    print("Hi")
    return "Hello"

if __name__ == "__main__":
    execute()