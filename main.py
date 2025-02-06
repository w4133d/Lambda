import os, sys, traceback, yaml, multiprocessing
import PIL.Image, PIL.ImageOps
from utils import *

SETTINGS_PATH = 'settings.cfg'
SETTINGS: dict[ str, str | bool ] = {
	"Require input before exit": false,
	"Converted suffix": '_converted',
	"Converted format": 'PNG'
}
SUPP_IMG_READS = sorted( PIL.Image.registered_extensions() )
SUPP_IMG_WRITES = sorted( ( 'png', 'jpg', 'jpeg', 'tif', 'tiff', 'exr', 'dds' ) )

endswith_color = ( '_c', '_col', '_color', '_colour', '_albedo', '_diffuse', '_diff' )
endswith_metal = ( '_m', '_metal', '_metallic', '_metalness' )

def __init__():
	clear_console()
	
	gvar.debug = false
	log.set_level( log.Levels.ERROR )
	#console.log( "Current working directory:", os.getcwd() )
	#console.log( "__file__: ", __file__ )

def __main__():
	__init__()
	console.log( console.bold( console.bcolors.OKCYAN + "LAMBDA - Metallic-roughness to specular-gloss conversion tool" ) )

	parse_settings()

	if( sys.argv.__len__() < 3 ):
		raise_unresolved()

	# Validate that the argvs are actually image files and that we can identify them
	metallic_path = undefined
	albedo_path = undefined
	for arg in sys.argv[ 1: ]:
		file_name = path.get_base_name( arg )
		log.info( f"Checking path '{ arg }'..." )
		if( not path.exists( arg ) ):
			raise_unresolved()
		
		# Check file extension
		if( stdlib.binary_search( path.get_file_extension( arg ), SUPP_IMG_READS ) == undefined ):
			raise_unresolved()
		
		# Sort for semantic
		## Colour
		if( any( file_name.endswith( _ext ) for _ext in endswith_color ) ):
			albedo_path = arg
			log.info( "ALBEDO MAP FOUND:", path.get_base_name( albedo_path, true ) )
			continue
		## Metalness
		elif( any( file_name.endswith( _ext ) for _ext in endswith_metal ) ):
			metallic_path = arg
			log.info( "METALLIC MAP FOUND:", path.get_base_name( metallic_path, true ) )
			continue

		# Semantic type could not be found, hence image could not be identified 
		raise_unidentifiable()
	
	# This should only be true if they've passed two of the same map type (i.e. 
	# two albedo maps or two metallic maps), and the tool recognised both maps
	# because that's the only way that raise_unidentifiable() isn't called above,
	# but one of the map paths are still undefined. 
	if( any( _path == undefined for _path in ( metallic_path, albedo_path ) ) ):
		console.error( "To use this tool, you", console.bold( "MUST" ), "pass in both a metallic texture map", console.bold( "AND" ), "an albedo / diffuse map" )
		stdlib.exit()

	metallic = PIL.Image.open( metallic_path ).convert( 'L' )
	albedo = PIL.Image.open( albedo_path ).convert( 'RGB' )

	start_time = get_time()
	# Generate converted albedo map
	console.log( "Converting albedo..." )
	converted_albedo = PIL.Image.composite( PIL.Image.new( 'RGB', albedo.size ), albedo, mask=metallic )
	converted_albedo.save( ''.join( ( os.path.splitext( albedo_path )[ 0 ], SETTINGS[ 'Converted suffix' ], '.', SETTINGS[ 'Converted format' ].lower() ) ), SETTINGS[ 'Converted format' ] )
	console.log( "Albedo successfully converted in", console.timef( get_time() - start_time ) )

	start_time = get_time()
	# Step 2: Generate converted specular map
	converted_specular = PIL.Image.composite( PIL.Image.new( 'RGB', albedo.size, ( 56,56,56 ) ), albedo, mask=PIL.ImageOps.invert( metallic ) )
	converted_specular.save( ''.join( ( os.path.splitext( metallic_path )[0].replace( '_metallic', '_spec' ), '.', SETTINGS['Converted format'].lower() ) ), SETTINGS['Converted format'] )
	console.log( "Specular map successfully converted in", console.timef( get_time() - start_time ) )
	# Step 3: Output converted files



#############
# Functions #
#############

def raise_unresolved():
	console.error( "UNRESOLVED ARGUMENTS" )
	console.error( 'Please drag and drop an albedo / diffuse texture map and a metallic texture map at the same time to use this tool!' )
	stdlib.exit()

def raise_unidentifiable():
	console.error( "UNABLE TO IDENTIFY IMAGES" )
	console.error( "No suitable suffix was found (e.g. '_metallic', or '_albedo')." )
	console.error( "For this tool to work, colour / metallic maps", console.bold( 'MUST' ), "be suffixed with their respective suffix." )
	console.error( console.bold( "BAD image name:" ), "'metallic_sci_fi_panel_2k.png'" )
	console.error( console.bold( "GOOD image name:" ), "'i_sci_fi_panel_2k_metallic.png'" )
	stdlib.exit()

def parse_settings():
	global SETTINGS

	if( not path.exists( SETTINGS_PATH ) or path.is_empty( SETTINGS_PATH ) ):
		converted_formats = "# Converted formats can be PNG, TIF/TIFF, JPG, etc."
		with open( SETTINGS_PATH, 'w', encoding='utf-8' ) as cfg:
			cfg.write( f'# YAML\n{ converted_formats }\n' + yaml.safe_dump( SETTINGS, indent=4, explicit_start=true ) )
	
	with open( SETTINGS_PATH ) as cfg:
		SETTINGS = yaml.safe_load( cfg )
	
	# Validation
	SETTINGS[ 'Converted format' ] = SETTINGS[ 'Converted format' ].strip( '.' )

	if stdlib.binary_search( SETTINGS[ 'Converted format' ].lower(), SUPP_IMG_WRITES ) is undefined:
		console.error( "Unknown image conversion format mentioned inside", SETTINGS_PATH )
		console.error( "Allowed image formats:", SUPP_IMG_WRITES )
		stdlib.exit()



if __name__ == '__main__':
	try: __main__()
	except Exception as _e:
		tb = sys.exception().__traceback__
		#console.error( traceback.format_exc() )
		console.error( _e )

		dialogue.MsgBox(
			title = "UNHANDLED EXCEPTION",
			text = concatenate(
				"UNHANDLED EXCEPTION: An error has occured.",
				f"{_e}",
				"\nThere's a traceback in your log file. Please either open a new issue on the GitHub & attach the log file, or dm me your log file on discord (Username: prov3ntus). OR @ me in DEVRAW's discord server. You can find the link to the server on DEVRAW.net",
				f'\nYour log file can be located here: { os.path.abspath( "console.log" ) }',
				sep = '\n'
			),
			style = dialogue.MsgBox.Styles.ICONWARNING
		)

		print( "\nTraceback:" )
		if gvar.debug: raise _e.with_traceback( tb )
	
	if SETTINGS[ 'Require input before exit' ]:
		stdlib.exit()