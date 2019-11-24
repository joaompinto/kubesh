class Command:
    Name = ".quit"
    Description = "Quit the current shell"

    def run(self, console, api):
        return "quit"
