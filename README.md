### Description of the problem
We have 250 colorful spots in the shape of a circle at our disposal.
The task is to find the optimal arrangement of the wheels and select the parameters of each wheel in such a way that the resulting image best resembles the input image.

We defined the distance between two images as the sum of the differences within all pixels between a given image and the target image.
The objective function is the distance of a given image from the target image.<br/>
We also considered a slightly modified version of the above objective function. To take into account a greater penalty for large color deviations, the squared differences at individual pixels are summed instead of differences in the objective function.

Each stain is described by 3 parameters: color, center coordinates and radius. The stains are applied in layers, so each stain is also assigned a ranking.
It indicates the layer on which the stain is located.

### Algrithm 

Simple Genetic Algorithm was used to solve the problem. The main mechanism used during evolution is mutations.

### Results 
![mona_szara](https://github.com/michalfica/algorytmy-ewolucyjne---projekt-/assets/51112297/9152c136-bbe9-436d-8178-f7eaae81e66d) ![22050__0%](https://github.com/michalfica/algorytmy-ewolucyjne---projekt-/assets/51112297/0319ca5b-a97a-4b45-ac5f-f0204bbc1502)

