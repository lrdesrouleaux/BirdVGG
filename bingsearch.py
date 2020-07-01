from requests import exceptions
import argparse
import requests
import cv2 as cv
import os
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", default="blue jay", required=False,
                help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", default="/Users/lens/Documents/CVproject/dataset/bluejaypics", required=False,
                help="path to output directory of images")
ap.add_argument("-m","--max",default=100,required=False,
help="Maximum number of searches committed" )
args = vars(ap.parse_args())
#APIKEY = can't show my API key for obvious reasons
maxresults = int(args["max"])
groupsize = 50

URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"
# filter out these errors
EXCEPTIONS = set([IOError, FileNotFoundError,
                  exceptions.RequestException, exceptions.HTTPError,
                  exceptions.ConnectionError, exceptions.Timeout])
# store the search term and set headers and parameters for search
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key": APIKEY}
params = {"q": term, "offset": 0, "count": groupsize}
# search
print("<info> searching bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()
# find results from search, including roral of results
results = search.json()
enr = min(results["totalEstimatedMatches"], maxresults)
print("<info> {} total results for '{}'".format(enr, term))
#total number of images downloaded
total = 0
#loop over results in groupsize groups
for offset in range(0, enr, groupsize):
    print("<info> making requests for group {}-{} of {}...".format(offset,
                                                                   offset+groupsize, enr))
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()
    print("<info> saving images for group {}-{} of {}...".format(
        offset, offset+groupsize, enr))
    for v in results["value"]:
        #try to download the image
        try:
            #request to download
            print("<info> fetching: []".format(v["contentUrl"]))
            r = requests.get(v["contentUrl"], timeout=30)
            #build path to output image
            ext = v["contentUrl"][v["contentUrl"].rfind("."):]
            p = os.path.sep.join([args["output"], "{}{}".format(
                str(total).zfill(8), ext)])
            #write image to file
            f = open(p, "wb")
            f.write(r.content)
            f.close()
            #catch errors relating to downloading te image and skip if error is related
        except Exception as e:
            if type(e) in EXCEPTIONS:
                print("<info> error downloading {} skipping...".format(
                    v["contentUrl"]))
                continue
        image=cv.imread(p)
        #delete if image is None
        if image is None:
            print("<info> deleting: {} as it is null or not a .jpg".format(p))
            try:
                os.remove(p)
            #When I tested this I found that sometimes it couldn't find the null image 
            #So I added this error to skip the deletion if it cannot find the null image
            except FileNotFoundError:
                print("<info> {} not found skipping deletion...".format(p))
                pass
            continue
        total+=1