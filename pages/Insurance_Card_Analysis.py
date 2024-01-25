from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import streamlit as st
import os

# Replace with your Azure AI Document Intelligence API key and endpoint
#api_key = "a557ec59de5746df90c68c728938714c"
#endpoint = "https://myazureai01.cognitiveservices.azure.com/"

endpoint = os.environ["AZURE_DOCUMENT_ENDPOINT"]
api_key = os.environ["AZURE_DOCUMENT_KEY"]


def process_health_insurance_card(api_key, endpoint, image_path):
    # Set up Azure Document Analysis client
    credential = AzureKeyCredential(api_key)
    client = DocumentAnalysisClient(endpoint, credential)

    # Read the image file
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Perform document analysis
    poller = client.begin_analyze_document("prebuilt-healthInsuranceCard.us", image_data)
    result = poller.result()

    summary = {}
    for d in result.documents:
        groupNumber = d.fields.get("GroupNumber")
        if groupNumber:
            summary["Group Number"] = groupNumber.value
        memberID = d.fields.get("IdNumber")
        if memberID and memberID.value.get("Number"):
            summary["Member ID"] = memberID.value.get("Number").value
        memberName = d.fields.get("Member")
        if memberName and memberName.value.get("Name"):
            summary ["Member Name"] = memberName.value.get("Name").value
        plan = d.fields.get("Plan")
        if plan and plan.value.get("Name"):
            summary ["Plan"] = plan.value.get("Name").value
    st.sidebar.success(summary)

imageCaptured = st.camera_input("Take a picture of Insurance Card", key="firstCamera", help="help info" )
if imageCaptured:
   fullname = os.path.join("tmpDir",imageCaptured.name)
   with open(fullname,"wb") as f:
         f.write(imageCaptured.getbuffer())
   # Process the health insurance card
   process_health_insurance_card(api_key, endpoint, fullname)
