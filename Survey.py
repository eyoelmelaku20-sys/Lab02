# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import csv # The 'csv' module is used to write rows to data.csv safely.
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What activity did you spend time on? (e.g., Sleep, Studying, Gaming)")
    value_input = st.text_input("About how many hours per week did you spend on it? (e.g., 7.5)")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        category = category_input.strip().title()
        value_text = value_input.strip()

        # VALIDATE: the category must not be blank, and the value must be a
        # number between 0 and 168 (the number of hours in a week).
        try:
            hours = float(value_text)
        except ValueError:
            hours = None

        if category == "":
            st.error("Please enter an activity before submitting.")
        elif hours is None or hours < 0 or hours > 168:
            st.error("Please enter the hours as a number between 0 and 168 (e.g., 7.5).")
        else:
            # Format the number for CSV storage (7.0 -> "7", 7.5 -> "7.5").
            value_for_csv = f"{hours:g}"

            # If the file is new/empty, write the header first. If the last line
            # of the file has no newline, add one so rows never run together.
            needs_header = (not os.path.exists("data.csv")) or os.path.getsize("data.csv") == 0
            needs_newline = False
            if not needs_header:
                with open("data.csv", "rb") as check_file:
                    check_file.seek(-1, os.SEEK_END)
                    needs_newline = check_file.read(1) not in (b"\n", b"\r")

            # Append the new row to data.csv (append mode: 'a').
            with open("data.csv", "a", newline="") as csv_file:
                if needs_newline:
                    csv_file.write("\n")
                writer = csv.writer(csv_file)
                if needs_header:
                    writer.writerow(["Category", "Value"])
                writer.writerow([category, value_for_csv])

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category}, **Value:** {value_for_csv} hours per week")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")