"""
PFAD Impact Analysis Dashboard Page

Business-focused analysis showing:
- Which factors drove PFAD price changes
- Why these factors affected prices  
- Quantified impact of each parameter
- Clear procurement insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from analytics.impact_analyzer import PFADImpactAnalyzer
except:
    st.error("Impact analyzer not found. Please ensure the analytics module is properly installed.")

def show_impact_analysis_page(data):
    """Main impact analysis page"""
    
    st.markdown("# 🔍 PFAD Impact Analysis")
    st.markdown("### Understanding What Drives Your Palm Oil Prices")
    
    if data is None or len(data) < 100:
        st.warning("⚠️ Need more data for comprehensive impact analysis")
        return
    
    # Initialize analyzer
    analyzer = PFADImpactAnalyzer()
    
    # Run analysis
    with st.spinner("🔄 Analyzing historical price impacts..."):
        try:
            results = analyzer.analyze_historical_impact(data)
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
            return
    
    # Display results in business-friendly format
    show_executive_summary(results)
    show_key_drivers_analysis(results)
    show_correlation_insights(results)
    show_time_period_analysis(results)
    show_procurement_recommendations(results)

def show_executive_summary(results):
    """Executive summary section"""
    
    st.markdown("## 📊 Executive Summary")
    
    if 'business_insights' in results and 'executive_summary' in results['business_insights']:
        insights = results['business_insights']['executive_summary']
        
        if insights:
            for insight in insights:
                st.markdown(f"• **{insight}**")
        else:
            st.info("Executive insights will appear here after analysis")
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'regression' in results and 'r_squared' in results['regression']:
            r_squared = results['regression']['r_squared'] * 100
            st.metric("Model Accuracy", f"{r_squared:.1f}%", "of price movements explained")
        else:
            st.metric("Model Accuracy", "Calculating...", "")
    
    with col2:
        if 'correlations' in results:
            strong_factors = len([f for f in results['correlations'].values() 
                                if abs(f.get('correlation', 0)) > 0.5])
            st.metric("Strong Drivers", f"{strong_factors}", "factors with >50% correlation")
        else:
            st.metric("Strong Drivers", "0", "")
    
    with col3:
        if 'period_analysis' in results:
            years_analyzed = len(results['period_analysis'])
            st.metric("Time Period", f"{years_analyzed} years", "of historical data")
        else:
            st.metric("Time Period", "0", "")
    
    with col4:
        if 'volatility_analysis' in results:
            volatility = results['volatility_analysis'].get('average_volatility', 0)
            st.metric("Average Volatility", f"{volatility:.1f}%", "daily price fluctuation")
        else:
            st.metric("Average Volatility", "0%", "")

def show_key_drivers_analysis(results):
    """Key price drivers section"""
    
    st.markdown("## 🎯 Key Price Drivers")
    
    if 'correlations' not in results:
        st.info("Correlation analysis in progress...")
        return
    
    # Create correlation chart
    correlations = results['correlations']
    
    # Prepare data for visualization
    factors = []
    correlations_values = []
    strengths = []
    
    for factor, data in correlations.items():
        factors.append(factor.replace('_', ' '))
        correlations_values.append(data['correlation'])
        strengths.append(data['strength'])
    
    # Sort by absolute correlation
    sorted_data = sorted(zip(factors, correlations_values, strengths), 
                        key=lambda x: abs(x[1]), reverse=True)
    
    if sorted_data:
        factors_sorted, corr_sorted, strength_sorted = zip(*sorted_data)
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        # Color code by strength
        colors = []
        for corr in corr_sorted:
            if abs(corr) > 0.7:
                colors.append('#FF4444')  # Red for very strong
            elif abs(corr) > 0.5:
                colors.append('#FF8800')  # Orange for strong
            elif abs(corr) > 0.3:
                colors.append('#FFAA00')  # Yellow for moderate
            else:
                colors.append('#888888')  # Gray for weak
        
        fig.add_trace(go.Bar(
            y=factors_sorted,
            x=corr_sorted,
            orientation='h',
            marker_color=colors,
            text=[f"{corr:.3f}" for corr in corr_sorted],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Impact of Market Parameters on PFAD Prices",
            xaxis_title="Correlation Coefficient",
            yaxis_title="Market Parameters",
            template='plotly_white',
            height=600,
            showlegend=False
        )
        
        fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="black")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Explanation
        st.markdown("### 📝 What This Means:")
        st.markdown("• **Red bars**: Very strong impact (>70% correlation)")
        st.markdown("• **Orange bars**: Strong impact (50-70% correlation)")  
        st.markdown("• **Yellow bars**: Moderate impact (30-50% correlation)")
        st.markdown("• **Positive values**: Factor increases → PFAD price increases")
        st.markdown("• **Negative values**: Factor increases → PFAD price decreases")

def show_correlation_insights(results):
    """Detailed correlation insights"""
    
    st.markdown("## 🔬 Detailed Impact Analysis")
    
    if 'correlations' not in results:
        return
    
    correlations = results['correlations']
    
    # Top 5 factors analysis
    top_factors = sorted(correlations.items(), 
                        key=lambda x: abs(x[1]['correlation']), 
                        reverse=True)[:5]
    
    for i, (factor, data) in enumerate(top_factors, 1):
        with st.expander(f"{i}. {factor.replace('_', ' ')} - {data['strength']} Impact ({data['correlation']:.3f})"):
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Business Explanation:**")
                st.markdown(f"{data['explanation']}")
                
                st.markdown(f"**Impact Direction:** {data['direction']}")
                st.markdown(f"**Correlation Strength:** {data['strength']} ({abs(data['correlation']):.3f})")
                
                # Business interpretation
                if abs(data['correlation']) > 0.7:
                    interpretation = "🔴 **Critical Factor** - Monitor daily for procurement decisions"
                elif abs(data['correlation']) > 0.5:
                    interpretation = "🟠 **Important Factor** - Include in weekly planning"
                elif abs(data['correlation']) > 0.3:
                    interpretation = "🟡 **Supporting Factor** - Consider in monthly analysis"
                else:
                    interpretation = "⚪ **Minor Factor** - Low priority for forecasting"
                
                st.markdown(interpretation)
            
            with col2:
                # Mini correlation visualization
                mini_fig = go.Figure()
                mini_fig.add_trace(go.Bar(
                    x=[factor.replace('_', ' ')],
                    y=[data['correlation']],
                    marker_color='#1f77b4' if data['correlation'] > 0 else '#ff7f0e'
                ))
                mini_fig.update_layout(
                    height=200,
                    showlegend=False,
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(mini_fig, use_container_width=True)

def show_time_period_analysis(results):
    """Time period analysis"""
    
    st.markdown("## 📅 Historical Period Analysis")
    
    if 'period_analysis' not in results:
        st.info("Time period analysis not available")
        return
    
    period_data = results['period_analysis']
    
    if not period_data:
        st.info("Insufficient data for period analysis")
        return
    
    # Convert to DataFrame for visualization
    df_periods = pd.DataFrame.from_dict(period_data, orient='index')
    df_periods.index.name = 'Year'
    df_periods = df_periods.reset_index()
    
    # Create time series chart
    fig = go.Figure()
    
    # Average price over time
    fig.add_trace(go.Scatter(
        x=df_periods['Year'],
        y=df_periods['avg_price'],
        mode='lines+markers',
        name='Average PFAD Price',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="PFAD Price Trends by Year",
        xaxis_title="Year",
        yaxis_title="Average PFAD Price (₹)",
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Year-by-year analysis table
    st.markdown("### 📊 Year-by-Year Performance")
    
    # Format the dataframe for display
    display_df = df_periods.copy()
    display_df['avg_price'] = display_df['avg_price'].apply(lambda x: f"₹{x:,.0f}")
    display_df['min_price'] = display_df['min_price'].apply(lambda x: f"₹{x:,.0f}")
    display_df['max_price'] = display_df['max_price'].apply(lambda x: f"₹{x:,.0f}")
    display_df['price_change_percent'] = display_df['price_change_percent'].apply(lambda x: f"{x:+.1f}%")
    display_df['volatility'] = display_df['volatility'].apply(lambda x: f"{x:.1f}%")
    
    display_df.columns = ['Year', 'Avg Price', 'Min Price', 'Max Price', 'Annual Change', 'Volatility']
    
    st.dataframe(display_df, use_container_width=True)

def show_procurement_recommendations(results):
    """Procurement recommendations based on analysis"""
    
    st.markdown("## 💼 Procurement Strategy Recommendations")
    
    if 'business_insights' not in results:
        st.info("Generating recommendations...")
        return
    
    insights = results['business_insights']
    
    # Key recommendations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Key Monitoring Factors")
        if 'key_drivers' in insights:
            for driver in insights['key_drivers']:
                st.markdown(f"• {driver}")
        
        st.markdown("### 📋 Procurement Actions")
        if 'procurement_implications' in insights:
            for implication in insights['procurement_implications']:
                st.markdown(f"• {implication}")
    
    with col2:
        st.markdown("### ⚠️ Risk Factors")
        if 'risk_factors' in insights:
            for risk in insights['risk_factors']:
                st.markdown(f"• {risk}")
        
        st.markdown("### 🎯 Success Metrics")
        st.markdown("• Track correlation accuracy monthly")
        st.markdown("• Monitor forecast vs actual price variance")
        st.markdown("• Measure procurement cost savings")
        st.markdown("• Assess inventory optimization benefits")
    
    # Overall strategy summary
    st.markdown("### 📈 Strategic Summary")
    
    if 'correlations' in results:
        # Find the strongest factor
        strongest_factor = max(results['correlations'].items(), 
                             key=lambda x: abs(x[1]['correlation']))
        
        st.success(f"""
        **Primary Strategy**: Focus on monitoring {strongest_factor[0].replace('_', ' ')} 
        as your primary price indicator with {abs(strongest_factor[1]['correlation']):.1%} correlation.
        
        **Procurement Timing**: Use this factor for optimal buying decisions and inventory planning.
        
        **Risk Management**: Implement hedging strategies when this factor shows high volatility.
        """)
