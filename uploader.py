import aiohttp, os
from tqdm import tqdm
from utils import log_message

async def get_upload_url(token):
    url = "https://api.socialverseapp.com/posts/generate-upload-url"
    headers = {"Flic-Token": token, "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                log_message(f"Failed to get upload URL: {response.status}")
                return None

async def upload_video(pre_signed_url, file_path):
    try:
        file_size = os.path.getsize(file_path)
        headers = {"Content-Type": "video/mp4"}
        
        # Open file as binary stream
        with open(file_path, 'rb') as video_file:
            # Initialize the progress bar
            with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading") as progress_bar:
                async with aiohttp.ClientSession() as session:
                    # Read the entire file to ensure server compatibility
                    file_data = video_file.read()
                    
                    # Update progress manually (no chunking here)
                    progress_bar.update(len(file_data))
                    
                    # Perform the PUT request
                    async with session.put(pre_signed_url, data=file_data, headers=headers) as response:
                        response_text = await response.text()
                        log_message(f"Upload response: {response_text}")
                        
                        if response.status == 200:
                            log_message("Video uploaded successfully.")
                            return True
                        else:
                            log_message(f"Failed to upload video. Status code: {response.status}")
                            return False
    except Exception as e:
        log_message(f"Error during video upload: {e}")
        return False


async def create_post(token, title, video_hash, category_id):
    url = "https://api.socialverseapp.com/posts"
    headers = {"Flic-Token": token, "Content-Type": "application/json"}
    body = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as response:
            if response.status == 200:
                log_message("Post created successfully.")
                return await response.json()
            else:
                log_message(f"Failed to create post: {response.status}")
                return None