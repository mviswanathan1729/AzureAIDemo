# -------------------------------------------------------------------------
# Voice of the Customer Review
# -------------------------------------------------------------------------

import streamlit as st
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.ai.textanalytics import TextAnalyticsClient

text = st.text_area(label="VoC Text", value="")
submit_button = st.button(label="Submit")

# [START multi_label_classify]
def sample_classify_document_multi_label() -> None:

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    project_name = "voc2project"
    deployment_name = "voc2deploy"

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = text_analytics_client.begin_multi_label_classify(
        [text],
        project_name=project_name,
        deployment_name=deployment_name
    )
    summary = []
    document_results = poller.result()
    for doc, classification_result in zip([text], document_results):
        if classification_result.kind == "CustomDocumentClassification":
            classifications = classification_result.classifications
            #print(f"\nThe movie plot '{doc}' was classified as the following genres:\n")
            for classification in classifications:
                summary.append("{} (confidence: {})".format(
                    classification.category, classification.confidence_score
                ))
            st.sidebar.success(summary)  

        elif classification_result.is_error is True:
            print("VoC '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message
            ))
    # [END multi_label_classify]

def analyze_text(my_text):
    # analyze text
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

    # Create an Azure AI Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # Contruct request
    request = AnalyzeTextOptions(text=my_text)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise
    summary = response.get("categoriesAnalysis")
    st.sidebar.success(summary) 

def sentiment_analysis(text):

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]

    client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
    documents = [text]

    response = client.analyze_sentiment(documents)
    st.sidebar.success(response[0].confidence_scores)

    
if submit_button:
    sample_classify_document_multi_label()
    analyze_text(text)
    sentiment_analysis(text)

