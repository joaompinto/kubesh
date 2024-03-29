import sys
import yaml
from tabulate import tabulate


class StdinConsole:
    def __init__(self, config_context):
        pass

    def run(self):
        while True:
            command = sys.stdin.read()
            if not command:
                break
            command = command.strip()  # Remove stdin enf of lines
            short_cmd = command.split()[0]
            result = self.cmd_handler.process(command)
            if result == "not_found":
                print(f"Error: Command '{short_cmd}' is not defined", file=sys.stderr)

    def table(self, table_data):
        headers = table_data[0]
        values = table_data[1:]
        print(tabulate(values, headers=headers))

    def print_yaml(self, data):
        yaml.safe_dump(data, default_flow_style=False)
