# August'22
  
### Software
* Software is available at the [corresponding github repo](https://github.com/Clement-Cabriel/Evb-SMLM). The code is quite well documented and seems readable, at first glance.

### Next steps:
* lend the camera from IOF? It is the same model, as I remember. This increases our chances for painless setting up according to existing manual.
* find smlm setup that could be suitably modified.
* try to run the code with the example 10-second recording of blinking from event camera.

## Segmentation task:
* installed corresponding repos to ubuntu --> so much better to work with PC!
* rewriting the pipeline for MTs and vesicles in two separate scripts --> done.
* got the tiles working again.
* anna-palm works only with CPU-tensorflow on RTX3090.

# September - October '22

## Notes and ideas
* It is possible to predict the covered structure behind the other one --> discuss whether this is worth doing.
* Add full resolution images to the dataset along with 512px crops.

## Aims 
* Train the model with and without pretrained decoder with same hyperparameters.
  * The backbone (encoder) is usually left with pretrained weights for segmentation tasks. 
  * Try different decoder models available for HRNet backbone and ResNet.
* Add new data from Gregor to the dataset.
* Add new classes of organelles.

## Logs
* loaded new data from Gregor
* researched whether more than 8 bits in images is helpful for segmentation --> the cost of overhead is higher than benefits.
* next up: try segmentation with same hyperparameters, but with pixel values as masks.
* find if there is a better framework (fastai, hugginface, detectron2) --> mmdet turned out to be the best.
* created a dataset with ER, VES+CLATHRIN, MT full image overlaps with zero padding to 6541px. 
* calculated the class distrubution weights to be [Background, MT, Clathrin][0.0035031103, 0.3504681, 0.6460288]

|  Backbone  |    Decoder   | Pretrained |  mIoU |
|:----------:|:------------:|:----------:|:-----:|
|    HRNet   |     FCN48    |      +     | 84.91 |
|    HRNet   |     FCN48    |      -     |  65.3 |
|    HRNet   |     FCN48    |      +     | 84.18 |
|    HRNet   |     FCN48    |      +     | 85.71 |
| DeepLabV3+ |  ResNetV1c18 |      +     | 87.89 |
| DeepLabV3+ |  ResNetV1c50 |      +     | 90.87 |
| DeepLabV3+ | ResNetV1c100 |      +     | 85.93 |

ViTAE-B + RVSA |  UperNet | No Pretrain
+-------+-------+-------+---------+------------+---------+
|  aAcc |  mIoU |  mAcc | mFscore | mPrecision | mRecall |
+-------+-------+-------+---------+------------+---------+
| 53.77 | 33.41 | 58.82 |  48.18  |   72.38    |  58.82  |
+-------+-------+-------+---------+------------+---------+

ViTAE-B + RVSA |  UperNet | Potsdam Pretrain
+-------+-------+-------+---------+------------+---------+
|  aAcc |  mIoU |  mAcc | mFscore | mPrecision | mRecall |
+-------+-------+-------+---------+------------+---------+
| 58.54 | 38.89 | 63.13 |  54.86  |   75.13    |  63.13  |
+-------+-------+-------+---------+------------+---------+

Vit-B + RVSA |  UperNet | Potsdam Pretrain, 4k
+-------------+-------+-------+--------+-----------+--------+
|    Class    |  IoU  |  Acc  | Fscore | Precision | Recall |
+-------------+-------+-------+--------+-----------+--------+
|  Background | 95.09 |  98.8 | 97.48  |   96.21   |  98.8  |
| Microtubule | 21.28 | 24.85 |  35.1  |   59.74   | 24.85  |
|      ER     | 42.83 | 54.85 | 59.98  |   66.16   | 54.85  |
+-------------+-------+-------+--------+-----------+-------

Vit-B + RVSA |  UperNet | Potsdam Pretrain, 8k, focal+dice
+-------------+-------+-------+--------+-----------+--------+
|    Class    |  IoU  |  Acc  | Fscore | Precision | Recall |
+-------------+-------+-------+--------+-----------+--------+
|  Background | 95.03 | 97.61 | 97.45  |   97.29   | 97.61  |
| Microtubule | 29.54 | 40.52 | 45.61  |   52.17   | 40.52  |
|      ER     | 47.01 | 69.32 | 63.95  |   59.36   | 69.32  |
+-------------+-------+-------+--------+-----------+--------+

VitAE-B + RVSA |  UperNet | Potsdam Pretrain, 8k, focal+dice
+-------------+-------+-------+--------+-----------+--------+
|    Class    |  IoU  |  Acc  | Fscore | Precision | Recall |
+-------------+-------+-------+--------+-----------+--------+
|  Background | 94.81 | 98.19 | 97.34  |    96.5   | 98.19  |
| Microtubule | 20.27 | 25.55 |  33.7  |   49.49   | 25.55  |
|      ER     | 44.06 | 61.69 | 61.17  |   60.65   | 61.69  |
+-------------+-------+-------+--------+-----------+--------+

VitAE-B + RVSA |  UperNet | Potsdam Pretrain, 80k, focal+dice
+-------------+-------+-------+--------+-----------+--------+
|    Class    |  IoU  |  Acc  | Fscore | Precision | Recall |
+-------------+-------+-------+--------+-----------+--------+
|  Background | 95.17 | 97.86 | 97.53  |    97.2   | 97.86  |
| Microtubule | 28.56 | 37.55 | 44.43  |   54.41   | 37.55  |
|      ER     |  50.3 | 72.13 | 66.93  |   62.43   | 72.13  |
+-------------+-------+-------+--------+-----------+--------+

# November '22

## Logs
* I noticed that there are impurities in the MT data --> small blobs are definetely visible on the masked images. Will try `remove_small_objects` filtering.
* successfully removed the blobs with 3 step `remove_small_objects` filtering, minimally affecting the MT structure.
* MT_vs_ER model performed worse than MT_CL. MT mask was taking ER pieces in many cases. Will try to retrain with Focal loss without transfer learning from previous model.
* Compare overlay types.
* The DECODE paper would be helpful in writing our manuscript https://www.nature.com/articles/s41592-021-01236-x
