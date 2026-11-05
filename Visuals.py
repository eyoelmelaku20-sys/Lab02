# This creates the page for displaying data visualizations.

import json

import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
st.header("Part 1: Graphs from data.json")

# Load the JSON file into a dictionary.
with open("data.json", "r") as f:
    data = json.load(f)

# ---------------------------------------------------------------------------
# STATIC VISUALIZATION (advanced element: st.pyplot / Matplotlib)
# Depends only on data.json and never changes from user input.
# ---------------------------------------------------------------------------
st.subheader("Static: Average Hours per Week by Activity")

labels = [point["label"] for point in data["data_points"]]
values = [point["value"] for point in data["data_points"]]

fig, ax = plt.subplots()
ax.bar(labels, values, color="steelblue")
ax.set_title(data["chart_title"])
ax.set_xlabel("Activity")
ax.set_ylabel("Hours per Week")
plt.xticks(rotation=30)
st.pyplot(fig)

st.divider()

# ---------------------------------------------------------------------------
# DYNAMIC VISUALIZATION (Altair line chart + widgets + session state)
# The data stays the same; the chart changes with user input.
# ---------------------------------------------------------------------------
st.subheader("Dynamic: Weekly Trend Explorer")

weeks = data["weekly_log"]["weeks"]
activities = data["weekly_log"]["activities"]

# Initialize session state values once, so they persist across reruns.
if "selected_activities" not in st.session_state:
    st.session_state.selected_activities = [list(activities.keys())[0]]
if "num_weeks" not in st.session_state:
    st.session_state.num_weeks = len(weeks)


def reset_view():
    """Callback that resets the saved state back to its defaults."""
    st.session_state.selected_activities = [list(activities.keys())[0]]
    st.session_state.num_weeks = len(weeks)


# User input widgets. Their values are stored in session state via 'key'.
st.multiselect(
    "Choose activities to display:",
    options=list(activities.keys()),
    key="selected_activities",
)
st.slider(
    "Number of weeks to show:",
    min_value=2,
    max_value=len(weeks),
    key="num_weeks",
)
st.button("Reset view", on_click=reset_view)

# Build the chart from the current session state values.
if st.session_state.selected_activities:
    n = st.session_state.num_weeks
    rows = []
    for name in st.session_state.selected_activities:
        for week, hours in zip(weeks[:n], activities[name][:n]):
            rows.append({"Week": week, "Activity": name, "Hours": hours})
    df = pd.DataFrame(rows)

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Week:N", sort=weeks, title="Week"),
            y=alt.Y("Hours:Q", title="Hours"),
            color=alt.Color("Activity:N", title="Activity"),
            tooltip=["Week", "Activity", "Hours"],
        )
        .properties(title="Weekly Hours by Activity")
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Select at least one activity to see the chart.")


# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Part 2: Graphs from data.csv")

# Load the survey data collected on the Survey page.
try:
    survey_df = pd.read_csv("data.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    survey_df = pd.DataFrame(columns=["Category", "Value"])

# Make sure the Value column is numeric and drop any unusable rows.
survey_df["Value"] = pd.to_numeric(survey_df["Value"], errors="coerce")
survey_df = survey_df.dropna(subset=["Category", "Value"])

if survey_df.empty:
    st.info("There is no survey data yet. Add some on the Survey page, then come back!")
else:
    # -----------------------------------------------------------------------
    # STATIC VISUALIZATION (advanced element: st.pyplot / Matplotlib pie chart)
    # Depends only on data.csv; no user input on this page changes it.
    # -----------------------------------------------------------------------
    st.subheader("Static: Share of Average Weekly Hours by Activity")

    average_by_category = survey_df.groupby("Category")["Value"].mean()

    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(
        average_by_category.values,
        labels=average_by_category.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    ax_pie.set_title("Share of Average Weekly Hours by Activity")
    ax_pie.axis("equal")  # keeps the pie circular
    st.pyplot(fig_pie)

    st.divider()

    # -----------------------------------------------------------------------
    # DYNAMIC VISUALIZATION (Altair bar chart + widgets + session state)
    # The data stays the same; the chart changes with user input.
    # -----------------------------------------------------------------------
    st.subheader("Dynamic: Activity Explorer")

    num_categories = survey_df["Category"].nunique()

    # Initialize session state values once, so they persist across reruns.
    if "csv_aggregate" not in st.session_state:
        st.session_state.csv_aggregate = "Average"
    if "csv_top_n" not in st.session_state:
        st.session_state.csv_top_n = num_categories
    # Keep the saved slider value valid if the data has changed since last time.
    st.session_state.csv_top_n = max(1, min(st.session_state.csv_top_n, num_categories))

    def reset_csv_view():
        """Callback that resets the saved widget state back to its defaults."""
        st.session_state.csv_aggregate = "Average"
        st.session_state.csv_top_n = num_categories

    # User input widgets. Their values are stored in session state via 'key'.
    st.radio(
        "How should the hours be combined?",
        options=["Average", "Total"],
        key="csv_aggregate",
        horizontal=True,
    )
    if num_categories >= 2:
        st.slider(
            "Number of activities to show (highest hours first):",
            min_value=1,
            max_value=num_categories,
            key="csv_top_n",
        )
    st.button("Reset view", on_click=reset_csv_view, key="csv_reset")

    # Build the chart data from the current session state values.
    method = "mean" if st.session_state.csv_aggregate == "Average" else "sum"
    summary_df = (
        survey_df.groupby("Category")["Value"]
        .agg(method)
        .sort_values(ascending=False)
        .head(st.session_state.csv_top_n)
        .reset_index()
        .rename(columns={"Value": "Hours"})
    )

    bar_chart = (
        alt.Chart(summary_df)
        .mark_bar()
        .encode(
            x=alt.X("Category:N", sort="-y", title="Activity"),
            y=alt.Y("Hours:Q", title=f"{st.session_state.csv_aggregate} Hours per Week"),
            color=alt.Color("Category:N", legend=None),
            tooltip=["Category", alt.Tooltip("Hours:Q", format=".1f")],
        )
        .properties(title=f"{st.session_state.csv_aggregate} Hours per Week by Activity")
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # -----------------------------------------------------------------------
    # EXTRA CREDIT: st.metric() summary statistics that update with the chart.
    # Session state remembers the previous values so we can show the change.
    # -----------------------------------------------------------------------
    current_mean = round(float(summary_df["Hours"].mean()), 2)
    current_median = round(float(summary_df["Hours"].median()), 2)
    current_stats = (current_mean, current_median)

    if "csv_stats_current" not in st.session_state:
        st.session_state.csv_stats_current = current_stats
        st.session_state.csv_stats_previous = None
    elif st.session_state.csv_stats_current != current_stats:
        st.session_state.csv_stats_previous = st.session_state.csv_stats_current
        st.session_state.csv_stats_current = current_stats

    previous_stats = st.session_state.csv_stats_previous
    mean_delta = None if previous_stats is None else round(current_mean - previous_stats[0], 2)
    median_delta = None if previous_stats is None else round(current_median - previous_stats[1], 2)

    st.caption("Summary statistics for the bars shown above (change is compared to your previous view):")
    col_mean, col_median = st.columns(2)
    col_mean.metric("Mean hours", current_mean, delta=mean_delta)
    col_median.metric("Median hours", current_median, delta=median_delta)

