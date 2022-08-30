# August'22
## Event camera SMLM setup:
### Hardware
* Key idea: match the focal planes. Then finding the sample will be possible with the EMCCD camera, then beam splitter is changed to mirror mode to perform imaging solely on event sensor.
* Parts for the optical setup according to 'Methods' section in Cabriel, Specht and Izeddin [paper](https://doi.org/10.1101/2022.07.22.501162):
  *  RM21 body and a MANNZ micro- and nano-positioner. 
  *  Nikon 100x 1.49NA APO TIRF SR oil immersion. 
  *  638 nm laser (LBX-638-180, 180 mW, Oxxius) and a 488 nm
 laser (LBX-488-100, 100 mW, Oxxius) with a 405 nm laser for pumping (LBX-405-50, 50 mW, Oxxius).
  * A full multiband filter set (LF405/488/561/635-A-000, Semrock).
  * EMCCD camera (iXon Ultra 897, Andor)
  * EVK V2 Gen4.1, Prophesee
  * focal doublets to adjust the pixel sizes to 107 nm (EMCCD) and 65 nm (event-based sensor) in the object plane.
  
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
* 

# September'22
