# -*- coding: utf-8 -*-

import arcpy
from project import CompanyCamProject
import pandas as pd
import datetime
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        project_id = arcpy.Parameter(
            displayName="Project ID",
            name="project_id",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        
        output_feature = arcpy.Parameter(
            displayName="Output Feature Folder",
            name="output_feature",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        start_date = arcpy.Parameter(
            displayName="Start Date - Optional",
            name="start_date",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")
        
        end_date = arcpy.Parameter(
            displayName="End Date - Optional",
            name="end_date",
            datatype="GPDate",
            parameterType="Optional",
            direction="Input")
        
        input_feature = arcpy.Parameter(
            displayName="Text File with ",
            name="input_feature",
            datatype="DETextfile",
            parameterType="Required",
            direction="Input")


        params = [project_id, output_feature, start_date, end_date, input_feature]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        project_id = parameters[0].valueAsText
        output_feature = parameters[1].valueAsText
        start_date = parameters[2].valueAsText
        end_date = parameters[3].valueAsText
        input_feature = parameters[4].valueAsText

        start_date = self.date_to_unix(start_date)
        end_date = self.date_to_unix(end_date)


        with open(input_feature, 'r') as file:
            token = file.read().strip()
        # """The source code of the tool."""
        project = CompanyCamProject(token)

        project.get_project(project_id)
        name = 'Photos_'+self.clean_string(project.name.split(' ')[0])
        photos = project.get_project_photos(project_id, start_date, end_date)
        spatial_reference = arcpy.SpatialReference(4326)  # WGS 1984

        arcpy.management.CreateFeatureclass(
                                    arcpy.env.workspace,
                                    out_name=name, 
                                    geometry_type="POINT",
                                    spatial_reference=spatial_reference)
        
        arcpy.management.AddFields(name, 
                                    [['id', 'TEXT', 'ID', 50], 
                                    ['url', 'TEXT', 'URL', 255], 
                                    ['date', 'TEXT', 'DATE', 50], 
                                    ['user', 'TEXT', 'USER', 50]])
        
        with arcpy.da.InsertCursor(name, ["SHAPE@", 'id', 'url', 'date', 'user']) as cursor:
            for index, row in photos.iterrows():
                longitude = float(row['lon'])
                latitude = float(row['lat'])
                point = arcpy.Point(longitude, latitude)
                pt_geometry = arcpy.PointGeometry(point, spatial_reference=spatial_reference)
                cursor.insertRow([pt_geometry, row['id'], row['url'], row['date'], row['user']])

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        map = aprx.activeMap
        layer = arcpy.management.MakeFeatureLayer(name, name).getOutput(0)

        # Add the layer to the map
        map.addLayer(layer) 
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

    def date_to_unix(self, date):
        only_date = date.split(' ')[0]
        month, day, year = only_date.split(r'/')
        return int(datetime.datetime(int(year), int(month), int(day)).timestamp())
    
    def clean_string(self, string_in):
        return''.join(letter for letter in string_in if letter.isalnum())
        