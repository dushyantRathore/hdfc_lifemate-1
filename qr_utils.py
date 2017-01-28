import qrtools
import pyqrcode
import os
from bs4 import BeautifulSoup
import json

QR_CODE_DIRECTORY = os.path.join('images', 'qr')

def decode_qr(image_path):
	qr = qrtools.QR()
	if qr.decode(image_path):
		return qr.data
	return "Failed to decode"

def create_qr(data, image_name, scale=6):
	qr = pyqrcode.create(str(data))
	image_path = os.path.join(QR_CODE_DIRECTORY, image_name)
	qr.png(image_path, scale=scale)
	return image_path

def parse_aadhar(xml_data, json_reqd=False):
	soup = BeautifulSoup(xml_data)
	soup = soup.body.printletterbarcodedata
	obj = {
			"name": soup["name"],
			"address": {
				"local":soup["loc"],
				"town": soup["vtc"],
				"district":soup["dist"],
				"state": soup["state"],
				"pin_code": soup["pc"]
			},
			"gender": soup["gender"],
			"yob": soup["yob"],
			"uid": soup["uid"],
			"care_of": soup["co"]
		}
	if json_reqd:
		return json.dumps
	return obj

def decode_aadhar_from_qr(imagepath, is_json=False):
	out_xml = decode_qr(image_path)
	out = parse_aadhar(out_xml, is_json)
	return out