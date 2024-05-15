import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

img = st.file_uploader('Upload a JPG Image', type='jpg')

if img is not None:
    file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    retval, thresh = cv2.threshold(image_gray, 230, 255, cv2.THRESH_BINARY)
    image_inv = cv2.bitwise_not(thresh)

    bk, gk, rk = cv2.split(image)
    alpha = [bk, gk, rk, image_inv]

    image_trans = cv2.merge(alpha)
    image_trans = cv2.cvtColor(image_trans, cv2.COLOR_RGBA2BGRA)

    cv2.imwrite("Image Transparent.png", image_trans)

    st.image(image_trans)

    # Format suitable for download
    pil_image = Image.fromarray(image_trans)
    buf = io.BytesIO()
    pil_image.save(buf, format='PNG')
    byte_im = buf.getvalue()

    # Create download button
    # st.download_button(
    #     label='Download PNG Image',
    #     data=byte_im,
    #     filename="Image Transparent.png",
    #     mime='image/png'
    # )

    st.download_button(
        label='Download PNG Image',
        data=byte_im,
        file_name='Image_Transparent.png',
        mime='image/png'
    )
