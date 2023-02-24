# reproject_geojson
This repository contains various scripts used to create/modify the boundaries files used for the MultiViz Wombling Project: https://github.com/jloo0021/wombling_experiment

These scripts need to be run locally, and with the appropriate source files. Therefore, some changes will need to be made to the script (e.g. the source file location on your device) to produce the intended results.

transform_geojson_coords.py is used to buffer and/or reproject geojson features. It contains two functions; one to buffer and one to reproject. Buffering is necessary to create the source for the app's 3D mode, and reprojection is necessary as the app only works if the feature geometries are in wgs84 format. 

append_id_prop.py is used to append a unique ID to the properties of each geojson feature. These ID's are currently required to convert between 2D and 3D modes in the app.

appendDistances_SA1_2011.R is used to append distance between neighbouring areas' centroids to the properties of each geojson feature. Distances are needed for distance weighting in the womble calculation. Currently this script only works for SA1 2011 and I can't figure out why it doesn't work for SA1 2016.
