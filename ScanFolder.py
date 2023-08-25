import os
import json
import xml.etree.ElementTree as ET
import ProgressBar
from pathlib import Path

class ScanFolder:
    def __init__(self, rim_mods_dir: str):
        self.mod_dir = Path(rim_mods_dir)
        self._valid_path = self._validate_path()
        self.bar = ProgressBar.ProgressBar()

    def _validate_path(self) -> bool:
        if self.mod_dir.is_dir():
            modfolders = os.listdir(self.mod_dir.absolute())
            if "Core" in modfolders:
                return True
        return False

    def get_mods_as_json(self) -> str:
        if self._validate_path():
            modfolders = os.listdir(self.mod_dir.absolute())
            modfolders.remove("Core")
            mods = {}
            k = 0
            l = len(modfolders)
            for i in modfolders:
                self.bar.progress(k, l, i)
                mods[i] = self.try_finding_url(i)
                k += 1
            return json.dumps(mods)

    def try_finding_url(self, modfolder) -> str:
        if self._validate_path():
            About = f"{modfolder}\About\About.xml"
            filepath = os.path.join(self.mod_dir, About)
            if os.path.isfile(filepath):
                tree = ET.parse(filepath)
                root = tree.getroot()
                for child in root:
                    if child.tag == "url":
                        return child.text
        return ""
