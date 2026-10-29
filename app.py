import pandas as pd
import streamlit as st
import re
from io import BytesIO
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

# =========================================
# PAGE SETTINGS
# =========================================

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
<style>

/* ========================================
   MAIN BACKGROUND
======================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #CFDDF0 0%,
        #DDD5EC 50%,
        #D0E3E1 100%
    );
}

/* ========================================
   MAIN HEADER
======================================== */

.header {
    padding: 38px;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 35px;

    background: linear-gradient(
        135deg,
        #E3EEFF,
        #EEE7FF,
        #E1F5F0
    );

    border: 1px solid #D8DEEA;

    box-shadow:
        0 10px 30px rgba(60, 70, 100, 0.10);
}

/* Header Hover Effect */

.header {
    transition: all 0.4s ease;
}

.header:hover {
    transform: translateY(-3px);

    box-shadow:
        0 15px 35px rgba(60, 70, 100, 0.16);

    border-color: #A5B4FC;
}

.header h1 {
    font-size: 42px;
    margin-bottom: 10px;
    color: #172554;
    font-weight: 800;
}

.header p {
    font-size: 18px;
    color: #475569;
    margin-bottom: 0px;
}


/* ========================================
   SECTION HEADINGS
======================================== */

h2, h3 {
    color: #172554;
}


/* ========================================
   UPLOAD SECTION
======================================== */

.upload-card {
    background: rgba(255, 255, 255, 0.85);
    padding: 22px;
    border-radius: 20px;
    border: 1px solid #E2E8F0;

    box-shadow:
        0 8px 25px rgba(60, 70, 100, 0.07);

    margin-bottom: 28px;
}

[data-testid="stFileUploader"] {
    background: linear-gradient(
        135deg,
        #F8FAFF,
        #F7F4FF
    );

    padding: 16px;

    border-radius: 16px;

    border: 2px dashed #A5B4FC;
}


/* ========================================
   KPI CARDS
======================================== */

.kpi-card {
    padding: 22px;
    border-radius: 20px;
    min-height: 135px;

    box-shadow:
        0 8px 22px rgba(60, 70, 100, 0.10);

    margin-bottom: 20px;

    transition: all 0.3s ease;
    cursor: pointer;
}

.kpi-card:hover {
    transform: translateY(-7px) scale(1.02);

    box-shadow:
        0 16px 35px rgba(30, 41, 59, 0.20);

    filter: brightness(1.03);
}

.kpi-icon {
    font-size: 28px;
    margin-bottom: 8px;
}

.kpi-title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 30px;
    font-weight: 800;
}


/* BLUE */

.card-blue {
    background: linear-gradient(
        135deg,
        #E3EEFF,
        #CFE0FF
    );

    border-left: 6px solid #3B82F6;
}

.card-blue .kpi-title {
    color: #1E40AF;
}

.card-blue .kpi-value {
    color: #1D4ED8;
}


/* PURPLE */

.card-purple {
    background: linear-gradient(
        135deg,
        #F0E8FF,
        #E1D1FF
    );

    border-left: 6px solid #9333EA;
}

.card-purple .kpi-title {
    color: #6B21A8;
}

.card-purple .kpi-value {
    color: #7E22CE;
}


/* GREEN */

.card-green {
    background: linear-gradient(
        135deg,
        #DCFCE7,
        #C9F7D5
    );

    border-left: 6px solid #16A34A;
}

.card-green .kpi-title {
    color: #166534;
}

.card-green .kpi-value {
    color: #15803D;
}


/* ORANGE */

.card-orange {
    background: linear-gradient(
        135deg,
        #FFF1DB,
        #FFE1B8
    );

    border-left: 6px solid #F59E0B;
}

.card-orange .kpi-title {
    color: #92400E;
}

.card-orange .kpi-value {
    color: #D97706;
}


/* ========================================
   SECTION CARD
======================================== */

.section-card {
    background: rgba(255, 255, 255, 0.90);

    padding: 22px;

    border-radius: 20px;

    border: 1px solid #E2E8F0;

    box-shadow:
        0 8px 25px rgba(60, 70, 100, 0.07);

    margin-bottom: 28px;

    transition: all 0.3s ease;
}

.section-card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 14px 30px rgba(30, 41, 59, 0.15);

    border-color: #A5B4FC;
}

/* ========================================
   STUDENT PERFORMANCE BOXES
======================================== */

.student-box {
    flex: 1;
    min-width: 120px;
    padding: 18px;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        #F8FAFF,
        #F1F5FF
    );
    border: 1px solid #E2E8F0;
    text-align: center;
    box-shadow:
        0 5px 15px rgba(60, 70, 100, 0.06);
}

.student-title {
    font-size: 14px;
    font-weight: 600;
    color: #475569;
    margin-bottom: 8px;
}

.student-value {
    font-size: 24px;
    font-weight: 800;
    color: #172554;
}


/* ========================================
   PASS / FAIL CARDS
======================================== */

.result-card {
    padding: 22px;
    border-radius: 18px;
    text-align: center;

    box-shadow:
        0 6px 18px rgba(60, 70, 100, 0.08);

    margin-bottom: 18px;

    transition: all 0.3s ease;
    cursor: pointer;
}

.result-card:hover {
    transform: translateY(-5px) scale(1.02);

    box-shadow:
        0 14px 30px rgba(30, 41, 59, 0.15);
}

.pass-card {
    background: linear-gradient(
        135deg,
        #E8FAEF,
        #D4F5DF
    );

    border: 1px solid #B7E8C7;
}

.fail-card {
    background: linear-gradient(
        135deg,
        #FFF0F0,
        #FFE0E0
    );

    border: 1px solid #F3C2C2;
}

.result-number {
    font-size: 30px;
    font-weight: 800;
}

.pass-text {
    color: #15803D;
}

.fail-text {
    color: #DC2626;
}

.result-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 5px;
}


/* ========================================
   DATA TABLE
======================================== */
[data-testid="stVegaLiteChart"] {
    pointer-events: none;
}


[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
    border: 1px solid #E2E8F0;
}


/* ========================================
   ALERT / SUCCESS MESSAGE
======================================== */

[data-testid="stAlert"] {
    border-radius: 12px;
}


/* ========================================
   DIVIDER
======================================== */

hr {
    border: none;
    height: 1px;
    background: #E2E8F0;
    margin: 30px 0;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================
# HEADER
# =========================================

st.markdown(
    """
<div class="header">
<h1>🎓 Student Performance Analyzer</h1>
<p>Analyze student performance and discover useful insights.</p>
</div>
""",
    unsafe_allow_html=True
)


# =========================================
# UPLOAD STUDENT DATA
# =========================================

st.subheader("📂 Upload Student Data")

st.markdown(
    """
<div class="upload-card">
<p style="color:#475569; font-size:16px;">
Upload a CSV file containing student marks for analysis.
</p>
</div>
""",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose your CSV file",
    type=["csv"]
)


# =========================================

# =========================================
# READ CSV SAFELY
# =========================================

if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV file is empty.")
        st.stop()
    except (pd.errors.ParserError, UnicodeDecodeError, OSError, ValueError):
        st.error("Unable to read this CSV file. Please check its format.")
        st.stop()

else:
    try:
        data = pd.read_csv("students.csv", encoding="utf-8-sig")
    except FileNotFoundError:
        st.error(
            "students.csv was not found. "
            "Please upload a valid student CSV file."
        )
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("The default students.csv file is empty.")
        st.stop()
    except (pd.errors.ParserError, UnicodeDecodeError, OSError, ValueError):
        st.error("Unable to read students.csv. Please check its format.")
        st.stop()



# =========================================
# CHECK REQUIRED COLUMNS
# =========================================

required_columns = [
    "Name",
    "Maths",
    "Science",
    "English",
    "Computer"
]

missing_columns = []

for column in required_columns:
    if column not in data.columns:
        missing_columns.append(column)

if missing_columns:

    st.error(
        "❌ Missing columns: "
        + ", ".join(missing_columns)
    )

    st.stop()

    
# =========================================
# CHECK EMPTY DATA AND STUDENT NAMES
# =========================================

if data.empty:
    st.error("No student records found in the CSV file.")
    st.stop()

# Remove extra spaces from student names
data["Name"] = data["Name"].astype("string").str.strip()

# Check missing or blank student names
invalid_names = data["Name"].isna() | data["Name"].eq("")

if invalid_names.any():
    st.error(
        "Some student names are missing or blank. "
        "Please correct the CSV file."
    )
    st.stop()

# Check duplicate names
duplicate_names = data.loc[
    data["Name"].str.casefold().duplicated(keep=False),
    "Name"
].unique()

if len(duplicate_names) > 0:
    st.error(
        "Duplicate student names found: "
        + ", ".join(duplicate_names)
        + ". Please make each student name unique "
        "before continuing."
    )
    st.stop()


# =========================================
# SUBJECTS
# =========================================

subjects = [
    "Maths",
    "Science",
    "English",
    "Computer"
]

# =========================================
# CHECK NUMERIC MARKS
# =========================================

for subject in subjects:

    data[subject] = pd.to_numeric(
        data[subject],
        errors="coerce"
    )

if data[subjects].isnull().any().any():

    st.error(
        "❌ Invalid marks found! "
        "Please enter numbers only."
    )

    st.stop()

# =========================================
# CHECK MARKS
# =========================================

invalid_marks = False

for subject in subjects:

    if (data[subject] < 0).any() or (data[subject] > 100).any():
        invalid_marks = True

if invalid_marks:

    st.error(
        "❌ Invalid marks found! "
        "Marks should be between 0 and 100."
    )

    st.stop()


# =========================================
# CALCULATE AVERAGE
# =========================================

data["Average"] = data[subjects].mean(axis=1)


# =========================================
# CALCULATE RESULT
# =========================================

data["Result"] = data["Average"].apply(
    lambda x: "Pass" if x >= 40 else "Fail"
)

# =========================================
# STEP 6: PERFORMANCE CATEGORY
# =========================================

def get_category(average):
    if average >= 80:
        return "Excellent"
    elif average >= 60:
        return "Good"
    elif average >= 40:
        return "Average"
    else:
        return "Needs Improvement"

data["Performance Category"] = data["Average"].apply(get_category)


# =========================================
# STUDENT RANKING SYSTEM
# =========================================

data["Rank"] = data["Average"].rank(
    ascending=False,
    method="min"
).astype(int)



# =========================================
# FIND TOP STUDENT
# =========================================

top_student = data.loc[
    data["Average"].idxmax(),
    "Name"
]

# =========================================
# TOP 3 STUDENTS
# =========================================

top_3 = data.sort_values(
    by="Average",
    ascending=False
).head(3)

# =========================================
# STATISTICS
# =========================================

total_students = len(data)

average_marks = data["Average"].mean()

pass_percentage = (
    data["Result"] == "Pass"
).mean() * 100

passed_students = (
    data["Result"] == "Pass"
).sum()

failed_students = (
    data["Result"] == "Fail"
).sum()


# =========================================
# PERFORMANCE OVERVIEW
# =========================================

st.subheader("📊 Performance Overview")

col1, col2, col3, col4 = st.columns(4)


# Blue Card

with col1:

    st.markdown(
        f"""
<div class="kpi-card card-blue">
<div class="kpi-icon">👨‍🎓</div>
<div class="kpi-title">Total Students</div>
<div class="kpi-value">{total_students}</div>
</div>
""",
        unsafe_allow_html=True
    )


# Purple Card

with col2:

    st.markdown(
        f"""
<div class="kpi-card card-purple">
<div class="kpi-icon">📊</div>
<div class="kpi-title">Average Marks</div>
<div class="kpi-value">{average_marks:.1f}</div>
</div>
""",
        unsafe_allow_html=True
    )


# Green Card

with col3:

    st.markdown(
        f"""
<div class="kpi-card card-green">
<div class="kpi-icon">✅</div>
<div class="kpi-title">Pass Percentage</div>
<div class="kpi-value">{pass_percentage:.1f}%</div>
</div>
""",
        unsafe_allow_html=True
    )


# Orange Card

with col4:

    st.markdown(
        f"""
<div class="kpi-card card-orange">
<div class="kpi-icon">🏆</div>
<div class="kpi-title">Top Student</div>
<div class="kpi-value">{escape(str(top_student))}</div>
</div>
""",
        unsafe_allow_html=True
    )

# =========================================
# STUDENT FILTER
# =========================================

st.subheader("🔍 Search Student")

selected_student = st.selectbox(
    "Select a student",
    data["Name"]
)

student_data = data[
    data["Name"] == selected_student
].iloc[0]


# =========================================
# INDIVIDUAL STUDENT REPORT CARD
# =========================================

st.subheader("📄 Individual Student Report Card")

# Calculate student result details
total_marks = student_data[subjects].sum()
maximum_marks = len(subjects) * 100

percentage = (total_marks / maximum_marks) * 100
student_average = student_data["Average"]
student_rank = int(student_data["Rank"])
student_result = student_data["Result"]
performance_category = student_data["Performance Category"]

# Find strongest and weakest subjects
strongest_subject = student_data[subjects].idxmax()
weakest_subject = student_data[subjects].idxmin()

strongest_marks = student_data[strongest_subject]
weakest_marks = student_data[weakest_subject]

# Generate teacher-style remarks
if student_average >= 80:
    teacher_remarks = (
        "Excellent work! Keep maintaining your performance "
        "and continue challenging yourself."
    )
elif student_average >= 60:
    teacher_remarks = (
        "Good performance. Regular revision and practice "
        "can help you achieve even better marks."
    )
elif student_average >= 40:
    teacher_remarks = (
        "Satisfactory performance. Focus on weaker subjects "
        "and practise questions regularly."
    )
else:
    teacher_remarks = (
        "More attention and regular practice are needed. "
        "Create a study timetable and seek help when required."
    )

# Create a PDF in memory
pdf_buffer = BytesIO()

pdf = SimpleDocTemplate(
    pdf_buffer,
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=18 * mm,
    bottomMargin=18 * mm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=20,
    leading=25,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#1D4ED8"),
    spaceAfter=6
)

subtitle_style = ParagraphStyle(
    "ReportSubtitle",
    parent=styles["Normal"],
    alignment=TA_CENTER,
    fontSize=10,
    textColor=colors.HexColor("#475569")
)

section_style = ParagraphStyle(
    "ReportSection",
    parent=styles["Heading2"],
    fontSize=12,
    leading=16,
    textColor=colors.HexColor("#1D4ED8"),
    spaceBefore=12,
    spaceAfter=7
)

body_style = ParagraphStyle(
    "ReportBody",
    parent=styles["Normal"],
    fontSize=10,
    leading=15
)

story = []

# Report heading
story.append(
    Paragraph("STUDENT PERFORMANCE REPORT", title_style)
)

story.append(
    Paragraph("Academic Result Card", subtitle_style)
)

story.append(Spacer(1, 18))

# Student details
story.append(
    Paragraph("1. Student Details", section_style)
)

student_details = [
    ["Student Name", str(selected_student)],
    ["Overall Result", str(student_result)],
    ["Performance Category", str(performance_category)],
    ["Class Rank", str(student_rank)]
]

details_table = Table(
    student_details,
    colWidths=[55 * mm, 105 * mm]
)

details_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, -1),
     colors.HexColor("#DBEAFE")),
    ("TEXTCOLOR", (0, 0), (0, -1),
     colors.HexColor("#1E3A8A")),
    ("GRID", (0, 0), (-1, -1), 0.5,
     colors.HexColor("#CBD5E1")),
    ("PADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
]))

story.append(details_table)

# Overall result summary
story.append(
    Paragraph("2. Overall Academic Result", section_style)
)

summary_data = [
    ["Total Marks", "Maximum Marks", "Percentage", "Average"],
    [
        f"{total_marks:.1f}",
        f"{maximum_marks}",
        f"{percentage:.1f}%",
        f"{student_average:.1f}/100"
    ]
]

summary_table = Table(
    summary_data,
    colWidths=[40 * mm, 40 * mm, 40 * mm, 40 * mm]
)

summary_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0),
     colors.HexColor("#1D4ED8")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("BACKGROUND", (0, 1), (-1, 1),
     colors.HexColor("#EFF6FF")),
    ("GRID", (0, 0), (-1, -1), 0.5,
     colors.HexColor("#CBD5E1")),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("PADDING", (0, 0), (-1, -1), 8),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
]))

story.append(summary_table)

# Subject-wise marks
story.append(
    Paragraph("3. Subject-wise Result", section_style)
)

subject_rows = [
    ["Subject", "Marks Obtained", "Maximum Marks", "Status"]
]

for subject in subjects:
    marks = student_data[subject]

    subject_status = "Pass" if marks >= 40 else "Needs Improvement"

    subject_rows.append([
        subject,
        f"{marks:.1f}",
        "100",
        subject_status
    ])

subject_table = Table(
    subject_rows,
    colWidths=[42 * mm, 40 * mm, 40 * mm, 38 * mm],
    repeatRows=1
)

subject_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0),
     colors.HexColor("#1D4ED8")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5,
     colors.HexColor("#CBD5E1")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [colors.white, colors.HexColor("#F8FAFC")]),
    ("PADDING", (0, 0), (-1, -1), 7),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
]))

story.append(subject_table)

# Performance analysis
story.append(
    Paragraph("4. Performance Analysis", section_style)
)

story.append(
    Paragraph(
        f"<b>Strongest Subject:</b> "
        f"{escape(str(strongest_subject))} "
        f"with {strongest_marks:.1f}/100 marks.",
        body_style
    )
)

story.append(Spacer(1, 5))

story.append(
    Paragraph(
        f"<b>Subject Needing Focus:</b> "
        f"{escape(str(weakest_subject))} "
        f"with {weakest_marks:.1f}/100 marks.",
        body_style
    )
)

story.append(Spacer(1, 5))

story.append(
    Paragraph(
        f"<b>Performance Category:</b> "
        f"{escape(str(performance_category))}.",
        body_style
    )
)

story.append(Spacer(1, 5))

story.append(
    Paragraph(
        "<b>Result Rule:</b> Overall Pass requires an average "
        "of at least 40 marks. Individual subject status is "
        "shown separately above.",
        body_style
    )
)

# Teacher remarks and improvement suggestions
story.append(
    Paragraph("5. Teacher's Remarks", section_style)
)

story.append(
    Paragraph(escape(teacher_remarks), body_style)
)

story.append(Spacer(1, 8))

if weakest_marks < 40:
    improvement_text = (
        f"Focus first on {escape(str(weakest_subject))}. "
        "Revise the basic concepts, practise questions daily "
        "and review mistakes regularly."
    )
else:
    improvement_text = (
        f"Continue practising all subjects. Maintain your "
        f"performance in {escape(str(strongest_subject))} "
        f"and work towards improving {escape(str(weakest_subject))}."
    )

story.append(
    Paragraph("6. Improvement Suggestions", section_style)
)

story.append(
    Paragraph(improvement_text, body_style)
)

story.append(Spacer(1, 18))

story.append(
    Paragraph(
        "Generated by Student Performance Analyzer",
        subtitle_style
    )
)

# Build PDF
pdf.build(story)

pdf_bytes = pdf_buffer.getvalue()
pdf_buffer.close()


# Create a safe filename for downloads
safe_student_filename = re.sub(
    r"[^A-Za-z0-9_-]+",
    "_",
    str(selected_student)
).strip("_")

if not safe_student_filename:
    safe_student_filename = "student"


# Download report card as PDF
st.download_button(
    label="📥 Download Student Report Card (PDF)",
    data=pdf_bytes,
    file_name=f"{safe_student_filename}_report_card.pdf",
    mime="application/pdf",
    key="download_student_report_pdf"
)

# Keep the existing CSV download option
student_report = student_data.to_frame().T

student_report_csv = student_report.to_csv(index=False)

st.download_button(
    label="📊 Download Student Data (CSV)",
    data=student_report_csv,
    file_name=f"{safe_student_filename}_report.csv",
    mime="text/csv",
    key="download_student_report_csv"
)

st.markdown(
    f"""
<div class="section-card">

<h3>📌 {escape(str(selected_student))}'s Performance</h3>

<div style="display:flex; gap:15px; flex-wrap:wrap;">

<div class="student-box">
<div class="student-title">📐 Maths</div>
<div class="student-value">{student_data["Maths"]}</div>
</div>

<div class="student-box">
<div class="student-title">🔬 Science</div>
<div class="student-value">{student_data["Science"]}</div>
</div>

<div class="student-box">
<div class="student-title">📖 English</div>
<div class="student-value">{student_data["English"]}</div>
</div>

<div class="student-box">
<div class="student-title">💻 Computer</div>
<div class="student-value">{student_data["Computer"]}</div>
</div>

<div class="student-box">
<div class="student-title">📊 Average</div>
<div class="student-value">{student_data["Average"]:.1f}</div>
</div>

<div class="student-box">
<div class="student-title">🏆 Result</div>
<div class="student-value">{student_data["Result"]}</div>
</div>

</div>

</div>
""",
    unsafe_allow_html=True
)

# =========================================
# SELECTED STUDENT CHART
# =========================================

st.markdown(
    """
<div class="section-card">
<h3>📊 Subject-wise Performance</h3>
<p style="color:#64748B;">
Subject-wise marks of the selected student.
</p>
</div>
""",
    unsafe_allow_html=True
)

student_chart = pd.DataFrame(
    {
        "Subject": subjects,
        "Marks": [
            student_data["Maths"],
            student_data["Science"],
            student_data["English"],
            student_data["Computer"]
        ]
    }
)

st.bar_chart(
    student_chart.set_index("Subject")
)

# =========================================
# STUDENT PERFORMANCE INSIGHT
# =========================================

highest_subject = student_data[subjects].idxmax()
lowest_subject = student_data[subjects].idxmin()

highest_marks = student_data[highest_subject]
lowest_marks = student_data[lowest_subject]

st.markdown(
    f"""
<div class="section-card">

<h3>💡 Performance Insight</h3>

<p style="color:#475569; font-size:16px;">
🏆 <b>Strongest Subject:</b> {highest_subject}
with <b>{highest_marks}</b> marks
</p>

<p style="color:#475569; font-size:16px;">
⚠️ <b>Needs Improvement:</b> {lowest_subject}
with <b>{lowest_marks}</b> marks
</p>

<p style="color:#475569; font-size:16px;">
📊 <b>Overall Average:</b> {student_data["Average"]:.1f}
</p>

</div>
""",
    unsafe_allow_html=True
)

# =========================================
# SUBJECT COMPARISON
# =========================================

st.subheader("📚 Subject Comparison")

selected_subject = st.selectbox(
    "Select a subject",
    subjects
)

class_average = data[selected_subject].mean()
student_marks = student_data[selected_subject]

difference = student_marks - class_average

st.markdown(
    f"""
<div class="section-card">

<h3>📊 {escape(str(selected_student))} vs Class Average</h3>

<p style="color:#475569; font-size:16px;">
🎓 <b>Student Marks:</b> {student_marks:.1f}
</p>

<p style="color:#475569; font-size:16px;">
🏫 <b>Class Average:</b> {class_average:.1f}
</p>

<p style="color:#475569; font-size:16px;">
📈 <b>Difference:</b> {difference:+.1f} marks
</p>

</div>
""",
    unsafe_allow_html=True
)

# =========================================
# PERFORMANCE SUMMARY
# =========================================

if student_data["Average"] >= 80:
    performance_message = "🌟 Excellent performance!"
elif student_data["Average"] >= 60:
    performance_message = "👍 Good performance!"
elif student_data["Average"] >= 40:
    performance_message = "📚 Average performance. There is room for improvement."
else:
    performance_message = "⚠️ Performance needs improvement."

st.markdown(
    f"""
<div class="section-card">

<h3>📝 Performance Summary</h3>

<p style="font-size:18px; color:#172554; font-weight:600;">
{performance_message}
</p>

<p style="color:#64748B;">
{escape(str(selected_student))} scored an overall average of
<b>{student_data["Average"]:.1f}</b> marks.
</p>

</div>
""",
    unsafe_allow_html=True
)


# =========================================
# STEP 9: STUDENTS NEEDING IMPROVEMENT
# =========================================

st.subheader("⚠️ Students Needing Improvement")

# Find students scoring below 40 in any subject
weak_students = data[
    data[subjects].lt(40).any(axis=1)
].copy()

if weak_students.empty:

    st.success(
        "🎉 No students have marks below 40 in any subject!"
    )

else:

    # Identify subjects that need improvement
    weak_students["Subjects Below 40"] = weak_students.apply(
        lambda row: ", ".join(
            subject for subject in subjects
            if row[subject] < 40
        ),
        axis=1
    )

    st.warning(
        f"{len(weak_students)} student(s) need attention "
        "in one or more subjects."
    )

    st.dataframe(
        weak_students[
            [
                "Name",
                *subjects,
                "Subjects Below 40",
                "Average",
                "Result"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

# =========================================
# TOP 3 STUDENTS CARDS
# =========================================

st.subheader("🏆 Top 3 Students")

top_columns = st.columns(len(top_3))

for i, (_, row) in enumerate(top_3.iterrows()):

    with top_columns[i]:

        st.markdown(
            """
            <div class="section-card">
            <h3>🏆 Top Performer</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric(
            label=f"Rank {int(row['Rank'])}",
            value=row["Name"],
            delta=f"{row['Average']:.1f} average marks"
        )


# =========================================
# STUDENT DETAILS
# =========================================

st.subheader("📋 Student Details")

st.markdown(
    """
<div class="section-card">
<h3>📚 Student Performance Records</h3>
<p style="color:#64748B;">
Detailed marks, average score and result of each student.
</p>
</div>
""",
    unsafe_allow_html=True
)


# =========================================
# ADVANCED STUDENT FILTERS
# =========================================

st.subheader("🔎 Advanced Student Filters")

col1, col2 = st.columns(2)

with col1:
    result_filter = st.selectbox(
        "Filter by Result",
        ["All", "Pass", "Fail"]
    )

with col2:
    min_average = st.slider(
        "Minimum Average Marks",
        min_value=0,
        max_value=100,
        value=0
    )

filtered_data = data.copy()

if result_filter != "All":
    filtered_data = filtered_data[
        filtered_data["Result"] == result_filter
    ]

filtered_data = filtered_data[
    filtered_data["Average"] >= min_average
]

st.write(
    f"Showing {len(filtered_data)} "
    f"out of {len(data)} students"
)

st.dataframe(
    filtered_data,
    use_container_width=True
)

# =========================================
# DOWNLOAD FILTERED DATA
# =========================================

filtered_csv = filtered_data.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Students",
    data=filtered_csv,
    file_name="filtered_students.csv",
    mime="text/csv",
    key="download_filtered"
)


# =========================================
# STEP 7: SUBJECT-WISE PERFORMANCE INSIGHTS
# =========================================

subject_averages = data[subjects].mean()

highest_subject = subject_averages.idxmax()
highest_average = subject_averages.max()

lowest_subject = subject_averages.idxmin()
lowest_average = subject_averages.min()

st.subheader("📚 Class Performance by Subject")

st.bar_chart(subject_averages)

# Show average marks of every subject
subject_summary = pd.DataFrame({
    "Subject": subject_averages.index,
    "Class Average": subject_averages.values.round(1)
})

st.dataframe(
    subject_summary,
    use_container_width=True,
    hide_index=True
)

# Best and weakest subject insights
insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown(
        f"""
        <div class="section-card">
            <h3>🏆 Best Performing Subject</h3>
            <p>
                <b>{highest_subject}</b> has the highest
                class average of <b>{highest_average:.1f}</b> marks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with insight_col2:
    st.markdown(
        f"""
        <div class="section-card">
            <h3>📌 Subject Needing Focus</h3>
            <p>
                <b>{lowest_subject}</b> has the lowest
                class average of <b>{lowest_average:.1f}</b> marks.
                Students may need more practice in this subject.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================
# DOWNLOAD DATA
# =========================================

csv_data = data.to_csv(index=False)

st.download_button(
    label="📥 Download Student Report",
    data=csv_data,
    file_name="student_performance_report.csv",
    mime="text/csv"
)


# =========================================
# CHARTS
# =========================================

st.subheader("📈 Performance Analysis")

chart_col1, chart_col2 = st.columns(2)


# =========================================
# SUBJECT-WISE CHART
# =========================================

with chart_col1:

    st.markdown(
        """
<div class="section-card">
<h3>📊 Subject-wise Performance</h3>
<p style="color:#64748B;">
Average marks obtained in each subject.
</p>
</div>
""",
        unsafe_allow_html=True
    )

    subject_averages = data[subjects].mean()

    st.bar_chart(
        subject_averages
    )


# =========================================
# STUDENT PERFORMANCE CHART
# =========================================

with chart_col2:

    st.markdown(
        """
<div class="section-card">
<h3>📈 Student Performance</h3>
<p style="color:#64748B;">
Average marks of individual students.
</p>
</div>
""",
        unsafe_allow_html=True
    )

    chart_data = data.set_index("Name")["Average"]

    st.bar_chart(
        chart_data
    )


# =========================================
# PASS / FAIL SUMMARY
# =========================================

st.subheader("✅ Pass / Fail Analysis")


# Summary cards

result_col1, result_col2 = st.columns(2)


# Pass Card

with result_col1:

    st.markdown(
        f"""
<div class="result-card pass-card">
<div class="result-title">✅ Students Passed</div>
<div class="result-number pass-text">{passed_students}</div>
</div>
""",
        unsafe_allow_html=True
    )


# Fail Card

with result_col2:

    st.markdown(
        f"""
<div class="result-card fail-card">
<div class="result-title">❌ Students Failed</div>
<div class="result-number fail-text">{failed_students}</div>
</div>
""",
        unsafe_allow_html=True
    )


# Pass Fail Chart

st.markdown(
    """
<div class="section-card">
<h3>📊 Result Distribution</h3>
<p style="color:#64748B;">
Comparison between passed and failed students.
</p>
</div>
""",
    unsafe_allow_html=True
)

result_count = data["Result"].value_counts()

st.bar_chart(
    result_count
)

# =========================================
# REFRESH ANALYZER
# =========================================

st.markdown("---")

if st.button("🔄 Rerun Analyzer"):

    st.rerun()