"""
PFAD Professional Analytics - Working Version
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Page configuration
st.set_page_config(
    page_title="PFAD Professional Analytics",
    page_icon="🌴",
    layout="wide"
)

# Header
st.markdown("""
# 🌴 PFAD Professional Procurement Analytics
## Enterprise-Grade Solution for Soap Manufacturing Industry
""")

# Sidebar
st.sidebar.markdown("## 🎛️ System Control Panel")

# Data upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Bloomberg PFAD Data",
    type=['xlsx', 'xls', 'csv'],
    help="Upload your market data"
)

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        
        st.success(f"✅ Data loaded: {len(data)} records")
        
        # Show data preview
        st.markdown("## 📊 Data Preview")
        st.dataframe(data.head(), use_container_width=True)
        
        # Basic price chart
        if 'PFAD_Rate' in data.columns and 'Date' in data.columns:
            st.markdown("## 📈 PFAD Price Trends")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pd.to_datetime(data['Date']),
                y=data['PFAD_Rate'],
                mode='lines',
                name='PFAD Rate',
                line=dict(color='#667eea', width=2)
            ))
            
            fig.update_layout(
                title="PFAD Price Analysis",
                xaxis_title="Date",
                yaxis_title="Price (₹/ton)",
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Basic statistics
            current_price = data['PFAD_Rate'].iloc[-1]
            price_change = data['PFAD_Rate'].pct_change().iloc[-1] * 100
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Price", f"₹{current_price:,.0f}", f"{price_change:+.2f}%")
            
            with col2:
                st.metric("Average Price", f"₹{data['PFAD_Rate'].mean():,.0f}")
            
            with col3:
                st.metric("Price Range", f"₹{data['PFAD_Rate'].max() - data['PFAD_Rate'].min():,.0f}")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

else:
    # Welcome screen
    st.markdown("""
    ## 🎉 Welcome to PFAD Professional Analytics
    
    ### 📁 Getting Started
    1. Upload your Bloomberg PFAD data using the sidebar
    2. View price trends and analysis
    3. Get procurement insights
    
    ### 📊 Expected Data Format
    - `Date` - Trading dates
    - `PFAD_Rate` - PFAD prices
    - Other market parameters
    """)
    
    # Sample data
    sample_data = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=5),
        'PFAD_Rate': [82000, 82500, 81800, 83200, 82700]
    })
    
    st.markdown("### 📋 Sample Data Structure")
    st.dataframe(sample_data, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:** ✅ Ready")
