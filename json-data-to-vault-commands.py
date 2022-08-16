import json
import sys

DATA_PATH = '.\\vault-test-data.json'


def read_data(file_path) -> dict:
    with open(file_path, 'r') as f:
        return json.loads(f.read())


def write_key(path, key, val):
    return f'vault kv put {path} {key}={val}'


def create(current_path, data):
    cmds = list()
    for k, v in data.items():
        if isinstance(v, dict):
            cmds.extend(create(f'{current_path}/{k}', v))
        else:
            cmds.append(write_key(current_path, k, v))
    return cmds


if __name__ == '__main__':
    test_data = read_data(DATA_PATH)
    commands = create('secret', test_data.get('secret', {}))
    for cmd in commands:
        print(cmd)
    sys.exit(0)
