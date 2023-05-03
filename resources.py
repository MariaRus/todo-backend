import json
import os
from typing import List

class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def __str__(self):
        return self.title

    def print_entries(self, indent=0):
        print_with_indent(self, indent=indent)
        for entry in self.entries:
            # print(entry.parent, entry)
            entry.print_entries(indent=indent + 1)

    def json(self):
        entries_list = [entry.json() for entry in self.entries]
        return {
            "title": self.title,
            "entries": entries_list
        }

    @classmethod
    def from_json(cls, value):
        title = value['title']
        entries = []
        for entry in value.get('entries', []):
            entries.append(cls.from_json(entry))
        return cls(title, entries=entries)

    def save(self, path):
        filename = f"{self.title}.json"
        filepath = os.path.join(path, filename)
        with open(filepath, "w") as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            content = json.load(f)
        return cls.from_json(content)


def print_with_indent(value, indent=0):
    print('\t' * indent + str(value))


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry_path = os.path.join(self.data_path)
            entry.save(entry_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_path, filename)
                entry = Entry.load(filepath)
                self.entries.append(entry)

    def add_entry(self, title: str):
        entry = Entry(title)
        self.entries.append(entry)