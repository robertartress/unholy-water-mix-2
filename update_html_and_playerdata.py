import re
import os
import re
import sys

def resource_path(relative_path):
    """ Get the path to the resource, which is expected to be in the same directory as the executable """
    if getattr(sys, 'frozen', False):
        # If the application is frozen (executable), use the directory of the executable
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    else:
        # If running as a script, use the directory of the script
        return os.path.join(os.path.dirname(__file__), relative_path)


def update_file(filename, replacements):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    for placeholder, new_value in replacements.items():
        content = re.sub(placeholder, new_value, content)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    html_filename = resource_path('index.html')
    js_filename = resource_path('playerData.js')

    new_link = input("Enter the Dropbox link: ")
    new_artist = input("Enter the  artist name: ")
    new_file_name = input("Enter the file name: ")

    # Check if the last character of the link is "0" and replace it with "1"
    if new_link.endswith("0"):
        new_link = new_link[:-1] + "1"

    # Remove the file extension for the song title
    new_song_title, _ = os.path.splitext(new_file_name)

    # Update index.html
    html_replacements = {
        r'href="PLACEHOLDER_LINK"': f'href="{new_link}"',
        'PLACEHOLDER_ARTIST': new_artist
    }
    update_file(html_filename, html_replacements)

    # Update playerData.js
    js_replacements = {
        'PLACEHOLDER_FILENAME': new_file_name,
        'PLACEHOLDER_SONG_TITLE': new_song_title
    }
    update_file(js_filename, js_replacements)

    print("HTML and JavaScript files have been updated.")

if __name__ == "__main__":
    main()
