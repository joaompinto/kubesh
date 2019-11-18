from collections import OrderedDict
from ..mapper import table_from_list


class Command:
    callers = [".pods", ".p"]
    description = "List the pods"

    default_fields = OrderedDict(
        {"Namespace": "metadata.name", "Name": "metadata.name"}
    )

    def run(self, console, api, argv):
        if len(argv) == 0:
            response = api.list_pod_for_all_namespaces()
            response_data = table_from_list(response, self.default_fields)
            console.table(response_data)
