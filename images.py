from PIL import Image
import requests
from io import BytesIO
import cred

def get_data(name):
    url = f"https://api.nookipedia.com/nh/fish/{name}?api_key={cred.API}"
    response = requests.get(url)
    content = response.json()
    filtered_data = content["image_url"]
    response_img = requests.get(filtered_data)
    img = Image.open(BytesIO(response_img.content))
    return img

if __name__ == "__main__":
    print(get_data(name="Salmon"))

