import asyncio, os
from utils import log_message
from downloader import download_video
from uploader import get_upload_url, upload_video, create_post
from dotenv import load_dotenv

async def main():
    # first take input for the platform whose video you wants to download
    platform = input("Enter Platform name either instagram or tiktok : ")
    # paste video_url ex- "https://www.instagram.com/reel/DC6miieiK7s/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
    video_url = input("Paste the link of video you wants to download :")
    video_dir = "videos"

    #download video and store the file name
    video_filename = await download_video(platform, video_url, video_dir)
    
    if video_filename:
        # Construct the full video path
        video_path = os.path.join(video_dir, video_filename)
        
        # Process the video (upload and delete)
        load_dotenv()
        token = os.getenv("FLIC_TOKEN")
        title = "Uploaded Video"
        category_id = None

        upload_data = await get_upload_url(token)
        if upload_data:
            upload_url = upload_data["url"]
            video_hash = upload_data["hash"]
            if await upload_video(upload_url, video_path):
                await create_post(token, title, video_hash, category_id)
                os.remove(video_path)
                log_message(f"File {video_path} deleted after upload.")
        
    else:
        log_message("Video download failed, skipping upload.")



if __name__ == "__main__":
    asyncio.run(main())
