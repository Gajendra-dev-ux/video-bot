# Video Bot

A Python-based bot to search, download, and upload videos from Instagram and TikTok.

## Features
- Download videos from Instagram and TikTok.
- Upload videos to a server using provided APIs.
- Auto-delete videos after successful upload.
- Concurrent processing of downloads and uploads.

## Setup
1. Clone this repository:   git clone <repository_url>
2. Install dependencies:    pip install -r requirements.txt

## bot structure
1. It contains total of 7 files(4 python files, 1 readme.md and 1 .env file) and 1 videos directory.
2. Python files - 
    main.py - contains the code that calls different functions of downloading, uploading and then removing it from local file, 
    downloader.py - contains the functions that downloads video from both platform based on platform provided on parameter from main.py , 
    uploader.py - contains functions to upload video on the server using api-integration. It involves get_upload_url then upload_video and then create_post, 
    utils.py - conatins function that logs the message with timestamp;
3. readme.md file - Gives the detailed information regarding the structure, working, features and requirements related to bot; 
4. .env(Store your sensitive credentials like the token.)
    - Add your `FLIC_TOKEN` in `.env`.

## Usage
1. Run the bot: python main.py
2. Specify the platform and video URL when prompted.
3. The bot will handle the rest!

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`