import ScanFolder
import Repository
import json
import os
from halo import Halo
from prettytable import PrettyTable
from colorama import Fore
from colorama import Style

repo = Repository.Repository()


# Menu
def menu():
    while True:
        print("Rim Manager menu")
        print("[0] Exit")
        print("[1] List Mods")
        print("[2] List repository")
        print("[3] Modify repository")
        choice: str = input(">>")
        if choice == "0":
            print("Bye!")
            return
        if choice == "1":
            show_mods()
        if choice == "2":
            show_repo()
        if choice == "3":
            modify_mod()


def show_mods(numbered=False):
    modlist = json.loads(repo.installed_mods())
    t = PrettyTable(["Mod", "Link"])
    count = 0
    for i in modlist:
        if modlist[i] != None:
            if len(modlist[i]) > 0:
                t.add_row([f"{str(count) + ' ' if numbered else ''} {Fore.GREEN}{i}", f"{modlist[i]}{Style.RESET_ALL}"])
            else:
                t.add_row([f"{str(count) + ' ' if numbered else ''}{Fore.YELLOW}{i}",
                           f"{Fore.YELLOW}No url on mod description{Style.RESET_ALL}"])
        else:
            t.add_row([f"{str(count) + ' ' if numbered else ''}{Fore.RED}{i}",
                       f"{Fore.RED}No description about this mod{Style.RESET_ALL}"])
        count += 1
    print(f"{Style.RESET_ALL}{t}")
    return modlist


def modify_mod():
    modlist = show_repo(True)
    modcount: list = []
    for i in modlist:
        modcount.append(i)
    while True:
        print("Type -1 to cancel")
        choice = input(">>")
        if choice == "-1":
            return
        if int(choice) in range(len(modcount)):
            print(f"Modifying {modcount[int(choice)]}, {modlist[modcount[int(choice)]]}")
            newlink: str = input("Insert new link!\n>>")
            if newlink.find("https://") != -1:
                print(f"Modified: {modcount[int(choice)]}, {newlink}\nSave? N/y")
                confirm_choice = input(">>")
                if confirm_choice.lower() == "y":
                    modlist[modcount[int(choice)]] = newlink
                    repo.update_repo(modlist)
                    print("OK!")
                    return
                else:
                    print("Cancelled")
                    return
            else:
                print("Link must be a complete URL")
                continue
        else:
            print("Choose a mod from the list")
            continue


# List current mods
def show_repo(numbered=False) -> dict:
    modlist = (repo.read_repo())
    t = PrettyTable(["Mod", "Link"])
    count = 0
    for i in modlist:
        if modlist[i] != None:
            if len(modlist[i]) > 0:
                t.add_row([f"{str(count) + ' ' if numbered else ''} {Fore.GREEN}{i}", f"{modlist[i]}{Style.RESET_ALL}"])
            else:
                t.add_row([f"{str(count) + ' ' if numbered else ''}{Fore.YELLOW}{i}",
                           f"{Fore.YELLOW}No url on mod description{Style.RESET_ALL}"])
        else:
            t.add_row([f"{str(count) + ' ' if numbered else ''}{Fore.RED}{i}",
                       f"{Fore.RED}No description about this mod{Style.RESET_ALL}"])
        count += 1
    print(f"{Style.RESET_ALL}{t}")
    return modlist


menu()
