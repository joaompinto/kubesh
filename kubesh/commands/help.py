class Command:
    Name = ".help"
    Description = "List all available commands"
    Aliases = [".h"]

    def run(self, console, api):
        for cmd in console.cmd_handler.all_commands:
            print(f"{cmd.Name} - {cmd.Description}")
