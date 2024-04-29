#!/bin/bash

# Check if directory name is passed as an argument
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory name> <path to audio file>"
    exit 1
fi

DIRECTORY_NAME="$1"
AUDIO_FILE_PATH="$2"

# Navigate to the specific directory
cd ~/Documents/GitHub/"$DIRECTORY_NAME"

# Run custom upload executable
./upload "$AUDIO_FILE_PATH"

# Add all new files to git
git add .

# Commit changes
git commit -m "Added audio file"

# Push to the repository
git push origin main

# View repository in web browser
gh repo view --web

echo "Sharing link: https://listen.elevationrecording.com/$DIRECTORY_NAME"
