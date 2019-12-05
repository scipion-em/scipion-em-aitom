import json

from tomo.objects import Coordinate3D


def json2Coordinates3D(jsonFile, coordinates):
    """ Loads a json file containing picking 3D coordinates and populates a
    SetOfCoordinates"""
    # NOTE: What is the box size?

    # Format is like this:
    # [{"peak": {"loc": [149, 12, 15]}}, ....]
    print ("File to parse: %s" % jsonFile)

    # read file
    with open(jsonFile, 'r') as myfile:
        data = myfile.read()

    # load json file
    peaks = json.loads(data)

    for item in peaks:
        x, y, z = item['peak']['loc']
        coord = Coordinate3D()
        coord.setPosition(x, y, z)
        coordinates.append(coord)
