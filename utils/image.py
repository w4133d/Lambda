from utils import console
import numpy as np, PIL.Image

def get_dimensions( _img_path: str ):
	#return imread( _img_path ).shape[ :2 ]
	return PIL.Image.open( _img_path ).size

def has_alpha( _img_path: str ):
	'''Returns True if image path has alpha channel'''
	try:
		return PIL.Image.open( _img_path ).has_transparency_data
	except AttributeError:
		console.log( 'engine.ImageHasAlpha(): Falling back to slower method for transparency deduction' )
	
	return True if np.array( PIL.Image.open( _img_path ) ).shape[ -1 ] == 4 else False
	
	# The below code works fine, except it's really
	# expensive & slows the whole program down by 50-100x
	# It's probably because I'm iterating over every pixel and
	# checking its alpha value, if it even has any (if mode == 'P')
	img = PIL.Image.open( _img_path )

	if img.info.get( "transparency", None ) is not None:
		return True

	if img.mode == "P":
		transparent = img.info.get( "transparency", -1 )
		for _, index in img.getcolors():
			if index == transparent:
				return True
	elif img.mode == "RGBA":
		extrema = img.getextrema()
		if extrema[ 3 ][ 0 ] < 255:
			return True

	return False
