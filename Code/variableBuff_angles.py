'''
SET THESE PARAMETERS
1. Input path
		Path to folder containing RGI Polygon Shapefile and Centerline Shapefile
		example: inputPath = '/Users/lucasjakober/Documents/Semester 9/Geog4990/script inputs'
		Output path is optional. Set a path if you'd like, otherwise one will be created 'outputs_glacier_angles'

2. RGI Polygon Shapefile
		example: rgiPolygonShapefile = 'rgi60_Alaska.shp'

3. Centerline Shapefile
		example: centerlineShapefile = 'Centerlines_all.shp'
'''

inputPath = "/Users/lucasjakober/Documents/Semester 9/Geog4990/inputs"
outputPath = ""
rgiPolygonShapefile = "rgi60_Alaska.shp"
centerlineShapefile = "Centerlines_all.shp"

##############################
import my_utility
import os
import sys
from mmqgis import mmqgis_library
import operator
from qgis.core import *
# Next 3 lines MUST be in this order
app = QgsApplication([],True)
# QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/Plugins', True)
QgsApplication.setPrefixPath('/Applications/QGIS.app/Contents/MacOS', True)

app.initQgis()
import PyQt4
# from PyQt4 import QtCore, QtGui
# from PyQt4.QtGui import *
from PyQt4.QtCore import QVariant
import processing
from processing.core.Processing import Processing
Processing.initialize()
Processing.updateAlgsList()

# # Create output folder if not created
if not outputPath:
	outputPath = os.path.join(os.path.dirname(inputPath), 'outputs')
	if not os.path.isdir(outputPath):
		os.mkdir(outputPath)

# # Copy files to output folder (to preserve input files and folder)
# rgiSrc = os.path.join(inputPath, rgiPolygonShapefile)
# lineSrc = os.path.join(inputPath, centerlineShapefile)
# my_utility.copyShapefile(rgiSrc, outputPath)
# my_utility.copyShapefile(lineSrc, outputPath)
# # All processing will occur in output folder, so source filepaths are set to the copied files.
# rgiSrc = os.path.join(outputPath, rgiPolygonShapefile)
# lineSrc = os.path.join(outputPath, centerlineShapefile)
# # Initialize the shapefiles as vector layers.
# rgiLayer = QgsVectorLayer(rgiSrc, os.path.basename(rgiSrc), "ogr")
# lineLayer = QgsVectorLayer(lineSrc, os.path.basename(lineSrc), "ogr")

# # Step 1: Check that input files are valid.
# if not rgiLayer.isValid():
# 	print "%s failed to load!" % rgiLayer.name()
# if not rgiLayer.crs().isValid():
# 	print "%s does not have a valid CRS." % rgiLayer.name()
# if not lineLayer.isValid():
# 	print "%s failed to load!" % lineLayer.name()
# if not lineLayer.crs().isValid():
# 	print "%s does not have a valid CRS." % lineLayer.name()

# # Step 2: Delete any existing fields that will not be needed for angle calculations.
# print "Cleaning attribute table... (%s)" % rgiLayer.name()
# rgiFieldsToKeep = ['RGIId','GLIMSId']
# rgiFields = [field.name() for field in rgiLayer.pendingFields()]
# fieldsDeleted = 0
# for f in rgiFields:
# 	if f not in rgiFieldsToKeep:
# 		QgsMessageLog.logMessage("Getting Field Index for: %s" % f, "ForceDelete")
# 		fieldID = rgiLayer.fieldNameIndex(f)
# 		print "  delete field... (%s)" % f
# 		QgsMessageLog.logMessage("Deleting Field", "ForceDelete")
# 		rgiLayer.dataProvider().deleteAttributes([fieldID])
# 		rgiLayer.updateFields()
# 		fieldsDeleted+=1
# print "%d fields deleted from %s" % (fieldsDeleted, rgiLayer.name())
# QgsMessageLog.logMessage("Reload Table...", "ForceDelete")
# QgsMapLayerRegistry.instance().reloadAllLayers()

# print "Cleaning attribute table... (%s)" % lineLayer.name()
# centerlineFieldsToKeep = ['GLIMSID','OBJECTID','LENGTH_CL']
# centerlineFields = [field.name() for field in lineLayer.pendingFields()]
# fieldsDeleted = 0
# for f in centerlineFields:
# 	if f not in centerlineFieldsToKeep:
# 		QgsMessageLog.logMessage("Getting Field Index for: %s" % f, "ForceDelete")
# 		fieldID = lineLayer.fieldNameIndex(f)
# 		print "  deleting field... (%s)" % f
# 		QgsMessageLog.logMessage("Deleting Field", "ForceDelete")
# 		lineLayer.dataProvider().deleteAttributes([fieldID])
# 		lineLayer.updateFields()
# 		fieldsDeleted+=1
# print "%d fields deleted from %s" % (fieldsDeleted, lineLayer.name())
# QgsMessageLog.logMessage("Reload Table...", "ForceDelete")
# QgsMapLayerRegistry.instance().reloadAllLayers()


# # Step 3: Reproject both shapefiles to EPSG4326 (GCS - WGS '84)
# # crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
# # Step 3: Reproject both shapefiles to EPSG3395 WGS '84 Transverse Mercator (for distance calculations in meters)
# crs = QgsCoordinateReferenceSystem(3395, QgsCoordinateReferenceSystem.EpsgCrsId)
# print "Coordinate Reference System (CRS) %s %s will be used." % (crs.authid(), crs.description())
# print "--> %s's CRS is: %s" % (rgiLayer.name(),rgiLayer.crs().authid())
# if rgiLayer.crs().authid() == crs.authid():
# 	print "		No need to reproject."
# else:
# 	print "		Reprojecting %s to %s %s" % (rgiLayer.name(), crs.authid(), crs.description())
# 	reprojectRgi = os.path.join(os.path.dirname(rgiSrc),'reproject_'+os.path.basename(rgiSrc))
# 	processing.runalg('qgis:reprojectlayer', rgiLayer, crs.authid(), reprojectRgi)
# 	rgiSrc = reprojectRgi
# 	rgiLayer.setDataSource(rgiSrc, os.path.basename(rgiSrc), "ogr")
# print "--> %s's CRS is: %s" % (lineLayer.name(),lineLayer.crs().authid())
# if lineLayer.crs().authid() == crs.authid():
# 	print "		No need to reproject."
# else:
# 	print "		Reprojecting %s to %s %s" % (lineLayer.name(), crs.authid() ,crs.description())
# 	reprojectLines = os.path.join(os.path.dirname(lineSrc),'reproject_'+os.path.basename(lineSrc))
# 	processing.runalg('qgis:reprojectlayer', lineLayer, crs.authid(), reprojectLines)
# 	lineSrc = reprojectLines
# 	lineLayer.setDataSource(lineSrc, os.path.basename(lineSrc), "ogr")

# # Step 4: Add length field to Centerline Shapefile
# # lineLayer.dataProvider().AddAttributes([QgsField("LENGTH_M", QVariant.Double)])
# # lineLayer.updateFields()
# lineLayer.startEditing()
# #step 1
# lineLayer.addAttribute( QgsField( 'LENGTH_M', QVariant.Double ) )
# idx = lineLayer.fieldNameIndex( 'LENGTH_M' )
# #step 2
# e = QgsExpression( '$LENGTH' )
# e.prepare( lineLayer.pendingFields() )
# for f in lineLayer.getFeatures():
#     f[idx] = e.evaluate( f )
#     lineLayer.updateFeature( f )
# lineLayer.commitChanges()

## PATHS FOR TESTING ##
rgiSrc = "/Users/lucasjakober/Documents/Semester 9/Geog4990/outputs/reproject_rgi60_Alaska.shp"
lineSrc = "/Users/lucasjakober/Documents/Semester 9/Geog4990/outputs/reproject_Centerlines_all.shp"


# Step 5: Extract one glacier polygon and all corresponding centerlines by GLIMS Id
# REPEAT this step for every unique GLIMSID
glimsId = 'G220886E60666N'
print "Processing glacier: "+glimsId
idPath = os.path.join(outputPath, glimsId)
if not os.path.isdir(idPath):
	os.mkdir(idPath)

glacierLinesSrc = os.path.join(idPath, 'ALL_lines_'+glimsId+'.shp')
processing.runalg("qgis:extractbyattribute",lineSrc,"GLIMSID",0,glimsId,glacierLinesSrc)
glacierLinesLayer = QgsVectorLayer(glacierLinesSrc, os.path.basename(glacierLinesSrc), "ogr")
res = glacierLinesLayer.dataProvider().addAttributes([QgsField("LINE_ID", QVariant.Int)])
glacierLinesLayer.updateFields()

# tempBoundaryPoly = QgsVectorLayer("Polygon?crs=epsg:3395", "boundaryPoly", "memory")
# tempBoundaryPoly = processing.runalg("qgis:extractbyattribute",rgiSrc,"GLIMSId",0,glimsId, None)
tempBoundaryPoly = processing.runalg("qgis:extractbyattribute",rgiSrc,"GLIMSId",0,glimsId, None)
tempBoundaryLines = processing.runalg("qgis:polygonstolines",tempBoundaryPoly['OUTPUT'], None)
glacierBoundaryLineSrc = os.path.join(idPath, 'ALL_line_boundary_'+glimsId+'.shp')
processing.runalg("qgis:dissolve",tempBoundaryLines['OUTPUT'],False,"GLIMSId;RGIId",glacierBoundaryLineSrc)
glacierBoundaryLineLayer = QgsVectorLayer(glacierBoundaryLineSrc, os.path.basename(glacierBoundaryLineSrc), "ogr")
del tempBoundaryPoly
del tempBoundaryLines

# test = tempBoundaryPoly['OUTPUT']
# QgsMapLayerRegistry.instance().reloadAllLayers()
# tempBoundaryPoly = QgsMapLayerRegistry.instance().mapLayersByName("memory:tempBoundaryPoly")[0]

# test2 = QgsVectorLayer(test,"area", "ogr")
# QgsMapLayerRegistry.instance().addMapLayers([test2])
# print test2.name()
# print test2.isValid()
# QgsMapLayerRegistry.instance().addMapLayer(tempBoundaryPoly)
# # tempBoundaryLines = QgsVectorLayer("Line?crs=epsg:3395", "boundaryLines", "memory")
# tempBoundaryLines = processing.runalg("qgis:polygonstolines",tempBoundaryPoly['OUTPUT'], None)
# glacierBoundaryLineSrc = os.path.join(idPath, 'ALL_line_boundary_'+glimsId+'.shp')
# processing.runalg("qgis:dissolve",tempBoundaryLines['tempBoundaryLines'],False,"GLIMSId;RGIId",glacierBoundaryLineSrc)
# del tempBoundaryPoly
# del tempBoundaryLines

# glacierBoundaryPolySrc = os.path.join(idPath, 'ALL_poly_boundary_'+glimsId+'.shp')
# processing.runalg("qgis:extractbyattribute",rgiSrc,"GLIMSId",0,glimsId, glacierBoundaryPolySrc)
# glacierBoundaryLineSrc = os.path.join(idPath, 'ALL_line_boundary_'+glimsId+'.shp')
# processing.runalg("qgis:polygonstolines",glacierBoundaryPolySrc, glacierBoundaryLineSrc)

# glacierBoundaryLineLayer = QgsVectorLayer(glacierBoundaryLineSrc, os.path.basename(glacierBoundaryLineSrc), "ogr")


'''
Step 6: Sort the centerlines in descending order of field "LENGTH_M"
'''
sortedLengthSrc = os.path.join(idPath,"ALL_sorted_"+glimsId+".shp")
writer = QgsVectorFileWriter(sortedLengthSrc, "CP1250", glacierLinesLayer.fields(), glacierLinesLayer.wkbType(), glacierLinesLayer.crs(), "ESRI Shapefile")
if writer.hasError() != QgsVectorFileWriter.NoError:
	print("Error when creating shapefile: ", writer.errorMessage())
sortindex = glacierLinesLayer.fieldNameIndex("LENGTH_M")
direction = "descending"
table = []
for index, feature in enumerate(glacierLinesLayer.getFeatures()):
	record = feature.id(), feature.attributes()[sortindex]
	table.append(record)
if (direction.lower() == "descending"):
	table.sort(key = operator.itemgetter(1), reverse=True)
else:
	table.sort(key = operator.itemgetter(1))
# Add features to new shapefile in same order as sorted table
writecount = 0
provider = glacierLinesLayer.dataProvider()
objectIdIndex = glacierLinesLayer.fieldNameIndex("OBJECTID")
print (
	"  Glacier has "+str(len(table))+" centerlines. Sorting centerlines by length.\n"+
	"  Sorted file will be written to: \n"+
	"    "+sortedLengthSrc)
for index, record in enumerate(table):
	iterator = glacierLinesLayer.getFeatures(QgsFeatureRequest(record[0]))
	feature = QgsFeature()
	if iterator.nextFeature(feature):
		feature.setAttribute("LINE_ID", feature.attributes()[objectIdIndex])
		writer.addFeature(feature)
		writecount += 1
	if writecount == len(table):
		print "  "+str(writecount)+" of "+str(len(table))+" features sorted successfully."
# Delete the writer to flush features to disk
del writer
sortedLengthLayer = QgsVectorLayer(sortedLengthSrc, os.path.basename(sortedLengthSrc), "ogr")
print "Sorted Length Layer crs: ",sortedLengthLayer.crs().authid()

# Step 7: Extract centerlines 1 by 1 and put into individual folders
# 	      (they are now ordered in the db longest to shortest)
# singleLineSrcPaths = []
# provider = sortedLengthLayer.dataProvider()
# count = 0
# iter = sortedLengthLayer.getFeatures()
# for feature in iter:
# 	line_ID = feature['OBJECTID']
# 	singleLinePath = os.path.join(idPath, "id_"+str(line_ID))
# 	if not os.path.isdir(singleLinePath):
# 		os.mkdir(singleLinePath)
# 	src = os.path.join(singleLinePath, "line_"+str(line_ID)+".shp")
# 	singleLineSrcPaths.append(src)
# 	writer = QgsVectorFileWriter(src, "CP1250", sortedLengthLayer.fields(), sortedLengthLayer.wkbType(), sortedLengthLayer.crs(), "ESRI Shapefile")
# 	if writer.hasError() != QgsVectorFileWriter.NoError:
# 	    print("Error when creating shapefile: ", writer.errorMessage())
# 	writer.addFeature(feature)
# 	del writer

# 	count+=1

# linesRem = count
# bufferDistance = 250 #meters
# print "Creating "+str(bufferDistance)+"m buffer for " + str(linesRem) + " lines."
# for src in singleLineSrcPaths:
# 	print src
# 	if (linesRem % 25 == 0):
# 		print str(linesRem) + " lines remaining to buffer."
# 	if (linesRem == 0):
# 		print "Done creating buffers."
# 	if os.path.isfile(src):	
# 		buffSrc = os.path.join(os.path.dirname(src), "buffer_"+str(bufferDistance)+".shp")
# 		processing.runalg("qgis:fixeddistancebuffer",src,bufferDistance,5,True,buffSrc)
# 	linesRem-=1

# linesRem = count
# bufferDistance = 250 #meters
# print "Converting buffer polygon to line for " + str(linesRem) + " lines."
# for src in singleLineSrcPaths:
# 	print src
# 	if (linesRem % 25 == 0):
# 		print str(linesRem) + " lines remaining to buffer."
# 	if (linesRem == 0):
# 		print "Done converting buffers to lines."
# 	if os.path.isfile(src):	
# 		buffSrc = os.path.join(os.path.dirname(src), "buffer_"+str(bufferDistance)+".shp")
# 		buffLineSrc = os.path.join(os.path.dirname(src), "buffer_"+str(bufferDistance)+"_line.shp")
# 		processing.runalg("qgis:polygonstolines",buffSrc, buffLineSrc)
# 		intersectSrc = os.path.join(os.path.dirname(src), "intersect.shp")
# 		# processing.runalg("qgis:polygonstolines",buffSrc, intersectSrc)
# 		processing.runalg("qgis:lineintersections",buffLineSrc,sortedLengthSrc,"OBJECTID","LINE_ID",intersectSrc)
# 	linesRem-=1

# linesRem = count
# print "Finding glacier intersections for " + str(linesRem) + " lines."
# for src in singleLineSrcPaths:
# 	print src
# 	if (linesRem % 25 == 0):
# 		print str(linesRem) + " lines remaining to find intersections."
# 	if (linesRem == 0):
# 		print "Done finding intersections."
# 	if os.path.isfile(src):	
# 		buffLineSrc = os.path.join(os.path.dirname(src), "buffer_"+str(bufferDistance)+"_line.shp")
# 		intersectSrc = os.path.join(os.path.dirname(src), "intersect.shp")
# 		# processing.runalg("qgis:polygonstolines",buffSrc, intersectSrc)
# 		processing.runalg("qgis:lineintersections",buffLineSrc,sortedLengthSrc,"OBJECTID","LINE_ID",intersectSrc)
# 	linesRem-=1

'''
Step 7: Extract centerlines 1 by 1 and put into individual folders
 	      (they are now ordered in the db longest to shortest)
'''
bufferDistance = 250 #meters
count = 0
print (
	"  --> Extracting " + str(writecount) + " individual centerlines.\n"+
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
extent = glacierBoundaryLineLayer.extent()
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
iter = sortedLengthLayer.getFeatures()
for feature in iter:
	if counter == 0 :
		line_ID = feature['LINE_ID']
		
		print "line_ID = " + str(line_ID)

		# Create a folder for each centerline which will contain all sub-processes
		singleLinePath = os.path.join(idPath, "id_"+str(line_ID))
		if not os.path.isdir(singleLinePath):
			os.mkdir(singleLinePath)

# USE THIS CODE TO DELETE INTERMEDIATE STEPS (USE TEMP FILES IN MEMORY AND DELETE ON EXIT)
		
		print "singleLine"
		# Extract one line
		singleLine = processing.runalg("qgis:extractbyattribute",sortedLengthLayer,"LINE_ID",0,line_ID,None)
		
		print "singleLinePoints"
		# Convert lines to points
		singleLinePoints = processing.runalg("grass7:v.to.points",singleLine['OUTPUT'],"50",1,True,stringExtent,-1,0.0001,0,None)
		
		print "adding DST_TO_EGE field"
		# Add distance field for v.distance to tool
		linePtsLayer = QgsVectorLayer(singleLinePoints['output'], "dist_to_boundary.shp", "ogr")
		provider = linePtsLayer.dataProvider()
		linePtsLayer.startEditing()
		provider.addAttributes( [ QgsField("DST_TO_EGE", QVariant.Double, 'double', 10, 2) ])
		linePtsLayer.commitChanges()
		
		print "v.distance"
		# Find the minimum distance from every centerline point to the glacier boundary
		
		vdistPointsSrc = os.path.join(singleLinePath, "vdistPoints.shp")
		vdistLinesSrc = os.path.join(singleLinePath, "vdistLines.shp")
		processing.runalg("grass7:v.distance",linePtsLayer.source(),"point",glacierBoundaryLineLayer.source(),"point,line",-1,-1,"dist","DST_TO_EGE",None,stringExtent,-1,0.0001,vdistPointsSrc,vdistLinesSrc)

		print "varBuff"
		# Create variable distance buffer along centerline points
		varBuff = processing.runalg("qgis:variabledistancebuffer",vdistPointsSrc,"DST_TO_EGE",10,True,None)
		
		print "lineVarBuff"
		# Convert buffer to line
		lineVarBuff = processing.runalg("qgis:polygonstolines",varBuff['OUTPUT'],None)
		
		print "angleVertices"
		# Intersect line buffer with all the glaciers centerlines
		angleVertices = processing.runalg("qgis:lineintersections",lineVarBuff['OUTPUT'],sortedLengthLayer.source(),"LINE_ID","OBJECTID",None)
		
		print "circles"
		# Buffer intersection points to create 50m circles around them
		circles = processing.runalg("qgis:fixeddistancebuffer",angleVertices['OUTPUT'],50,10,False,None)
		
		print "lineCircles"
		# Convert buffered circles to lines
		lineCircles = processing.runalg("qgis:polygonstolines",circles['OUTPUT'],None)
		
		print "intersectBuffer"
		# Intersect line circles with centerline buffer
		intersectBuffer = processing.runalg("qgis:lineintersections",lineVarBuff['OUTPUT'],lineCircles['OUTPUT'],"LINE_ID","OBJECTID",None)

		print "intersectCenterlines"
		# Intersect line circles with centerlines
		intersectCenterlines = processing.runalg("qgis:lineintersections",lineCircles['OUTPUT'],sortedLengthLayer.source(),"LINE_ID","OBJECTID",None)	

		print "clippedIntersectCenterlines"
		# Clip/delete the intersection point inside the glacier boundary
		clippedIntersectCenterlines = processing.runalg("qgis:difference",intersectCenterlines['OUTPUT'],varBuff['OUTPUT'],True,None)
		# Delete the features since they are clipped but still exist with NULL geometry
		clippedIntLayer = QgsVectorLayer(clippedIntersectCenterlines['OUTPUT'],"clippedICL","ogr")
		with edit(clippedIntLayer):
			icl_feats = clippedIntLayer.getFeatures()
			for icl_feat in icl_feats:
				if not icl_feat.geometry():
					clippedIntLayer.deleteFeature(icl_feat.id())
			print clippedIntersectCenterlines
		# Convert the geometry of the file from type 'Multi-Point' to 'Point'
		clippedSinglePart = processing.runalg("qgis:multiparttosingleparts",clippedIntersectCenterlines['OUTPUT'],None)

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
			('intersect_angleVertices.shp', angleVertices['OUTPUT'], [line_ID, intersectId, 1, 0, 0, 0, 0]),
			('intersect_fromBuffVertices.shp', intersectBuffer['OUTPUT'], [line_ID, intersectId, 0, 0, 1, 0, 0]),
			('intersect_CLineVertices.shp', clippedSinglePart['OUTPUT'], [line_ID, intersectId, 0, 1, 0, 0, 0])
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
		buffLayer = QgsVectorLayer(lineVarBuff['OUTPUT'],"line_buffer","ogr")
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


	# Hester recommends CUT OFF THRESHOLD = 2km
	# Also intersecting glacier width must be greater than 10% of current centerline glacier width for it to be a valid important intersection









		# buff_feats = [feat for feat in buffLayer.getFeatures()]
		# pt_feats = [feat for feat in ptLayer.getFeatures()]
		# my_tupla = buff_feats[0].geometry().closestSegmentWithContext(pt_feats[0].geometry().asPoint())
		# my_line = [ feat.geometry().asPolyline() for feat in buff_feats ]
		# first_segment = []
		# second_segment = [my_tupla[1]]
		# for line in my_line:
		#     for i, point in enumerate(line):
		#         if i < my_tupla[2]:
		#             first_segment.append(point)
		#         else:
		#             second_segment.append(point)
		# first_segment.append(my_tupla[1])


		# # epsg = sortedLengthLayer.crs().postgisSrid()

		# # uri = "LineString?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"

		# testSplitFields = QgsFields()
		# testSplitFields.append(QgsField("id", QVariant.Int, '', 6))
		
		# writer = QgsVectorFileWriter(
		# 	os.path.join(singleLinePath, "test_split.shp"),
		# 	"CP1250", 
		# 	testSplitFields, buffLayer.wkbType(), buffLayer.crs(), "ESRI Shapefile")
		# if writer.hasError() != QgsVectorFileWriter.NoError:
		#     print("Error when creating shapefile: ", writer.errorMessage())
		# del writer

		# testSplitLayer = QgsVectorLayer(os.path.join(singleLinePath, "test_split.shp"), "test_split","ogr")

		# prov = testSplitLayer.dataProvider()

		# feat = QgsFeature()

		# feat.setAttributes([0])

		# feat.setGeometry(QgsGeometry.fromPolyline(first_segment))

		# prov.addFeatures([feat])

		# feat.setAttributes([1])

		# feat.setGeometry(QgsGeometry.fromPolyline(second_segment))

		# prov.addFeatures([feat])

		# print testSplitLayer.source()


		# mem_layer = QgsVectorLayer(uri,
		#                            'split_line',
		#                            'memory')

		# prov = mem_layer.dataProvider()

		# feat = QgsFeature()

		# feat.setAttributes([0])

		# feat.setGeometry(QgsGeometry.fromPolyline(first_segment))

		# prov.addFeatures([feat])

		# feat.setAttributes([1])

		# feat.setGeometry(QgsGeometry.fromPolyline(second_segment))

		# prov.addFeatures([feat])

		# print mem_layer.source()

		# QgsMapLayerRegistry.instance().addMapLayer(mem_layer)		


		# num+=1
		# memlayers = [angleVertices['OUTPUT'],intersectBuffer['OUTPUT'],clippedIntersectCenterlines['OUTPUT']]
		# num = 0
		# for l in memlayers:
		# 	layer = QgsVectorLayer(l,os.path.basename(l),"ogr")
		# 	provider = layer.dataProvider()
		# 	layer.startEditing()
		# 	provider.addAttributes( [ 
		# 		QgsField("CENTERLINE", QVariant.Int, '', 10),
		# 		QgsField("INTSCT_ID", QVariant.Int, '', 10),
		# 		QgsField("INTSCT_VTX", QVariant.Int, '', 1),
		# 		QgsField("INTSCT_LNE", QVariant.Int, '', 1),
		# 		QgsField("FROM_BUFF", QVariant.Int, '', 1),
		# 		QgsField("UP_POINT", QVariant.Int, '', 1),
		# 		QgsField("DOWN_POINT", QVariant.Int, '', 1) ] )
		# 	layer.commitChanges()
			# tempSrc = os.path.join(singleLinePath, "intersect_"+str(num)+".shp")
			# writer = QgsVectorFileWriter(tempSrc, "CP1250", layer.fields(), layer.wkbType(), layer.crs(), "ESRI Shapefile")
			# if writer.hasError() != QgsVectorFileWriter.NoError:
			#     print("Error when creating shapefile: ", writer.errorMessage())
			# intFeats = layer.getFeatures()
			# for intFeat in intFeats:
			# 	feature.setAttribute("LINE_ID", feature.attributes()[objectIdIndex])
			# 	writer.addFeature(feature)
			# 	writer.addFeature(feature)
			# del writer
			# num+=1

		# print "refact_angleVertices"
		# print angleVertices
		# # Refactor fields in the 3 intersect points layers so they can be merged
		# refact_angleVertices = processing.runalg("qgis:refactorfields",angleVertices['OUTPUT'], 
		# 	[
		# 	{'expression': u'10267', 'length': 10, 'type': 4, 'name': u'CENTERLINE', 'precision': 0}, 
		# 	{'expression': u'"LINE_ID"', 'length': 10, 'type': 4, 'name': u'INTSCT_ID', 'precision': 0}, 
		# 	{'expression': u'1', 'length': 1, 'type': 2, 'name': u'INTSCT_VTX', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'INTSCT_LNE', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'FROM_BUFF', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'UP_POINT', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'DOWN_POINT', 'precision': 0}, 
		# 	],
		# 	None)

		# print "refact_intersectBuffer"
		# refact_intersectBuffer = processing.runalg("qgis:refactorfields",intersectBuffer['OUTPUT'], 
		# 	[
		# 	{'expression': u'10267', 'length': 10, 'type': 4, 'name': u'CENTERLINE', 'precision': 0}, 
		# 	{'expression': u'"OBJECTID"', 'length': 10, 'type': 4, 'name': u'INTSCT_ID', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'INTSCT_VTX', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'INTSCT_LNE', 'precision': 0}, 
		# 	{'expression': u'1', 'length': 1, 'type': 2, 'name': u'FROM_BUFF', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'UP_POINT', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'DOWN_POINT', 'precision': 0}, 
		# 	],
		# 	None)
		
		# print "refact_clippedIntersectCenterlines"
		# refact_clippedIntersectCenterlines = processing.runalg("qgis:refactorfields",clippedIntersectCenterlines['OUTPUT'], 
		# 	[
		# 	{'expression': u'10267', 'length': 10, 'type': 4, 'name': u'CENTERLINE', 'precision': 0}, 
		# 	{'expression': u'"OBJECTID"', 'length': 10, 'type': 4, 'name': u'INTSCT_ID', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'INTSCT_VTX', 'precision': 0}, 
		# 	{'expression': u'1', 'length': 1, 'type': 2, 'name': u'INTSCT_LNE', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'FROM_BUFF', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'UP_POINT', 'precision': 0}, 
		# 	{'expression': u'0', 'length': 1, 'type': 2, 'name': u'DOWN_POINT', 'precision': 0}, 
		# 	],
		# 	None)
		
		# mergeSrc = os.path.join(singleLinePath, "merged_intersect_pts.shp")
		# processing.runalg("qgis:mergevectorlayers",
		# 	refact_angleVertices['OUTPUT_LAYER']
		# 	+";"+
		# 	refact_intersectBuffer['OUTPUT_LAYER']
		# 	+";"+
		# 	refact_clippedIntersectCenterlines['OUTPUT_LAYER'],
		# 	mergeSrc)

	counter +=1

#*******************************************************************************************************************************************************
	# # your point
	# point_x = 2.5
	# point_y = 1.5

	# # your line
	# gLine = QgsGeometry.fromPolyline([QgsPoint(1, 1), QgsPoint(2, 2),QgsPoint(3,1),QgsPoint(6,1)])
	# gPoint = QgsGeometry.fromPoint(QgsPoint(point_x,point_y))
	# lineGeom = gLine.asPolyline() 

	# # step through line segments
	# total_len = 0
	# for seg_start, seg_end in zip(lineGeom, lineGeom[1:]):
	#    line_start = QgsPoint(seg_start)
	#    line_end = QgsPoint(seg_end) 
	#    segment = QgsGeometry.fromPolyline([line_start,line_end])
	#    print segment.exportToWkt()
	#    if gPoint.intersects(segment):
	#        to_point = QgsGeometry.fromPolyline([line_start, QgsPoint(point_x,point_y)])
	#        total_len += to_point.length()
	#        break
	#    else:
	#        total_len += segment.length()
	# print total_len



	# count+=1
	# if (count % 25 == 0):
	# 	print "     Successfully processed "+str(count)+" of "+str(writecount)+" centerlines for "+glimsId
	# if (count == writecount): 
	# 	print "Finished "+glimsId+"."

'''
Step 8: Add distance to boundary as an attribute value for every intersection point
	We need the extent of glacier boundary layer to use the tool "grass7:v.distance".
	Calling layer.extent() returns a QgsRectangle() object, but "grass7:v.distance" 
	takes a string, so we need to extract the x-min, x-max, y-min, y-max from the
	rectangle object and store it as string to be used as a parameter for the tool.
'''
# extent = glacierBoundaryLineLayer.extent()
# xmin = extent.xMinimum()
# xmax = extent.xMaximum()
# ymin = extent.yMinimum()
# ymax = extent.yMaximum()
# stringExtent = "%f,%f,%f,%f" %(xmin, xmax, ymin, ymax) # creates the string we need
# mycounter = 0
# for line in lineFolderPaths:
# 	if mycounter < 5:
# 		if os.path.isfile(glacierBoundaryLineLayer.source()) and os.path.isfile(line[2]):
# 			intersectPtsLayer = QgsVectorLayer(line[2], os.path.basename(line[2]), "ogr")
# 			provider = intersectPtsLayer.dataProvider()
# 			intersectPtsLayer.startEditing()
# 			provider.addAttributes( [ 
# 				QgsField("DST_TO_EGE", QVariant.Double, 'double', 10, 2),
# 				QgsField("TO_XCOORD", QVariant.Double, 'double', 10, 2),
# 				QgsField("TO_YCOORD", QVariant.Double, 'double', 10, 2),
# 				QgsField("TO_ANGLE", QVariant.Double, 'double', 10, 2)])
# 			intersectPtsLayer.commitChanges()
# 			vdistanceLineSrc = os.path.join(os.path.dirname(line[2]),"vdistanceLines.shp")
# 			vdistancePointSrc = os.path.join(os.path.dirname(line[2]), "vdistancePoints.shp")
# 			processing.runalg("grass7:v.distance",line[2],"point",glacierBoundaryLineLayer.source(),"point,line",-1,-1,"dist,to_x,to_y,to_angle","DST_TO_EGE,TO_XCOORD,TO_YCOORD,TO_ANGLE",None,stringExtent,-1,0.0001,vdistancePointSrc,vdistanceLineSrc)
# 		else:
# 			print "ERROR PROCESSING "+str(line[0])
# 	mycounter+=1



# iter = sortedLengthLayer.getFeatures()
# for feature in iter:
# 	if (count % 25 == 0):
# 		print str(count) + " lines remaining."
# 	if (count == 0):
# 		print "Done."
# 	line_ID = feature['OBJECTID']
# 	singleLinePath = os.path.join(idPath, str(line_ID))
# 	src = os.path.join(singleLinePath, str(line_ID)+".shp")
# 	if os.path.isdir(singleLinePath):
# 		if os.path.isfile(src):	
# 			buffSrc = os.path.join(singleLinePath, "buffer_"+str(bufferDistance)+".shp")
# 			processing.runalg("qgis:fixeddistancebuffer",src,bufferDistance,5,True,buffSrc)
# 			buffLineSrc = os.path.join(singleLinePath, "buffer_"+str(bufferDistance)+"_line.shp")
# 			processing.runalg("qgis:polygonstolines",buffSrc, buffLineSrc)
# 			intersectSrc = os.path.join(singleLinePath, "intersect.shp")
# 			# processing.runalg("qgis:polygonstolines",buffSrc, intersectSrc)
# 			processing.runalg("qgis:lineintersections",buffLineSrc,sortedLengthSrc,"OBJECTID","LINE_ID",intersectSrc)
# 	count-=1



# exp = QgsExpression("'LENGTH_M' = maximum( 'LENGTH_M' )")
# # longestLineSrc = os.path.join(os.path.dirname(glacierLinesSrc), 'longest_line_'+currentID+'.shp')
# glacierLinesSrc = "/Users/lucasjakober/Documents/Semester 9/Geog4990 - Glacier Automation/outputs_glacier_angles/lines_G220886E60666N.shp"
# longestLineSrc = "/Users/lucasjakober/Documents/Semester 9/Geog4990 - Glacier Automation/outputs_glacier_angles/longest_line_G220886E60666N.shp"
# processing.runalg("qgis:extractbyexpression", glacierLinesSrc, exp ,longestLineSrc)
# longestLineLayer = QgsVectorLayer(longestLineSrc, os.path.basename(longestLineSrc), "ogr")

# print processing.alghelp("qgis:extractbyexpression")




# # Step 2: DELETE UNDEEDED FIELDS IN ATTRIBUTE TABLE ###
# # Delete unnecessary fields in RGI Polygon shapefile
# rgiPolyFieldsToDelete = ['BgnDate', 'EndDate', 'CenLon', 'CenLat', 'O1Region', 'O2Region', 'Area', 'Zmin', 'Zmax', 'Zmed', 'Slope', 'Aspect', 'Lmax', 'Status', 'Connect', 'Form', 'TermType', 'Surging', 'Linkages', 'Name']
# rgiFields = [field.name() for field in rgiLayer.pendingFields()]
# count = 0
# inFile = inputPath+'/'+rgiPolygonShapefile+'.shp'
# outFile = outputPath+'/'+rgiPolygonShapefile+'_clean'+str(count)+'.shp'
# for field in rgiFields:
# 	if field in rgiPolyFieldsToDelete:
# 		print "Deleting field: " + field
# 		processing.runalg('qgis:deletecolumn', inFile, field, outFile)
# 		count+=1
# 		inFile = outFile
# 		outFile = outputPath+'/'+rgiPolygonShapefile+'_clean'+str(count)+'.shp'
# print "Deleted " + str(count-1) + " fields." 		
# inFile = ''
# outFile  =''
# my_utility.renameShapefile(outputPath, rgiPolygonShapefile+'_clean'+str(count-1), rgiPolygonShapefile)
# while count > 0:
# 	my_utility.deleteShapefile(outputPath, rgiPolygonShapefile+'_clean'+str(count-1))
# 	count-=1

# # Delete unnecessary fields in Centerline shapefile
# centerlineFieldsToDelete = ['SLOPE_CL', 'AREA', 'ABSMAX', 'TECHN', 'SUMUP', 'SUMDOWN', 'NR_UP', 'ITERATIONS', 'POWER1', 'POWER2', 'SMOOTHTOL', 'LENGTH_BR', 'MAIN', 'ORDER_LE', 'BUFDIST', 'LENGTHRES', 'ELEV_TOP', 'Shape_Leng']
# centerlineFields = [field.name() for field in lineLayer.pendingFields()]
# count = 0
# inFile = inputPath+'/'+centerlineShapefile+'.shp'
# outFile = outputPath+'/'+centerlineShapefile+'_clean'+str(count)+'.shp'
# for field in centerlineFields:
# 	if field in centerlineFieldsToDelete:
# 		print "Deleting field: " + field
# 		processing.runalg('qgis:deletecolumn', inFile, field, outFile)
# 		count+=1
# 		inFile = outFile
# 		outFile = outputPath+'/'+centerlineShapefile+'_clean'+str(count)+'.shp'
# print "Deleted " + str(count-1) + " fields." 		
# inFile = ''
# outFile  =''
# my_utility.renameShapefile(outputPath, centerlineShapefile+'_clean'+str(count-1), centerlineShapefile)
# while count > 0:
# 	my_utility.deleteShapefile(outputPath, centerlineShapefile+'_clean'+str(count-1))
# 	count-=1








# app.exitQgis()


# def extractNextLine(layer, order_le):
# 	query = '"ORDER_LE" = ' + order_le

# 	print Processing.getAlgorithm("qgis:extractbyexpression")
# 	single_centerline = outputPath + "/" + "single_centerline.shp"
# 	result = processing.runalg("qgis:extractbyexpression", lineLayer, query, single_centerline)
# 	output = result['OUTPUT']
	
	# tempLayer = processing.runalg('qgis:saveselectedfeatures', inputTrees, None)


	# selection = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
	# layer.setSelectedFeatures([k.id() for k in selection])

	# single_centerline = outputPath + "/" + "single_centerline.shp"
	# error = QgsVectorFileWriter.writeAsVectorFormat(layer, single_centerline, "CP1250", layer.crs(), "ESRI Shapefile")
	# if error == QgsVectorFileWriter.NoError:
 #    	print "success!"

# del rgiLayer
# del lineLayer


# app.exitQgis()

# when yat(-1)-yat(0) < 0 or yat(-1)-yat(0) > 0 then 
# (atan((xat(-1)-xat(0))/(yat(-1)-yat(0)))) * 180/3.14159 + 
# (180 *
# (((yat(-1)-yat(0)) < 0) + 
# (((xat(-1)-xat(0)) < 0 AND (yat(-1) - yat(0)) >0)*2)
# ))
# when ((yat(-1)-yat(0)) = 0 and (xat(-1) - xat(0)) >0) then 90
# when ((yat(-1)-yat(0)) = 0 and (xat(-1) - xat(0)) <0) then 270
# end


###

# True
# # loop through layer 
# for elem in layer.getFeatures():
#     geom= elem.geometry()
#     attr =elem.attributes()
#     (processing)

#  # interaction with other Python module: Shapely, for example
#  from shapely.geometry import shape
#  from json import loads
#  for elem in layer.getFeatures():
#        shapely_geometry = shape(loads(elem.geometry().exportToGeoJSON()))


# rgiLayer = processing.getObject(rgiPolygonShapefile)
# layer = iface.activeLayer()
# crs = layer.crs().authid()
# #crs = utils.iface.activeLayer().crs().authid()
# print(crs)

# rgi_id_field = 'RGIId'
# glims_id_field = 'GLIMSId'
# rgi_ids = rgiLayer.fieldNameIndex(rgi_id_field)

# # Find unique rgi_ids from field 'glac_id' in Randolph glacier polygons
# unique_rgi_ids = set([f[rgi_id_field] for f in processing.features(rgiLayer)])
# print(unique_rgi_ids)


#centerlines_all = processing.getObject(centerlineShapefile)
