#!/usr/bin/env python3
import requests
import time
import argparse
import os
import json
import subprocess

# File paths
CONFIG_FILE = 'config.json'
LAST_CHECK_FILE = 'last_check.json'

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return json.load(file)

def get_latest_sha(repo_url, check_type):
    if check_type == 'commits':
        response = requests.get(f'{repo_url}/commits')
    elif check_type == 'tags':
        response = requests.get(f'{repo_url}/tags')
    elif check_type == 'releases':
        response = requests.get(f'{repo_url}/releases')
    response.raise_for_status()
    items = response.json()
    if check_type == 'commits':
        return items[0]['sha']
    elif check_type == 'tags':
        return items[0]['name']
    elif check_type == 'releases':
        return items[0]['tag_name']

def load_last_check():
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r') as file:
            return json.load(file)
    return None

def save_last_check(data):
    with open(LAST_CHECK_FILE, 'w') as file:
        json.dump(data, file)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f'Command executed successfully with return code: {result.returncode}')
    except subprocess.CalledProcessError as e:
        print(f'Command failed with return code: {e.returncode}')

def check_for_updates(repo_url, check_type, command):
    last_check = load_last_check()
    if last_check is None or last_check['type'] != check_type:
        last_check = {'type': check_type, 'sha': None}
        save_last_check(last_check)

    last_sha = last_check['sha']
    latest_sha = get_latest_sha(repo_url, check_type)
    if last_sha is None:
        last_check['sha'] = latest_sha
        save_last_check(last_check)
        print(f'Initial {check_type[:-1]}: {latest_sha}')
    elif latest_sha != last_sha:
        print(f'New {check_type[:-1]} detected: {latest_sha}')
        last_check['sha'] = latest_sha
        save_last_check(last_check)
        if command:
            execute_command(command)
    else:
        print(f'No new {check_type}.')

if __name__ == '__main__':
    config = load_config()
    repo_url = f"https://api.github.com/repos/{config['repo']}"
    delay = config['delay']
    check_type = config['type']
    command = config.get('command', '')

    while True:
        check_for_updates(repo_url, check_type, command)
        time.sleep(delay)