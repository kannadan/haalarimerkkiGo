#code for making predictions from test data

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
		return pred_prob.argmax()



img_paths = [img for img in glob.glob("test1/*jpg")]

ids = []
predics = []
analyzer = Predictor()
for path in img_paths:
	img = cv2.imread(path, cv2.IMREAD_COLOR)
	img = modify(img)
	ids = ids + [path.split("/")[-1][:-4]]
	label = analyzer.imageIs(img)
	if label == 0:
		name = "kissa"
	else:
		name = "koira"
	cv2.namedWindow(name)
	cv2.imshow(name, img)
	cv2.waitKey(1000)
	cv2.destroyAllWindows()
