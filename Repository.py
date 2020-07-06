import json
import os
import ScanFolder
from halo import Halo


class Repository:
    def __init__(self):
        self.filename = "Repo.json"
        self.loaded_mods = self.read_repo()

    def installed_mods(self) -> str:
        with Halo(text='Loading\n', spinner='dots'):
            scanner = ScanFolder.ScanFolder(r"C:\Sandbox\mathe\RimWorld\user\current\RimWorld.v1.0.2231\X64\Mods")
            return scanner.get_mods_as_json()

    def read_repo(self) -> dict:
        if os.path.isfile(self.filename):
            file = open(self.filename, 'r')
            data: dict = json.load(file)
            file.close()
            return data
        else:
            self._create_repo()
            return self.read_repo()

    @Halo(text="Updating repo...", spinner='dots')
    def update_repo(self, modlist: dict):
        if os.path.isfile(self.filename):
            file = open(self.filename, 'r')
            mods = json.load(file)
            file.close()
            for mod in modlist:
                if mod not in mods:
                    print(f"Added {mod} to repo")
                    mods[mod] = modlist[mod]
                elif mods[mod] != modlist[mod]:
                    print(f"Updating {mod} link")
                    mods[mod] = modlist[mod]
            file = open(self.filename, 'w')
            json.dump(mods, file)
            file.close()
        else:
            print("Creating repository file.")
            self._create_repo()
            self.update_repo(modlist)

        self.loaded_mods = self.read_repo()

    def _create_repo(self):
        data = {}
        if os.path.isfile(self.filename):
            return
        f = open(self.filename, 'w')
        json.dump(data, f)
        f.close()
