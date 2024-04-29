#!/bin/bash

# Check if song name is passed as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <song name>"
    exit 1
fi

SONG_NAME="$1"

# Navigate to GitHub directory
cd ~/Documents/GitHub

# Create a new repository from a template
gh repo create "$SONG_NAME" --public --template robertartress/audio_template

# Wait for 3 seconds to allow GitHub to setup the repository
sleep 3

# Retrieve repository URL
REPO_URL=$(gh repo view "$SONG_NAME" --json url -q .url)

# Check if URL retrieval was successful
if [ -z "$REPO_URL" ]; then
    echo "Failed to retrieve repository URL. Exiting."
    exit 1
fi

# Clone the repository
git clone "$REPO_URL"

# Check if clone was successful
if [ $? -ne 0 ]; then
    echo "Failed to clone repository. Exiting."
    exit 1
fi

# Change directory to the song name
cd "$SONG_NAME" || exit

# Open the directory in Finder (Mac specific)
open .
