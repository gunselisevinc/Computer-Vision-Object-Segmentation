# Computer Vision Object Segmentation
Segmentation step of Automatic Sign Language Recognition System (ASLRS)

## Functions
### NormRGB
The common RGB representation of color images is not suitable for characterizing skin-color. In the RGB space, the components R, G and B represents not only color, but also luminance. Luminance may vary across skin due to the ambient lighting and is not a reliable measure in separating skin from non- skin regions. Luminance can be removed from the color representation in the normalized RGB space. Chromatic colors, also known as "pure" colors in the absence of luminance, are defined by the simple normalization process shown below:
r = R/(R+G+B)
b = B/(R+G+B)
g = G/(R+G+B)

### KMeans
The program selects the seeds and K intelligently from the image using its color histogram. Given the histogram, the seed and K selection are automatic. One way to go is to find the peaks in the color histogram as candidates for seeds. Also, K is closely related to the number of peaks in the histogram. Not all the peaks are necessary so only the dominant ones are needed, so the ones that occupies a certain portion of image in terms of pixels are picked.

### Masking
This function finds come up with a characterization for skin pixels. Then, any other pixel rather than skin is set to zero.

### EuclidianDistance
Calculates the euclidian distance between two pixels.

### findNumOfPeaks
Calculates the number of peaks of an image intelligently.

## Input/Output Format
### Input:
The path of the database. (such as: /Users/xxx/Desktop/Dataset)

### Output:
Folder named as “SegmentationResults” is created in the database folder and segmented images are saved.
