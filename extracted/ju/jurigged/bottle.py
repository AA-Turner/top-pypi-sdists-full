import time

# from jurigged.dev import loop

separator = "==="


class Song:
    def __init__(self, n):
        self.n = n

    def format(self, i):
        if i == 0:
            return "no more"
        elif i == 1:
            return "one"
        else:
            return str(i)

    def plural(self, i):
        return "s" if i != 1 else ""

    def bottle(self, i):
        return f"{self.format(i)} bottle{self.plural(i)} of beer"

    def verse(self, i):
        print(f"{self.bottle(i).capitalize()} on the wall, {self.bottle(i)}")
        if i > 0:
            print(
                f"Take one down and pass it around, {self.bottle(i - 1)} on the wall"
            )
        else:
            print(
                f"Go to the store and buy some more, {self.bottle(self.n)} on the wall"
            )
        print(separator)

    delay = 1

    def sing(self):
        while self.n >= 0:
            self.verse(self.n)
            time.sleep(self.delay)
            self.n -= 1


if __name__ == "__main__":
    Song(99).sing()
