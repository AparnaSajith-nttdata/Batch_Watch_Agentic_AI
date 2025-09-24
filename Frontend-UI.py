import streamlit as st 

st.title =("Batch Agent")

uploaded_files  = st.file_uploader("Upload  files",  accept_multiple_files=True)
for  file  in uploaded_files:
        st.write("Uploaded:", file.name)

import  pandas  as pd

if uploaded_files:
        df =  pd.read_csv(uploaded_files)
        st.dataframe(df)

if  uploaded_files:
        content  = uploaded_files.read().decode("utf-8")
        st.text(content)


