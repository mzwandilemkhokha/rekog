import streamlit as st
import boto3
import os

# AWS credentials and region for S3
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_REGION = "us-east-1"

# AWS credentials and region for Rekognition
AWS_REKOGNITION_ACCESS_KEY_ID = "YOUR_REKOGNITION_ACCESS_KEY"
AWS_REKOGNITION_SECRET_ACCESS_KEY = "YOUR_REKOGNITION_SECRET_KEY"

# S3 bucket name
S3_BUCKET_NAME = "recogaws"

# Initialize AWS Rekognition client
rekognition = boto3.client(
    "rekognition",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_REKOGNITION_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_REKOGNITION_SECRET_ACCESS_KEY,
)

# Streamlit UI setup
st.title("Image Search and Upload")

# User input for image description
description = st.text_input("Enter a single-word description:")

if description:
    # Process user input
    description = description.lower()

    # List to store matching image URLs
    matching_images = []

    # List objects in the S3 bucket
    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    objects = s3.list_objects(Bucket=S3_BUCKET_NAME)

    for obj in objects.get("Contents", []):
        # Analyze image content using AWS Rekognition
        image_key = obj["Key"]
        response = rekognition.detect_labels(
            Image={
                "S3Object": {
                    "Bucket": S3_BUCKET_NAME,
                    "Name": image_key,
                }
            }
        )

        # Check if the description matches any label with a confidence score > 90%
        for label in response["Labels"]:
            if label["Confidence"] > 90 and description in label["Name"].lower().split():
                # Add the matching image URL to the list
                matching_images.append(image_key)

    # Display matching images
    if matching_images:
        st.subheader("Matching Images:")
        for image_url in matching_images:
            image_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{image_url}"
            st.image(image_url, caption=image_url, use_column_width=True)

            # Add a download link for the image
            st.markdown(f"[Download Image]({image_url})")

    else:
        st.info("No matching images found.")

# User input for image upload
uploaded_file = st.file_uploader("Upload an image to S3:", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Upload the image to the S3 bucket
    file_name = os.path.basename(uploaded_file.name)

    try:
        s3.upload_fileobj(uploaded_file, S3_BUCKET_NAME, file_name)
        st.success(f"Image '{file_name}' uploaded to S3 bucket '{S3_BUCKET_NAME}'.")
    except Exception as e:
        st.error(f"Error uploading image: {e}")

# Note: Replace all placeholders with your AWS credentials and S3 bucket name.
