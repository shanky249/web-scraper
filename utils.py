import os
from urllib.parse import urlparse, unquote

def create_directory_if_not_exists(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def get_output_path(base_dir, url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    if not path or path.endswith('/'):
        path = path.rstrip('/') + '/index.html'
    path = unquote(path)
    return os.path.join(base_dir, path[1:])
