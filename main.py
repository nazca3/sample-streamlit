import streamlit as st
from PIL import Image
import requests
from PIL import ImageFont
from PIL import ImageDraw
import io

st.title("顔認識アプリ")

subscription_key = 'dc0f056c341f4de29b53bb2789f15b3a'
assert subscription_key
face_api_url = 'https://220105-nazca.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("choose an image…", type='jpg')

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }   

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses'
    }
    res = requests.post(face_api_url,params=params,headers=headers, data=binary_img)
    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        att = result['faceAttributes']
        age = att['age']
        gender = att['gender']
        if gender=="male":
            gender = "man"
        else:
            gender = "woman"
        size = int(rect['width']/6)
    
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline="red",width=5)
        
        font = ImageFont.truetype("NotoSansJP-Regular.otf", size=size)
        draw.text((rect['left'],rect['top']-size),gender+str(int(age)),font=font)
        
      
    st.image(img, caption='uploaded Image.', use_column_width=True)
