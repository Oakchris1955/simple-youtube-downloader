# import UI libs
import tkinter as tk
import tkinter.ttk as ttk
# import the Youtube video downloader
import yt_dlp
# import JSON to parse JSON strings
import json
# import os module to get misc stuff about the user
import os


# import program-related modules
import functions, variables

class Video:
	default_options = {
		# downloads folder path
		'outtmpl': '%(title)s.%(ext)s',
		'progress_hooks': []
	} 
	status_dict = {
		"G": "Gathering info...",
		"Q": "Queued for downloading",
		"B": "Download initiated and will begin shortly",
		"D": "Downloaded {percent}% from total of {size}",
		"O": "Done"
	}

	def __init__(self, url: str, UI: object, options: dict = default_options):
		self.status = "G"  # for more info about video status, check self.status_dict
		self.root = UI.root
		self.UI = UI
		self.url = url
		self.options = options
		self.output_dir = variables.out_dir
		# this variable used to be below self.percent = "?" in self.start_downloading, but because of a bug was moved here
		self.downloaded_formats = []

		# also, add _download_progress_hook to progrss hooks
		self.options["progress_hooks"].append(self._download_progress_hook)

		# if URL already inputed, quit
		if self.url in list(vid.url for vid in variables.videos):
			functions.insert_to_err_logger(self.UI.err_logger, "URL already inputed")
			return None

		# and add self to videos list
		variables.videos.append(self)

		# add an incomplete version of the info to the video queue
		self.iid = self.add_to_queue(self.UI.tree, has_iid=False)
		# get video info
		try:
			self.video_info = self.get_video_info()
		except yt_dlp.DownloadError:
			functions.insert_to_err_logger(self.UI.err_logger, f'A download error occured while downloading "{self.url}"')
			self.UI.tree.delete(self.iid)
			variables.videos.remove(self)
		else:
			# also, save some important data
			self.title = self.video_info["title"]
			self.total_size = self._get_total_formats_size(frmt['format_id'] for frmt in self.video_info['requested_downloads'])
			self.human_total_size = self._humansize(self.total_size)
			# change video status
			self.status = "Q"
			# don't forget to update the table info too
			self.add_to_queue(self.UI.tree)
			# and save the requested formats
			save_order = [0, 1]
			self.requested_formats = self.video_info["requested_downloads"]
			if len(self.requested_formats) != 1:
				if self.requested_formats[1]["fps"]:
					save_order.reverse()
				# unused variables
				self.best_video = self.requested_formats[save_order[0]]
				self.best_audio = self.requested_formats[save_order[1]]


	def start_downloading(self) -> None:
		# check if status is fine to begin downloading
		if self.status == 'G':
			functions.insert_to_err_logger(self.UI.err_logger, 'Please wait until enough info are gathered')
		elif self.status in ['B', 'D']:
			functions.insert_to_err_logger(self.UI.err_logger, 'Download has began, please wait for it to finish')
		elif self.status == 'O':
			functions.insert_to_err_logger(self.UI.err_logger, 'This video is already downloaded')
		# and don't forget to stop function if not ready to begin downloading
		if self.status != 'Q':
			return None

		# create a temporary copy of self.options
		options = self.options.copy()
		print(self.output_dir)
		options['outtmpl'] = (self.output_dir or variables.default_out_dir) + '/' + options['outtmpl']
		options['format'] = variables.download_format

		# update status
		self._update_status(self.UI.tree, "B")
		# also, set some variables
		self.percent = "?"
		with yt_dlp.YoutubeDL(options) as ydl:
			self._update_status(self.UI.tree, "D")
			ydl.download(self.url)
			# once done with downloading, change status and update one last time
			self._update_status(self.UI.tree, "O")


	def get_video_info(self) -> dict:
		# update the UI
		self.root.update_idletasks()
		with yt_dlp.YoutubeDL({'simulate':True, 'format': variables.download_format}) as ydl:
			return ydl.sanitize_info(ydl.extract_info(self.url))


	def _get_total_formats_size(self, formats: list) -> int:
		total_size = 0
		for frmt in self.video_info['requested_downloads']:
			if frmt['format_id'] in formats:
				total_size += frmt['filesize']
		return total_size
			

	def _download_progress_hook(self, info: dict):
		# to begin with, check if currently downloading audio or video (currently unused)
		if info['info_dict']['fps']:
			# if audio, save this as a variable
			current_type = 'audio'
		else:
			# else, it is a video
			current_type = 'video'

		current_format = info['info_dict']['format_id']
		if current_format not in [frmt for frmt in self.downloaded_formats]:
			self.downloaded_formats.append(current_format)

		if info["status"] == "downloading":
			# update the downloaded bytes
			total_downloaded_bytes = self._get_total_formats_size(self.downloaded_formats[:-1])+info['downloaded_bytes']
			# also, update percent downloaded
			self.percent = round(total_downloaded_bytes/self.total_size*100, 2)
		
		# lastly, update the displayed status
		self._update_status(self.UI.tree)


	def _humansize(self, nbytes: int):
		'''Code obtained from https://stackoverflow.com/a/14996816'''
		suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
		i = 0
		while nbytes >= 1024 and i < len(suffixes)-1:
			nbytes /= 1024.
			i += 1
		f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
		return '%s %s' % (f, suffixes[i])


	def add_to_queue(self, parent: ttk.Treeview, has_iid: bool = True) -> int or None:
		if has_iid:
			parent.item(self.iid, values=(self.title, self.url, self.status_dict[self.status]))
		else:
			return parent.insert("", tk.END, values=("Unknown", self.url, self.status_dict[self.status]))
	
	def _update_status(self, parent: ttk.Treeview, new_status: str = None, *args) -> None:
		if new_status:
			self.status = new_status
		
		status = self.status_dict[self.status]

		# if status is "D", treat the string differently
		if self.status == "D":
			status = status.format(percent=self.percent, size=self.human_total_size)

		parent.set(self.iid, column="Status", value=status)