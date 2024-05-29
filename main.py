import os
import requests
import subprocess
from urllib.parse import urlparse
from os.path import basename
import pickle
import json

# Configuration
executable_url = 'https://compkiller.net/forums/cheat/getloader.php'
script_dir = os.path.dirname(os.path.abspath(__file__))
state_file = os.path.join(script_dir, 'executable_state.pkl')
cookies_file = os.path.join(script_dir, 'cookies.txt')

# HTTP headers
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

# Function to load cookies from a file
def load_cookies(file_path):
    with open(file_path, 'r') as file:
        cookies_list = json.load(file)
        cookies = {cookie['name']: cookie['value'] for cookie in cookies_list}
    return cookies

# Function to download the executable
def download_executable(url, headers, cookies):
    response = requests.get(url, headers=headers, cookies=cookies, allow_redirects=True)
    if response.status_code == 200:
        filename = response.headers.get('Content-Disposition')
        if filename:
            filename = filename.split('filename=')[-1].strip('\"')
        else:
            filename = basename(urlparse(response.url).path)
        
        target_path = os.path.join(script_dir, filename)
        with open(target_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded executable to {target_path}")
        return target_path
    else:
        print(f"Failed to download executable. Status code: {response.status_code}")
        return None

# Function to execute the executable
def execute_executable(path):
    try:
        print(f"Attempting to execute: {path}")
        subprocess.run([path], check=True)
        print(f"Executed {path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {path}. Error: {e}")

# Function to load state
def load_state():
    if os.path.exists(state_file):
        with open(state_file, 'rb') as f:
            return pickle.load(f)
    return None

# Function to save state
def save_state(state):
    with open(state_file, 'wb') as f:
        pickle.dump(state, f)

def main():
    # Load cookies
    cookies = load_cookies(cookies_file)
    
    # Load previous state and delete old executable if it exists
    previous_executable = load_state()
    if previous_executable and os.path.exists(previous_executable):
        os.remove(previous_executable)
        print(f"Deleted old executable at {previous_executable}")
    
    # Download and execute the new executable
    new_executable_path = download_executable(executable_url, headers, cookies)
    if new_executable_path:
        save_state(new_executable_path)
        execute_executable(new_executable_path)

if __name__ == '__main__':
    main()
