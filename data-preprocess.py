import os
import numpy as np
from natsort import natsorted
from resources.helpers import *

# # input_dir = './data/mt/raw_inputs/'
# mt_images_path = '/home/smlm-workstation/segmentation/data/mt/tiles/'

# # clean_folder(mt_images_path)
# # make_tiles_w_overlap(input_dir, mt_images_path)

# # os.system("python3 ./ANNA-PALM/run_img.py --workdir=./data/mt/masks/ --load_dir=./ANNA-PALM/models/945/ --phase=test")

# # input_dir = '/home/smlm-workstation/segmentation/data/mt/masks/outputs/'
# mt_masks_path = '/home/smlm-workstation/segmentation/data/mt/masks/'

# # clean_folder(mt_masks_path)
# # anna_palm_process(input_dir, mt_masks_path)

# # input_dir = '/home/smlm-workstation/segmentation/data/ves/raw_inputs/'
# ves_images_path = '/home/smlm-workstation/segmentation/data/ves/tiles/'

# # clean_folder(ves_images_path)
# # make_tiles_w_overlap(input_dir, ves_images_path)

# input_dir = '/home/smlm-workstation/segmentation/data/ves/tiles/'
# ves_masks_path = '/home/smlm-workstation/segmentation/data/ves/masks/'

# # clean_folder(ves_masks_path)
# # ves_process(input_dir, ves_masks_path)

# # mt_images_list, mt_masks_list = get_img_mask_list(
# #     mt_images_path, mt_masks_path)
# # ves_images_list, ves_masks_list = get_img_mask_list(
# #     ves_images_path, ves_masks_path)

# output_dir_img = '/home/smlm-workstation/segmentation/data/combined/images/'
# output_dir_masks = '/home/smlm-workstation/segmentation/data/combined/masks/'

# # clean_folder(output_dir_img)
# # clean_folder(output_dir_masks)

# # combine_masks(natsorted(mt_images_list), natsorted(mt_masks_list),
# #               natsorted(ves_images_list), natsorted(ves_masks_list),
# #               output_dir_img, output_dir_masks)

# input_dir_masks = '/home/smlm-workstation/segmentation/data/combined/masks/'
# output_dir_bit_masks = '/home/smlm-workstation/segmentation/data/combined/bit_masks'

# # convert_to_bit_mask(input_dir_masks, output_dir_bit_masks)

# input_dir = '/home/smlm-workstation/segmentation/data/npy/mt_clathrin'
# output_dir = '/home/smlm-workstation/segmentation/data/clathrin/raw_inputs/'

'''
FULL IMAGE/PIXEL MASKS EXPERIMENT
'''

'''
Microtubules/clathrin
'''

#1 convert all images to gray values
# input_dir = '/home/smlm-workstation/segmentation/data/ves/raw_inputs/'
# save_grey_p(input_dir, output_dir)

#2 pad images to same size and make mask from pixels
# input_dir = '/home/smlm-workstation/segmentation/data/mt/raw_inputs/'
mt_images_path = '/home/smlm-workstation/segmentation/data/mt/full_pad'
mt_masks_path = '/home/smlm-workstation/segmentation/data/mt/full_mask'
# make_pixelwise_mask_pad(input_dir, output_dir, output_dir_mask)

# input_dir = '/home/smlm-workstation/segmentation/data/clathrin/raw_inputs/'
clathrin_images_path = '/home/smlm-workstation/segmentation/data/clathrin/full_pad'
clathrin_masks_path = '/home/smlm-workstation/segmentation/data/clathrin/full_mask'
# make_pixelwise_mask_pad(input_dir, output_dir, output_dir_mask)

#3 overlap the images and masks

# mt_images_list, mt_masks_list = get_img_mask_list(
#     mt_images_path, mt_masks_path)
# clathrin_images_list, clathrin_masks_list = get_img_mask_list(
#     clathrin_images_path, clathrin_masks_path)

# output_dir_img = '/home/smlm-workstation/segmentation/data/full_combined/images/'
# output_dir_masks = '/home/smlm-workstation/segmentation/data/full_combined/masks/'

# combine_masks(natsorted(mt_images_list), natsorted(mt_masks_list),
#               natsorted(clathrin_images_list), natsorted(clathrin_masks_list),
#               output_dir_img, output_dir_masks)

#4 convert masks to bit masks

# input_dir_rgb_mask = '/home/smlm-workstation/segmentation/data/full_combined/masks/'
# output_dir_bit_masks = '/home/smlm-workstation/segmentation/data/full_combined/bit_masks/'

# convert_to_bit_mask(input_dir_rgb_mask, output_dir_bit_masks)

# input_dir = '/home/smlm-workstation/segmentation/data/full_combined/bit_masks/'
# calc_weights(input_dir)

# mt, cl, bg = np.float32(6510370976.0), np.float32(
#     3653127823.0), np.float32(79555977258.0)
# all_p = np.float32(mt+cl+bg)
# w_bg = (mt+cl)/(bg)
# w_mt = (cl+bg)/mt
# w_cl = (mt+bg)/cl
# ap = w_bg+w_mt+ w_cl
# a, b, c = w_bg/ap, w_mt/ap, w_cl/ap
# print(a, b, c)
# print(bg, mt, cl, all_p)

'''
Microtubules/ER
'''

#1 convert all images to gray values
# input_dir = '/home/smlm-workstation/segmentation/data/ves/raw_inputs/'
# save_grey_p(input_dir, output_dir)

#2 pad images to same size and make mask from pixels
input_dir = '/home/smlm-workstation/segmentation/data/er/raw_inputs/'
er_images_path = '/home/smlm-workstation/segmentation/data/er/full_pad'
er_masks_path = '/home/smlm-workstation/segmentation/data/er/full_mask'
make_pixelwise_mask_pad(input_dir, er_images_path, er_masks_path)

#3 overlap the images and masks

# mt_images_list, mt_masks_list = get_img_mask_list(
#     mt_images_path, mt_masks_path)
# clathrin_images_list, clathrin_masks_list = get_img_mask_list(
#     clathrin_images_path, clathrin_masks_path)

# output_dir_img = '/home/smlm-workstation/segmentation/data/full_combined/images/'
# output_dir_masks = '/home/smlm-workstation/segmentation/data/full_combined/masks/'

# combine_masks(natsorted(mt_images_list), natsorted(mt_masks_list),
#               natsorted(clathrin_images_list), natsorted(clathrin_masks_list),
#               output_dir_img, output_dir_masks)

#4 convert masks to bit masks

# input_dir_rgb_mask = '/home/smlm-workstation/segmentation/data/full_combined/masks/'
# output_dir_bit_masks = '/home/smlm-workstation/segmentation/data/full_combined/bit_masks/'

# convert_to_bit_mask(input_dir_rgb_mask, output_dir_bit_masks)

# input_dir = '/home/smlm-workstation/segmentation/data/full_combined/bit_masks/'
# calc_weights(input_dir)
