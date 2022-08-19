import json
import sys


def read_data(file_path) -> dict:
    with open(file_path, 'r') as f:
        return json.loads(f.read())


def write_key(path, key, val):
    return f'{path} {key}={val}'


def create(current_path, data):
    cmds = list()
    for k, v in data.items():
        if isinstance(v, dict):
            cmds.extend(create(f'{current_path}/{k}', v))
        else:
            cmds.append(write_key(current_path, k, v))
    return cmds


if __name__ == '__main__':
    DATA_PATH = '.\\vault-test-data.json'
    test_data = read_data(DATA_PATH)
    commands = create('secret', test_data.get('secret', {}))
    for cmd in commands:
        print(cmd)
    sys.exit(0)
