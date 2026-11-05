# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Homepage",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to My Data Dashboard! 📊")
st.caption("Created by Eyoel Melaku")

# INTRODUCTORY TEXT
st.write("""
This application collects and visualizes data about **how I spend my time each week**,
from sleeping and studying to exercising and gaming.
You can navigate to the different pages using the sidebar on the left.

### How to use this app:
- **Survey Page**: Go here to input new data into our CSV file.
- **Visuals Page**: Go here to see the data visualized in different graphs.
  - A **static** bar chart shows my average hours per week for each activity.
  - A **dynamic** line chart lets you pick activities and how many weeks to display.
  - Part 2 adds charts built from the survey data in `data.csv`: a **static** pie chart of
    each activity's share of average weekly hours, and a **dynamic** bar chart where you choose
    average vs. total hours and how many activities to show, with live mean and median metrics.

This project is part of CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
# st.image("images/welcome_image.png")
