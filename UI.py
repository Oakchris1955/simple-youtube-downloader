import tkinter as tk
import tkinter.ttk as ttk

import sys

from threading import Thread

# import program-releated modules
import functions, classes, variables


root = tk.Tk()
root.resizable(False, False) 
'''
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)'''

# make a table to show the links
tree = ttk.Treeview(
				root,
				columns=('Name', 'URL', 'Status'),
				height=5,
				show=(
					'headings'
				)
)

# modify the table columns
'''
tree.heading('Number', text='#')
tree.column('Number', width=30)'''
tree.heading('Name', text='Video Name')
tree.column('Name', width=200)
tree.heading('URL', text='Video URL')
tree.column('URL', width=200)
tree.heading('Status', text='Video status')
tree.column('Status', width=200)

# grid the table
tree.grid(columnspan=2)


queue_input = tk.Frame(root)
queue_input.grid(row=1, columnspan=2)
'''
queue_input.grid_rowconfigure(0, weight=1)
queue_input.grid_columnconfigure(0, weight=1)
queue_input.grid_columnconfigure(1, weight=1)'''

url_entry = tk.Entry(queue_input, width=55, font="Calibri 11")
url_entry.grid(row=0, column=0, padx=2)

submit_button = tk.Button(
		queue_input,
		text="Add to queue",
		width=10,
		command=lambda:Thread(target=functions.add_vid_to_queue, args=(url_entry.get(), sys.modules[__name__], variables.videos)).start()
	)
submit_button.grid(row=0, column=1)

download_button = tk.Button(
		queue_input,
		text="Start downloading",
		command=lambda:Thread(target=functions.start_downloading, args=(variables.videos, tree)).start()
)
download_button.grid(row=0, column=2, padx=2)

err_frame = tk.Frame(root)
err_frame.grid(row=2)
'''
err_frame.grid_rowconfigure(0, weight=1)
err_frame.grid_rowconfigure(1, weight=1)
err_frame.grid_columnconfigure(0, weight=1)
err_frame.grid_columnconfigure(1, weight=1)'''

err_text = tk.Label(err_frame, text="Any errors will be outputed below:")
err_text.grid(row=0, ipadx=2, columnspan=2)

err_logger = tk.Text(err_frame, width=74, height=5, state=tk.DISABLED)
err_logger.grid(row=1, column=0)

sb_err_logger = tk.Scrollbar(err_frame, orient=tk.VERTICAL)
sb_err_logger.grid(row=1, column=1, sticky=tk.NS)

# bind the scrollbar to the err_logger
err_logger.config(yscrollcommand=sb_err_logger.set)
sb_err_logger.config(command=err_logger.yview)