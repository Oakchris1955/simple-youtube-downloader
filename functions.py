import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import asyncio
from threading import Thread

import classes

import variables

def insert_to_err_logger(logger: tk.Text, text: str) -> None:
	logger.configure(state=tk.NORMAL)
	logger.insert(tk.END, f"{text}\n")
	logger.configure(state=tk.DISABLED)

def add_vid_to_queue(url: str, mod: dict, videos: dict) -> None:
	classes.Video(url, mod)

def start_downloading(videos: list, tree: ttk.Treeview) -> None:
	# obtain user selection from video tree
	selection = tree.selection()

	for video_iid in selection:
		# the 5 lines below get the classes.Video object with the same iid as the user selection
		my_vid = None
		for vid in videos:
			print(vid.iid)
			if vid.iid == video_iid:
				my_vid = vid
				break
		# if found something, then start downloading it
		if my_vid:
			Thread(target=my_vid.start_downloading).start()

def change_download_format(video_format: str):
	variables.download_format = video_format

def change_download_dir():
	download_location = filedialog.askdirectory()
	variables.out_dir = download_location
	for video in variables.videos:
		video.output_dir = download_location

def temp_change_button_text(button: tk.Button, text: str, time: int, root: tk.Tk) -> None:
	'''Unused function'''
	old_text = button.cget("text")
	# change button text
	button.config(text=text)
	root.after(
		time,
		(
			lambda:
			button.config(text=old_text)
		)
	)