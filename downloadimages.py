from imutils import paths
import argparse
import requests
import cv2 as cv
import os
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", default="/Users/lens/Documents/CVproject/dataset/urls.txt", required=False,
                help="path to file containing image URLs")
ap.add_argument("-o", "--output", default="/Users/lens/Documents/CVproject/dataset/bluejaypics", required=False,
                help="path to output directory of images")
args = vars(ap.parse_args())
# grab the list of URLs from the input file, then initialize the
# total number of images downloaded thus far
rows = open(args["urls"]).read().strip().split("\n")
total = 0
#loop over the urls
for url in rows:
    try:
        #make the requests on the url and download them to files
        r = requests.get(url, timeout=60)
        p = os.path.sep.join([args["output"], "{}.jpg".format(
            str(total).zfill(8))])
        f = open(p, "wb")
        f.write(r.content)
        f.close()
        print("<info> downloaded:{}".format(p))
        total += 1
    #skip any images with errors downloading
    except:
            print("<info> error downloading {}... skipping".format(p))
#loop over the image path I downloaded
for imagepath in paths.list_images(args["output"]):
    #initialize if image should be deleted
    delete=False
    #try to load the image
    try:
        image=cv.imread(imagepath)
        #if the image is null it wasn't properly loaded so delete
        if image is None:
            delete=True
        #if opencv can't load it needs to be deleted too
    except:
        print("Except")
        delete=True

    if delete:
        print("<info> deleting {}".format(imagepath))
        os.remove(imagepath)
