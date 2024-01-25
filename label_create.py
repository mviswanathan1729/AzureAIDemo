import json
import pandas as pd

excel_file_path = "voc.xlsx"
output_folder_path = "text-folder"

# Create Labels JSON
metadata = {
    "projectKind": "CustomMultiLabelClassification",
    "storageInputContainerName": "voc-data",
    "projectName": "VoC",
    "multilingual": False,
    "description": "VoC Classification",
    "language": "en",
    "settings": {}
}

labels_json = {"projectFileVersion": "2022-05-01", "stringIndexType": "Utf16CodeUnit", "metadata": metadata, "assets": {}}
labels_json["assets"]["projectKind"] = "customMultiLabelClassification"
labels_json["assets"]["classes"] = []
labels_json["assets"]["documents"] = []

all_classes = ["label1", "label2", "label3"]
for c in all_classes:
    labels_json["assets"]["classes"].append({"category": c})

# Process Excel File
def processExcel(excel_file, output_folder):
    df = pd.read_excel(excel_file)

    # Process each row 
    for index, row in df.iterrows():

        # create a text file from 'Details' column
        filename = f"file-{index + 1}.txt"
        filelocation = f"{output_folder}/{filename}"
        with open(filelocation, 'w') as text_file:
            text_file.write(str(row['Details']))

        labels = [row['Label'], row['Label']+"11"]
        entry = {
             "location": filename,
            "language": "en-us",
            "classes": []
        }
       
        for d in labels:
            entry["classes"].append({"category": d}) 

        labels_json["assets"]["documents"].append(entry)  

processExcel(excel_file_path, output_folder_path)

# Save JSON to a file
with open("labels.json", "w") as json_file:
    json.dump(labels_json, json_file, indent=2)



