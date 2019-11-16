import sys


class StdinConsole():

    def run():
        while True:
            line = sys.stdin.read()
            if not line:
                break
            print(line)
