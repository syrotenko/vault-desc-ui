class VNode:
    def __init__(self, parent, name=None, dirs=None, kv=None):
        self.parent = parent
        self.name = name
        self.children = dirs if dirs else []
        self.kv = kv if kv else {}

    def get_full_path(self):
        full_path = f'{self.name}/'
        if self.parent is not None:
            full_path = self.parent.get_full_path() + full_path
        return full_path

    def get_node(self, path):
        paths = path.split(self.get_full_path(), maxsplit=1)
        if len(paths) > 1:
            further_path = paths[1]
            if further_path:
                child_name = further_path.split('/')[0]
                for child in self.children:
                    if child.name == child_name:
                        return child.get_node(path)
        return self
