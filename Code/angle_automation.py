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
	in_a = os.path.join(utility.getPath_inputs()['step_1'],os.path.basename(utility.getPath_centerlines()))
	in_b = os.path.join(utility.getPath_inputs()['step_1'],os.path.basename(utility.getPath_glaciers()))

	out_a = utility.getPath_outputs()['step_1']
	out_b = utility.getPath_outputs()['step_1']
	
	utility.copyShapefile(in_a,out_a)
	utility.copyShapefile(in_b,out_b)

	out_a = os.path.join(utility.getPath_outputs()['step_1'],utility.getPath_centerlines())
	out_b = os.path.join(utility.getPath_outputs()['step_1'],utility.getPath_glaciers())

	centerline = QgsVectorLayer(out_a, os.path.basename(out_a), "ogr")
	glacier = QgsVectorLayer(out_b, os.path.basename(out_b), "ogr")

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


def step_2():
	# Step 3: Reproject both shapefiles to EPSG3395 WGS '84 Transverse Mercator (for distance calculations in meters)
	in_a = os.path.join(utility.getPath_outputs()['step_1'],utility.getPath_centerlines())
	in_b = os.path.join(utility.getPath_outputs()['step_1'],utility.getPath_glaciers())

	out_a = os.path.join(utility.getPath_outputs()['step_2'],'reproject_'+os.path.basename(in_a))
	out_b = os.path.join(utility.getPath_outputs()['step_2'],'reproject_'+os.path.basename(in_b))

	centerline = QgsVectorLayer(in_a, os.path.basename(in_a), "ogr")
	glacier = QgsVectorLayer(in_b, os.path.basename(in_b), "ogr")

	crs = QgsCoordinateReferenceSystem(3395, QgsCoordinateReferenceSystem.EpsgCrsId)
	print "Coordinate Reference System (CRS) %s %s will be used." % (crs.authid(), crs.description())
	
	print "--> %s's CRS is: %s" % (centerline.name(),centerline.crs().authid())
	print "		Reprojecting %s to %s %s" % (centerline.name(), crs.authid() ,crs.description())
	processing.runalg('qgis:reprojectlayer', centerline, crs.authid(), out_a)
	print "--> %s's CRS is: %s" % (glacier.name(),glacier.crs().authid())
	print "		Reprojecting %s to %s %s" % (glacier.name(), crs.authid(), crs.description())
	processing.runalg('qgis:reprojectlayer', glacier, crs.authid(), out_b)












