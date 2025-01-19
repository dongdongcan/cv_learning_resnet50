#!/usr/bin/env python3

import argparse
import json
import os
import subprocess
import sys
from typing import Callable, Dict, List, Union


def get_git_branch() -> str:
    return "origin/master"


def is_c_cpp(filename: str) -> bool:
    return filename.endswith((".c", ".cc", ".cpp", ".h"))


def is_cmake(filename: str) -> bool:
    return os.path.basename(filename) == "CMakeLists.txt"


def is_json(filename: str) -> bool:
    return filename.endswith(".json")


def is_python(filename: str) -> bool:
    return filename.endswith(".py")


def format_json(filename: str):
    """Format json files, update in-place."""
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    # recursively sort dict keys in json. Do not change order of list.
    def sort_keys_recursive(obj):
        if isinstance(obj, dict):
            return {k: sort_keys_recursive(v) for k, v in sorted(obj.items())}
        if isinstance(obj, list):
            return [sort_keys_recursive(elem) for elem in obj]
        return obj

    data = sort_keys_recursive(data)
    formatted_data = json.dumps(data, indent=4)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(formatted_data)
        file.write("\n")


def find_all_source_files(root_path: str, filter_func: callable) -> List[str]:
    source_files = []

    # files in root dir, no recursive
    for file in os.listdir(root_path):
        print(file)
        if file.startswith("tmp") or file.startswith("temp"):
            continue
        file_path = os.path.join(root_path, file)
        if os.path.isfile(file_path) and filter_func(file_path):
            source_files.append(str(file_path))

    # files in subdir, recursive
    for d in ("projects", "scripts", "side_job", "3rd_party"):
        for root, dirs, files in os.walk(os.path.join(root_path, d)):
            dirs[:] = [d for d in dirs if not d.startswith("tmp") and not d.startswith("temp")]  # ignore these dirs
            for file in files:
                if file.startswith("tmp") or file.startswith("temp"):
                    continue
                file_path = os.path.join(root, file)
                if filter_func(file_path):
                    source_files.append(str(file_path))
    return source_files


def find_modified_source_files(root_path: str, filter_func: callable) -> List[str]:
    git_cmd = "git --no-pager diff --name-only --diff-filter=d " + get_git_branch()
    result = subprocess.check_output(git_cmd.split())
    source_files = result.decode("utf-8").splitlines()
    source_files = [f for f in source_files if filter_func(f)]
    return [str(os.path.join(root_path, f)) for f in source_files]


def find_source_files(args, root_path: str, filter_func: callable):
    if args.all:
        files = find_all_source_files(root_path, filter_func)
    else:
        files = find_modified_source_files(root_path, filter_func)

    # filter by keywords
    if args.keyword:
        files = [x for x in files if args.keyword.lower() in x.lower()]

    # sort files, newest first
    mtime_and_files = [(os.path.getmtime(f), f) for f in files]
    mtime_and_files.sort(reverse=True)
    files = [f for t, f in mtime_and_files]

    return files


def process_files(args, filter_to_commands: Dict[Callable, Union[Callable, List[str]]], batch_process: bool = False):
    """must specify either filter_to_commands or filter_to_func"""

    script_path = os.path.abspath(__file__)
    root_path = os.path.dirname(os.path.dirname(script_path))

    def process(this_command: List[str]):
        if args.verbose:
            print(" ".join(this_command))
        result = subprocess.run(this_command)
        if result.returncode:
            sys.exit(result.returncode)

    for filter_func, cmd in filter_to_commands.items():
        files = find_source_files(args, root_path, filter_func)
        if not files:
            continue

        # callback
        if isinstance(cmd, Callable):
            if any(cmd(f) for f in files):
                sys.exit(1)
            continue

        # run shell command
        if batch_process:
            process(cmd + files)
        else:
            for f in files:
                process(cmd + [f])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="print format command")
    parser.add_argument("--all", action="store_true", help="tidy all files (not only modified ones)")
    parser.add_argument("--keyword", type=str, help="select only interested files, case insensitive")
    return parser.parse_args()


def format_main():
    args = parse_args()

    filter_to_commands = {
        is_c_cpp: ["clang-format", "-i"],
        is_cmake: ["cmake-format", "-i", "--line-width", "120"],
        is_json: format_json,
        is_python: ["black", "-q", "--line-length", "120"],
    }

    process_files(args, filter_to_commands)


if __name__ == "__main__":
    format_main()
