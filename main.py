from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Security, Depends, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey
from pydantic import BaseModel

from starlette.status import HTTP_403_FORBIDDEN

from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import requests as re



API_KEY = "6e8e8295-cfa1-4bb7-9ea6-c15df77e11e2"
API_KEY_NAME = 'access_token'

api_key_query = APIKeyQuery(name=API_KEY_NAME)

app = FastAPI()

# define function for retrieving API key from query parameter
async def get_api_key(api_key_query: str = Security(api_key_query)):
	if api_key_query == API_KEY:
		return api_key_query
	else:
		raise HTTPException(
			status_cod=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
		)

# pydantic offers BaseModel class for request body declaration/validation
class Urls(BaseModel):
	img_url_1: Optional[str] = None
	img_url_2: Optional[str] = None


@app.post("/image/files") # create route for receiving image files
async def image(		# set params of UploadFile and APIKey for security
		images: Optional[List[UploadFile]] = File(None),
		api_key: APIKey = Depends(get_api_key)
	):
	if images:
		img1, img2 = images	# unpack both images
		img1, img2 = await img1.read(), await img2.read()	# read both images
		img1_np, img2_np = convert_image(img1), convert_image(img2) # convert images in np arrays and grey images
		similarity_percent = round(ssim(img1_np, img2_np) * 100)	# calculate structural similarity index
	else:
		return { 'message': 'No images were received' }
	return { 'similarity_percent': similarity_percent }

@app.post("/image/urls") # create route for receiving string urls
async def image_urls(	# set params of Urls instance and APIKey for security
	urls: Urls,
	api_key: APIKey = Depends(get_api_key)
):
	if urls.img_url_1 and urls.img_url_2:
		img1, img2 = re.get(urls.img_url_1).content, re.get(urls.img_url_2).content # get request images from urls
		img1_np, img2_np = convert_image(img1), convert_image(img2) # convert images in np arrays and grey images
		similarity_percent = round(ssim(img1_np, img2_np) * 100)	# calculate structural similarity index
	else:
		return { 'message': 'No images were received' }
	return { 'similarity_percent': similarity_percent }

# This function is converting the bytes of our image
# into a workable numpy array as well as greying out the image
def convert_image(image):
	nparr = np.frombuffer(image, np.uint8)
	img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
	return img_np

