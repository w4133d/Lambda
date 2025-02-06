# Lambda
A tool to convert metallic-roughness texture maps to the specular-gloss pipeline

Roughness to gloss support **will be added** at some point in the future for convenience (whenever I get the time). For now, you can easily convert roughness maps to gloss yourself; invert the roughness map in photoshop / GIMP / paint.net.

---

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

If you want to do this in bulk, and all your textures follow a different naming scheme, I recommend getting [Microsoft Power Toys](https://learn.microsoft.com/en-us/windows/powertoys/) and using the [bulk renaming feature](https://learn.microsoft.com/en-us/windows/powertoys/powerrename) _(PowerRename)_ and get them into a format that the tool can read. 

In the future, I will update / recreate this tool (possibly in C#) with a GUI so you can input the maps themselves so the file names don't have to follow one of the supported naming schemes. 

## Settings

There is a `settings.cfg` file next to Lambda.exe.

Below you'll find each setting, as well as its respective description.

| Setting 					| Description 	|
| ------- 					| ------- 		|
| Converted format 			| The image format to output the converted files to. (Support will be added to keep original at some point lol sorry made this tool in a day `¯\_(ツ)_/¯`)	|
| Converted suffix			| A string that gets added to the end of the converted albedo file name	|
| Require input before exit	| Quick exit; If `true`, the program will not close the cmd window without the user pressing enter when prompted once conversion is finished. Recommended to set this to `true` if you want to see console output after conversion is finished, i.e. to see conversion times.	|


