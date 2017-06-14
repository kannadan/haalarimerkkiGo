# Functions for modifying images, labeling them and inserting into a database.

import os
import glob
import random
import numpy
import cv2
import caffe
from caffe.proto import caffe_pb2
import lmdb
from datetime import datetime

TIME = datetime.now()
IMAGE_WIDTH = 227
IMAGE_HEIGHT = 227

def modify(img):
	img[:, :, 0] = cv2.equalizeHist(img[:,:,0])
	img[:, :, 1] = cv2.equalizeHist(img[:,:,1])
	img[:, :, 2] = cv2.equalizeHist(img[:,:,2])

	img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation = cv2.INTER_CUBIC)

	return img

def to_datum_and_beyond(img, label):
	contensed = caffe_pb2.Datum(channels = 3, width = IMAGE_WIDTH, height = IMAGE_HEIGHT, label = label, data = numpy.rollaxis(img, 2).tostring())
	return contensed



training_lmdb = "training_lmdb"
validation_lmdb = "validation_lmdb"

#deleates old data
os.system('rm -rf  ' + training_lmdb)
os.system('rm -rf  ' + validation_lmdb)

#fetch images
training_data = [img for img in glob.glob("./train/*jpg")]
validation_data = [img for img in glob.glob("./test1/*jpg")]

random.shuffle(training_data)

training_db = lmdb.open(training_lmdb, map_size=int(1e10))

with training_db.begin(write=True) as txn:
	for id, path in enumerate(training_data):
		if id%6 == 0:
			continue
		img = cv2.imread(path, cv2.IMREAD_COLOR)
		cv2.namedWindow("Picture")
		cv2.imshow("Picture", img)
		cv2.waitKey(100)
		img = modify(img)
		if "cat" in path:
			label = 0
		else:
			label = 1
		datum = to_datum_and_beyond(img, label)
		txn.put("{:0>5d}".format(id), datum.SerializeToString())
		print "{:0>5d}".format(id) + ":" + path
		if label == 0:
			print "Kihha!!!"
		else:
			print "Doggo!!!"
training_db.close()

validation_db = lmdb.open(validation_lmdb, map_size=int(1e10))

with validation_db.beging(write=True) as txn:
	for id, path in enumerate(training_data):
		if id%6 != 0:
			continue
		img = cv2.imread(path, cv2.IMREAD_color)
		cv2.namedWindow("Picture")
		cv2.imshow("Picture", img)
		cv2.waitKey(100)
		img = modify(img)
		if "cat" in path:
			label = 0
		else:
			label = 1
		datum = to_datum_and_beyond(img, label)
		txn.put("{:0>5d}".format(id), datum.SerializeToString())
		print "{:0>5d}".format(id) + ":" + path
		if label == 0:
			print "Kihha!!!"
		else:
			print "Doggo!!!"
validation_db.close()

print "\nAll my bases are done\nRuntime was " + str(datetime.now()-TIME)
