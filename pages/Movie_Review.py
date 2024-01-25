# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_multi_label_classify.py

DESCRIPTION:
    This sample demonstrates how to classify documents into multiple custom categories. For example,
    movie plot summaries can be categorized into multiple movie genres like "Action" and "Thriller",
    or "Comedy" and "Drama", etc. Classifying documents is also available as an action type through
    the begin_analyze_actions API.

    For information on regional support of custom features and how to train a model to
    classify your documents, see https://aka.ms/azsdk/textanalytics/customfunctionalities

USAGE:
    python sample_multi_label_classify.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_LANGUAGE_ENDPOINT - the endpoint to your Language resource.
    2) AZURE_LANGUAGE_KEY - your Language subscription key
    3) MULTI_LABEL_CLASSIFY_PROJECT_NAME - your Language Studio project name
    4) MULTI_LABEL_CLASSIFY_DEPLOYMENT_NAME - your Language Studio deployment name
"""

import streamlit as st

text = st.text_area(label="Movie Plot", value="")
submit_button = st.button(label="Submit")
reset_button = st.button(label="Reset")

def sample_classify_document_multi_label() -> None:
    # [START multi_label_classify]
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]
    project_name = os.environ["MULTI_LABEL_CLASSIFY_PROJECT_NAME"]
    deployment_name = os.environ["MULTI_LABEL_CLASSIFY_DEPLOYMENT_NAME"]

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
            print("Movie plot '{}' has an error with code '{}' and message '{}'".format(
                doc, classification_result.error.code, classification_result.error.message
            ))
    # [END multi_label_classify]

#if reset_button:
    #
if submit_button:
    sample_classify_document_multi_label()

