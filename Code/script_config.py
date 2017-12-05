import os
import sys
import utility


def configure_folders():
	main_path = utility.getPath_main()
	if not os.path.isdir(main_path):
		print "Invalid main_path parameter in settings.py"
		sys.exit(1)

	shapefile_folder = utility.getPath_all_shapefiles()
	input_folder = utility.getPath_orig_shapefiles()
	if not os.path.isdir(shapefile_folder):
		os.mkdir(shapefile_folder)
	if not os.path.isdir(input_folder):
		os.mkdir(input_folder)
	inputs = utility.getPath_inputs()
	outputs = utility.getPath_outputs()
	for key in inputs:
		step_path = os.path.dirname(inputs[key])
		if not os.path.isdir(step_path):
			os.mkdir(step_path)
		if not os.path.isdir(inputs[key]):
			os.mkdir(inputs[key])
	for key in outputs:
		if not os.path.isdir(outputs[key]):
			os.mkdir(outputs[key])
	if not os.path.isfile(utility.getPath_centerlines()):
		return "Not a valid input centerline filepath"
		sys.exit(1)
	if not os.path.isfile(utility.getPath_glaciers()):
		return "Not a valid input glacier filepath"
		sys.exit(1)
	utility.copyShapefile(utility.getPath_centerlines(),input_folder)
	utility.copyShapefile(utility.getPath_glaciers(),input_folder)

	utility.copyShapefile(utility.getPath_centerlines(),inputs['step_1'])
	utility.copyShapefile(utility.getPath_glaciers(),inputs['step_1'])

configure_folders()




