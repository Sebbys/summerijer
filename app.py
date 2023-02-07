import streamlit as st
import base64
import io
import functions

def main():

    st.set_page_config(page_title="Text Summarizer", page_icon=":memo:", layout="wide")
    st.title('🐋 Summarijer 🐋')


    st.write("Pilih Mode Input String / File (txt)")
    choice = st.radio("", ["Input String", "Upload File"])

    if choice == "Input String":
        input_text = st.text_area("Masukkan Text Untuk Di Summerize")
        n = st.number_input("Banyaknya Kalimat Summary", min_value=1, step=1)
        if st.button("Summarize"):
            summarized_text = functions.summarijer(input_text, n)
            st.write("Summary:")
            st.write(summarized_text)
            bio = download_summary(summarized_text)
            st.markdown("<a href='data:text/plain;base64,{}' download='summary.txt'>Download Summary</a>".format(base64.b64encode(bio.getvalue().encode('utf-8')).decode("utf-8")), unsafe_allow_html=True)

    if choice == "Upload File":
        st.write("Upload File Untuk Di Summerize")
        uploaded_file = st.file_uploader("Pilih File (txt)", type=["txt"])

        if uploaded_file is not None:
            file_text = uploaded_file.read().decode("utf-8")
            n = st.number_input("Banyaknya Kalimat Summary", min_value=1, max_value=len(file_text.split(".")), value=3, step=1)

            if st.button("Summarize"):
                summarized_text = functions.summarijer(file_text, n)
                st.write("Summary:")
                st.write(summarized_text)
                bio = download_summary(summarized_text)
                st.markdown("<a href='data:text/plain;base64,{}' download='summary.txt'>Download Summary</a>".format(base64.b64encode(bio.getvalue().encode('utf-8')).decode("utf-8")), unsafe_allow_html=True)
    
def download_summary(summarized_text):
    bio = io.StringIO(summarized_text)
    return bio
if __name__ == "__main__":
    main()
