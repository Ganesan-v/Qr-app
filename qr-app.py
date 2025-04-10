import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

st.set_page_config(page_title="QR Code Generator & Scanner", layout="centered")
st.title("🧾 QR Code Generator & Scanner (Pure OpenCV)")

# --- QR Code Generator ---
st.header("Generate QR Code")
input_text = st.text_input("Enter text to encode:")

if st.button("Generate QR Code"):
    if input_text:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(input_text)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Generated QR Code", use_column_width=True)
        st.download_button("Download QR Code", data=buf.getvalue(), file_name="qr_code.png", mime="image/png")
    else:
        st.warning("Please enter text to generate a QR code.")

# --- QR Code Scanner ---
st.header("Scan QR Code from Image")

uploaded_file = st.file_uploader("Upload QR Code Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to OpenCV format
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Use OpenCV QRCodeDetector
    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(cv_image)

    if data:
        st.success(f"Scanned QR Code Content: {data}")
    else:
        st.error("No QR code found in the image.")
