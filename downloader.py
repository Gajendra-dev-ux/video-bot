import os, glob
from TikTokApi import TikTokApi
from datetime import datetime
import instaloader
from utils import log_message

async def download_instagram_video(video_url, output_path):
    try:
        loader = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(loader.context, video_url.split("/")[-2])
        loader.download_post(post, target=output_path)
        cleanup_extra_files(output_path)  # Clean up unnecessary files
        log_message("Instagram video downloaded successfully.")

        # Construct the filename for the video and return it
        video_filename = f"{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}.mp4"
        return video_filename
            
    except Exception as e:
        log_message(f"Failed to download Instagram video: {e}")
        return None



async def download_tiktok_video(video_url, output_path):
    try:
        # Initialize TikTokApi and download video data
        with TikTokApi() as api:
            video_data = api.video(url=video_url).bytes()

        # Generate a unique filename based on the current timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S_UTC')
        video_filename = f"{timestamp}.mp4"
        video_path = os.path.join(output_path, video_filename)

        # Write video data to the file
        with open(video_path, 'wb') as video_file:
            video_file.write(video_data)

        log_message("TikTok video downloaded successfully.")
        return video_filename

    except Exception as e:
        log_message(f"Failed to download TikTok video: {e}")
        return None



async def download_video(platform, video_url, output_path):
    if not os.path.exists("videos"):
        os.makedirs("videos")
    if platform == 'instagram':
        return await download_instagram_video(video_url, output_path)
    elif platform == 'tiktok':
        await download_tiktok_video(video_url, output_path)
    else:
        log_message("Unsupported platform.")


def cleanup_extra_files(directory):#removes extra files other than .mp4
    extensions_to_remove = ['*.jpg', '*.json','*.txt', '*.json.xz']
    for ext in extensions_to_remove:
        for file in glob.glob(os.path.join(directory, ext)):
            os.remove(file)