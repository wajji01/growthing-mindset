import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="💿 Data Sweeper",layout="wide")
st.title("💿 _**Data Sweeper**_")
st.write("Transform your file between CSV and Excel formats with built-in data cleaning and visualization!")

uploaded_file = st.file_uploader("Upload your file (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type: {file.ext}")
            continue

        st.write(f"**File name:** {file.name}")
        st.write(f"**File size:** {file.size / 1024:.2f} KB")

        st.write("Preview the Head of the DataFrame:")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Options")
        if st.checkbox(f"clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df = df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully!")

            with col2:
                    if st.button(f"Fill Missing Values for {file.name}"): 
                      numeric_cols = df.select_dtypes(include=['number']).columns
                      df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                      st.write("Missing values filled successfully!")

        st.subheader("Column Selection")
        columns = st.multiselect(f"choose columns for {file.name}", df.columns, default=list(df.columns))
        df = df[columns]
    
        st.subheader("📊 Data Visualizations")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:,:2])

        st.subheader("💿 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"],key=file.name)
        if st.button(f"Convert {file.name} "):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
            
            st.success("🎉 All files converted to successfully!")





