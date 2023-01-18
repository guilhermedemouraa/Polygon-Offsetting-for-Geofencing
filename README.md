# Polygon Offsetting for Geofencing

This repo contains a Python and a MATLAB script for generating offset polygons from a set of 2D coordinates. The scripts were originally developed for geofencing purposes, but can be applied for other uses as well.

## Description

The script `polygon_offset.py` for Python and `polygon_offset.m` for MATLAB takes a set of 2D coordinates that make a polygon, an offseting distance, and a desired direction (inward or outward) to calculate new coordinates that make an offset polygon. The python script is more advanced than the one in MATLAB as it uses the `utm` library for Python to convert latitude and longitude coordinates to UTM coordinates, and performs the offset calculation in UTM space. The script returns the offset polygon in lat/long and UTM coordinates. The script in MATLAB doesn't have the capability of working with latitude/longitude coordinates. However, one could use the matlab function `utmconv` for that purpose.

## Inputs
- `polygon`: 2D array containing the coordinates of all vertices of a polygon
- `offset`: desired offset distance
- `direction`: direction at which the offset is desired ('i' for inward or 'o' for outward)
- `zone` and `letter`: UTM zone at which the lat/long coordinates were collected (python script only)

## Outputs
- 2D array containing the coordinates of all vertices of the offset polygon (lat/long and UTM)

## Dependencies
The Python script has the following dependencies:
- `numpy`
- `utm`

## Usage

### Python
`import polygon_offset`

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
offset_polygon = polygon_offset(geofence, offset, direction)

## Limitations
- script assumes that the input polygon is closed, i.e., the first and last vertex are the same.
- script assumes that the input polygon is simple, i.e., it does not self-intersect
- The script only works with 2D polygons.

## Examples
- The repository includes example [Excel files](https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/tree/main/example) that demonstrate the usage of the python script. Below are a few screenshots from the outputs of the python script:

![python_example_1](https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/figures/python_example_1.png)
![python_example_2](https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/figures/python_example_2.png)
![python_example_3](https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/figures/python_example_3.png)
![python_example_4](https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/example/figures/python_example_4.png)

- In addition, this repository includes a MATLAB file ([`Polygon_ofsett_demo.m`](https://github.com/guilhermedemouraa/Polygon-Offsetting-for-Geofencing/blob/main/Polygon_offset_demo.m)) that demonstrates the usage of the MATLAB script.

## References
[1] https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges

## Contributions

If you would like to contribute to this project, please [contact the author](mailto:gdemoura@ucdavis.edu).

## License

This project is licensed under the terms of the MIT license.

Please let me know if there's anything else I can help you with.
