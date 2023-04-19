import os

# variable to store all Videos
videos = []
download_format = 'bestaudio+bestvideo'
default_out_dir = str(os.path.join(os.getenv('USERPROFILE'), 'Downloads'))
out_dir = None