# Lambda
A tool to convert metallic-roughness texture maps to the specular-gloss pipeline

Roughness to gloss support **will be added** at some point in the future for convenience (whenever I get the time). 

## Usage

To use Lambda, you simply drag and drop textures onto Lambda.exe and wait for the conversion to finish.

This tool needs to be able to identify which image texture is the metallic map / colour map, etc. Therefore the image name needs to be **suffixed** with its respective semantic type (i.e. `TCom_Scifi_Panel_4K_albedo.tif` | `TCom_Scifi_Panel_4K_metallic.tif`)

A table of recognised suffixes can be found here:

| Metallic 	| Albedo 	|
| ------- 	| ------- 	|
| _m 		| _c 		|
| _metal 	| _col 		|
| _metallic	| _color 	|
| 			| _colour 	|
| 			| _albedo 	|
| 			| _diffuse 	|
| 			| _diff 	|

## Settings

There is a `settings.cfg` file next to Lambda.exe.

Below you'll find each setting, as well as its respective description.

| Setting 					| Description 	|
| ------- 					| ------- 		|
| Converted format 			| The image format to output the converted files to. (Support will be added to keep original at some point lol sorry made this tool in a day `¯\_(ツ)_/¯`)	|
| Converted suffix			| A string that gets added to the end of the converted albedo file name	|
| Require input before exit	| Quick exit; If `true`, the program will not close the cmd window without the user pressing enter when prompted once conversion is finished. Recommended to set this to `true` if you want to see console output after conversion is finished, i.e. to see conversion times.	|


