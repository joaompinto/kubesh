from collections import OrderedDict


class Command_Nodes:
    callers = [".nodes", ".n"]
    description = "List the cluster nodes"

    default_fields = OrderedDict(
        {"NAME": 'metadata.name'}
    )

    def run(self, console, api):
        response = api.list_node()
        response_data = []
        response_data.append(list(self.default_fields))
        for node_item in response.items:
            row = []
            for field_item, field_value in self.default_fields.items():
                value = eval(f'node_item.{field_value}')
                row.append(value)
            response_data.append(row)
        console.table(response_data)
        return "nodes"