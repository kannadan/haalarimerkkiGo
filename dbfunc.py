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
import time

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
training_data = [img for img in glob.glob("./kuvat/*jpg")]

random.shuffle(training_data)

training_db = lmdb.open(training_lmdb, map_size=int(1e11))

with training_db.begin(write=True) as txn:
	for my_id, path in enumerate(training_data):
		if my_id%6 == 0:
			continue
#		elif my_id > 100:
#			break

		img = cv2.imread(path, cv2.IMREAD_COLOR)
		img = modify(img)
		if "deeggari" in path:
			label = 0
		elif "friday" in path:
			label = 1
		elif "heijastin" in path:
			label = 2
		elif "leivo" in path:
			label = 3
		elif "longcat" in path:
			label = 4
		elif "mkrapula" in path:
			label = 5
		elif "pasila" in path:
			label = 6
		elif "sieni" in path:
			label = 7
		elif "teekkari" in path:
			label = 8
		elif "tnainen" in path:
			label = 9
		else:
			continue
		datum = to_datum_and_beyond(img, label)
		txn.put("{:0>5d}".format(my_id), datum.SerializeToString())
		print "{:0>5d}".format(my_id) + ":" + path

training_db.close()


time.sleep(60)

validation_db = lmdb.open(validation_lmdb, map_size=int(1e11))
with validation_db.begin(write=True) as txn:
	for my_id, path in enumerate(training_data):
		if my_id%6 != 0:
			continue
#		elif my_id > 100:
#			break
		img = cv2.imread(path, cv2.IMREAD_COLOR)
		img = modify(img)
		if "deeggari" in path:
			label = 0
		elif "friday" in path:
			label = 1
		elif "heijastin" in path:
			label = 2
		elif "leivo" in path:
			label = 3
		elif "longcat" in path:
			label = 4
		elif "mkrapula" in path:
			label = 5
		elif "pasila" in path:
			label = 6
		elif "sieni" in path:
			label = 7
		elif "teekkari" in path:
			label = 8
		elif "tnainen" in path:
			label = 9
		else:
			continue
		datum = to_datum_and_beyond(img, label)
		txn.put("{:0>5d}".format(my_id), datum.SerializeToString())
		print "{:0>5d}".format(my_id) + ":" + path
validation_db.close()

print "\nAll my bases are done\nRuntime was " + str(datetime.now()-TIME)
