# -*- coding: utf-8 -*-
"""
Spatial Leave-One-SubGroup-Out (SLOSGO)
======================================================

This example shows how to make a Spatial Leave-One-SubGroup-Out.

"""

##############################################################################
# Import librairies
# -------------------------------------------
import numpy as np
from museotoolbox.cross_validation import SpatialLeaveOneSubGroupOut
from museotoolbox import datasets,processing
##############################################################################
# Load HistoricalMap dataset
# -------------------------------------------

_,centroid = datasets.load_historical_data(low_res=True,centroid=True)
raster,vector = datasets.load_historical_data(low_res=True)

field = 'Class'

##############################################################################
# Extract label ('Class' field) and groups ('uniquefid' field)
# Compute distanceMatrix with centroid (one point per group)

X,y,groups = processing.extract_ROI(raster,vector,field,'uniquefid')
distance_matrix,distance_label = processing.get_distance_matrix(raster,centroid,'uniquefid')

##############################################################################
# Create CV
# -------------------------------------------
# n_splits will be the number  of the least populated class

SLOSGO = SpatialLeaveOneSubGroupOut(distance_thresold=100,distance_matrix=distance_matrix,
                                   distance_label=distance_label,random_state=12)


###############################################################################
# .. note::
#    Split is made to generate each fold
SLOSGO.get_n_splits(X,y,groups)
for tr,vl in SLOSGO.split(X,y,groups):
    print(np.unique(groups[vl]))
    print(np.unique(groups[tr]))
    
SLOSGO.save_to_vector(vector,'Class','uniquefid','/tmp/slosgo.gpkg')
#############################################
# Draw image
from __drawCVmethods import plotMethod
plotMethod('SLOO-group')