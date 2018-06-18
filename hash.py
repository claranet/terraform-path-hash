#!/usr/bin/env python
#
# Generates a content hash of a path,
# ignoring file modification and access times.
#

import hashlib
import json
import os
import sys


IGNORED_NAMES = set((
    '.git',
))


def abort(message):
    """
    Exits with an error message.

    """

    sys.stderr.write(message + '\n')
    sys.exit(1)


def list_files(top_path):
    """
    Returns a sorted list of all files in a directory.

    """

    results = []

    for root, dirs, files in os.walk(top_path):
        for file_name in files:
            if file_name not in IGNORED_NAMES:
                results.append(os.path.join(root, file_name))

    results.sort()
    return results


def generate_content_hash(source_path):
    """
    Generate a content hash of the source path.

    """

    sha256 = hashlib.sha256()

    if os.path.isdir(source_path):
        source_dir = source_path
        for source_file in list_files(source_dir):
            update_hash(sha256, source_dir, source_file)
    else:
        source_dir = os.path.dirname(source_path)
        source_file = source_path
        update_hash(sha256, source_dir, source_file)

    return sha256


def update_hash(hash_obj, file_root, file_path):
    """
    Update a hashlib object with the relative path and contents of a file.

    """

    relative_path = os.path.relpath(file_path, file_root)
    hash_obj.update(relative_path.encode())

    with open(file_path, 'rb') as open_file:
        while True:
            data = open_file.read(1024)
            if not data:
                break
            hash_obj.update(data)


# Parse the query.
query = json.load(sys.stdin)
path = query['path']

# Validate the query.
if not path:
    abort('path must be set')

# Generate a hash based on file names and content.
content_hash = generate_content_hash(path)

# Output the result to Terraform.
json.dump({
    'result': content_hash.hexdigest(),
}, sys.stdout, indent=2)
sys.stdout.write('\n')
