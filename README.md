# exif-extractor
Python program to extrat exif data from images.

Program extracts image object data and exif data and prints to console, this includes camera data, location data, brightness settings etc.

came across gpsinfo within the metadata and got curious so done some looking around and found out how to convert the coordinates into decimal degrees so that i may find a geo location according to the coordinates, and used the geopy library to use the converted coordinates to find the location the image was taken.

