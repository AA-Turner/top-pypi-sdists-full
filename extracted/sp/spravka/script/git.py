import os


def add():
    os.system('git add .')


def commit():
    os.system('git commit -m"new features"')


def push():
    os.system('git push')


def main():
    add()
    commit()
    push()
