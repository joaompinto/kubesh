import sys


class StdinConsole:
    def __init__(self, cmd_handler):
        self.cmd_handler = cmd_handler

    def run(self):
        while True:
            line = sys.stdin.read()
            if not line:
                break
            print(line)
