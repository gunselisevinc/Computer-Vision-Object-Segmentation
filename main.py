
###IMPORTANT###
# I wrote this code on Mac so file paths organization can differ in Windows, so please run on Linux if you get a file path error.

import math
from PIL import Image, ImageDraw
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import random
import glob
import os


### FUNCTION DEFINITIONS ###

# This function returns normalized version of an image.
def NormRGB(fileName):
    # Load image:
    input_image = Image.open(fileName)
    input_pixels = input_image.load()

    # Create output image
    output_image = Image.new("RGB", input_image.size)
    draw = ImageDraw.Draw(output_image)

    # Generate image
    for x in range(output_image.width):
        for y in range(output_image.height):
            r, g, b = input_pixels[x, y]
            r = int(r / (r + g + b) * 255)  # since the result of this operation gives a number between 0-1, had to multiplied with 255
            b = int(b / (r + g + b) * 255)
            g = int(g / (r + g + b) * 255)
            draw.point((x, y), (r, g, b))

    return output_image


# This function returns a clustered version of the image.
def Kmeans(imageFile, k):
    listOfCentroid = []
    for i in range(k):
        listOfRGBVal = []
        for j in range(3):
            listOfRGBVal.append(random.randrange(0, 255))
        listOfRGBVal.append(-1)
        listOfCentroid.append(listOfRGBVal)

    # Load image:
    input_image = Image.open(imageFile)
    input_pixels = input_image.load()

    # Create output image
    output_image = Image.new("RGB", input_image.size)
    draw = ImageDraw.Draw(output_image)

    for iteration in range(10):
        # Generate image
        for x in range(output_image.width):
            for y in range(output_image.height):
                currentRGB = input_pixels[x, y]
                minDist = 500  # to determine the closest centroid
                for centroid in listOfCentroid:
                    dist = euclidianDistance(currentRGB, centroid)
                    centroid[3] = dist
                    if dist < minDist:
                        minDist = dist     # finding minimum distance to centroids

                currentCentroid = listOfCentroid[0]
                for centroid in listOfCentroid:
                    if centroid[3] == minDist:
                        currentCentroid = centroid  # storing the closest centroid

                # assigning the closest centroid values to the current pixel
                r, g, b = currentRGB

                r = int(currentCentroid[0])
                g = int(currentCentroid[1])
                b = int(currentCentroid[2])
                draw.point((x, y), (r, g, b))

        """
        inputclusterpixels = output_image.load()
        for centroid in listOfCentroid:   # updating cluster centroids
            sumR, sumG, sumB = 0, 0, 0
            count = 0
            for x in range(output_image.width):
                for y in range(output_image.height):
                    currentR, currentG, currentB = inputclusterpixels[x, y]
                    normalisedR, normalisedG, normalisedB = input_pixels[x,y]
                    if ((currentR == centroid[0]) and (currentG == centroid[1]) and (currentB == centroid[2])):
                        sumR += normalisedR
                        sumG += normalisedG
                        sumB += normalisedB
                        count += 1
            rCent = sumR / count
            gCent = sumG / count
            bCent = sumB / count
            centroid[0] = rCent
            centroid[1] = gCent
            centroid[2] = bCent
        """
        # updating cluster centroids part is commented because it doesn't work properly.
    return output_image


# This function masks the image and changes all object colors
# rather than skin to white.
def Masking(imageFile):
    # Load image:
    input_image = Image.open(imageFile)
    input_pixels = input_image.load()

    # Create output image
    output_image = Image.new("RGB", input_image.size)
    draw = ImageDraw.Draw(output_image)

    # Assuming the middle pixel is a part of skin
    midx = int(output_image.width / 2)
    midy = int(output_image.height / 2)
    rSkin, gSkin, bSkin = input_pixels[midx, midy]

    # Generate image
    for x in range(output_image.width):
        for y in range(output_image.height):
            r, g, b = input_pixels[x, y]
            if r != rSkin and g != gSkin and b != bSkin:
                r, g, b = 255, 255, 255
            draw.point((x, y), (r, g, b))
    return output_image


# This function returns euclidian distance between
# two pixel values.
def euclidianDistance(x1, x2):
    distance = math.sqrt(((x1[0] - x2[0]) ** 2) + ((x1[1] - x2[1]) ** 2) + ((x1[2] - x2[2]) ** 2))
    return distance


# This function defines a value as peak if bigger than 110% of the
# neighbors and bigger than 15% of the max value.
def findNumOfPeaks(a):
    x = np.array(a)
    max = np.max(x)
    lenght = len(a)
    ret = []
    for i in range(lenght):
        ispeak = True
        if i - 1 > 0:
            ispeak &= (x[i] > 1.1 * x[i - 1])
        if i + 1 < lenght:
            ispeak &= (x[i] > 1.1 * x[i + 1])

        ispeak &= (x[i] > 0.15 * max)
        if ispeak:
            ret.append(i)
    return len(ret)


### MAIN ###
filePath = input("Enter the path of database: ")
i = 0

# Directory creation for storing output results.
try:
    os.mkdir(filePath + "/Segmentation Details")
    print("Segmentation Details directory created")

except:
    print("Segmentation Details directory already exists")

try:
    os.mkdir(filePath + "/Segmentation Details" + "/Normalised Images")
    print("Segmentation Details - Normalised Images directory created")
except:
    print("Normalised Images directory already exists")

try:
    os.mkdir(filePath + "/Segmentation Details" + "/Histograms")
    print("Segmentation Details - Histograms directory created")
except:
    print("Histograms directory already exists")

try:
    os.mkdir(filePath + "/Segmentation Details" + "/Clustered Images")
    print("Segmentation Details - Clustered Images directory created")
except:
    print("Clustered Images directory already exists")

# All function calls and operations
for filename in glob.glob(filePath + '/*.png'):
    # print(filename)
    im = Image.open(filename)
    i += 1
    normalisedFileName = filePath + "/Segmentation Details/Normalised Images/normalised" + str(i) + ".png"
    NormRGB(filename).save(normalisedFileName)  # Image normalized and saved.

    image = io.imread(normalisedFileName)
    hist = plt.hist(image.ravel(), bins=256, color='black', alpha=0.5)
    hist = plt.legend(['Total'])
    plt.savefig(filePath + "/Segmentation Details" + "/Histograms" + '/plot' + str(i) + '.png')  # Histograms created and saved.

    imageForPeak = Image.open(normalisedFileName)
    a = imageForPeak.histogram()
    k = findNumOfPeaks(a)  # K value is determined intelligently by finding number of peaks.
    # print(k)
    Kmeans(normalisedFileName, k).save(filePath + "/Segmentation Details" + "/Clustered Images/clustered" + str(i) + ".png")

    clusteredFileName = filePath + "/Segmentation Details" + "/Clustered Images/clustered" + str(i) + ".png"
    Masking(clusteredFileName).save(filePath + "/Segmentation Details/masked" + str(i) + ".png")