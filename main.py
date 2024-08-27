
import streamlit as st
from google.cloud import storage
import io

# Initialize Google Cloud Storage client
def upload_to_gcs(bucket_name, file_name, file_data):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Reset file pointer to the beginning
    file_data.seek(0)
    
    # Upload the file
    blob.upload_from_file(file_data, content_type='text/csv')
    
    st.success(f"File {file_name} uploaded successfully to bucket: {bucket_name}.")


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
        if uploaded_file.size > 200 * 1024 * 1024:  # 50 MB limit
            st.error("The file size exceeds the 200 MB limit. Please upload a smaller file.")
        else:
            st.write("**File Details:**")
            st.write(f"Filename: {uploaded_file.name}")
            st.write(f"File type: {uploaded_file.type}")
            st.write(f"File size: {uploaded_file.size / (1024 * 1024):.2f} MB")
            
            if st.button("Upload to GCS"):
                # Upload the file to Google Cloud Storage
                try:
                    upload_to_gcs(bucket_name, uploaded_file.name, uploaded_file)
                except Exception as e:
                    st.error(f"An error occurred during upload: {e}")

if __name__ == "__main__":
    main()

