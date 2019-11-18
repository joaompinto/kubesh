from collections import OrderedDict
from ..mapper import table_from_list
from kubernetes.client import V1Namespace, V1ObjectMeta


class Command:
    callers = [".namespaces", ".ns"]
    description = "List namespaces"

    default_fields = OrderedDict({"Name": "metadata.name", "Status": "status.phase"})

    def run(self, console, api, argv):
        if len(argv) == 0:
            response = api.list_namespace()
            response_data = table_from_list(response, self.default_fields)
            console.table(response_data)
        else:
            ns_args = argv[0]
            if ns_args[0] in ["+", "-"]:
                ns_name = ns_args[1:]
                if ns_args[0] == "+":
                    body = V1Namespace(metadata=V1ObjectMeta(name=ns_name))
                    api.create_namespace(body)
                    console.success(f"Created namespace '{ns_name}'")
                else:
                    api.delete_namespace(name=ns_name)
                    console.success(f"Deleted namespace '{ns_name}'")
