
from tkinter import filedialog
import ctypes

# 24th March, 2024

def UserOpenDir( **options ) -> str:
	"""Opens a file dialogue & requests the user to open a folder.

	Args:
		`initialdir` | the directory that the dialog starts in
		`mustexist` | determines if selection must be an existing directory
		`parent` | the window to place the dialog on top of
		`title` | the title of the window
	"""
	return filedialog.askdirectory( **options )

def UserOpenFile( b_multiple_files: bool = False, **options ) -> str | list[ str ]:
	"""Opens a file dialogue & requests the user to open a file or multiple files.
	Will return an empty list / str if b_multiple_files is true / false respectively. 

	Args:
		`parent` | the window to place the dialog on top of\n
		`title` | the title of the window\n
		`initialdir` | the directory that the dialog starts in\n
		`initialfile` | the file selected upon opening of the dialog\n
		`filetypes` | a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed\n
		`defaultextension` | default extension to append to file (save dialogs)\n
		`b_multiple_files` | when true, selection of multiple items is allowed
	"""
	if( b_multiple_files ):
		return filedialog.askopenfilenames( **options )
	else:
		return filedialog.askopenfilename( **options )

def UserSaveAsFile( **options ) -> str:
	"""Prompts the user to save a file.
	Returns the path to the file to be saved to.

	Args:
		`parent` | the window to place the dialog on top of\n
		`title` | the title of the window\n
		`initialdir` | the directory that the dialog starts in\n
		`initialfile` | the file selected upon opening of the dialog\n
		`defaultextension` | default extension to append to file\n
		`filetypes` | a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed\n
		`confirmoverwrite` | if true, will ask the user to confirm overwriting a file\n
		`typevariable` | ???
	"""
	return filedialog.asksaveasfilename( options )



# Info Message Box
class MsgBox:
	class Styles:
		OK					= 0
		OKCANCEL			= 1
		ABORTRETRYIGNORE	= 2
		YESNOCANCEL			= 3
		YESNO				= 4
		RETRYCANCEL			= 5
		CANCELTRYCONTINUE	= 6
		NO					= 7
		TRYAGAIN			= 10
		CONTINUE			= 11
		HELP				= 0x4000

		ICONEXCLAMATION = ICONWARNING	= 0x30
		ICONINFORMATION = ICONASTERISK	= 0x40
		ICONQUESTION					= 0x20
		ICONSTOP = ICONERROR = ICONHAND = 0x10

		# These are all just 'OK'
		DEFBUTTON1 = 0
		DEFBUTTON2 = 0x100
		DEFBUTTON3 = 0x200
		DEFBUTTON4 = 0x300
		APPLMODAL	= 0
		SYSTEMMODAL = 0x1000
		TASKMODAL	= 0x2000
		DESKTOP_ONLY	= 0x20000
		RIGHT			= 0x80000 # Message text starts from the right
		RTLREADING		= 0x100000 # Title text starts from the right
		SETFOREGROUND	= 0x10000
		TOPMOST			= 0x40000
		SERVICE_NOTIF	= 0x200000

	result_to_str = {
		1: 'OK',
		2: 'Cancel',
		3: 'Abort',
		4: 'Retry',
		5: 'Ignore',
		10: 'Try Again',
		11: 'Continue',

	}

	def __new__( self, title: str, text: str, style: Styles ):
		return MsgBox.spawn( self, title, text, style )

	def spawn( self, title: str, text: str, style: Styles ):
		return ctypes.windll.user32.MessageBoxW(0, text, title, style)

class MsgBoxStyles:
	...

__all__ = [
	'UserOpenDir',
	'UserOpenFile',
	'UserSaveAsFile',
	'MsgBox'
]
