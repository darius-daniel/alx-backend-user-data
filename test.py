#!/usr/bin/env python3
from typing import List


def require_auth(path: str, excluded_paths: List[str]) -> bool:
    """ Return True if path is not in the list of strings excluded_paths
    """
    if not path or not excluded_paths:
        return True

    if not path.endswith('/'):
        path = '{}/'.format(path)

    for excluded_path in excluded_paths:
        if excluded_path.endswith('/'):
            excluded_path = excluded_path[:-1]

        path_end = excluded_path.split('/')[-1]
        if path_end.endswith('*'):
            path_end = path_end[:-1]
        
        if path[:-1].split('/')[-1].startswith(path_end):
            return False
        
    return True


paths = [
    '/api/v1/users',
    '/api/v1/status',
    '/api/v1/stats',
]

for path in paths:
    print(require_auth(path, ['/api/v1/stat*']))
