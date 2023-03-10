import argparse
import getpass
import os
import platform
import requests
import sys
import time

openai_api = os.environ.get('openai_api')
os_name = platform.system()
os_version = platform.release()
username = getpass.getuser()
parser = argparse.ArgumentParser(description='Console helper bot')
parser.add_argument('query', type=str, help='What do you need help with?')
parser.add_argument('--user', type=str, default=username, help='Who is asking?')
args = parser.parse_args()
cyan = "\033[36m"
endpoint = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + openai_api
}
                                                                                                                    
data = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    "max_tokens": 150,
    "messages": [
        { 
            "role": "system",
            "content": """You are a bot that helps developers and system administrators. You are accurate and efficient. This means you provide commands requested!\n
            You reply in the format: [command or code] [one brief sentence of text]! This is important!\n
            For example: df -h is the command to check free diskspace\n
            Current environment: {0} {1}""".format(os_name, os_version)
        },
        {
            "role": "user",
            "content": "My name is " + args.user +". First question: " + args.query + "? Provide detailed commmands if needed, but otherwise reply as briefly as possible!"
        }
    ]
}
try:
    response = requests.post(url=endpoint, headers=headers, json=data)
    tokens_used = response.json()['usage']['total_tokens']
    message_content = response.json()['choices'][0]['message']['content']
    print(f"{tokens_used} 🤖 {cyan}", end='', flush=True)
    for char in message_content:
        print(char, end='', flush=True)
        time.sleep(0.005) 
    print()
    sys.exit(0)
except (KeyError, ValueError) as e:
    print(f"Error: {e}")
    sys.exit(2)