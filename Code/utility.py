import os
import settings
import shutil


fileExt = ['cpg', '.csv', '.dbf', '.prj', '.qpj', '.sbn', '.shp', '.shx']

def copyShapefile(srcPath, dstPath):
    if os.path.isfile(srcPath):
        try:
            srcPath = srcPath[:-4]
            if os.path.isfile(dstPath): 
                dstPath = dstPath[:-4]
                for ext in fileExt:
                    if os.path.isfile(srcPath+ext):
                        if(ext == '.qpj'):
                            os.remove(srcPath+ext)
                        else:
                            shutil.copy2(srcPath+ext, dstPath+ext)
            elif os.path.isdir(dstPath):
                for ext in fileExt:
                    if os.path.isfile(srcPath+ext):
                        if(ext == '.qpj'):
                            os.remove(srcPath+ext)
                        
                        else:
                            shutil.copy2(srcPath+ext, dstPath)
        except shutil.Error:
                print shutil.Error
    else:
        print "Error: 'srcPath': %s is not a valid filepath." % srcPath

def deleteShapefile(filePath):
    filePath = filePath[:-4]
    for ext in fileExt:
        if os.path.isfile(filePath+ext):
            os.remove(filePath+ext)

def getPath_centerlines():
    return settings.centerlines

def getPath_main():
    return settings.main_path

def getPath_glaciers():
    return settings.glaciers

def getPath_inputs():
    return settings.input_paths

def getPath_outputs():
    return settings.output_paths

def getSteps():
    return settings.steps

def renameShapefile(oldFilePath, newFilePath):
    if not os.path.isfile(oldFilePath):
        print "ERROR renaming shapefile:\n %s is not a valid path" % oldFilePath
        return
    else:
        oldFilePath = oldFilePath[:-4]
        newFilePath = newFilePath[:-4]
        for ext in fileExt:
            if os.path.isfile(oldFilePath+ext):
                if(ext == '.qpj'):
                    os.remove(oldFilePath+ext)
                else:
                    os.rename(oldFilePath+ext, newFilePath+ext)
                # print "Renamed %s to: %s" % (os.path.basename(oldFilePath+ext),os.path.basename(newFilePath+ext))