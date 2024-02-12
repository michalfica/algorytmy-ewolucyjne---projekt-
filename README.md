### Description of the problem
We have 250 colorful spots in the shape of a circle at our disposal.
The task is to find the optimal arrangement of the wheels and select the parameters of each wheel in such a way that the resulting image best resembles the input image.

We defined the distance between two images as the sum of the differences within all pixels between a given image and the target image.
The objective function is the distance of a given image from the target image.<br/>
We also considered a slightly modified version of the above objective function. To take into account a greater penalty for large color deviations, the squared differences at individual pixels are summed instead of differences in the objective function.

The image is encoded using an individual. Each individual remembers the list of spots that make up this picture.

Each stain is described by 3 parameters: color, center coordinates and radius. The stains are applied in layers, so each stain is also assigned a ranking.
It indicates the layer on which the stain is located.
