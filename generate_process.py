import os
from text_to_audio import text_to_speech_file
import time
import subprocess

def text_to_audio(folder):
    with open(f"user_uploads/{folder}/desc.txt", "r") as f:
        text = f.read()
    print(text, folder)
    text_to_speech_file(text, folder)
    

def create_reel(folder):
    input_path = f'user_uploads/{folder}/input.txt'
    audio_path = f'user_uploads/{folder}/audio.mp3'
    output_path = f'static/reels/{folder}.mp4'

    command = f'''ffmpeg -y -f concat -safe 0 -i "{input_path}" -i "{audio_path}" -fps_mode vfr -pix_fmt yuv420p -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -c:a aac -shortest "{output_path}"'''
    
    try:
        subprocess.run(command, shell=True, check=True)
        print(folder)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg failed for {folder}: {e}")

if __name__ == "__main__":
    while True:
        print("Waiting for queue...")
        with open("done.txt", "r") as f:
            done_folders = f.readlines()
        done_folders = [f[:-1] for f in done_folders]
        
        folders = os.listdir('user_uploads')
        # print(done_folders)
        # print(folders)
        for folder in folders:
            if folder not in done_folders:
                text_to_audio(folder)
                create_reel(folder)
                
                with open("done.txt", "a") as f:
                    f.write(folder+'\n')
        time.sleep(3)