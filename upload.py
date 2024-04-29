import os
import re
import sys
import subprocess
from pydub import AudioSegment  # Audio handling

def get_base_path():
    """ Get base path for resources when running as an executable or script. """
    # You might want to explicitly set a base path if it's supposed to run from a specific directory.
    if getattr(sys, 'frozen', False):
        # Running as executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

base_path = get_base_path()

def upload_file(file_path):
    """ Use the dropbox-uploader script to upload the file to Dropbox and retrieve the shareable link. """
    file_name = os.path.basename(file_path)
    target_path = '/' + file_name
    dbup_path = '/Users/robertartress/Dropbox-Uploader/dropbox_uploader.sh'

    upload_result = subprocess.run([dbup_path, 'upload', file_path, target_path], capture_output=True, text=True)
    if upload_result.returncode != 0:
        print("Error during upload:", upload_result.stderr)
        return None

    share_result = subprocess.run([dbup_path, 'share', target_path], capture_output=True, text=True)
    if share_result.returncode == 0:
        output = share_result.stdout
        link_match = re.search(r"Share link: (\S+)", output)
        if link_match:
            link = link_match.group(1).strip()
            if link.endswith('0'):
                link = link[:-1] + '1'
            return link, file_name
        else:
            print("No link found in output.")
            return None
    else:
        print("Failed to retrieve shareable link:", share_result.stderr)
        return None

def convert_wav_to_flac(file_path):
    if file_path.lower().endswith('.wav'):
        flac_path = file_path[:-4] + '.flac'
        sound = AudioSegment.from_wav(file_path)
        sound.export(flac_path, format='flac')
        return flac_path
    return file_path

def update_files(link, artist_name, wav_path, flac_path):
    base_name, _ = os.path.splitext(os.path.basename(flac_path))
    flac_file_name = base_name + '.flac'

    # Assuming the files are in the main directory or a specific directory.
    html_filename = os.path.join(os.getcwd(), 'index.html')
    js_filename = os.path.join(os.getcwd(), 'playerData.js')

    html_replacements = {
        r'href="PLACEHOLDER_LINK"': f'href="{link}"',
        'PLACEHOLDER_ARTIST': artist_name
    }
    js_replacements = {
        'PLACEHOLDER_FILENAME': flac_file_name,
        'PLACEHOLDER_SONG_TITLE': base_name
    }

    update_file(html_filename, html_replacements)
    update_file(js_filename, js_replacements)

def update_file(filename, replacements):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        for placeholder, new_value in replacements.items():
            content = re.sub(placeholder, new_value, content)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    except FileNotFoundError:
        print(f"File not found: {filename}")

def main(file_path):
    artist_name = input("Enter the artist name: ")
    file_path = os.path.join(base_path, 'audio', file_path)
    flac_path = convert_wav_to_flac(file_path) if file_path.lower().endswith('.wav') else file_path
    link, _ = upload_file(file_path)
    if link:
        update_files(link, artist_name, file_path, flac_path)
        print("Upload and file update completed.")
    else:
        print("Failed to upload and retrieve link.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No file provided.")
