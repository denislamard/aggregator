import os
import json

FILENAME = "entries.json"


class Agregator:
    def __init__(self):
        self._routes = None
        self._loaddata(self.filedata)

    def _loaddata(self, path: str):
        with open(path) as json_file:
            self._routes = json.load(json_file)

    def _savedata(self, path: str):
        with open(path, 'w') as json_file:
            json.dump(self._routes, json_file, indent=4)

    def addentry(self, entry: dict):
        if self._routes is not None:
            self._routes.append(entry)
            self._savedata(self.filedata)

    def findentry(self, entry: str) -> dict:
        if self._routes is None:
            return None
        for route in self._routes:
            if route['name'] == entry:
                return route
        return None

    routes = property(lambda self: self._routes)
    filedata = property(lambda self: os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME))
