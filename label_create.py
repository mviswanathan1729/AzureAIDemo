import json
import pandas as pd
import re

excel_file_path = "voc2.xlsx"
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


# Process Excel File
def processExcel(excel_file, output_folder):
    all_classes = []
    df = pd.read_excel(excel_file)

    # Process each row 
    all_documents = []
    for index, row in df.iterrows():
        
        filename = f"file-{index + 1}.txt"

        # create a text file from 'Improvement Comment' column only if previous and current are different
        if index==0 or (index > 0 and df.loc[index - 1, 'Improvement Comment'] != row['Improvement Comment']):
            filelocation = f"{output_folder}/{filename}"
            with open(filelocation, 'w') as text_file:
                text_file.write(str(row['Improvement Comment']))
            # add a new entry

            entry = {
                "location": filename,
                "language": "en-us",
                "classes": []
            }
            all_documents.append(entry)

        else:
            # previous and current are same, so use the same filename
            filename = f"file-{index}.txt"
            # dont add a new entry but append to the existing entry
            entry = all_documents[-1]
                    
        # Add feature and sub-featuire labels
        labels = [row['VoC Feature'], row['VoC Sub-Feature']]

        # Add to full list of classification labels. Remove special characters and strip whitespace
        for d in labels:
            if d is not None and isinstance(d, str):
                d = d.strip()
                d = re.sub(r'[^\w\s]+', ' ', d)
                # check if category is already in entry["classes"]
                if not any(c['category'] == d for c in entry["classes"]):
                    entry["classes"].append({"category": d}) 
                    all_classes.append(d)
    
    # Create unique classes of all classification labels
    unique_classes = list(set(all_classes))
    for c in unique_classes:
        labels_json["assets"]["classes"].append({"category": c})
    for d in all_documents:
        labels_json["assets"]["documents"].append(d)  

processExcel(excel_file_path, output_folder_path)

# Save JSON to a file
with open("labels.json", "w") as json_file:
    json.dump(labels_json, json_file, indent=2)



