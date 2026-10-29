# Student Performance Analyzer

A Python-based web application that analyzes student academic performance using an interactive Streamlit dashboard.

## Features

- Upload student marks through CSV files
- Validate student data and marks
- Calculate averages, results, performance categories, and ranks
- Display class performance statistics and charts
- Generate individual student report cards in PDF format
- Download individual, filtered, and complete reports as CSV files
- Compare student marks with class averages
- Identify students who need improvement
- Filter students by result and minimum average
- Responsive dashboard styling with custom HTML and CSS

## Technologies Used

- Python
- Streamlit
- Pandas
- HTML and CSS
- ReportLab
- CSV data processing

## Installation

1. Install Python on your computer.
2. Clone or download this repository.
3. Open a terminal in the project folder.
4. Install the required libraries:

   `pip install -r requirements.txt`

## Run the Application

Run the following command:

`streamlit run app.py`

Replace `app.py` with your actual Python filename if it is different.

## Input Data

The application accepts a CSV file containing these required columns:

`Name, Maths, Science, English, Computer`

Subject marks must be numeric values between 0 and 100. If no file is uploaded, the application looks for a local file named `students.csv`.

## Learning Outcomes

This project helped me practise Python programming, data analysis, interactive dashboard development, data visualization, input validation, and PDF/CSV report generation.

## Future Improvements

- Database integration
- Student ID support
- Customizable subjects and grading rules
- User authentication
- Predictive academic analytics