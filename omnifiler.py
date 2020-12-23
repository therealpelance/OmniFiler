### Omnifiler File Utility
### Created by Rob Pelance
### V1.0 Dec 2020

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
import shutil
import os
import sys
import hashlib

HEIGHT = 700
WIDTH = 900
BACKGROUND = '#cce6ff'
LARGE_FONT = ("Verdana", 14)
NORM_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 10)
source_1 = ''
source_2 = ''
final_dest = ''
source_1_file_count = ''
source_2_file_count = ''
final_dest_file_count = ''
dupe_solution = 1

# Generic Syst Functions

def popupmsg(message):
	popup = tk.Tk()
	popup.wm_title("!")
	label = ttk.Label(popup, text=message, font=NORM_FONT)
	label.pack(side="top", fill="x", pady=10)
	B1 = ttk.Button(popup, text="Okay", command= lambda: popup.destroy())
	B1.pack()
	popup.mainloop()

# File Operations Functions

# Count Files

def count_files(path):
	file_count = 0
	for dirName, subDirs, fileList in os.walk(path):
		for files in fileList:
			file_count += 1
	return file_count

# Select Directories
def modir_select_file(choice):
	if choice == 1:
		global source_1
		source_1 = fd.askdirectory(title="Choose a directory")
		modir_source1_file_label.config(text=source_1)
		source_1_file_count = count_files(source_1)
		modir_source1_file_count.config(text=source_1_file_count)
	elif choice == 3:
		global final_dest
		final_dest = fd.askdirectory(title="Choose a directory")
		modir_dest_file_label.config(text=final_dest)
	else:
		print ("File selection error")

def medir_select_file(choice):
	if choice == 1:
		global source_1
		source_1 = fd.askdirectory(title="Choose a directory")
		medir_source1_file_label.config(text=source_1)
		source_1_file_count = count_files(source_1)
		medir_source1_file_count.config(text=source_1_file_count)
	elif choice == 2:
		global source_2
		source_2 = fd.askdirectory(title="Choose a directory")
		medir_source2_file_label.config(text=source_2)
		source_2_file_count = count_files(source_2)
		medir_source2_file_count.config(text=source_2_file_count)
	elif choice == 3:
		global final_dest
		final_dest = fd.askdirectory(title="Choose a directory")
		medir_dest_file_label.config(text=final_dest)
	else:
		print ("File selection error")

def codir_select_file(choice):
	if choice == 1:
		global source_1
		source_1 = fd.askdirectory(title="Choose a directory")
		codir_source1_file_label.config(text=source_1)
		source_1_file_count = count_files(source_1)
		codir_source1_file_count.config(text=source_1_file_count)
	elif choice == 3:
		global final_dest
		final_dest = fd.askdirectory(title="Choose a directory")
		codir_dest_file_label.config(text=final_dest)
	else:
		print ("File selection error")


def hashfile(path, blocksize = 65536):
	active_file = open(path, 'rb')
	hasher = hashlib.md5()
	buffer = active_file.read(blocksize)
	while len(buffer) > 0:
		hasher.update(buffer)
		buffer = active_file.read(blocksize)
	active_file.close()
	return hasher.hexdigest()

def findDupe(parentFolder):
	# Dupes in format {hash:[names]}
	dupes = {}
	for dirName, subdirs, fileList in os.walk(parentFolder):
		# print('Scanning %s...' % dirName)
		for filename in fileList:
			# Get the path to the file
			path = os.path.join(dirName, filename)
			# Calculate hash
			file_hash = hashfile(path)
			# Add or append the file path
			if file_hash in dupes:
				dupes[file_hash].append(path)
			else:
				dupes[file_hash] = [path]
	return dupes

# Joins two dictionaries
def joinDicts(dict1, dict2):
	for key in dict2.keys():
		if key in dict1:
			dict1[key] = dict1[key] + dict2[key]
		else:
			dict1[key] = dict2[key]
	return dict1

# Move, Merge, Copy Directories
def move_dir(source, destination):
	shutil.move(source, destination)

def dupePathsList(dict1):
	results = list(filter(lambda x: len(x) > 1, dict1.values()))
	if len(results) > 0:
		print ("Duplicate Files Identified")
		return results
	else:
		print('No duplicate files found.')

def dupe_list_clean_source(list):
	for file_set in list:
		if len(file_set) > 0:
			del (file_set[0])
		else:
			pass
	return list

def delete_dupes(list):
	for path_set in list:
		for path in path_set:
			if os.path.exists(path):
				os.remove(path)
			else:
				popupmsg("This file does not exist!")
	print ("Duplicate files deleted")

def move_directory_confirm():
	global source_1
	global final_dest
	global dupe_solution
	# Check that source and dest aren't the same directory
	if source_1 != final_dest:
		# Find all dupes in source and dest
		source1_dupe_list = findDupe(source_1)
		final_dest_dupe_list = findDupe(final_dest)
		joinDicts(source1_dupe_list, final_dest_dupe_list)
		dupe_paths_list = dupePathsList(source1_dupe_list)
		# Remove dupe files to keep from dupe list
		if dupe_solution == 1:
			dupe_list_clean_source(dupe_paths_list)
			delete_dupes(dupe_paths_list)
			# Move Source Directory to Destination
			move_dir(source_1, final_dest)
			print ("Files Moved")
			popupmsg("Files successfully moved!")
		else:
			popupmsg("Invalid Duplicate Handling Choice!")
	else:
		popupmsg("Source and Destination cannot be the same directory!")

def merge_directories_confirm():
	global source_1
	global source_2
	global final_dest
	global dupe_solution
	# Check that source and dest aren't the same directory
	if source_1 != source_2:
		# Find all dupes in source and dest
		source1_dupe_list = findDupe(source_1)
		source2_dupe_list = findDupe(source_2)
		final_dest_dupe_list = findDupe(final_dest)
		joinDicts(source1_dupe_list, source2_dupe_list)
		joinDicts(source1_dupe_list, final_dest_dupe_list)
		dupe_paths_list = dupePathsList(source1_dupe_list)
		# Remove dupe files to keep from dupe list
		if source_1 != final_dest:
			if source_2 != final_dest:
				if dupe_solution == 1:
					dupe_list_clean_source(dupe_paths_list)
					delete_dupes(dupe_paths_list)
					# Move Source Directory to Destination
					move_dir(source_1, final_dest)
					move_dir(source_2, final_dest)
					print ("Files Moved")
					popupmsg("Files successfully moved!")
				else:
					popupmsg("Invalid Duplicate Handling Choice!")
			else:
				popupmsg("Source 2 and Destination cannot be the same directory!")
		else:
			popupmsg("Source 1 and Destination cannot be the same directory!")
	else:
		popupmsg("Source directories cannot be the same directory!")

def copy_directory_confirm():
	global source_1
	global final_dest
	global dupe_solution
	# Check that source and dest aren't the same directory
	if source_1 != final_dest:
		# Find all dupes in source and dest
		source1_dupe_list = findDupe(source_1)
		final_dest_dupe_list = findDupe(final_dest)
		joinDicts(source1_dupe_list, final_dest_dupe_list)
		dupe_paths_list = dupePathsList(source1_dupe_list)
		# Remove dupe files to keep from dupe list
		if dupe_solution == 1:
			dupe_list_clean_source(dupe_paths_list)
			delete_dupes(dupe_paths_list)
			# Move Source Directory to Destination
			shutil.copytree(source_1, final_dest, dirs_exist_ok=True)
			print ("Files Moved")
			popupmsg("Files successfully moved!")
		else:
			popupmsg("Invalid Duplicate Handling Choice!")
	else:
		popupmsg("Source and Destination cannot be the same directory!")

class OmniFiler(tk.Tk):
	
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		tk.Tk.wm_title(self, "OmniFiler")
		
		container = tk.Frame(self)
		container.pack(side='top', fill='both', expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
		self.frames = {}
		
		for F in {StartPage, MoveDirectory, MergeDirectory, CopyDirectory, Settings}:
		
			frame = F(container, self)
			
			self.frames[F] = frame 
			
			frame.grid(row=0, column=0, sticky='nsew')
			
		self.show_frame(StartPage)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		content_frame = tk.Frame(self)
		# Grid Dynamic Resizing
		content_frame.pack(side='top', fill='both', expand= True)
		content_frame.grid_rowconfigure(0, weight=1)
		content_frame.grid_columnconfigure(0, weight=1)
		content_frame.grid_rowconfigure(6, weight=1)
		content_frame.grid_columnconfigure(6, weight=1)
		
		label = ttk.Label(content_frame, text="Welcome to OmniFiler", font=LARGE_FONT)
		label.grid(column=2, row=1, columnspan=3, pady=10, padx=10, sticky='n')
		
		modir_desc = ttk.Label(content_frame, text="Move a directory (folder) to a new location.", font=NORM_FONT)
		modir_desc.grid(column=2, columnspan=2, row=2, padx=5, pady=10)
		
		modir_button = ttk.Button(content_frame, text="Move a Directory", command=lambda: controller.show_frame(MoveDirectory))
		modir_button.grid(column=4, row=2, padx=5)
		
		medir_desc = ttk.Label(content_frame, text="Merge two directories (folders) into a new location.", font=NORM_FONT)
		medir_desc.grid(column=2, columnspan=2, row=3, padx=5, pady=10)
		
		medir_button = ttk.Button(content_frame, text="Merge Two Directories", command=lambda: controller.show_frame(MergeDirectory))
		medir_button.grid(column=4, row=3, padx=5)
		
		codir_desc = ttk.Label(content_frame, text="Copy a directory (folder) to a new location.", font=NORM_FONT)
		codir_desc.grid(column=2, columnspan=2, row=4, padx=5, pady=10)
		
		codir_button = ttk.Button(content_frame, text="Copy a Directory", command=lambda: controller.show_frame(CopyDirectory))
		codir_button.grid(column=4, row=4, padx=5)
		
		settings_button = ttk.Button(content_frame, text="Settings", command=lambda: controller.show_frame(Settings))
		settings_button.grid(column=1, columnspan=2, row=5, padx=5, pady=20)
		
		quit_button = ttk.Button(content_frame, text="Quit", command=quit)
		quit_button.grid(column=4, columnspan=2, row=5, padx=5, pady=20)

class MoveDirectory(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		content_frame = tk.Frame(self)
		# Grid Dynamic Resizing
		content_frame.pack(side='top', fill='both', expand= True)
		content_frame.grid_rowconfigure(0, weight=1)
		content_frame.grid_columnconfigure(0, weight=1)
		content_frame.grid_rowconfigure(100, weight=1)
		content_frame.grid_columnconfigure(6, weight=1)
		
		title_label = ttk.Label(content_frame, text="Welcome to OmniFiler", font=LARGE_FONT)
		title_label.grid(column=2, row=1, columnspan=3, pady=10, padx=10, sticky='n')
		
		subtitle_label = ttk.Label(content_frame, text="Move a Directory", font=LARGE_FONT)
		subtitle_label.grid(column=2, row=2, columnspan=3, pady=10, padx=10, sticky='n')
		
		description_label = ttk.Label(content_frame, text="Move a directory (folder) to a new location.  This feature checks all files \nin the source directory for existing duplicates in the destination directory.", font=NORM_FONT, justify='center')
		description_label.grid(column=2, row=3, columnspan=3, pady=5, padx=10, sticky='n')
		
		seperator = ttk.Separator(content_frame, orient=tk.HORIZONTAL)
		seperator.grid(column=1, row=4, columnspan=5, padx=5, pady=10, sticky='we')
		
		choose_source_directory_label = ttk.Label(content_frame, text="Choose a Source Directory", font=NORM_FONT)
		choose_source_directory_label.grid(column=1, row=5, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_source_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: modir_select_file(1))
		choose_source_directory_button.grid(column=4, row=5, padx=10, pady=10)
		
		chosen_source_directory_label = ttk.Label(content_frame, text="Source directory:", font=NORM_FONT)
		chosen_source_directory_label.grid(column=1, row=6, columnspan=2, pady=10, padx=10, sticky='w')
		
		global modir_source1_file_label
		modir_source1_file_label = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		modir_source1_file_label.grid(column=3, row=6, columnspan=2, pady=10, padx=10, sticky='w')
		
		source_1_count_label = ttk.Label(content_frame, text="Files to be moved:", font=NORM_FONT)
		source_1_count_label.grid(column=1, row=7, columnspan=2, pady=10, padx=10, sticky='w')
		
		global modir_source1_file_count
		modir_source1_file_count = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		modir_source1_file_count.grid(column=3, row=7, columnspan=2, pady=10, padx=10, sticky='w')
		
		choose_dest_directory_label = ttk.Label(content_frame, text="Choose a Destination Directory", font=NORM_FONT)
		choose_dest_directory_label.grid(column=1, row=8, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_dest_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: modir_select_file(3))
		choose_dest_directory_button.grid(column=4, row=8, padx=10, pady=10)
		
		chosen_dest_directory_label = ttk.Label(content_frame, text="Destination directory:", font=NORM_FONT)
		chosen_dest_directory_label.grid(column=1, row=9, columnspan=2, pady=10, padx=10, sticky='w')
		
		global modir_dest_file_label
		modir_dest_file_label = ttk.Label(content_frame, text=final_dest, font=NORM_FONT)
		modir_dest_file_label.grid(column=3, row=9, columnspan=2, pady=10, padx=10, sticky='w')
		
		modir_confirm_button = ttk.Button(content_frame, text="Move Directory", command=lambda: move_directory_confirm())
		modir_confirm_button.grid(column=3, row=10, pady=20, padx=10)
		
		settings_button = ttk.Button(content_frame, text="Settings", command=lambda: controller.show_frame(Settings))
		settings_button.grid(column=1, columnspan=2, row=11, padx=5, pady=20)
		
		home_button = ttk.Button(content_frame, text="Return to Home", command=lambda: controller.show_frame(StartPage))
		home_button.grid(column=3, row=11, padx=5, pady=20)
		
		quit_button = ttk.Button(content_frame, text="Quit", command=quit)
		quit_button.grid(column=4, columnspan=2, row=11, padx=5, pady=20)

class MergeDirectory(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		content_frame = tk.Frame(self)
		# Grid Dynamic Resizing
		content_frame.pack(side='top', fill='both', expand= True)
		content_frame.grid_rowconfigure(0, weight=1)
		content_frame.grid_columnconfigure(0, weight=1)
		content_frame.grid_rowconfigure(100, weight=1)
		content_frame.grid_columnconfigure(6, weight=1)
		
		title_label = ttk.Label(content_frame, text="Welcome to OmniFiler", font=LARGE_FONT)
		title_label.grid(column=2, row=1, columnspan=3, pady=10, padx=10, sticky='n')
		
		subtitle_label = ttk.Label(content_frame, text="Merge Two Directories", font=LARGE_FONT)
		subtitle_label.grid(column=2, row=2, columnspan=3, pady=10, padx=10, sticky='n')
		
		description_label = ttk.Label(content_frame, text="Merge two directories (folders) in a new location.  This feature checks all files \nin both source directories for existing duplicates in the destination directory and each other.", font=NORM_FONT, justify='center')
		description_label.grid(column=2, row=3, columnspan=3, pady=5, padx=10, sticky='n')
		
		seperator = ttk.Separator(content_frame, orient=tk.HORIZONTAL)
		seperator.grid(column=1, row=4, columnspan=5, padx=5, pady=10, sticky='we')
		
		choose_source1_directory_label = ttk.Label(content_frame, text="Choose the First Source Directory", font=NORM_FONT)
		choose_source1_directory_label.grid(column=1, row=5, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_source1_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: medir_select_file(1))
		choose_source1_directory_button.grid(column=4, row=5, padx=10, pady=10)
		
		chosen_source1_directory_label = ttk.Label(content_frame, text="First Source directory:", font=NORM_FONT)
		chosen_source1_directory_label.grid(column=1, row=6, columnspan=2, pady=10, padx=10, sticky='w')
		
		global medir_source1_file_label
		medir_source1_file_label = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		medir_source1_file_label.grid(column=3, row=6, columnspan=2, pady=10, padx=10, sticky='w')
		
		source_1_count_label = ttk.Label(content_frame, text="Files to be moved:", font=NORM_FONT)
		source_1_count_label.grid(column=1, row=7, columnspan=2, pady=10, padx=10, sticky='w')
		
		global medir_source1_file_count
		medir_source1_file_count = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		medir_source1_file_count.grid(column=3, row=7, columnspan=2, pady=10, padx=10, sticky='w')
		
		choose_source2_directory_label = ttk.Label(content_frame, text="Choose the Second Source Directory", font=NORM_FONT)
		choose_source2_directory_label.grid(column=1, row=8, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_source2_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: medir_select_file(2))
		choose_source2_directory_button.grid(column=4, row=8, padx=10, pady=10)
		
		chosen_source2_directory_label = ttk.Label(content_frame, text="Second Source directory:", font=NORM_FONT)
		chosen_source2_directory_label.grid(column=1, row=9, columnspan=2, pady=10, padx=10, sticky='w')
		
		global medir_source2_file_label
		medir_source2_file_label = ttk.Label(content_frame, text=source_2, font=NORM_FONT)
		medir_source2_file_label.grid(column=3, row=9, columnspan=2, pady=10, padx=10, sticky='w')
		
		source_2_count_label = ttk.Label(content_frame, text="Files to be moved:", font=NORM_FONT)
		source_2_count_label.grid(column=1, row=10, columnspan=2, pady=10, padx=10, sticky='w')
		
		global medir_source2_file_count
		medir_source2_file_count = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		medir_source2_file_count.grid(column=3, row=10, columnspan=2, pady=10, padx=10, sticky='w')
		
		choose_dest_directory_label = ttk.Label(content_frame, text="Choose a Destination Directory", font=NORM_FONT)
		choose_dest_directory_label.grid(column=1, row=11, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_dest_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: medir_select_file(3))
		choose_dest_directory_button.grid(column=4, row=11, padx=10, pady=10)
		
		chosen_dest_directory_label = ttk.Label(content_frame, text="Destination directory:", font=NORM_FONT)
		chosen_dest_directory_label.grid(column=1, row=12, columnspan=2, pady=10, padx=10, sticky='w')
		
		global medir_dest_file_label
		medir_dest_file_label = ttk.Label(content_frame, text=final_dest, font=NORM_FONT)
		medir_dest_file_label.grid(column=3, row=12, columnspan=2, pady=10, padx=10, sticky='w')
		
		modir_confirm_button = ttk.Button(content_frame, text="Merge Directories", command=lambda: merge_directories_confirm())
		modir_confirm_button.grid(column=3, row=13, pady=20, padx=10)
		
		settings_button = ttk.Button(content_frame, text="Settings", command=lambda: controller.show_frame(Settings))
		settings_button.grid(column=1, columnspan=2, row=14, padx=5, pady=20)
		
		home_button = ttk.Button(content_frame, text="Return to Home", command=lambda: controller.show_frame(StartPage))
		home_button.grid(column=3, row=14, padx=5, pady=20)
		
		quit_button = ttk.Button(content_frame, text="Quit", command=quit)
		quit_button.grid(column=4, columnspan=2, row=14, padx=5, pady=20)

class CopyDirectory(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		content_frame = tk.Frame(self)
		# Grid Dynamic Resizing
		content_frame.pack(side='top', fill='both', expand= True)
		content_frame.grid_rowconfigure(0, weight=1)
		content_frame.grid_columnconfigure(0, weight=1)
		content_frame.grid_rowconfigure(100, weight=1)
		content_frame.grid_columnconfigure(6, weight=1)
		
		title_label = ttk.Label(content_frame, text="Welcome to OmniFiler", font=LARGE_FONT)
		title_label.grid(column=2, row=1, columnspan=3, pady=10, padx=10, sticky='n')
		
		subtitle_label = ttk.Label(content_frame, text="Copy a Directory", font=LARGE_FONT)
		subtitle_label.grid(column=2, row=2, columnspan=3, pady=10, padx=10, sticky='n')
		
		description_label = ttk.Label(content_frame, text="Copy a directory (folder) to a new location.  This feature checks all files \nin the source directory for existing duplicates in the destination directory.", font=NORM_FONT, justify='center')
		description_label.grid(column=2, row=3, columnspan=3, pady=5, padx=10, sticky='n')
		
		seperator = ttk.Separator(content_frame, orient=tk.HORIZONTAL)
		seperator.grid(column=1, row=4, columnspan=5, padx=5, pady=10, sticky='we')
		
		choose_source_directory_label = ttk.Label(content_frame, text="Choose a Source Directory", font=NORM_FONT)
		choose_source_directory_label.grid(column=1, row=5, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_source_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: codir_select_file(1))
		choose_source_directory_button.grid(column=4, row=5, padx=10, pady=10)
		
		chosen_source_directory_label = ttk.Label(content_frame, text="Source directory:", font=NORM_FONT)
		chosen_source_directory_label.grid(column=1, row=6, columnspan=2, pady=10, padx=10, sticky='w')
		
		global codir_source1_file_label
		codir_source1_file_label = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		codir_source1_file_label.grid(column=3, row=6, columnspan=2, pady=10, padx=10, sticky='w')
		
		source_1_count_label = ttk.Label(content_frame, text="Files to be copied:", font=NORM_FONT)
		source_1_count_label.grid(column=1, row=7, columnspan=2, pady=10, padx=10, sticky='w')
		
		global codir_source1_file_count
		codir_source1_file_count = ttk.Label(content_frame, text=source_1, font=NORM_FONT)
		codir_source1_file_count.grid(column=3, row=7, columnspan=2, pady=10, padx=10, sticky='w')
		
		choose_dest_directory_label = ttk.Label(content_frame, text="Choose a Destination Directory", font=NORM_FONT)
		choose_dest_directory_label.grid(column=1, row=8, columnspan=3, pady=10, padx=10, sticky='w')
		
		choose_dest_directory_button = ttk.Button(content_frame, text="Browse", command=lambda: codir_select_file(3))
		choose_dest_directory_button.grid(column=4, row=8, padx=10, pady=10)
		
		chosen_dest_directory_label = ttk.Label(content_frame, text="Destination directory:", font=NORM_FONT)
		chosen_dest_directory_label.grid(column=1, row=9, columnspan=2, pady=10, padx=10, sticky='w')
		
		global codir_dest_file_label
		codir_dest_file_label = ttk.Label(content_frame, text=final_dest, font=NORM_FONT)
		codir_dest_file_label.grid(column=3, row=9, columnspan=2, pady=10, padx=10, sticky='w')
		
		codir_confirm_button = ttk.Button(content_frame, text="Copy Directory", command=lambda: copy_directory_confirm())
		codir_confirm_button.grid(column=3, row=10, pady=20, padx=10)
		
		settings_button = ttk.Button(content_frame, text="Settings", command=lambda: controller.show_frame(Settings))
		settings_button.grid(column=1, columnspan=2, row=11, padx=5, pady=20)
		
		home_button = ttk.Button(content_frame, text="Return to Home", command=lambda: controller.show_frame(StartPage))
		home_button.grid(column=3, row=11, padx=5, pady=20)
		
		quit_button = ttk.Button(content_frame, text="Quit", command=quit)
		quit_button.grid(column=4, columnspan=2, row=11, padx=5, pady=20)

class Settings(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		content_frame = tk.Frame(self)
		# Grid Dynamic Resizing
		content_frame.pack(side='top', fill='both', expand= True)
		content_frame.grid_rowconfigure(0, weight=1)
		content_frame.grid_columnconfigure(0, weight=1)
		content_frame.grid_rowconfigure(100, weight=1)
		content_frame.grid_columnconfigure(6, weight=1)
		
		title_label = ttk.Label(content_frame, text="Welcome to OmniFiler", font=LARGE_FONT)
		title_label.grid(column=2, row=1, columnspan=3, pady=10, padx=10, sticky='n')
		
		subtitle_label = ttk.Label(content_frame, text="Settings", font=LARGE_FONT)
		subtitle_label.grid(column=2, row=2, columnspan=3, pady=10, padx=10, sticky='n')
		
		description_label = ttk.Label(content_frame, text="Options for the overall operation of the application.", font=NORM_FONT, justify='center')
		description_label.grid(column=2, row=3, columnspan=3, pady=5, padx=10, sticky='n')
		
		settings_button = ttk.Button(content_frame, text="Return Home", command=lambda: controller.show_frame(StartPage))
		settings_button.grid(column=1, columnspan=2, row=5, padx=5, pady=20)
		
		quit_button = ttk.Button(content_frame, text="Quit", command=quit)
		quit_button.grid(column=4, columnspan=2, row=5, padx=5, pady=20)




app = OmniFiler()
app.mainloop()