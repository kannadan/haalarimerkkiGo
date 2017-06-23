#code for making predictions from test data

import random
import os
import glob
import cv2
import caffe
import lmdb
import numpy
from caffe.proto import caffe_pb2

caffe.set_mode_gpu()

IMAGE_WIDTH = 277
IMAGE_HEIGHT = 277

def modify(img):
	img[:, :, 0] = cv2.equalizeHist(img[:,:,0])
	img[:, :, 1] = cv2.equalizeHist(img[:,:,1])
	img[:, :, 2] = cv2.equalizeHist(img[:,:,2])

	img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT), interpolation = cv2.INTER_CUBIC)

	return img
class Predictor:
	"""Takes images as input and returns evaluation of it's subject"""
	def __init__(self):
		mean_blob = caffe_pb2.BlobProto()
		with open("/home/jondan/Documents/Ohjelmat/haalarimerkkiGo/mean.binaryproto") as pic:
			mean_blob.ParseFromString(pic.read())
		mean_arr = numpy.asarray(mean_blob.data, dtype=numpy.float32).reshape(
		(mean_blob.channels, mean_blob.height, mean_blob.width)
		)
		print "mean picture found"
		self.brain = caffe.Net("/home/jondan/Documents/Ohjelmat/haalarimerkkiGo/caffenet_deploy_1.prototxt",
			"/home/jondan/Documents/Ohjelmat/haalarimerkkiGo/caffe_model_1_iter_5000.caffemodel", caffe.TEST)

		self.optimus_prime = caffe.io.Transformer({"data": self.brain.blobs["data"].data.shape})
		self.optimus_prime.set_mean("data", mean_arr)
		self.optimus_prime.set_transpose("data", (2,0,1))

	def imageIs(self, img):
		self.brain.blobs["data"].data[...] = self.optimus_prime.preprocess("data", img)
		out = self.brain.forward()
		pred_prob = out["prob"]
		#print out["prob"]
		return pred_prob.argmax(), pred_prob[0][pred_prob.argmax()]



img_paths = [img for img in glob.glob("kuvat/*jpg")]
random.shuffle(img_paths)
ids = []
predics = []
analyzer = Predictor()
kuvia = 0
oikein = 0
for path in img_paths:
	img = cv2.imread(path, cv2.IMREAD_COLOR)
	img = modify(img)
	ids = ids + [path.split("/")[-1][:-4]]
	label, probability = analyzer.imageIs(img)
	if label == 0:
		name = "deeggari"
	elif label ==1:
		name = "friday"
	elif label == 2:
		name = "heijastin"
	elif label == 3:
		name = "leivo"
	elif label == 4:
		name = "longcat"
	elif label == 5:
		name = "mkrapula"
	elif label == 6:
		name = "pasila"
	elif label == 7:
		name = "sieni"
	elif label == 8:
		name = "teekkari"
	else:
		name = "tnainen"
	#print "{} at {} % probability".format(name, probability)

	kuvia = kuvia + 1
	if name in path:
		oikein = oikein + 1
	if kuvia%100 == 0:
		print kuvia
	"""cv2.namedWindow(name)
	cv2.imshow(name, img)
	cv2.waitKey(2000)
	cv2.destroyAllWindows()"""

	
print "Kuvia: {}\nOikein: {}\nTarkkuus: {}".format(kuvia, oikein, float(oikein)/kuvia)
