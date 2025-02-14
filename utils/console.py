import utils.log
from utils import WARNING_STR, ERROR_STR
from utils.stdlib import CONSOLE_STR

# Colour text when printing
class bcolors:
	"""Struct of constants to color console text when printing.
	Usage: print( bcolors.OKBLUE + "This text is blue" + bcolors.ENDC + Bold(" and now it's BOLD!") )
	
	Variables:
	- bcolors.HEADER
	- bcolors.OKBLUE
	- bcolors.OKCYAN
	- bcolors.OKGREEN
	- bcolors.WARNING
	- bcolors.FAIL
	- bcolors.ENDC
	- bcolors.BOLD | use console.bold()
	- bcolors.UNDERLINE | use console.underline()
	"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

	def __str__( self ):
		"""Return str(self)"""
		return {
			'HEADER': '\033[95m', 'OKBLUE': '\033[94m',
			'OKCYAN': '\033[96m', 'OKGREEN': '\033[92m',
			'WARNING': '\033[93m', 'FAIL': '\033[91m',
			'ENDC': '\033[0m', 'BOLD': '\033[1m',
			'UNDERLINE': '\033[4m'
		}.__str__()

	__list__ = [
		'\033[95m', '\033[94m', '\033[96m',
		'\033[92m', '\033[93m', '\033[91m',
		'\033[0m', '\033[1m', '\033[4m'
	]

def log( *print_args, sep: str = ' ', end: str ='\n' ):
	"""Prints to console & writes print statements to the current log file

	`console.log` can be found in the same directory as the utils folder.
	"""

	print_str = sep.join( map( str, print_args ) )
	print( CONSOLE_STR + print_str + bcolors.ENDC, end=end )
	utils.log.info( print_str )


def warning( *args, sep = f' { bcolors.WARNING }', end = '\n' ):
	_str = f'{ sep.join( map( str, args ) ) }'
	
	print( f'{ bcolors.WARNING }{ WARNING_STR } { _str }{ bcolors.ENDC }', end = end )
	utils.log.warning( _str )

def error( *args, sep = f' { bcolors.FAIL }', end = '\n' ):
	_str = sep.join( map( str, args ) )

	print( f'{ bcolors.FAIL }{ ERROR_STR } { _str }{ bcolors.ENDC }', end = end )
	utils.log.error( _str )

def bold( *args, sep = ' ' ):
	"""Returns a string with a bold format. 

	If you were to print this string, text would be bold in console
	
	You must clear console first for cmd otherwise it'll break"""
	
	return bcolors.BOLD + sep.join( map( str, args ) ) + bcolors.ENDC

def underline( *args, sep = ' ' ):
	"""Returns a string with an underlined format. 

	If you were to print this string, text would be underlined in console
	
	You must clear console first for cmd otherwise it'll break"""
	return bcolors.UNDERLINE + sep.join( map( str, args ) ) + bcolors.ENDC

# Progress bar
def progress_bar( iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 100, fill: str = '█', print_end: str = "\r" ):
	"""Call me in a loop to create progress bar in the console.\n
	**WARNING!** I'm *very expensive*!

	Args:
		iteration (int): Current iteration of the loop.
		total (int): Total iterations of the loop.
		prefix (str, optional): String to append to the start of the progress bar. Defaults to `''`.
		suffix (str, optional): String to append to the end of the progress bar. Defaults to `''`.
		decimals (int, optional): Positive number of decimals in percent complete. Defaults to `1`.
		length (int, optional): Character length of the progress bar. Defaults to `100`.
		fill (str, optional): The progress bar's fill character. Defaults to `'█'`.
		print_end (str, optional): The end character to print. Defaults to `"\\r"`.
	"""

	#str_percent = ( "{0:." + str(decimals) + "f}" ).format( 100 * ( iteration / float( total ) ) )
	filledLength = int( length * iteration // total )
	#bar = fill * filledLength + '-' * ( length - filledLength )
	
	percent = iteration / total
	if percent < .5: bcolour = bcolors.FAIL
	elif percent < .8: bcolour = bcolors.WARNING
	else:
		bcolour = bcolors.OKGREEN
		if iteration == total: print_end = '\n'
	
	#print( f'\r{ prefix } { bcolour }|{ bar }| { str_percent }%{ bcolors.ENDC } { suffix }', end = print_end )
	print( f'\r{ prefix } { bcolour }|{ fill * filledLength + "-" * ( length - filledLength ) }| { ( "{0:." + str(decimals) + "f}" ).format( 100 * ( iteration / float( total ) ) ) }%{ bcolors.ENDC } { suffix }', end = print_end )

units_of_time = (
	( 'weeks',	604800	),
	( 'days',	86400	),
	( 'hours',	3600	),
	( 'mins',	60		),
	( 'secs',	1		),
	( 'ms',		10**-3	),
	( 'μs',		10**-6	)
)

def timef( seconds: float, granularity=2 ):
	"""Formats the given time from seconds into a readable string.

	E.g.:
	- 180 (w/ a granularity of 2) would return "3 mins"
	- 192 (w/ a granularity of 2) would return "3 mins, 12 secs"
	- 3604 (w/ a granularity of 2) would return "1 hour, 4 secs"
	- 4825 (w/ a granularity of 2) would return "1 hour, 20 mins"
	- 4825 (w/ a granularity of 3) would return "1 hour, 20 mins, 25 secs"
	"""
	result = []

	for name, count in units_of_time:
		value = seconds // count
		if value:
			seconds -= value * count
			if value == 1:
				name = name.rstrip( 's' )
			result.append( "{} {}".format( int( value ), name ) )

	return ', '.join( result[ :granularity ] )

byte_intervals = (
	( 'GB',		10**9	),
	( 'MB',		10**6	),
	( 'KB',		10**3	),
	( 'bytes',	1		),
	( 'bits',	.125	)
)

def bytesf( _bytes: float, granularity = 2 ):
	"""Formats a given byte int into a readable str.
	Useful when outputing size of files.

	E.g.:
	- 650211430 (w/ a granularity of 2) would return "650 MB, 211 KB"
	- 650211430 (w/ a granularity of 3) would return "650 MB, 211 KB, 430 bytes"
	"""
	result = []

	for name, count in units_of_time:
		value = _bytes // count
		if value:
			_bytes -= value * count
			if value == 1:
				name = name.rstrip( 's' )
			result.append( "{} {}".format( int( value ), name ) )
	
	return ', '.join( result[ :granularity ] )

__all__ = [ 'bcolors', 'log', 'warning', 'error', 'bold', 'underline', 'progress_bar', 'timef', 'bytesf' ]
