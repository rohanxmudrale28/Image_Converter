import streamlit as st
from PIL import Image
import io

def convert_and_resize(image_file, output_format, width=None, height=None, quality=85):
    with Image.open(image_file) as img:
        # Resize if width and height specified
        if width and height:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        output_img = io.BytesIO()
        save_params = {'format': output_format.upper()}
        if output_format.lower() == 'jpeg':
            save_params['quality'] = quality  # Controls JPEG compression quality
        img.save(output_img, **save_params)
        output_img.seek(0)
        return output_img

st.title("Image Converter and Compressor")

uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg", "jfif", "bmp"])

if uploaded_file:
    original_image = Image.open(uploaded_file)
    st.image(original_image, caption="Original Image", use_column_width=True)

    output_format = st.selectbox("Select output format", ["PNG", "JPEG", "JFIF", "BMP"])
    
    # Default width and height from original image to help user
    width = st.number_input("Width (pixels, optional)", min_value=1, max_value=10000, value=original_image.width)
    height = st.number_input("Height (pixels, optional)", min_value=1, max_value=10000, value=original_image.height)
    
    quality = st.slider("JPEG Quality (only for JPEG)", min_value=10, max_value=100, value=85, help="Higher means better quality and larger file size")

    if st.button("Convert and Download"):
        converted_img = convert_and_resize(uploaded_file, output_format, width, height, quality)

        st.download_button(
            label=f"Download {output_format} Image",
            data=converted_img,
            file_name=f"converted_image.{output_format.lower()}",
            mime=f"image/{output_format.lower()}"
        )
