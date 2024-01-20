"""
Get NASA's Astronomy Picture Of the Day (APOD)

View the API on "https://api.nasa.gov/"

Create a config.py file containing the following globals:

    BASE_URL    : url of nasa apod api https://api.nasa.gov/planetary/apod
    API_KEY     : API key you need to use the api
    IMG_PATH    : path to save the image to

To set the resulting picture as wallpaper on Linux, run:

    gsettings set org.gnome.desktop.background picture-uri-dark file://<IMG_PATH>

This command only needs to be done once as future runs of this script will override the existing image and the wallpaper engine will detect the change and update the wallpaper for you. To update your wallpaper daily, run this script as an anacron job
"""

import requests
import msgspec

from io import BytesIO
from PIL import Image
from typing import Optional

from config import BASE_URL, API_KEY, IMG_PATH


class ApodData(msgspec.Struct):

    title: str
    date: str
    hdurl: str
    url: str
    media_type: str
    explanation: str
    copyright: str
    concepts: Optional[str] = []

    def from_json(json):
        return msgspec.json.decode(json, type=ApodData)
    
    def today():
        params = dict()
        params["api_key"] = API_KEY
        response = requests.get(BASE_URL, params, timeout=5)
        
        if not response.ok:
            raise RuntimeError(f"retrieving apod data from {BASE_URL} failed")

        return ApodData.from_json(response.content)
    
    def get_image(self, hd=True, img_path=IMG_PATH):

        url = self.hdurl if hd else self.url
        response = requests.get(url, timeout=5)

        if not response.ok:
            raise RuntimeError(f"retrieving apod image from {url} failed")
        
        apod_image = Image.open(BytesIO(response.content))
        apod_image.save(img_path)


if __name__ == "__main__":
    apod = ApodData.today()
    apod.get_image()
