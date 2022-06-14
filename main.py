from listaudioint import list_insterfaces
from audioapp import runn_app
import json
import os

clear = lambda: os.system("cls")

devices = dict(list_insterfaces()["devices"])

with open("config.json") as f:
    config = json.load(f)


def menu() -> str:
    with open("config.json") as f:
        config = json.load(f)
    dev_id = config["device_id"]
    print(f"Your app running use the interface {dev_id} - ({devices[dev_id]})")
    print("For running the app with the selected interface, press 1.")
    print("For select another interface, press 2.")
    return input("Select the options: ")


def repeat_menu() -> None:
    clear()
    print("Invalid option, select 1 or 2!")
    return process_menu()


def process_menu() -> None:
    input_user = menu()
    if input_user not in ["1", "2"]:
        return repeat_menu()

    if input_user == "1":
        return runn_app(config["device_id"])
    if input_user == "2":
        return change_interface()


def change_interface(error=None) -> None:
    clear()
    if error:
        print(error)
    print("Select the index of the interface: ")
    for index, name in devices.items():
        print(f"Index {index} <-> {name}")
    input_data = input()
    if not input_data.isnumeric():
        return change_interface("Select a numeric index.")
    index_dev = devices.keys()
    if not int(input_data) in index_dev:
        return change_interface("Number not in informed index.")
    config["device_id"] = int(input_data)
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    return runn_app(int(input_data))


if __name__ == "__main__":
    process_menu()
