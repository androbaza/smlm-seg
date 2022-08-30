from os import listdir
from os.path import isfile, join
import numpy as np
import cv2
import skimage
import os
import pathlib
import glob
from natsort import natsorted
from pathlib import *
from openslide import open_slide
from PIL import Image
from openslide.deepzoom import DeepZoomGenerator
import matplotlib.pyplot as plt
from skimage.io import imread, imshow, imsave
from skimage import morphology
from skimage.measure import label
from skimage.exposure import rescale_intensity
from skimage.segmentation import random_walker

def clean_folder(input_dir):
    for fname in os.listdir(input_dir):
        os.remove(os.path.join(input_dir, fname))


def make_tiles_w_overlap(input_dir, output_dir):
    img_n, column = 0, 0

    for fname in natsorted(os.listdir(input_dir)):
        row = 0
        img = imread(os.path.join(input_dir, fname), as_gray=1)
        for h in range(0, img.shape[1], 256):
            for w in range(0, img.shape[0], 256):
                w_end = w + 512
                h_end = h + 512
                # crop the pixels that don't fit in tiles
                if w_end > img.shape[0] or h_end > img.shape[1]:
                    continue

                tile = img[h:h_end, w: w_end]
                if(np.count_nonzero(tile)/tile.size < 0.01):
                    continue
                imsave(output_dir + 'A_' + str(img_n) +
                       "_" + str(row) + "_" + str(column) + ".png", tile, check_contrast = 0)
                column += 1
            row += 1
            column = 0
        img_n += 1


def anna_palm_process(input_dir, output_dir):
    for fname in os.listdir(input_dir):
        if fname.endswith("reco_B_b0_i0.tif"):
            img = imread(os.path.join(input_dir, fname), as_gray=1)
            # blur = (cv2.GaussianBlur(img, (3, 3), 0)*255).astype(np.uint8)
            blur = (img*255).astype(np.uint8)
            # ret, fig = cv2.threshold(
            #     blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            
            ret, fig2 = cv2.threshold(
                blur, 5, 255, cv2.THRESH_BINARY)

            fig = morphology.erosion(fig2, selem=morphology.disk(1))
            # filtered1 = morphology.erosion(morphology.dilation(labels2, morphology.square(4)), morphology.square(2))

            filtered = (morphology.remove_small_objects(
                fig > 0, 50)).astype(np.uint8)*255

            imsave(os.path.join(output_dir, os.path.splitext(
                os.path.splitext(fname)[0])[0])+"_999.png", filtered, check_contrast=0)
        else:
            os.remove(os.path.join(input_dir, fname))


def ves_process(input_dir, output_dir):
    for fname in os.listdir(input_dir):

        img = imread(os.path.join(input_dir, fname), as_gray=1)
        markers = np.zeros(img.shape, dtype=np.uint)
        markers[img < 0.01] = 1
        markers[img > 0.05] = 2

        # Run random walker algorithm
        labels = random_walker(img, markers, beta=5, mode='bf')
        labels2 = rescale_intensity(labels, out_range=(0, 1))

        filtered2 = morphology.remove_small_holes(
            morphology.remove_small_objects(
                labels2 > 0, 100),
            350).astype(np.uint8)*255

        filtered = morphology.dilation(filtered2, selem = morphology.disk(3))

        imsave(os.path.join(output_dir, os.path.splitext(
            os.path.splitext(fname)[0])[0])+"_999.png", filtered, check_contrast=0)


def combine_masks(mt_images_list, mt_masks_list, ves_images_list, ves_masks_list, output_dir_img, output_dir_masks):
    
    images_mt = [read(f) for f in mt_images_list]
    images_ves = [read(f) for f in ves_images_list]

    masks_mt = [mask_paletterize(mask, 255)
                for mask in (read(f) for f in mt_masks_list)]
    masks_ves = [mask_paletterize(mask, 180)
                 for mask in (read(f) for f in ves_masks_list)]
    
    k = 0
    for i in range(0, len(images_mt), 3):
        for j in range(0, len(images_ves)):
            
            # save original overlap
            comb_mask, comb_im = embed_pair(images_mt[i], masks_mt[i], images_ves[j], masks_ves[j])
            imsave(str(output_dir_img) +
                   "{:07d}.png".format(k), comb_im, check_contrast=0)
            imsave(str(output_dir_masks) +
                   "{:07d}.png".format(k), comb_mask, check_contrast=0)

            # save rotations
            # rot, rot2 = 0, 270
            # for x in range(3):
            #     rot += 90
            #     rot2 += 90
            #     k += 1
            #     comb_mask, comb_im = embed_pair(rotate(images_mt[i], rot), rotate(masks_mt[i], rot), rotate(images_ves[j], rot2), rotate(masks_ves[j], rot2))
            #     imsave(str(output_dir_img) +
            #                       "{:07d}.png".format(k), comb_im, check_contrast=0)
            #     imsave(str(output_dir_masks) +
            #                       "{:07d}.png".format(k), comb_mask, check_contrast=0)

            # save flipped rotations
            rot, rot2 = 90, 0
            for x in range(3):
              rot += 90
              rot2 += 90
              k += 1
              comb_mask, comb_im = embed_pair(flip(rotate(images_mt[i], rot)), flip(rotate(masks_mt[i], rot)), flip(rotate(images_ves[j], rot2)), flip(rotate(masks_ves[j], rot2)))
              imsave(str(output_dir_img) +
                                "{:07d}.png".format(k), comb_im, check_contrast=0)
              imsave(str(output_dir_masks) +
                     "{:07d}.png".format(k), comb_mask, check_contrast=0)

            # now change overlap order
            k += 1

            # save original overlap
            comb_mask, comb_im = embed_pair(images_ves[j], masks_ves[j], images_mt[i], masks_mt[i])
            imsave(str(output_dir_img) +
                              "{:07d}.png".format(k), comb_im, check_contrast=0)
            imsave(str(output_dir_masks) +
                   "{:07d}.png".format(k), comb_mask, check_contrast=0)

            rot, rot2 = 180, 0
            for x in range(3):
                rot += 90
                rot2 += 90
                k += 1
                comb_mask, comb_im = embed_pair(rotate(images_mt[i], rot), rotate(masks_mt[i], rot), rotate(images_ves[j], rot2), rotate(masks_ves[j], rot2))
                imsave(str(output_dir_img) +
                                  "{:07d}.png".format(k), comb_im, check_contrast=0)
                imsave(str(output_dir_masks) +
                       "{:07d}.png".format(k), comb_mask, check_contrast=0)

            # save flipped rotations
            # rot, rot2 = 270, 90
            # for x in range(3):
            #   rot += 90
            #   rot2 += 90
            #   k += 1
            #   comb_mask, comb_im = embed_pair(flip(rotate(images_mt[i], rot)), flip(rotate(masks_mt[i], rot)), flip(rotate(images_ves[j], rot2)), flip(rotate(masks_ves[j], rot2)))
            #   imsave(str(output_dir_img) +
            #                     "{:07d}.png".format(k), comb_im, check_contrast=0)
            #   imsave(str(output_dir_masks) +
            #                     "{:07d}.png".format(k), comb_mask, check_contrast=0)

            k += 1
        print(k)
    print('finished')



def list_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]

def get_img_mask_list(img_path, mask_path, img_prefix='data', mask_prefix='masked_'):

    files_path = list_files(img_path)
    files_path = [os.path.join(img_path, f) for f in files_path if
                    f.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']]

    mask_files_path = list_files(mask_path)
    mask_files_path = [os.path.join(mask_path, f) for f in mask_files_path if
                        f.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']]

    return files_path, mask_files_path


def get_images_list(path):
    files_path = list_files(path)
    files_path = [os.path.join(path, f) for f in files_path if f.split(
        '.')[-1].lower() in ['jpg', 'jpeg', 'png']]
    return files_path

def read(path):
    """Reads an image from the specified path.

    Args:
        path (str): image path.

    :Returns:
        img (numpy.array): RGB image
    """
    return imread(path, as_gray=1)


def rotate_pair(img, mask, degree):
    """Rotates image and mask for the degree from range [-degree, degree]
    Args:
        img (numpy.array): RGB or grayscale image.
        mask (numpy.array): image mask.
        degree (int): maximum rotation degree.
    Returns:
        img (numpy.array): rotated image.
        mask (numpy.array): rotated image mask.
    """
    rotation_degree = degree
    # rotation_degree = int(random.random() * degree)
    # rotation_degree = rotation_degree if random.random() < 0.5 else - \
    #     rotation_degree

    img = rotate(img, rotation_degree)
    mask = rotate(mask, rotation_degree)

    return img, mask


def np2pil(arrayIn):
    imgOut = Image.fromarray(arrayIn)
    return imgOut


def pil2np(imgIn, arrayOut=None):
    if arrayOut == None:
        arrayOut = np.array(imgIn)
        return arrayOut
    else:
        arrayOut[:] = np.array(imgIn)
        return None


def rotate(img, degree):
    """Rotates image for the specified degree.
    Args:
        img (numpy.array): RGB or grayscale image.
        degree (int): rotation degree
    Returns:
        img (numpy.array): rotated image.
    """
    pil_img = np2pil(img)
    pil_img = pil_img.rotate(degree)
    np_img = pil2np(pil_img)

    return np_img


def flip_pair(img, mask):
    """Flips image and mask horizontally with probability p.
    Args:
        img (numpy.array): RGB or grayscale image.
        mask (numpy.array): object image.
        p (float): probability of flipping.
    Returns:
        img (numpy.array): flipped image.
        mask (numpy.array): flipped object image.
    """
    # if random.random() < p:
    img = flip(img)
    mask = flip(mask)

    return img, mask


def flip(img):
    """Flips image horizontally.
    Args:
        img (numpy.array): RGB or grayscale image.
        p (float): probability of flipping.
    Returns:
        img (numpy.array): flipped image.
    """
    # return img[:, ::-1]

    # if random.random() < p:
    if len(img.shape) == 3:
        return img[:, ::-1, :]
    else:
        return img[:, ::-1]
    # else:
    #     return img


def embed_pair(img_top, mask_top, img_bottom, mask_bottom):

    # m_top = (mask_top[:, :, 0] > 0) | (mask_top[:, :, 1] > 0) | (mask_top[:, :, 2] > 0)

    m_top = (mask_top > 0)
    mask_comb = mask_bottom.copy()

    # copy the pixels from under the mask of the top image to bottom image
    mask_comb[m_top] = mask_top[m_top]

    top_non_zero = img_top[:, :] > 0
    cc = skimage.util.img_as_uint(img_bottom.copy())

    # copy the non-zero pixels from the top image to bottom image
    cc[top_non_zero] = skimage.util.img_as_uint(img_top[top_non_zero])

    return mask_comb, cc


def plot_comparison(original, filtered):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 8), sharex=True,
                                   sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.axis('off')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    # ax2.set_title(filter_name)
    ax2.axis('off')


def format_image(img):
    if img.max() <= 1:
        return (img * 255).astype('uint8')
    else:
        return img.astype('uint8')


def mask_paletterize(mask, value):
    m = (mask > 0)
    new_mask = mask.copy()
    new_mask[m] = value
    return format_image(new_mask)
