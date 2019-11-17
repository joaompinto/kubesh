class Command:
    callers = [".help", ".h"]
    description = "List all available commands"

    def run(self, console, api):
        for cmd in console.cmd_handler.all_commands:
            callers = "\t".join(cmd.callers)  # tab between full/short
            print(f"{callers} - {cmd.description}")
