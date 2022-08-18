from PIL import Image
from PIL.ExifTags import TAGS
import sys
from exif import Image as exifGPS
from geopy.geocoders import Nominatim

# calling nominatim tool for geo location services
geoLoc = Nominatim(user_agent="GetLoc")

# May only work with jpeg images
# will try to work with other formats
def captureImgObj():
    try:
        imageToUse = sys.argv[1]
        print("\nsys argv was used to get image\n\n")
    except:
        imageToUse = input("Please enter image path or paste image in program folder and enter imageName.jpg: ")

    # read image data using the pillow library
    image = Image.open(imageToUse)

    # extracting basic metadata from image object
    metadata = {
        "Filename": image.filename,
        "Image Size": image.size,
        "Image Height": image.height,
        "Image Width": image.width,
        "Image Format": image.format,
        "Image Mode": image.mode,
        "Image is Animated": getattr(image, "is_animated", False),
        "Frames in Image": getattr(image, "n_frames", 1)
    }
    return [imageToUse, image, metadata]

# function to print the metadata in a pretty format
def printMetadata(metadata):
    print("\t\tImage Object Metadata:\n")
    for label,value in metadata.items():
        print(f"{label:25}: {value}")
    print("\n\t\tExif Data:\n")


# extract exif data
# field names in variable exifData are now non human readable hence we use TAGS
# which maps each tag id to human readable text
def getAndPrintExif(image):
    exifData = image.getexif()

    for tagId in exifData:
        # get tag name in human readble formats
        tag = TAGS.get(tagId, tagId)
        data = exifData.get(tagId)

        # decode bytes
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except:
                data = 'error decoding data'
        print(f"{tag:25}: {data}")

    print("\n\n--------------------------------\n\n")

# long = image.gps_longitude
# ref = image.gps_longitude_ref

# convert coordinates into decimal degrees(DD)
# coords are given in the format (degrees, minutes, seconds)
# that is why the function is degrees + minutes / 60 + seconds / 3600
# 60 minutes in an hour, 3600 seconds in an hour
def decimal_coords(coords, ref):
    DD = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W": 
        DD = -DD
    return DD

def image_coordinates(img_path):
    # state for image with no exif to clost without printing final statements
    exif = True

    # imported the exif library to easily grab gps data for conversion
    # may hack around and get pillow to do the same thing
    # but works either way
    
    with open(img_path, 'rb') as src:
        # open image with exif
        img = exifGPS(src)
        #if exif data exists 
        if img.has_exif:
            try:
                img.gps_longitude
                coords = (decimal_coords(img.gps_latitude,
                      img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
            except AttributeError:
                print('No Coordinates available.')
                exif = False
        else:
            print('The Image has no EXIF information' ) 
            exif = False
    if exif:
        print(f"Taken at: {img.datetime_original}\nCoordinates:{coords}")
        print("\n\t\tLocation taken: \n\n"+ str(geoLoc.reverse(coords)) + "\n\n")


if __name__ == "__main__": 
    imageToUse, image, metadata = captureImgObj()
    printMetadata(metadata)
    getAndPrintExif(image)
    image_coordinates(imageToUse)
