import streamlit as st
from google.cloud import storage
import toml
import json
import os

def load_google_credentials_from_toml():
    toml_str = st.secrets["google_credentials"]
    credentials_dict = toml.loads(toml_str)
    return json.dumps(credentials_dict)

def upload_to_gcs(bucket_name, file_name, file_data):
    try:
        # Load credentials from TOML
        credentials_json = load_google_credentials_from_toml()
        credentials_dict = json.loads(credentials_json)
        
        # Initialize Google Cloud Storage client with the credentials
        client = storage.Client.from_service_account_info(credentials_dict)
        
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        file_data.seek(0)  # Reset file pointer to the beginning
        blob.upload_from_file(file_data, content_type='text/csv')
        
        st.success(f"File {file_name} uploaded successfully to bucket: {bucket_name}.")
    except Exception as e:
        st.error(f"Error uploading file to GCS: {e}")

# Streamlit app
def main():
    st.title("Upload to Google Cloud Storage")
    bucket_name = st.text_input("Enter your GCS Bucket Name", "")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file and st.button("Upload to GCS"):
        upload_to_gcs(bucket_name, uploaded_file.name, uploaded_file)

if __name__ == "__main__":
    main()


