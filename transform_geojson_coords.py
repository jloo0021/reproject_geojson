# must install pyproj: open cmd and type "pip install pyproj"
from pyproj import Transformer
import json
from shapely.geometry import multilinestring, mapping
import cProfile
import time


# function to convert all geojson multiline string coordinates from one CRS to another CRS
# currently supports geojson features that are: {multiline strings, polygons, multipolygons}, with coordinates in long, lat order
# source and dest are the EPSG codes of the source and destination CRSs respectively
def reproject_geojson_coords(source_epsg_code: int, dest_epsg_code: int, geojson):

    # set always_xy to true so that we get our output coordinates in long, lat order
    transformer = Transformer.from_crs(source_epsg_code, dest_epsg_code, True)

    # iterate over features
    for feature in geojson["features"]:

        # get all coordinates
        coords = feature["geometry"]["coordinates"]

        # TODO: find out if there is a less repetitive way to do this instead of else-if'ing based on geometry type
        # TODO: add support for point, multipoint, and linestring
        # multiline string feature
        if feature["geometry"]["type"] == "MultiLineString":
            # each element in coords is a line, i.e. an array containing 2 coordinate pairs, e.g. [[x1, y1], [x2, y2]]
            for line in coords:
                for point in line:

                    # transform each point
                    transformed_point = transformer.transform(point[0], point[1])

                    # overwrite old geojson data with transformed coords
                    point[0] = transformed_point[0]
                    point[1] = transformed_point[1]

        # polygon feature
        elif feature["geometry"]["type"] == "Polygon":
            # each element in a polygon is an array of points
            for points in coords:

                # each element in polygon is a point
                for point in points:

                    # transform each point
                    transformed_point = transformer.transform(point[0], point[1])

                    # overwrite old geojson data with transformed coords
                    point[0] = transformed_point[0]
                    point[1] = transformed_point[1]

        # multipolygon feature
        elif feature["geometry"]["type"] == "MultiPolygon":

            # each element in coords is a polygon, each polygon is a 1 element array, containing an array of points
            for polygon in coords:
                for points in polygon:
                    for point in points:
                        # transform each point
                        transformed_point = transformer.transform(point[0], point[1])

                        # overwrite old geojson data with transformed coords
                        point[0] = transformed_point[0]
                        point[1] = transformed_point[1]

    # convert back to geojson
    return json.dumps(geojson)


# converts all features in a geojson from multiline strings to polygons by using shapely buffer
def buffer_multilinestr_to_polygon(geojson, buffer_size: int):
    # iterate over features
    num_features = len(geojson["features"])

    for i in range(num_features):
        feature = geojson["features"][i]

        # each feature should be a multiline string, so we want to create a shapely multiline string using its coords
        multiline_str = multilinestring.MultiLineString(feature["geometry"]["coordinates"])

        # apply buffer to turn each feature into a polygon and map it into geojson geometry form
        # cap_style: 1 = round, 2 = flat, 3 = square
        # join_style: 1 = round, 2 = mitre, 3 = bevel
        # TODO: figure out the best cap/join style. round cap + join gives best looking lines but costs the most
        # cap 2 join 3 is quite cheap, doesn't look amazing tho
        buffered_feature = multiline_str.buffer(buffer_size, cap_style=2, join_style=3)
        buffered_feature = mapping(buffered_feature)

        # overwrite existing multiline string feature geometry with new polygon feature geometry
        geojson["features"][i]["geometry"] = buffered_feature

    # call json.dumps to convert all the tuples back into geojson valid format
    return json.dumps(geojson)


if __name__ == "__main__":

    # TRANSFORMS INPUT GEOJSON BY BUFFERING, THEN REPROJECTING
    # EDIT THESE VARIABLES TO MAKE THE SCRIPT DO WHAT YOU WANT
    file_path = r"D:\Software Projects\Multiviz Internship\Misc GeoJSON Files\liveability_sa1_2011_difference.geojson"
    source_epsg_code = 7845
    dest_epsg_code = 4236

    # load geojson from file
    with open(file_path, "r") as infile:
        geojson = json.load(infile)

    # buffer the geojson
    geojson = buffer_multilinestr_to_polygon(geojson, 1)

    # convert buffered geojson back to python dict
    geojson = json.loads(geojson)

    # reproject from ... to ...
    geojson = reproject_geojson_coords(source_epsg_code, dest_epsg_code, geojson)

    # write transformed geojson to a new file
    with open("transformed_geojson.geojson", "w") as outfile:
        outfile.write(geojson)





