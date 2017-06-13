# Functions for modifying images, labeling them and inserting into a database.

import os
import glob
import random
import numpy
import cv2
from caffe.proto import caffe_pb2
import lmdb

IMAGE_WIDTH = 227
IMAGE_HIGHT = 227

def modify(img):
	img[:, :, 0] = cv2.equalizeHist(img[:,:,0])
	img[:, :, 1] = cv2.equalizeHist(img[:,:,1])
	img[:, :, 2] = cv2.equalizeHist(img[:,:,2])

	img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HIGHT), interpolation = cv2.INTER_CUBIC)

	return img

