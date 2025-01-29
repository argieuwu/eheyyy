import os
import platform
import requests
import json
from time import sleep

# Terminal Colors
class Colors:
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    skyblue = "\033[1;36m"
    white = "\033[1;37m"
    reset = "\033[0m"

def clear_screen():
    if 'termux' in platform.system().lower():
        os.system('clear')
    elif platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

class FacebookAutoPoster:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        self.token_file = "fb_token.txt"
        self.access_token = None
        self.user_id = None

    def load_token(self):
        try:
            with open(self.token_file, 'r') as f:
                self.access_token = f.read().strip()
                print(f"{Colors.green}Token loaded successfully{Colors.reset}")
                return True
        except FileNotFoundError:
            print(f"{Colors.red}Token file not found!{Colors.reset}")
            return False

    def validate_token(self):
        try:
            response = requests.get(
                f"{self.base_url}/me",
                params={'access_token': self.access_token}
            )
            if response.status_code == 200:
                self.user_id = response.json().get('id')
                return True
            print(f"{Colors.red}Token validation failed: {response.text}{Colors.reset}")
            return False
        except Exception as e:
            print(f"{Colors.red}Validation error: {str(e)}{Colors.reset}")
            return False

    def post_to_facebook(self, message):
        try:
            response = requests.post(
                f"{self.base_url}/me/feed",
                params={
                    'access_token': self.access_token,
                    'message': message
                }
            )
            return response.json()
        except Exception as e:
            print(f"{Colors.red}Posting error: {str(e)}{Colors.reset}")
            return None

    def share_post(self, post_id):
        try:
            response = requests.post(
                f"{self.base_url}/{post_id}/shares",
                params={
                    'access_token': self.access_token
                }
            )
            if response.status_code == 200:
                print(f"{Colors.green}Post shared successfully!{Colors.reset}")
                return True
            print(f"{Colors.red}Failed to share the post: {response.text}{Colors.reset}")
            return False
        except Exception as e:
            print(f"{Colors.red}Error sharing post: {str(e)}{Colors.reset}")
            return False

    def termux_file_picker(self):
        if 'termux' in platform.system().lower():
            print(f"{Colors.yellow}Opening Termux file picker...{Colors.reset}")
            os.system("termux-storage-get")
            return "file.txt"  # Update with actual selected file
        return None

def main():
    clear_screen()
    print(f"{Colors.skyblue}Facebook Auto Post Tool{Colors.reset}")
    
    poster = FacebookAutoPoster()
    
    if not poster.load_token():
        print(f"{Colors.yellow}Please save your access token in {poster.token_file}{Colors.reset}")
        return
    
    if not poster.validate_token():
        print(f"{Colors.red}Invalid access token!{Colors.reset}")
        return
    
    print(f"\n{Colors.green}Logged in as User ID: {poster.user_id}{Colors.reset}")
    
    # Get post content
    post_content = input(f"{Colors.yellow}Enter your post text: {Colors.reset}")
    
    # For Termux file attachment (basic implementation)
    if input("Attach file from Termux? (y/n): ").lower() == 'y':
        file_path = poster.termux_file_picker()
        if file_path:
            print(f"{Colors.blue}File selected: {file_path}{Colors.reset}")
            # Add file upload logic here
    
    # Post to Facebook
    result = poster.post_to_facebook(post_content)
    
    if result and 'id' in result:
        print(f"{Colors.green}Post created successfully!{Colors.reset}")
        print(f"Post ID: {result['id']}")
    else:
        print(f"{Colors.red}Failed to create post!{Colors.reset}")
    
    # Share the post
    share_choice = input(f"{Colors.yellow}Do you want to share this post? (y/n): {Colors.reset}")
    if share_choice.lower() == 'y' and result and 'id' in result:
        post_id = result['id']
        if poster.share_post(post_id):
            print(f"{Colors.green}Post shared successfully!{Colors.reset}")
        else:
            print(f"{Colors.red}Failed to share the post!{Colors.reset}")

if __name__ == "__main__":
    main()
