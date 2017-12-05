import utility
import script_config

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

	out_a = os.path.join(utility.getPath_outputs()['step_1'],os.path.basename(utility.getPath_centerlines()))
	out_b = os.path.join(utility.getPath_outputs()['step_1'],os.path.basename(utility.getPath_glaciers()))

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
	in_a = os.path.join(utility.getPath_outputs()['step_1'],os.path.basename(utility.getPath_centerlines()))
	in_b = os.path.join(utility.getPath_outputs()['step_1'],os.path.basename(utility.getPath_glaciers()))
	print in_a
	print in_b


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


def step_3():
	# Step 3: Add length field to Centerline Shapefile
	in_a = os.path.join(utility.getPath_outputs()['step_2'],'reproject_'+os.path.basename(utility.getPath_centerlines()))
	utility.copyShapefile(in_a, utility.getPath_outputs()['step_3'])
	out_a = os.path.join(utility.getPath_outputs()['step_3'],'reproject_'+os.path.basename(utility.getPath_centerlines()))

	centerline = QgsVectorLayer(out_a, os.path.basename(out_a), "ogr")
	# lineLayer.dataProvider().AddAttributes([QgsField("LENGTH_M", QVariant.Double)])
	# lineLayer.updateFields()
	centerline.startEditing()
	centerline.addAttribute( QgsField( 'LENGTH_M', QVariant.Double ) )
	idx = centerline.fieldNameIndex( 'LENGTH_M' )
	e = QgsExpression( '$LENGTH' )
	e.prepare( centerline.pendingFields() )
	for f in centerline.getFeatures():
	    f[idx] = e.evaluate( f )
	    centerline.updateFeature( f )
	centerline.commitChanges()


def step_4a():
	# Step 4a: Extract one glacier polygon and all corresponding centerlines by GLIMS Id
	# REPEAT this step for every unique GLIMSID
	glimsId = 'G220886E60666N'
	print "Processing glacier: "+glimsId

	in_a = os.path.join(utility.getPath_outputs()['step_3'],'reproject_'+os.path.basename(utility.getPath_centerlines()))
	out_a = os.path.join(utility.getPath_outputs()['step_4'], glimsId)
	if not os.path.isdir(out_a):
		os.mkdir(out_a)
	out_a = os.path.join(out_a, 'ALL_lines_'+glimsId+'.shp')
	processing.runalg("qgis:extractbyattribute",in_a,"GLIMSID",0,glimsId,out_a)
	
	centerlines = QgsVectorLayer(out_a, os.path.basename(out_a), "ogr")
	res = centerlines.dataProvider().addAttributes([QgsField("LINE_ID", QVariant.Int)])
	centerlines.updateFields()


	in_b = os.path.join(utility.getPath_outputs()['step_2'],'reproject_'+os.path.basename(utility.getPath_glaciers()))
	out_b = os.path.join(os.path.dirname(out_a),"boundary_"+glimsId+"_poly.shp")
	processing.runalg("qgis:extractbyattribute",in_b,"GLIMSId",0,glimsId, out_b)

	in_c = out_b
	out_c = os.path.join(os.path.dirname(out_a),"boundary_"+glimsId+"_line.shp")
	processing.runalg("qgis:polygonstolines",in_c, out_c)

	in_d = out_c
	out_d = os.path.join(os.path.dirname(out_a),"diss_bound_"+glimsId+"_line.shp")
	processing.runalg("qgis:dissolve",in_d,False,"GLIMSId;RGIId",out_d)
	

def step_4b(glimsId):
	# Step 4b: Sort the centerlines in descending order of field "LENGTH_M"

	in_a = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId),'ALL_lines_'+glimsId+'.shp')
	centerline = QgsVectorLayer(in_a,os.path.basename(in_a),"ogr")
 	
	out_a = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId),"ALL_sorted_"+glimsId+".shp")

	writer = QgsVectorFileWriter(out_a, "CP1250", centerline.fields(), centerline.wkbType(), centerline.crs(), "ESRI Shapefile")
	if writer.hasError() != QgsVectorFileWriter.NoError:
		print("Error when creating shapefile: ", writer.errorMessage())
	sortindex = centerline.fieldNameIndex("LENGTH_M")
	direction = "descending"
	table = []
	for index, feature in enumerate(centerline.getFeatures()):
		record = feature.id(), feature.attributes()[sortindex]
		table.append(record)
	if (direction.lower() == "descending"):
		table.sort(key = operator.itemgetter(1), reverse=True)
	else:
		table.sort(key = operator.itemgetter(1))
	# Add features to new shapefile in same order as sorted table
	writecount = 0
	provider = centerline.dataProvider()
	objectIdIndex = centerline.fieldNameIndex("OBJECTID")
	print (
		"  Glacier has "+str(len(table))+" centerlines. Sorting centerlines by length.\n"+
		"  Sorted file will be written to: \n"+
		"    "+out_a)
	for index, record in enumerate(table):
		iterator = centerline.getFeatures(QgsFeatureRequest(record[0]))
		feature = QgsFeature()
		if iterator.nextFeature(feature):
			feature.setAttribute("LINE_ID", feature.attributes()[objectIdIndex])
			writer.addFeature(feature)
			writecount += 1
		if writecount == len(table):
			print "  "+str(writecount)+" of "+str(len(table))+" features sorted successfully."
	# Delete the writer to flush features to disk
	del writer

def step_4c(glimsId):
	# Step 4c: Reproject sorted layer
	in_a = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId),"ALL_sorted_"+glimsId+".shp")
	out_a = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId),"rpj_sorted_"+glimsId+".shp")
	
	all_sorted = QgsVectorLayer(in_a,os.path.basename(in_a),"ogr")


	crs = QgsCoordinateReferenceSystem(3395, QgsCoordinateReferenceSystem.EpsgCrsId)
	print "Coordinate Reference System (CRS) %s %s will be used." % (crs.authid(), crs.description())
	
	print "--> %s's CRS is: %s" % (all_sorted.name(),all_sorted.crs().authid())
	print "		Reprojecting %s to %s %s" % (all_sorted.name(), crs.authid() ,crs.description())
	processing.runalg('qgis:reprojectlayer', all_sorted, crs.authid(), out_a)

def step_5(glimsId):
	'''
	Step 5: Extract centerlines 1 by 1 and put into individual folders
	 	      (they are now ordered in the db longest to shortest)
	'''
	bufferDistance = 250 #meters
	count = 0
	print (
		"  --> Extracting " + str(252) + " individual centerlines.\n"+
		"  --> A "+str(bufferDistance)+" meter buffer will be made for each centerline.\n"+
		"  --> Each buffer will be converted to a linetype geometry shapefile.\n"
		"  --> Each line-buffer will be intersected with all centerlines from the glacier.")

	'''
		Extent of glacier boundary layer  is needed to use the tool "grass7:v.distance"
		in a later step. Calling layer.extent() returns a QgsRectangle() object, but 
		"grass7:v.distance" requires a string type, so we extract the x-min, x-max, y-min, 
		y-max from the rectangle object and store it as string to be used as a valid 
		parameter for the tool. We calculate this here so that it is not needlessly 
		repeated for every centerline within the glacier.
	'''

	in_a = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId),"diss_bound_"+glimsId+"_line.shp")
	glacier = QgsVectorLayer(in_a,os.path.basename(in_a),"ogr")
	extent = glacier.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()
	stringExtent = "%f,%f,%f,%f" %(xmin, xmax, ymin, ymax) # creates the string we need
	'''
		Iterate over the sorted centerlines for the current glacier and calculate the
		intersections for each individual centerline.
	'''
	counter = 0

	in_b = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId),"rpj_sorted_"+glimsId+".shp")
	rpj_sorted = QgsVectorLayer(in_b,os.path.basename(in_b),"ogr")

	iter = rpj_sorted.getFeatures()
	for feature in iter:
		# if counter == 0 :
		line_ID = feature['LINE_ID']
		
		print "line_ID = " + str(line_ID)

		# Create a folder for each centerline which will contain all sub-processes
		singleLinePath = os.path.join(os.path.join(utility.getPath_outputs()['step_4'], glimsId), "id_"+str(line_ID))
		if not os.path.isdir(singleLinePath):
			os.mkdir(singleLinePath)


# USE THIS CODE TO DELETE INTERMEDIATE STEPS (USE TEMP FILES IN MEMORY AND DELETE ON EXIT)
		out_a = os.path.join(singleLinePath,'single_line.shp')
		print "singleLine"
		# Extract one line
		processing.runalg("qgis:extractbyattribute",rpj_sorted,"LINE_ID",0,line_ID,out_a)
		
		print "singleLinePoints"
		out_b = os.path.join(singleLinePath,'single_line_points.shp')
		# Convert lines to points
		processing.runalg("grass7:v.to.points",out_a,"50",1,True,stringExtent,-1,0.0001,0,out_b)
		
		print "adding DST_TO_EGE field"
		# Add distance field for v.distance to tool
		linePts = QgsVectorLayer(out_b, "dist_to_boundary.shp", "ogr")
		provider = linePts.dataProvider()
		linePts.startEditing()
		provider.addAttributes( [ QgsField("DST_TO_EGE", QVariant.Double, 'double', 10, 2) ])
		linePts.commitChanges()
		
		print "v.distance"
		# Find the minimum distance from every centerline point to the glacier boundary
		out_c = os.path.join(singleLinePath, "vdistPoints.shp")
		out_d = os.path.join(singleLinePath, "vdistLines.shp")
		processing.runalg("grass7:v.distance",linePts.source(),"point",glacier.source(),"point,line",-1,-1,"dist","DST_TO_EGE",None,stringExtent,-1,0.0001,out_c,out_d)

		print "varBuff"
		# Create variable distance buffer along centerline points
		out_e = os.path.join(singleLinePath, "var_buff.shp")
		processing.runalg("qgis:variabledistancebuffer",out_c,"DST_TO_EGE",10,True,out_e)
		
		print "lineVarBuff"
		# Convert buffer to line
		out_f = os.path.join(singleLinePath, "line_var_buff.shp")
		processing.runalg("qgis:polygonstolines",out_e,out_f)
		
		print "angleVertices"
		# Intersect line buffer with all the glaciers centerlines
		out_g = os.path.join(singleLinePath, "angle_vertices.shp")
		processing.runalg("qgis:lineintersections",out_f,rpj_sorted.source(),"LINE_ID","OBJECTID",out_g)
		
		print "circles"
		# Buffer intersection points to create 50m circles around them
		out_h = os.path.join(singleLinePath, "circles.shp")
		processing.runalg("qgis:fixeddistancebuffer",out_g,50,10,False,out_h)
		
		print "lineCircles"
		# Convert buffered circles to lines
		out_i = os.path.join(singleLinePath, "line_circles.shp")
		processing.runalg("qgis:polygonstolines",out_h,out_i)
		
		print "intersectBuffer"
		# Intersect line circles with centerline buffer
		out_j = os.path.join(singleLinePath, "intersectBuffer.shp")
		processing.runalg("qgis:lineintersections",out_f,out_i,"LINE_ID","OBJECTID",out_j)

		print "intersectCenterlines"
		# Intersect line circles with centerlines
		out_k = os.path.join(singleLinePath, "intersectCenterlines.shp")
		processing.runalg("qgis:lineintersections",out_i,rpj_sorted.source(),"LINE_ID","OBJECTID",out_k)	

		print "clippedIntersectCenterlines"
		# Clip/delete the intersection point inside the glacier boundary
		out_l = os.path.join(singleLinePath, "clippedIntersectCenterlines.shp")
		processing.runalg("qgis:difference",out_k,out_e,True,out_l)
		# Delete the features since they are clipped but still exist with NULL geometry
		clippedIntLayer = QgsVectorLayer(out_l,"clippedICL","ogr")
		with edit(clippedIntLayer):
			icl_feats = clippedIntLayer.getFeatures()
			for icl_feat in icl_feats:
				if not icl_feat.geometry():
					clippedIntLayer.deleteFeature(icl_feat.id())
			# print clippedIntersectCenterlines
		# Convert the geometry of the file from type 'Multi-Point' to 'Point'
		out_m = os.path.join(singleLinePath, "clippedSinglePart.shp")
		processing.runalg("qgis:multiparttosingleparts",out_l,out_m)

		intersectFields = QgsFields()
		intersectFields.append(QgsField("CENTERLINE", QVariant.Double, '', 10))
		intersectFields.append(QgsField("INTSCT_ID", QVariant.Double, '', 10))
		intersectFields.append(QgsField("INTSCT_VTX", QVariant.Int, '', 1))
		intersectFields.append(QgsField("INTSCT_LNE", QVariant.Int, '', 1))
		intersectFields.append(QgsField("FROM_BUFF", QVariant.Int, '', 1))
		intersectFields.append(QgsField("UP_POINT", QVariant.Int, '', 1))
		intersectFields.append(QgsField("DOWN_POINT", QVariant.Int, '', 1))

		intersectId = -1
		intersectFileFieldValues = [
			('intersect_angleVertices.shp', out_g, [line_ID, intersectId, 1, 0, 0, 0, 0]),
			('intersect_fromBuffVertices.shp', out_j, [line_ID, intersectId, 0, 0, 1, 0, 0]),
			('intersect_CLineVertices.shp', out_m, [line_ID, intersectId, 0, 1, 0, 0, 0])
			]
		num = 0
		for f in intersectFileFieldValues:
			fileSrc = os.path.join(singleLinePath, f[0])
			layer = QgsVectorLayer(f[1],f[0],"ogr")
			writer = QgsVectorFileWriter(fileSrc, "CP1250", intersectFields, layer.wkbType(), layer.crs(), "ESRI Shapefile")
			if writer.hasError() != QgsVectorFileWriter.NoError:
			    print("Error when creating shapefile: ", writer.errorMessage())
			inFeats = layer.getFeatures()
			for inFeat in inFeats:
				outFeat = QgsFeature()
				outFeat.setGeometry(inFeat.geometry())
				f[2][1] = inFeat["OBJECTID"]
				outFeat.setAttributes(f[2])
				writer.addFeature(outFeat)
			del writer
			del layer
	# For every intersection, there are two intersection points generated from intersecting the glacier centerline buffer
	# with the intersection point circles.  We need to know which one is 'higher-up' the glacier so that it can be used to
	# calculate a consistent and relevent glacier angle (ie. the upslope intersection angle).  We do NOT want to include a
	# Digital Elevation Model (DEM) to check which point is higher because it will mean aquiring a LOT more input data and
	# also drastically decrease the algorithm performance. To solve this, I do the following for each pair of points:
	# 	- split the centerline buffer line at the vertice nearest to the first point
	# 	- calculate the distance of the 2 lines resulting from spliting the line
	# 	- repeat this for the second point
	# 	- compare and find the minimum distances of all 4 resulting line segments
	# 	- whichever point this line segment 'belongs to' is the higher point, because the centerline buffer line begins 
	# 	  and ends at the centerline head (highest point) for any given glacier or sub-glacier
		buffLayer = QgsVectorLayer(out_f,"line_buffer","ogr")
		ptLayer = QgsVectorLayer(os.path.join(singleLinePath,intersectFileFieldValues[1][0]),intersectFileFieldValues[1][0],"ogr")
		ptIds = ptLayer.uniqueValues(ptLayer.fieldNameIndex('INTSCT_ID'))
		buff_feats = [feat for feat in buffLayer.getFeatures()]
		point_Dict = {
			'pt_1 ID' : None,
			'pt_1 minDist' : None,
			'pt_2 ID' : None,
			'pt_2 minDist' : None 
			}
		highPoints = []
		lowPoints = []
		for ptId in ptIds:
			expr = QgsExpression("\"INTSCT_ID\"="+str(ptId))
			it = ptLayer.getFeatures(QgsFeatureRequest(expr))
			ids = [i.id() for i in it]
			ptLayer.setSelectedFeatures(ids)
			selection = ptLayer.selectedFeatures()
			if len(selection) != 2:
				if len(selection) > 2:
					print "ptId: " + str(ptId) + " has " + str(len(selection)) + " points. Perhaps multiple intersections in ablation zone?"
				continue
			count = 0
			for pt in selection:
				tup = buff_feats[0].geometry().closestSegmentWithContext(pt.geometry().asPoint())
				polyLine = [feat.geometry().asPolyline() for feat in buff_feats]
				first_segment = []
				second_segment = [tup[1]]
				for line in polyLine:
					for i, point in enumerate(line):
						if i < tup[2]:
							first_segment.append(point)
						else:
							second_segment.append(point)
				first_segment.append(tup[1])
				geom_1 = QgsGeometry.fromPolyline(first_segment)
				length_1 = geom_1.length()
				geom_2 = QgsGeometry.fromPolyline(second_segment)
				length_2 = geom_2.length()
				if count == 0:
					point_Dict['pt_1 ID'] = pt.id()
					point_Dict['pt_1 minDist'] = min(length_1,length_2)
				elif count == 1:
					point_Dict['pt_2 ID'] = pt.id()
					point_Dict['pt_2 minDist'] = min(length_1,length_2)
				count+=1
			# Compare the lengths of the resulting split line segments from splitting at each point
			if point_Dict['pt_1 minDist'] < point_Dict['pt_2 minDist']:
				highPoints.append(point_Dict['pt_1 ID'])
				lowPoints.append(point_Dict['pt_2 ID'])
			elif point_Dict['pt_2 minDist'] <= point_Dict['pt_1 minDist']:
				highPoints.append(point_Dict['pt_2 ID'])
				lowPoints.append(point_Dict['pt_1 ID'])
			# Clear selection for next iteration with an empty list
			ptLayer.setSelectedFeatures([])
		
		# Update attribute to indicate which buffer point is at higher elevation
		ptLayer.startEditing()
		ptLayer.updateFields()
		idx = ptLayer.fieldNameIndex('UP_POINT')
		for i in highPoints:
			ptLayer.changeAttributeValue(i,idx,1)
		# idx = ptLayer.fieldNameIndex('DOWN_POINT')
		# for i in lowPoints:
		# 	ptLayer.changeAttributeValue(i,idx,1)
		ptLayer.commitChanges()
		ptLayer.startEditing()
		for i in lowPoints:
			ptLayer.deleteFeature(i)
		ptLayer.commitChanges()

		for f in intersectFileFieldValues:
			fileSrc = os.path.join(singleLinePath, f[0])
			layer = QgsVectorLayer(f[1],f[0],"ogr")
		# Merge all of the intersection points needed for angle calculations into one point file
		mergeSrc = os.path.join(singleLinePath, "merged_intersect_pts.shp")
		processing.runalg("qgis:mergevectorlayers",
			os.path.join(singleLinePath,intersectFileFieldValues[0][0])
			+";"+
			os.path.join(singleLinePath,intersectFileFieldValues[1][0])
			+";"+
			os.path.join(singleLinePath,intersectFileFieldValues[2][0]),
			mergeSrc)
		# Calculate angles from merged point file
		intLayer = QgsVectorLayer(mergeSrc, os.path.basename(mergeSrc), "ogr")
		print intLayer.isValid()
		for intId in ptIds:
			expr = QgsExpression("\"INTSCT_ID\"="+str(intId))
			print "\"INTSCT_ID\"="+str(intId)
			print intId
			it = intLayer.getFeatures(QgsFeatureRequest(expr))
			ids = [i.id() for i in it]
			print ids
			intLayer.setSelectedFeatures(ids)
			selection = intLayer.selectedFeatures()
			print selection
			pt_A = QgsFeature() # Upslope point on current centerline
			pt_B = QgsFeature() # Angle/intersection vertex
			pt_C = QgsFeature() # Upslope point on intersecting centerline
			if len(selection) == 3:
				for s in selection:
					if s['UP_POINT'] == 1:
						pt_A = s
					elif s['INTSCT_VTX'] == 1:
						pt_B = s
					elif s['INTSCT_LNE'] == 1:
						pt_C = s
				gLine = QgsGeometry.fromPolyline([pt_A.geometry().asPoint(), pt_B.geometry().asPoint(), pt_C.geometry().asPoint()])
				angle1 = gLine.angleAtVertex(0)
				angle2 = gLine.angleAtVertex(1)
				angle3 = gLine.angleAtVertex(2)
				print angle1
				print angle2
				print angle3
			else:
				print "ERROR: Need exactly 3 points to calculate angle."
			intLayer.setSelectedFeatures([])
			
			# counter +=1

step_5('G220886E60666N')














