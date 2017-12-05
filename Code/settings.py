import os

centerlines = '/Users/lucasjakober/Documents/Semester 9/Geog4990/inputs/Centerlines_all.shp'
glaciers = '/Users/lucasjakober/Documents/Semester 9/Geog4990/inputs/rgi60_Alaska.shp'
main_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
all_shapefiles_path = os.path.join(main_path,'Shapefiles')
orig_shapefiles_path = os.path.join(all_shapefiles_path,'inputs')


input_paths = {
	'step_1' : os.path.join(os.path.join(all_shapefiles_path, 'step_1'),'in'),
	'step_2' : os.path.join(os.path.join(all_shapefiles_path, 'step_2'),'in'),
	'step_3' : os.path.join(os.path.join(all_shapefiles_path, 'step_3'),'in'),
	'step_4' : os.path.join(os.path.join(all_shapefiles_path, 'step_4'),'in'),
	'step_5' : os.path.join(os.path.join(all_shapefiles_path, 'step_5'),'in'),
	'step_6' : os.path.join(os.path.join(all_shapefiles_path, 'step_6'),'in'),
	'step_7' : os.path.join(os.path.join(all_shapefiles_path, 'step_7'),'in'),
	'step_8' : os.path.join(os.path.join(all_shapefiles_path, 'step_8'),'in'),
	'step_9' : os.path.join(os.path.join(all_shapefiles_path, 'step_9'),'in'),
	'step_10' : os.path.join(os.path.join(all_shapefiles_path, 'step_10'),'in'),
}

output_paths = {
	'step_1' : os.path.join(os.path.join(all_shapefiles_path, 'step_1'),'out'),
	'step_2' : os.path.join(os.path.join(all_shapefiles_path, 'step_2'),'out'),
	'step_3' : os.path.join(os.path.join(all_shapefiles_path, 'step_3'),'out'),
	'step_4' : os.path.join(os.path.join(all_shapefiles_path, 'step_4'),'out'),
	'step_5' : os.path.join(os.path.join(all_shapefiles_path, 'step_5'),'out'),
	'step_6' : os.path.join(os.path.join(all_shapefiles_path, 'step_6'),'out'),
	'step_7' : os.path.join(os.path.join(all_shapefiles_path, 'step_7'),'out'),
	'step_8' : os.path.join(os.path.join(all_shapefiles_path, 'step_8'),'out'),
	'step_9' : os.path.join(os.path.join(all_shapefiles_path, 'step_9'),'out'),
	'step_10' : os.path.join(os.path.join(all_shapefiles_path, 'step_10'),'out'),
}

variable_distance_buffer = True

