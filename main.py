import streamlit as st
import boto3

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
# Initialize AWS Rekognition client
rekognition = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)  # Replace 'your-region' with your AWS region

st.title("Image Analysis with AWS Rekognition")

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Analyze the uploaded image when a button is clicked
    if st.button("Analyze Image"):
        st.write("Analyzing...")

        # Use AWS Rekognition to detect labels in the image
        try:
            with st.spinner("Analyzing..."):
                response = rekognition.detect_labels(
                    Image={
                        'Bytes': uploaded_image.read()
                    }
                )

            # Display the detected labels
            st.subheader("Detected Labels:")
            for label in response['Labels']:
                st.write(f"{label['Name']} (Confidence: {label['Confidence']:.2f}%)")

        except Exception as e:
            st.error(f"Error: {str(e)}")

