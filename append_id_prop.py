import json

def append_id_prop(geojson):
    # iterate over features
    num_features = len(geojson["features"])

    for i in range(num_features):
        feature = geojson["features"][i]
        id = {"id": i}
        feature["properties"].update(id)

    # call json.dumps to convert all the tuples back into geojson valid format
    return json.dumps(geojson)


if __name__ == "__main__":

    # EDIT THESE VARIABLES TO MAKE THE SCRIPT DO WHAT YOU WANT
    file_path = r"D:\Software Projects\Multiviz Internship\Experimenting Repo\wombling_experiment\boundaries_SA1_2011_dist_wgs84_buffered7.geojson"

    # load geojson from file
    with open(file_path, "r") as infile:
        geojson = json.load(infile)

    geojson = append_id_prop(geojson)

    # write transformed geojson to a new file
    with open("appended_id_geojson.geojson", "w") as outfile:
        outfile.write(geojson)
