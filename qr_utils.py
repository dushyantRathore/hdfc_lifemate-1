import qrtools
import pyqrcode
from bs4 import BeautifulSoup
import json

def decode_qr(image_path):
	qr = qrtools.QR()
	if qr.decode(image_path):
		return qr.data
	return "Failed to decode"

def create_qr(data, image_name, scale=6):
	qr = pyqrcode.create(str(data))
	qr.png(image_name, scale=scale)

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

out_xml = decode_qr("images/vinay.jpg")
out = parse_aadhar(out_xml)
print(out)