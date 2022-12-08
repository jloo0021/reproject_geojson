# must install pyproj: open cmd and type "pip install pyproj"
from pyproj import Transformer
import json
from shapely.geometry import multilinestring, mapping


# function to convert all geojson multiline string coordinates from one CRS to another CRS
# assumes that geojson features are multiline strings, with coordinates in long, lat order
# source and dest are the EPSG codes of the source and destination CRSs respectively
def reproject_geojson_coords(source_epsg_code: int, dest_epsg_code: int, geojson):

    # set always_xy to true so that we get our output coordinates in long, lat order
    transformer = Transformer.from_crs(source_epsg_code, dest_epsg_code, True)

    # iterate over features
    for feature in geojson["features"]:

        # get all coordinates
        coords = feature["geometry"]["coordinates"]

        # each element in coords is a line, i.e. an array containing 2 coordinate pairs, e.g. [[x1, y1], [x2, y2]]
        for line in coords:
            for point in line:

                # transform each point
                transformed_point = transformer.transform(point[0], point[1])

                # overwrite old geojson data with transformed coords
                point[0] = transformed_point[0]
                point[1] = transformed_point[1]

    # write transformed geojson to a new file
    with open("transformed_geojson.geojson", "w") as outfile:
        outfile.write(json.dumps(geojson))


if __name__ == "__main__":

    # EDIT THESE VARIABLES TO MAKE THE SCRIPT DO WHAT YOU WANT
    file_path = r"D:\Software Projects\Multiviz Internship\Misc GeoJSON Files\liveability_sa1_2011_difference.geojson"
    source_epsg_code = 7845
    dest_epsg_code = 4236

    # load geojson from file
    with open(file_path, "r") as infile:
        geojson = json.load(infile)

    # reproject from ... to ..., writes to a new geojson file with the new projection
    reproject_geojson_coords(source_epsg_code, dest_epsg_code, geojson)




