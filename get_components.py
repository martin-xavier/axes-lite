#!/usr/bin/env python
"""
Get AXES-LITE components and store paths - see README.md for details
"""

import os
import subprocess
import json

from scaffoldutils import utils

with open(utils.COMPONENT_CFGS_FILE, 'r') as f:
    component_opts = json.load(f)

ensure_dirs = [
    component_opts['collection']['paths']['private_data'],
    component_opts['collection']['paths']['public_data'],
    component_opts['collection']['paths']['index_data'],
    component_opts['collection']['paths']['index_data'] + '/db',
    'logs'
]

component_repos = [
    ('git', 'cpuvisor-srv', 'https://github.com/kencoken/cpuvisor-srv.git', 'al-integration-prep'),
    ('git', 'imsearch-tools', 'https://github.com/kencoken/imsearch-tools.git'),
    ('git', 'medpackage', '--branch axes-lite --single-branch https://github.com/martin-xavier/medpackage.git'),
    ('hg' , 'limas', 'https://bitbucket.org/alyr/limas'),
    ('git', 'axes-home', 'https://github.com/kevinmcguinness/axes-home.git'),
    ('git', 'axes-research', 'https://github.com/kevinmcguinness/axes-research.git'),
]


def ensure_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def repo_clone(cmd, component, url, branch=None):
    default_val = '<PATH>'
    path = component_opts['components'][component]
    if path is None or path == default_val:
        return False
    if os.path.isdir(path):
        return False
    clone_cmd = ' '.join([cmd, 'clone', url, path])
    subprocess.call(clone_cmd, shell=True)
    if branch:
        with utils.change_cwd(path):
            checkout_cmd = ' '.join([cmd, 'checkout', branch])
            subprocess.call(checkout_cmd, shell=True)
    return True


# main entry point
# ................

def main():
    # Create dirs
    map(ensure_dir, ensure_dirs)

    # Clone repos
    for repo in component_repos:
        repo_clone(*repo)


if __name__ == '__main__':
    main()
