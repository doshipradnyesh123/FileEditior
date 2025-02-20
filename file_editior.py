import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title='Excel Editior', page_icon="🧊", layout="wide", initial_sidebar_state="auto",menu_items={
    'Report a bug': "mailto:pradnyeshdoshi01@gmail.com",
    'About': """"This web application is designed to allow you to view and edit your Excel files directly from your mobile device or laptop, without the need to install or set up any software on your device."

        Let me know if you need any further changes!

        pradnyeshdoshi01@gmail.com
"""
    })

st.title("File Editor Web Application")
def excel_editor():
    """A Streamlit function to upload, edit, and download an Excel file."""
    st.divider()    
    st.header('Excel Editior 📈')
    st.subheader('Feed me with your Excel file')

    uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
    if uploaded_file:
        st.markdown('---')
        sheets_dict = pd.read_excel(uploaded_file, engine='openpyxl',sheet_name=None)
        sheet_name = st.selectbox("Select a sheet to edit", list(sheets_dict.keys()))

        # Load the selected sheet into a DataFrame
        df = sheets_dict[sheet_name]
        df.insert(0, "Index", range(1, len(df) + 1))
        edited_df = st.data_editor(df,width = 1500, height = 500,num_rows="dynamic" )

    # Convert edited DataFrame to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            edited_df.drop(columns="Index", inplace=True)
            edited_df.to_excel(writer, index=False, sheet_name=sheet_name)
        output.seek(0)

        # Download button
        st.download_button(
            label="Download Edited Excel",
            data=output,
            file_name = f"Data_Correction_file_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    st.divider()
def text_file_editor():
    st.header("Text File Editor")
    st.subheader('Feed me with your text file')
    # Upload text file
    try:
        uploaded_file = st.file_uploader("Upload a text file")
    except UnicodeDecodeError as e:
        st.error(f"An error occurred: {e}")
    except Exception as e:
        st.error(f"An error while reading the file. ERROR : {e}")
    else:
        if uploaded_file:
            # Read file content
            text_content = uploaded_file.read().decode("utf-8")

            # Display text editor
            edited_text = st.text_area("Edit the text", text_content, height=800)

            # Convert edited text to bytes for download
            output = BytesIO()
            output.write(edited_text.encode("utf-8"))
            output.seek(0)

            # Download button
            st.download_button(
                label="Download Edited File",
                data=output,
                file_name="edited_text.txt",
                mime="text/plain"
            )
    st.divider()
# Call the function in your Streamlit app
if __name__ == "__main__":
    excel_editor()
    text_file_editor()
