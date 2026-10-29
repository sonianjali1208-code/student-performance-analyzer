import pandas as pd
import streamlit as st

st.title("Student Performance Analyzer")

st.write("Analyze student marks and performance easily.")

uploaded_file = st.file_uploader(
    "Upload Student CSV",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("students.csv")

subjects = ["Maths", "Science", "English", "Computer"]

data["Average"] = data[subjects].mean(axis=1)
data["Result"] = data["Average"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)

top_student = data.loc[data["Average"].idxmax(), "Name"]

pass_percentage = (data["Result"] == "Pass").mean() * 100

st.write("Student Performance Data")
st.dataframe(data)
st.write("Top Student:", top_student)
st.write("Pass Percentage:", pass_percentage)


total_students = len(data)
average_marks = data["Average"].mean()
failed_students = (data["Result"] == "Fail").sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("Average Marks", round(average_marks, 2))
col3.metric("Pass Percentage", f"{pass_percentage:.2f}%")
col4.metric("Top Student", top_student)

subject_averages = data[subjects].mean()

st.subheader("📊 Subject-wise Average")
st.bar_chart(subject_averages)

st.subheader("📈 Student Performance")
chart_data = data.set_index("Name")["Average"]
st.bar_chart(chart_data)

st.subheader("✅ Pass/Fail Summary")
result_count = data["Result"].value_counts()
st.bar_chart(result_count)











