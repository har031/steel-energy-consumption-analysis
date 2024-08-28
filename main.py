import streamlit as st
from google.cloud import storage
import io
import os

# Initialize Google Cloud Storage client
def save_locally_and_upload_to_gcs(bucket_name, file_name, file_data):
    try:
        # Save the file locally
        local_path = os.path.join("local_uploads", file_name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Write the file data to a local file
        with open(local_path, "wb") as f:
            f.write(file_data.getbuffer())
        
        st.success(f"File {file_name} saved locally at {local_path}.")
        
        # Print debug info
        print(f"File saved locally at: {local_path}")
        print(f"Bucket name: {bucket_name}")
        print(f"File name: {file_name}")
        print(f"File data: {file_data}")

        # Reset file pointer to the beginning before uploading
        file_data.seek(0)
        
        # Upload the file to GCS
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        print(f"Uploading file {file_name} to GCS bucket {bucket_name}...")
        
        blob.upload_from_file(file_data, content_type='text/csv')
        
        st.success(f"File {file_name} uploaded successfully to bucket: {bucket_name}.")
    
    except Exception as e:
        st.error(f"Error saving or uploading file: {e}")
        print(f"Error saving or uploading file: {e}")

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
            
            if st.button("Save Locally and Upload to GCS"):
                # Save locally and then upload the file to Google Cloud Storage
                try:
                    save_locally_and_upload_to_gcs(bucket_name, uploaded_file.name, uploaded_file)
                except Exception as e:
                    st.error(f"An error occurred during upload: {e}")

if __name__ == "__main__":
    main()

