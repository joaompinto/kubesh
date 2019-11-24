import io
import yaml
import pkgutil
import importlib
from os.path import dirname
from pathlib import Path
import inspect
import traceback
from wasabi import TracebackPrinter
from .mapper import table_from_list

# https://packaging.python.org/guides/creating-and-discovering-plugins/


class YAMLCommand:
    def __init__(self, yaml_data):
        self.yaml = yaml_data
        clone_fields = ["Name", "Aliases", "Description", "When"]
        for field in clone_fields:
            if field in yaml_data:
                setattr(self, field, yaml_data[field])

    def run(self, console, api):
        api_func = self.yaml["API"]
        api_call = f"api.{api_func}"
        response = eval(api_call)
        output_type = self.yaml["Output"]["Type"]
        content = self.yaml["Output"]["Content"]
        if output_type.lower() == "list":
            response_data = table_from_list(response, content)
            console.table(response_data)


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def yaml2cmds(filename):
    cmd_list = []
    with io.open(filename, encoding="utf8") as yaml_file:
        yaml_data = yaml.load_all(yaml_file, Loader=yaml.FullLoader)
        for cmd_data in yaml_data:
            cmd = YAMLCommand(cmd_data)
            cmd_list.append(cmd)
    return cmd_list


def load_yaml_commands():
    yaml_cmd_list = []
    commands_dir = Path(dirname((__file__))).joinpath("commands")
    for cmd_yaml_filename in Path(commands_dir).glob("*.yaml"):
        cmd_list = yaml2cmds(cmd_yaml_filename)
        yaml_cmd_list.extend(cmd_list)
    return yaml_cmd_list


def load_module_commands():
    cmd_list = []
    from . import commands

    for finder, name, ispkg in iter_namespace(commands):
        module = importlib.import_module(name)
        cls_members = inspect.getmembers(module, inspect.isclass)
        cls_members = [c[1] for c in cls_members if c[1].__name__.startswith("Command")]
        for cmd in cls_members:
            cmd_object = cmd()
            required_params = ["Name", "Description"]
            for param in required_params:
                if not hasattr(cmd_object, param):
                    tb = TracebackPrinter(
                        tb_base="kubesh", tb_exclude=("core.py", "runpy.py")
                    )
                    error = tb(
                        f"Command missing required '{param}' attribute",
                        f"File: {module.__file__}",
                        highlight="kwargs",
                        tb=traceback.extract_stack(),
                    )
                    raise ValueError(error)
                    # raise Exception(f"Command {cmd} does must provide a syntax field")
            cmd_list.append(cmd_object)
    return cmd_list


def load_commands():
    yaml_cmds = load_yaml_commands()
    module_cmds = load_module_commands()
    yaml_cmds.extend(module_cmds)
    return yaml_cmds + module_cmds
