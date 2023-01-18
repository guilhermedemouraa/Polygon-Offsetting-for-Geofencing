# Polygon Offsetting

A Python and MATLAB script for generating offset polygons from a set of 2D coordinates.

## Description

The script `polygon_offset.py` for Python and `polygon_offset.m` for MATLAB takes a set of 2D coordinates that make a polygon, an offseting distance, and a desired direction to calculate new coordinates that make an offset polygon. The script uses the `utm` library for Python and `utmconv` function for MATLAB to convert latitude and longitude coordinates to UTM coordinates, and performs the offset calculation in UTM space. The script returns the offset polygon in lat/long and UTM coordinates.

## Inputs
- `polygon`: 2D array containing the coordinates of all vertices of a polygon
- `offset`: desired offset distance
- `direction`: direction at which the offset is desired ('i' for inward or 'o' for outward)
- `zone` and `letter`: UTM zone at which the lat/long coordinates were collected

## Outputs
- 2D array containing the coordinates of all vertices of the offset polygon (lat/long and UTM)

## Dependencies
The Python script has the following dependencies:
- `numpy`
- `utm`

The MATLAB script has the following dependencies:
- `utmconv` function

## Usage

### Python
import polygon_offset

geofence = [[latitude_coordinates],[longitude_coordinates]]
offset = 10
direction = 'o'
zone = 10
letter = 'N'

offset_polygon = polygon_offset(geofence, offset, direction, zone, letter)
import polygon_offset

geofence = [[latitude_coordinates],[longitude_coordinates]]
offset = 10
direction = 'o'
zone = 10
letter = 'N'

offset_polygon = polygon_offset(geofence, offset, direction, zone, letter)

### Matlab
offset_polygon = polygon_offset(geofence, offset, direction, zone, letter)

## Limitations
- script assumes that the input polygon is closed, i.e., the first and last vertex are the same.
- script assumes that the input polygon is simple, i.e., it does not self-intersect
- The script only works with 2D polygons.

## Examples
The repository includes example Excel files that demonstrate the usage of the script.

## Author

`polygon_offset.py` was written by Guilherme De Moura Araujo (gdemoura@ucdavis.edu)

## References
- The script is based on the method described in [1]
- The algorithm for finding bisectors of the polygon is based on code from [2]

[1] 
[2] https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges

## Contributions

If you would like to contribute to this project, please contact the author.

## License

This project is licensed under the terms of the MIT license.
Please let me know if there's anything else I can help you with.
