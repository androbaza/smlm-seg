import os
from natsort import natsorted
from helpers import *

# input_dir = './data/mt/raw_inputs/'
mt_images_path = '/home/smlm-workstation/segmentation/data/mt/tiles/'

# clean_folder(mt_images_path)
# make_tiles_w_overlap(input_dir, mt_images_path)

# os.system("python3 ./ANNA-PALM/run_img.py --workdir=./data/mt/masks/ --load_dir=./ANNA-PALM/models/945/ --phase=test")

# input_dir = '/home/smlm-workstation/segmentation/data/mt/masks/outputs/'
mt_masks_path = '/home/smlm-workstation/segmentation/data/mt/masks/'

# clean_folder(mt_masks_path)
# anna_palm_process(input_dir, mt_masks_path)

# input_dir = '/home/smlm-workstation/segmentation/data/ves/raw_inputs/'
ves_images_path = '/home/smlm-workstation/segmentation/data/ves/tiles/'

# clean_folder(ves_images_path)
# make_tiles_w_overlap(input_dir, ves_images_path)

input_dir = '/home/smlm-workstation/segmentation/data/ves/tiles/'
ves_masks_path = '/home/smlm-workstation/segmentation/data/ves/masks/'

# clean_folder(ves_masks_path)
# ves_process(input_dir, ves_masks_path)

mt_images_list, mt_masks_list = get_img_mask_list(
    mt_images_path, mt_masks_path)
ves_images_list, ves_masks_list = get_img_mask_list(
    ves_images_path, ves_masks_path)

output_dir_img = '/home/smlm-workstation/segmentation/data/combined/images/'
output_dir_masks = '/home/smlm-workstation/segmentation/data/combined/masks/'

# clean_folder(output_dir_img)
# clean_folder(output_dir_masks)

combine_masks(natsorted(mt_images_list), natsorted(mt_masks_list),
              natsorted(ves_images_list), natsorted(ves_masks_list),
              output_dir_img, output_dir_masks)