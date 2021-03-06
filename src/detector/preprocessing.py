import numpy as np
import cv2
import skimage.measure


def binary_midgray(grayscale):
	"""
	Binary threshold at value 128
	"""
	return grayscale > 128

def binary_average(grayscale):
	"""
	Binary threshold at image's average value
	"""
	return grayscale > np.average(grayscale)

def binary_median(grayscale):
	"""
	Binary threshold at image's median value
	"""
	return grayscale > np.median(grayscale)

def intensity_mask(grayscale):
	'''
	return the intensity mask compute with sobel filters
	'''
	grad_x = cv2.Scharr(grayscale, cv2.CV_32F, 1, 0)
	grad_y = cv2.Scharr(grayscale, cv2.CV_32F, 0, 1)
	
	intensity = (grad_x ** 2 + grad_y ** 2) ** 0.5
	
	return (intensity > 100).astype(np.uint8)


def resize(src_img, max_dim):
	"""
	Resize an image if one of its dimension is greater than a specified max.
	:param src_img: source image
	:param max_dim: maximum dimension in pixels, over which image will be resized (None will not resize)
	:return: resized image
	"""

	resized = src_img.copy()
	if max_dim is not None:
		h = resized.shape[0]
		w = resized.shape[1]
		if h > max_dim and h > w:
			resized = cv2.resize(resized, (int(w / h * max_dim), max_dim), cv2.INTER_CUBIC)
		elif w > max_dim:
			resized = cv2.resize(resized, (max_dim, int(h / w * max_dim)), cv2.INTER_CUBIC)
	return resized


def preprocess(src_img, apply_filter='bilinear', binary_mode=binary_average, binary_mask=None):
	"""
	Preprocesses an RGB image into a grayscale image and a binary image.
	:param src_img: source RGB image
	:param apply_filter: should a filter be applied on image?
	:param binary_mode: binary threshold function
	:return: (grayscale, binary) resized and preprocessed images
	"""
	grayscale = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)

	if apply_filter == 'bilinear':
		grayscale = cv2.bilateralFilter(grayscale, 7, 50, 50)
	elif apply_filter == 'gaussian':
		grayscale = cv2.GaussianBlur(grayscale, (5, 5), 4)

	if binary_mask is not None:
		mask = binary_mask(grayscale)
	else:
		mask = None

	return grayscale, binary_mode(grayscale).astype(np.uint8), mask
