import json
import sys
import argparse


def read_data(file_path) -> dict:
    with open(file_path, 'r') as f:
        return json.loads(f.read())


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_path", required=True)
    return parser.parse_args()


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
    args = parse_command_line()
    test_data = read_data(args.data_path)
    commands = create('secret', test_data.get('secret', {}))
    for cmd in commands:
        print(cmd)
    sys.exit(0)
