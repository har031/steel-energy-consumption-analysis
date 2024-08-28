import streamlit as st
from google.cloud import storage
import io
import os

# Initialize Google Cloud Storage client
def upload_file_to_gcs(bucket_name, file_data):
    try:
        # Reset file pointer to the beginning before uploading
        file_data.seek(0)
        
        # Upload the file to GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_data.name)

        blob.upload_from_file(file_data, content_type='text/csv')
        
        st.success(f"File {file_data.name} uploaded successfully to bucket: {bucket_name}.")
    
    except Exception as e:
        st.error(f"Error uploading file: {e}")
        print(f"Error uploading file: {e}")

# Streamlit app
def main():
    # Page configuration
    st.set_page_config(page_title="Steel Energy Consumption Analysis", layout="wide")
    
    # Title and description
    st.title("Steel Industry Energy Consumption Analysis")
    st.markdown("""
        **Upload a CSV file** with energy consumption data for analysis. 
        The data should include relevant metrics for steel production and energy usage.
    """)
    
    # Bucket name input
    bucket_name = st.text_input("Enter your GCS Bucket Name", "")

    # File uploader with restrictions (CSV and size limit)
    uploaded_file = st.file_uploader(
        "Upload your energy data file (CSV, max 200 MB)", 
        type=["csv"]
    )
    
    # Check file size and process upload
    if uploaded_file is not None:
        if uploaded_file.size > 200 * 1024 * 1024:  # 200 MB limit
            st.error("The file size exceeds the 200 MB limit. Please upload a smaller file.")
        else:
            st.write("**File Details:**")
            st.write(f"Filename: {uploaded_file.name}")
            st.write(f"File type: {uploaded_file.type}")
            st.write(f"File size: {uploaded_file.size / (1024 * 1024):.2f} MB")
            
            if st.button("Upload to GCS"):
                # Upload the file to Google Cloud Storage
                upload_file_to_gcs(bucket_name, uploaded_file)

if __name__ == "__main__":
    main()
