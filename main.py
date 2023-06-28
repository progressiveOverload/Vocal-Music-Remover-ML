import os
import streamlit as st
import base64
from spleeter.separator import Separator

# Set up Streamlit
st.title("Vocal Separation App")

# Upload file and process
uploaded_file = st.file_uploader("Upload a music file", type=["wav", "mp3"])
if uploaded_file is not None:
    # Create the output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Save the uploaded file
    input_file_path = os.path.join("output", "input_file.wav")
    with open(input_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Perform vocal separation
    separator = Separator("spleeter:2stems")
    with st.spinner("Separating vocals..."):
        separator.separate_to_file(input_file_path, "output")

    # Display the separated files
    st.subheader("Separated Files")
    vocals_file = os.path.join("output", "input_file", "vocals.wav")
    instrumental_file = os.path.join("output", "input_file", "accompaniment.wav")

    # Check if output files exist
    if os.path.exists(vocals_file) and os.path.exists(instrumental_file):
        # Read audio files as bytes
        with open(vocals_file, "rb") as f:
            vocals_bytes = f.read()
        with open(instrumental_file, "rb") as f:
            instrumental_bytes = f.read()

        # Display audio using base64 encoding
        st.audio(vocals_bytes, format="audio/wav")
        st.write("Vocals")
        st.audio(instrumental_bytes, format="audio/wav")
        st.write("Instrumental")

        # Provide download links
        st.subheader("Download Separated Files")
        st.markdown(
            f'<a href="data:audio/wav;base64,{base64.b64encode(vocals_bytes).decode()}" download="vocals.wav">Download Vocals</a>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<a href="data:audio/wav;base64,{base64.b64encode(instrumental_bytes).decode()}" download="instrumental.wav">Download Instrumental</a>',
            unsafe_allow_html=True,
        )

        # Clean up the temporary files
        os.remove(input_file_path)
        os.remove(vocals_file)
        os.remove(instrumental_file)
        os.rmdir(os.path.join("output", "input_file"))
        os.rmdir("output")
    else:
        st.error("Error: Separated audio files not found.")
