class Command:
    names = [".nodes", ".n"]
    description = "List the cluster nodes"

    def run(args, api, formatter):
        response = api.list_node()
        formatter.table_output(response)
