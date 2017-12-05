import utility

import os
import sys
from mmqgis import mmqgis_library
import operator
from qgis.core import *

app = QgsApplication([],True)
QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)
app.initQgis()

import PyQt4
from PyQt4.QtCore import QVariant
import processing
from processing.core.Processing import Processing
Processing.initialize()
Processing.updateAlgsList()


def step_1():
	c_path_in = os.path.join(utility.getPath_inputs()['step_1'],os.path.basename(utility.getPath_centerlines()))
	g_path_in = os.path.join(utility.getPath_inputs()['step_1'],os.path.basename(utility.getPath_glaciers()))
	
	print c_path_in
	print g_path_in

	c_path_out = utility.getPath_outputs()['step_1']
	g_path_out = utility.getPath_outputs()['step_1']

	
	utility.copyShapefile(c_path_in,c_path_out)
	utility.copyShapefile(g_path_in,g_path_out)

	c_path_out = os.path.join(utility.getPath_outputs()['step_1'],utility.getPath_centerlines())
	g_path_out = os.path.join(utility.getPath_outputs()['step_1'],utility.getPath_glaciers())


	centerline = QgsVectorLayer(c_path_out, os.path.basename(c_path_out), "ogr")
	glacier = QgsVectorLayer(g_path_out, os.path.basename(g_path_out), "ogr")

	# Check that input files are valid.
	if not centerline.isValid():
		print "%s failed to load!" % centerline.name()
	if not centerline.crs().isValid():
		print "%s does not have a valid CRS." % centerline.name()
	if not glacier.isValid():
		print "%s failed to load!" % glacier.name()
	if not glacier.crs().isValid():
		print "%s does not have a valid CRS." % glacier.name()

	# Delete all unecessary fields.
	print "Cleaning attribute table... (%s)" % glacier.name()
	glacierFieldsToKeep = ['RGIId','GLIMSId']
	glacierFields = [field.name() for field in glacier.pendingFields()]
	fieldsDeleted = 0
	for f in glacierFields:
		if f not in glacierFieldsToKeep:
			fieldID = glacier.fieldNameIndex(f)
			print "  delete field... (%s)" % f
			glacier.dataProvider().deleteAttributes([fieldID])
			glacier.updateFields()
			fieldsDeleted+=1
	print "%d fields deleted from %s" % (fieldsDeleted, glacier.name())

	print "Cleaning attribute table... (%s)" % centerline.name()
	centerlineFieldsToKeep = ['GLIMSID','OBJECTID','LENGTH_CL']
	centerlineFields = [field.name() for field in centerline.pendingFields()]
	fieldsDeleted = 0
	for f in centerlineFields:
		if f not in centerlineFieldsToKeep:
			fieldID = centerline.fieldNameIndex(f)
			print "  deleting field... (%s)" % f
			centerline.dataProvider().deleteAttributes([fieldID])
			centerline.updateFields()
			fieldsDeleted+=1
	print "%d fields deleted from %s" % (fieldsDeleted, centerline.name())















