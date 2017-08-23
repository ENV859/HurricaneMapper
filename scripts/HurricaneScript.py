#HurricaneScript.py
#
# Description: Runs the hurricane mapping tool from a python interface
#
# Fall 2012
# John Fay for ENV 859

import sys, os, arcpy

# Script inputs
Season = sys.argv[1]
StormName = sys.argv[2]
outTrackFC = sys.argv[3]         #optional
outCountiesFC = sys.argv[4]     #optional

# Path dependent inputs
scriptPath = os.path.dirname(sys.argv[0])
rootPath = os.path.dirname(scriptPath)
trackPointsFC = os.path.join(rootPath,"Data",'IBTrACTs_NAD83.shp')
countiesFC = os.path.join(rootPath,"Data",'USACounties.shp')

# Process 1: Select track points
queryString = "\"SEASON\" = %s AND \"NAME\" = '%s'" %(Season, StormName)
arcpy.AddMessage("...Selecting track points for %s in %s" %(StormName, Season))
SelPoints = arcpy.Select_analysis(trackPointsFC,"in_memory/TrackPoints",queryString)

# Process 2: Create a track line from points
arcpy.AddMessage("...Creating a storm track")
TrackLine = arcpy.PointsToLine_management(SelPoints,"in_memory/TrackLine","","ISO_time")

# Process 3: Save track line, if requested
if outTrackFC <> '#':
    arcpy.AddMessage("...Writing tracks to %s" %outTrackFC)
    arcpy.CopyFeatures_management(TrackLine,outTrackFC)

if outCountiesFC <> '#':
    arcpy.AddMessage("...Extracting impacted counties")
    # Process 4: Make County feature layer
    CountiesLyr = arcpy.MakeFeatureLayer_management(countiesFC,"CountiesLyr")

    # Process 5: Select impacted counties
    ImpactedLyr = arcpy.SelectLayerByLocation_management(CountiesLyr,"WITHIN_A_DISTANCE",TrackLine,"500 meters","NEW_SELECTION")

    # Process 6:
    arcpy.AddMessage("Writing counties to %s" %outCountiesFC)
    arcpy.CopyFeatures_management(ImpactedLyr,outCountiesFC)