#!/usr/bin/python3

# init nornir objects
from nornir import InitNornir
# all the creations of Tasks and their Results
from nornir.core.task import Task, Result
# process results
from nornir_utils.plugins.functions import print_result

# import connection plugin
# import thor # thor can summon ragnarok
from nornir_mythos.connections import thor

# import commands
# from nornir.plugins.tasks import commands


def biography(task: Task) -> Result:
    with open("biography.txt", "w") as bio:
        task.host.open_connection(connection="ragnarok", configuration=task.host.data)
        for oneliner in task.host.data["nested_data"]["catch_phrases"]:
            bio.write(f"{oneliner}\n")
    result = "Creation of biography.txt was successful"
    task.host.close_connection()         # experimentation with manual open / close connections
    return Result(host=task.host, result=result)



def main():
    nr = InitNornir(config_file="config.yaml")

    # the nornir object now contains settings from config.yaml
    print(nr.config.runner.options["num_workers"])

    # access the inventory hosts
    # see inventory/hosts.yaml
    print(nr.inventory.hosts)

    # access the inventory groups
    # see inventory/groups.yaml
    print(nr.inventory.groups)

    # display an individual host
    host = nr.inventory.hosts["host1.planetexpress"]
    print(host.keys())

    # display individual host information
    # see inventory/hosts.yml
    print(host["site"])  # resolves to earth

    # display default settings
    # see inventory/defaults.yaml
    print(host["domain"])  # planetexpress.local

    # If you try to access data the does not exist
    # you get a typical python key error
    try:
        print(host["fuel"])
    except KeyError as e:
        print(f"Uh oh. We could not find the key: {e}")

    # use a filter to select those hosts with the following
    # characterists from our inventory
    targethost = nr.filter(site="earth", type="host")
    # run our biography creation task
    result = targethost.run(task=biography)

    print_result(result)

# call the futurama crew
if __name__ == "__main__":
    main()
