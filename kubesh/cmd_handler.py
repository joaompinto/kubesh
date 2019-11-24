""" Command handler """


class CommandHandler:
    def __init__(self, commands, console, api):
        self.commands = commands
        self.console = console
        self.api = api
        console.cmd_handler = self

    def tokenizer(self, command):
        command = command.strip()
        tokens = command.split()
        return tokens

    def process(self, cmd_line):
        handler, args, kwargs = self.find_command(cmd_line)
        if handler:
            process_args = [self.console, self.api] + args
            return handler.run(*process_args)
        return "not_found"

    def find_command(self, cmd_line):
        base_command = cmd_line.strip().split()[0].lower()
        for cmd in self.commands:
            _when = getattr(cmd, "When", True)
            if isinstance(_when, str):
                _when = eval(_when)
            if not _when:
                continue
            aliases = [cmd.Name.lower()] + getattr(cmd, "Aliases", [])
            if base_command in aliases:
                return cmd, [], {}
        return None, [], {}

    @property
    def all_commands(self):
        return self.commands
