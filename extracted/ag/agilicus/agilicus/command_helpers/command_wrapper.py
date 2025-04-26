import click


class Command:
    """Command wrapper wraps a CLI command definition the same way you would if you
    were to directly link it to the shell. Once you have accumulated all your
    commands, run `add_to_cli` to link them together.

    Example:
    ```
    cmd = Command()

    @cmd.command(name="doit)
    @click.pass_context
    def doit(ctx):
        print("hello world")

    @cmd.command(name="other)
    @click.pass_context
    def other(ctx):
        print("something els")

    def add_to_cli(cli):
        cmd.add_to_cli(cli)

    # Now in another module, where the shell is available, invoke add_to_cli against
    # it.
    ```
    """

    def __init__(self):
        self.commands = []

    def command(self, name: str, **kwargs):
        def decorator(function):
            command_factory = click.command(name=name, **kwargs)
            command = command_factory(function)
            self.commands.append(command)
            return command

        return decorator

    def add_to_cli(self, cli):
        for cmd in self.commands:
            cli.add_command(cmd)
