import tkinter as tk
import tkinter.ttk as ttk
import asyncio

import classes

def insert_to_err_logger(logger: tk.Text, text: str) -> None:
	logger.configure(state=tk.NORMAL)
	logger.insert(tk.END, f"{text}\n")
	logger.configure(state=tk.DISABLED)

def add_vid_to_queue(url: str, mod: dict, videos: dict) -> None:
	classes.Video(url, mod)

def start_downloading(videos: list, tree: ttk.Treeview) -> None:
	# some checks to see if there is anything selected
	selection = tree.selection()
	if selection:
		# if it is, save the iid
		iid = selection[0]
	else:
		# else, return early
		return None
	# the 5 lines below get the classes.Video object with the matched iid
	my_vid = None
	for vid in videos:
		if vid.iid == iid:
			my_vid = vid
			break
	# if found something, then start downloading
	if my_vid:
		my_vid.start_downloading()
	

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