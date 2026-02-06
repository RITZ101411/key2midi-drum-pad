import requests
import json
import os
import subprocess
import tempfile
from packaging import version

GITHUB_REPO = "ritz101411/key2midi-pad"
CURRENT_VERSION = "0.1.0"

def check_for_updates():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        latest_version = data['tag_name'].lstrip('v')
        
        if version.parse(latest_version) > version.parse(CURRENT_VERSION):
            return {
                'version': latest_version,
                'url': data['html_url'],
                'download_url': None,
                'notes': data.get('body', '')
            }
        
        for asset in data.get('assets', []):
            if asset['name'].endswith('.dmg'):
                return {
                    'version': latest_version,
                    'url': data['html_url'],
                    'download_url': asset['browser_download_url'],
                    'notes': data.get('body', '')
                }
        
        return None
    except Exception as e:
        print(f'Update check failed: {e}')
        return None

def download_update(download_url):
    try:
        response = requests.get(download_url, stream=True, timeout=30)
        
        if response.status_code != 200:
            return None
        
        suffix = '.dmg' if download_url.endswith('.dmg') else '.zip'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            return tmp_file.name
    except Exception as e:
        print(f'Download failed: {e}')
        return None

def open_dmg(dmg_path):
    try:
        subprocess.run(['open', dmg_path], check=True)
        return True
    except Exception as e:
        print(f'Failed to open DMG: {e}')
        return False
