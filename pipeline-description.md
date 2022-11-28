## Model 
  * ViTAE Transformer RVSA, [paper](https://ieeexplore.ieee.org/document/9956816), [model with weights](https://github.com/ViTAE-Transformer/Remote-Sensing-RVSA).
  * Pretrained on Million-AID (a large-scale benchmark dataset containing a million instances for remote sensing (satellite images) scene classification.
  * Finetuned on ISPRS Potsdam dataset (a smaller satellite imagery dataset with 5 classes)
  * Encoder/Backbone is a transformer with some fancy stuff to encode the plain vision/top-down view data -- exactly what we have as well.
  * Decoder is UPerNet.
## Our dataset preparation
  * 3 classes - background, MT, and ER/CL.
  * created masks for each class by taking all pixels 0< as a mask.
  * Padded all images with 0s to 6500px, to match the size of the largest image in dataset
  * Filtered small (<50 px area) standalone (connectivity = 50) objects in MT masks.
  * Overlapped the masks and images by summing the pixel values in real images.
  * MT/ER dataset is ~2200 images, MT/CL dataset is ~2900 images.
## Training
  * First trained on MT/ER:
    * deteriorated the MT masks by flipping 25% of MT mask pixels to black (background).
    * Loaded the model Finetuned on ISPRS Potsdam dataset.
    * Trained for 160k iterations with random crops of 512x512px. The random crop is discarded, if the background is more than 97% of the image.
    * Used Dice loss + Focal loss to overcome the class imbalance.
  * The model that was trained for MT/ER was then loaded and trained with MT/CL data for 160k iterations.
  * The model requires ~10Gb of GPU memory.
## Inference
  * The inference is performed by sliding window of 512px with stride of 384px.
  * Inference on 6000px images is as good as with small images. No pre-cropping or tiling is needed.
