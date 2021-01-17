# FastAPI-Image-Similarity
Small FastAPI project that can receive two images and return the images' percent of similarity.

![](https://github.com/diegofigueroa79/FastAPI-Image-Similarity/blob/main/cabbage.jpg) | ![](https://github.com/diegofigueroa79/FastAPI-Image-Similarity/blob/main/filtered.jpg)

## Installation / Setup

After downloading or git cloning the repository, make sure you are setting up a virtual environment with Python 3.6+.
Then use pip to install all the necessary libraries from the requirements.txt.

```bash
pip install -r requirements.txt
```
Then, you'll want to run the live server with uvicorn
```bash
uvicorn main:app --reload
```
You can now send HTTP requests to http://127.0.0.1:8000 either on a separate terminal, with Postman, or other methods of your choice.

## Usage
This is a simple API built with FastAPI in one single script. It's only usecase is to load two photos, either through file upload or sending two image urls, and returning a percentage score of their similarity.

Calling the api can be done one of two ways. For simplicity's sake, I am providing the API key below.
The API key must be attached as a url parameter whenever you are making a request to the API.

The first API endpoint for sending two images is by local file
### '/image/files'
```python
import requests as re

access_token = "6e8e8295-cfa1-4bb7-9ea6-c15df77e11e2"  # This access token must be added as a url param
url = 'http://127.0.0.1:8000/image/files' # the endpoint for loading sending local files
url += '?access_token=' + access_token

# open the two local files that you want to send to the API
img1 = open('cabbage.jpg', 'rb')
img2 = open('filtered.jpg', 'rb')

# create list of tuples containing (str filename, file)
data = [
	('images', img1),
	('images', img2),
]

r = re.post(url, files=data) # send POST request passing out data list

print(r.status_code)
print(r.content) # expected { 'similarity_percent': 69 }
```

The second API endpoint for sending two images is by two image links
### '/image/urls'
```python
import requests as re

img_url = 'https://picsum.photos/id/237/200/300'

access_token = "6e8e8295-cfa1-4bb7-9ea6-c15df77e11e2"
url = 'http://127.0.0.1:8000/image/files' # the endpoint for sending image links
url += '?access_token=' + access_token

# Here we are making a dict containing two items whose value is the same image url
# we are designating both images to be the same so we expect a similarity of 100%
data = {
	'img_url_1': img_url,
	'img_url_2': img_url
}

r2 = re.post(url, json=data)

print(r2.status_code)
print(r2.content) # expected { 'similarity_percent': 100 }
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
