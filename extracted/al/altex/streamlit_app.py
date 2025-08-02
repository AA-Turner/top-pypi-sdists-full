"""
Altex Demo App

A simple showcase of the Altex library for creating charts with an express API.
Run with: streamlit run streamlit_app.py
"""

import numpy as np
import pandas as pd
import streamlit as st

import altex

# Page config
st.set_page_config(
    page_title="Altex Demo",
    page_icon="👸",
    layout="centered",
)

# Header
st.title("Altex 👸")
st.markdown("""
**Altex** is a simple wrapper on top of Altair to make charts with an express API. 
Perfect for quick data visualization in Streamlit!

[![GitHub](https://img.shields.io/badge/GitHub-altex-blue?logo=github)](https://github.com/arnaudmiribel/altex)
[![PyPI](https://img.shields.io/badge/PyPI-altex-blue?logo=pypi)](https://pypi.org/project/altex/)
""")

# Create sample data for demos
np.random.seed(42)
sample_data = pd.DataFrame(
    {
        "month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        "revenue": [
            850,
            920,
            1100,
            1250,
            1400,
            1300,
            1450,
            1600,
            1550,
            1700,
            1800,
            1900,
        ],
        "expenses": [650, 700, 800, 900, 950, 900, 1000, 1100, 1050, 1200, 1250, 1300],
        "category": [
            "Q1",
            "Q1",
            "Q1",
            "Q2",
            "Q2",
            "Q2",
            "Q3",
            "Q3",
            "Q3",
            "Q4",
            "Q4",
            "Q4",
        ],
    }
)

# Stock data for time series
stocks = altex.get_stocks_data()

# Chart demonstrations
st.header("Chart examples")

st.subheader("Line chart")
altex.line_chart(
    data=stocks.query("symbol == 'AAPL'").head(30),
    x="date",
    y="price",
    title="Apple stock price",
    color="symbol",
)

with st.expander("View code"):
    st.code(
        """
altex.line_chart(
    data=stocks.query("symbol == 'AAPL'"),
    x='date',
    y='price',
    title='Apple stock price'
)""",
        language="python",
    )

st.subheader("Bar chart")
altex.bar_chart(
    data=sample_data,
    x="month",
    y="revenue",
    color="category",
    title="Monthly revenue by quarter",
)

with st.expander("View code"):
    st.code(
        """
altex.bar_chart(
    data=sample_data,
    x='month',
    y='revenue',
    color='category',
    title='Monthly revenue by quarter'
)""",
        language="python",
    )

st.subheader("Scatter plot")
altex.scatter_chart(
    data=sample_data,
    x="expenses",
    y="revenue",
    color="category",
    title="Revenue vs expenses",
    opacity=0.8,
)

with st.expander("View code"):
    st.code(
        """
altex.scatter_chart(
    data=sample_data,
    x='expenses',
    y='revenue',
    color='category',
    title='Revenue vs expenses',
    opacity=0.8
)""",
        language="python",
    )

st.subheader("Area chart")
multi_stocks = stocks.head(60)
altex.area_chart(
    data=multi_stocks,
    x="date",
    y="price",
    color="symbol",
    title="Stock prices over time",
)

with st.expander("View code"):
    st.code(
        """
altex.area_chart(
    data=stocks,
    x='date',
    y='price',
    color='symbol',
    title='Stock prices over time'
)""",
        language="python",
    )

# Sparklines section
st.header("Sparklines for dashboards")

# Create metrics with sparklines
aapl_data = stocks.query("symbol == 'AAPL'").head(20)
goog_data = stocks.query("symbol == 'GOOG'").head(20)
msft_data = stocks.query("symbol == 'MSFT'").head(20)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AAPL", f"${aapl_data['price'].iloc[-1]:.2f}", "+2.3%")
    altex.sparkline_chart(data=aapl_data, x="date", y="price", height=60)

with col2:
    st.metric("GOOG", f"${goog_data['price'].iloc[-1]:.2f}", "+1.8%")
    altex.sparkline_chart(data=goog_data, x="date", y="price", height=60)

with col3:
    st.metric("MSFT", f"${msft_data['price'].iloc[-1]:.2f}", "-0.5%")
    altex.sparkline_chart(data=msft_data, x="date", y="price", height=60)

with st.expander("View sparkline code"):
    st.code(
        """
st.metric("AAPL", f"${price:.2f}", "+2.3%")
altex.sparkline_chart(
    data=aapl_data,
    x='date',
    y='price',
    height=60
)""",
        language="python",
    )

# Quick start section
st.header("Quick start")

st.code(
    """
# Install
pip install altex

# Usage
import altex
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)]
})

# Create charts with express API
altex.line_chart(data=data, x='x', y='y', title='My chart')
altex.bar_chart(data=data, x='x', y='y')
altex.scatter_chart(data=data, x='x', y='y', opacity=0.7)

# Use built-in sample data
stocks = altex.get_stocks_data()
altex.line_chart(data=stocks, x='date', y='price', color='symbol')
""",
    language="python",
)

# Features
st.header("Features")

st.markdown("""
**Chart types:**
- `line_chart()` - Line charts
- `bar_chart()` - Bar charts  
- `area_chart()` - Area charts
- `scatter_chart()` - Scatter plots
- `hist_chart()` - Histograms

**Sparklines:**
- `sparkline_chart()` - Mini line charts
- `sparkbar_chart()` - Mini bar charts
- `sparkarea_chart()` - Mini area charts
- Perfect for dashboards
""")

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: #666;'>
    Built with ❤️ using Altex, Altair, and Streamlit
</div>
""",
    unsafe_allow_html=True,
)
