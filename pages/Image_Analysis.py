# -------------------------------------------------------------------------
# Image_Analysis
# --------------------------------------------------------------------------

import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import streamlit as st
   
imageCaptured = st.camera_input("capture image", key="firstCamera", help="help info")


def main(image_name):
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]
    
    # Create an Image Analysis client for synchronous operations
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Load image to analyze into a 'bytes' object
    with open(image_name, "rb") as f:
        image_data = f.read()

    # Get a caption for the image. This will be a synchronously (blocking) call.
    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.CAPTION],
        gender_neutral_caption=True,  # Optional (default is False)
    )

    # Display image caption and confidence score
    if result.caption is not None:
        st.sidebar.success(f"{result.caption.text}, Confidence {result.caption.confidence:.2f}")

    


if imageCaptured:
   fullname = os.path.join("tmpDir",imageCaptured.name)
   with open(fullname,"wb") as f:
         f.write(imageCaptured.getbuffer())
   main(fullname)
