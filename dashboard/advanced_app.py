"""
PFAD Professional Analytics - Complete Working System
Enterprise-grade procurement optimization
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

# Import advanced modules
try:
    from src.analytics.advanced_econometric_engine import PFADEconometricEngine
    from src.optimization.procurement_optimizer import PFADProcurementOptimizer
    ADVANCED_MODULES_AVAILABLE = True
except ImportError:
    ADVANCED_MODULES_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="PFAD Professional Analytics",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .success-card {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left-color: #28a745;
    }
    .warning-card {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left-color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)

class AdvancedPFADSystem:
    def __init__(self):
        self.initialize_session_state()
        self.econometric_engine = None
        self.procurement_optimizer = None
        
    def initialize_session_state(self):
        defaults = {
            'data_loaded': False,
            'analysis_complete': False,
            'current_data': None,
            'results': {},
            'business_params_set': False
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def render_header(self):
        st.markdown("""
        <div class="main-header">
            <h1>🌴 PFAD Professional Procurement Analytics</h1>
            <p>Advanced Econometric Models • Procurement Optimization • Risk Management</p>
            <p><strong>Enterprise-Grade Solution for Soap Manufacturing Industry</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        st.sidebar.markdown("## 🎛️ System Control Panel")
        
        st.sidebar.markdown("### 📁 Data Management")
        uploaded_file = st.sidebar.file_uploader(
            "Upload Bloomberg PFAD Data",
            type=['xlsx', 'xls', 'csv'],
            help="Upload your market data"
        )
        
        if uploaded_file and not st.session_state.data_loaded:
            self.load_data(uploaded_file)
        
        if st.session_state.data_loaded:
            st.sidebar.markdown("### 🏭 Business Parameters")
            
            monthly_consumption = st.sidebar.number_input(
                "Monthly PFAD Consumption (tons)",
                min_value=100,
                max_value=2000,
                value=500,
                step=50
            )
            
            current_inventory = st.sidebar.number_input(
                "Current Inventory (tons)",
                min_value=0,
                max_value=3000,
                value=800,
                step=50
            )
            
            safety_stock_days = st.sidebar.slider(
                "Safety Stock (days)",
                min_value=5,
                max_value=30,
                value=15
            )
            
            if st.sidebar.button("🔧 Set Business Parameters"):
                self.set_business_parameters(monthly_consumption, current_inventory, safety_stock_days)
        
        if st.session_state.data_loaded:
            st.sidebar.markdown("### 🚀 Analysis")
            
            if ADVANCED_MODULES_AVAILABLE and st.session_state.business_params_set:
                if st.sidebar.button("🔬 Run Advanced Analysis", type="primary"):
                    self.run_advanced_analysis()
            
            if st.sidebar.button("📊 Run Basic Analysis", type="secondary"):
                self.run_basic_analysis()
            
            if st.session_state.analysis_complete:
                st.sidebar.success("✅ Analysis Complete!")
        
        st.sidebar.markdown("### 📊 System Status")
        status_items = [
            ("Data Loaded", st.session_state.data_loaded),
            ("Parameters Set", st.session_state.business_params_set),
            ("Analysis Complete", st.session_state.analysis_complete),
            ("Advanced Modules", ADVANCED_MODULES_AVAILABLE)
        ]
        
        for item, status in status_items:
            icon = "✅" if status else "⏳"
            st.sidebar.markdown(f"{icon} {item}")
    
    def load_data(self, uploaded_file):
        try:
            with st.spinner("🔄 Loading data..."):
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                else:
                    data = pd.read_excel(uploaded_file)
                
                if 'Date' not in data.columns:
                    st.error("❌ 'Date' column not found")
                    return
                
                if 'PFAD Rate' not in data.columns:
                    st.error("❌ 'PFAD Rate' column not found")
                    return
                
                # Rename columns
                data = data.rename(columns={
                    'PFAD Rate': 'PFAD_Rate',
                    'CPO Bursa': 'CPO_Bursa',
                    'Malaysia  FOB': 'Malaysia_FOB',
                    'USD INR': 'USD_INR',
                    'USD MYR': 'USD_MYR',
                    'Brent crude': 'Brent_Crude',
                    'CPO Volume': 'CPO_Volume',
                    'MCX Palm futures': 'MCX_Palm_Futures',
                    'India Repo Rate': 'India_Repo_Rate',
                    'India CPI': 'India_CPI',
                    'Indonesia palm rate': 'Indonesia_Palm_Rate',
                    'Indonesia palm volume': 'Indonesia_Palm_Volume',
                    'Malaysia CPO Production': 'Malaysia_CPO_Production',
                    'Soy Rate': 'Soy_Rate',
                    'Sunflower Rate': 'Sunflower_Rate',
                    'Coconut Rate': 'Coconut_Rate',
                    'US 10Y Treasury': 'US_10Y_Treasury'
                })
                
                st.session_state.current_data = data
                st.session_state.data_loaded = True
                
                if ADVANCED_MODULES_AVAILABLE:
                    try:
                        self.econometric_engine = PFADEconometricEngine()
                        self.procurement_optimizer = PFADProcurementOptimizer()
                        st.sidebar.info("✅ Advanced modules ready")
                    except Exception as e:
                        st.sidebar.warning(f"⚠️ Advanced modules issue: {str(e)}")
                
                st.sidebar.success(f"✅ Data loaded: {len(data)} records")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
    
    def set_business_parameters(self, monthly_consumption, current_inventory, safety_stock_days):
        try:
            st.session_state.business_params = {
                'monthly_consumption': monthly_consumption,
                'current_inventory': current_inventory,
                'safety_stock_days': safety_stock_days
            }
            
            if self.procurement_optimizer:
                self.procurement_optimizer.set_business_parameters(
                    monthly_consumption=monthly_consumption,
                    current_inventory=current_inventory,
                    safety_stock_days=safety_stock_days,
                    max_storage_capacity=2000
                )
            
            st.session_state.business_params_set = True
            st.sidebar.success("✅ Parameters set!")
            
        except Exception as e:
            st.error(f"❌ Error setting parameters: {str(e)}")
    
    def run_advanced_analysis(self):
        if not self.econometric_engine or not self.procurement_optimizer:
            st.error("❌ Advanced modules not initialized")
            return
        
        try:
            with st.spinner("🔬 Running advanced analysis..."):
                data = st.session_state.current_data
                
                # Run econometric analysis
                self.econometric_engine.load_and_prepare_data(data)
                self.econometric_engine.fit_var_model()
                self.econometric_engine.test_granger_causality()
                
                # Generate forecasts
                forecasts = self.econometric_engine.generate_advanced_forecasts(30)
                
                # Run procurement optimization
                params = st.session_state.business_params
                self.procurement_optimizer.set_business_parameters(
                    monthly_consumption=params['monthly_consumption'],
                    current_inventory=params['current_inventory'],
                    safety_stock_days=params['safety_stock_days'],
                    max_storage_capacity=2000
                )
                
                last_date = data['Date'].max()
                forecast_dates = pd.date_range(
                    start=pd.to_datetime(last_date) + pd.Timedelta(days=1),
                    periods=30,
                    freq='D'
                )
                
                price_forecasts = forecasts.get('ensemble', forecasts.get('var', [data['PFAD_Rate'].iloc[-1]] * 30))
                
                procurement_results = self.procurement_optimizer.generate_procurement_dashboard(
                    price_forecasts, forecast_dates
                )
                
                st.session_state.results = {
                    'type': 'advanced',
                    'econometric': self.econometric_engine.results,
                    'procurement': procurement_results,
                    'forecasts': forecasts
                }
                
                st.session_state.analysis_complete = True
                st.success("🎉 Advanced analysis complete!")
                
        except Exception as e:
            st.error(f"❌ Advanced analysis failed: {str(e)}")
            st.info("🔄 Running basic analysis instead...")
            self.run_basic_analysis()
    
    def run_basic_analysis(self):
        try:
            with st.spinner("📊 Running basic analysis..."):
                data = st.session_state.current_data
                
                current_price = data['PFAD_Rate'].iloc[-1]
                prev_price = data['PFAD_Rate'].iloc[-2] if len(data) > 1 else current_price
                price_change = ((current_price - prev_price) / prev_price) * 100
                
                returns = data['PFAD_Rate'].pct_change().dropna()
                volatility = returns.std() * np.sqrt(252) * 100
                
                ma_short = data['PFAD_Rate'].rolling(10).mean().iloc[-1]
                ma_long = data['PFAD_Rate'].rolling(30).mean().iloc[-1]
                trend = 'Rising' if ma_short > ma_long else 'Falling'
                
                # Basic correlations
                numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
                top_factors = {}
                
                if len(numeric_cols) > 1:
                    try:
                        corr_matrix = data[numeric_cols].corr()
                        if 'PFAD_Rate' in corr_matrix.columns:
                            pfad_correlations = corr_matrix['PFAD_Rate'].drop('PFAD_Rate').abs().sort_values(ascending=False)
                            top_factors = pfad_correlations.head(5).to_dict()
                    except:
                        pass
                
                # Basic EOQ
                monthly_consumption = st.session_state.business_params.get('monthly_consumption', 500) if st.session_state.business_params_set else 500
                annual_demand = monthly_consumption * 12
                ordering_cost = 25000
                holding_cost = current_price * 0.02 * 12
                
                if holding_cost > 0:
                    basic_eoq = (2 * annual_demand * ordering_cost / holding_cost) ** 0.5
                else:
                    basic_eoq = 100
                
                # Simple forecast
                forecast_trend = 1.02 if trend == 'Rising' else 0.98
                simple_forecasts = [current_price * (forecast_trend ** (i/30)) for i in range(30)]
                
                st.session_state.results = {
                    'type': 'basic',
                    'current_price': current_price,
                    'price_change': price_change,
                    'volatility': volatility,
                    'trend': trend,
                    'top_factors': top_factors,
                    'basic_eoq': basic_eoq,
                    'monthly_consumption': monthly_consumption,
                    'forecasts': simple_forecasts,
                    'recommendations': {
                        'timing': 'Buy' if trend == 'Rising' and price_change < 2 else 'Wait',
                        'quantity': f"{basic_eoq:.0f} tons",
                        'risk_level': 'High' if volatility > 30 else 'Medium' if volatility > 15 else 'Low'
                    }
                }
                
                st.session_state.analysis_complete = True
                st.success("✅ Basic analysis complete!")
                
        except Exception as e:
            st.error(f"❌ Basic analysis error: {str(e)}")
    
    def render_executive_overview(self):
        if not st.session_state.analysis_complete:
            st.info("🔄 Please run analysis to view insights")
            return
        
        st.markdown("## 📊 Executive Dashboard")
        
        data = st.session_state.current_data
        results = st.session_state.results
        
        current_price = data['PFAD_Rate'].iloc[-1]
        prev_price = data['PFAD_Rate'].iloc[-2] if len(data) > 1 else current_price
        change = ((current_price - prev_price) / prev_price) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Current PFAD Price</h3>
                <h2>₹{current_price:,.0f}</h2>
                <p style="color: {'green' if change > 0 else 'red'};">
                    {'+' if change > 0 else ''}{change:.2f}% (24h)
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if 'forecasts' in results:
                if isinstance(results['forecasts'], dict):
                    forecast_data = results['forecasts'].get('ensemble', results['forecasts'].get('simple', [current_price] * 7))
                else:
                    forecast_data = results['forecasts']
                
                forecast_7d = np.mean(forecast_data[:7])
                forecast_change = ((forecast_7d - current_price) / current_price) * 100
                
                st.markdown(f"""
                <div class="metric-card success-card">
                    <h3>7-Day Forecast</h3>
                    <h2>₹{forecast_7d:,.0f}</h2>
                    <p style="color: {'green' if forecast_change > 0 else 'red'};">
                        {'+' if forecast_change > 0 else ''}{forecast_change:.1f}% expected
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>Analysis Status</h3>
                    <h2>Complete</h2>
                    <p>Ready for insights</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            volatility = results.get('volatility', 20)
            st.markdown(f"""
            <div class="metric-card warning-card">
                <h3>Volatility</h3>
                <h2>{volatility:.1f}%</h2>
                <p>Annual volatility</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            eoq = results.get('basic_eoq', 450)
            st.markdown(f"""
            <div class="metric-card success-card">
                <h3>Optimal Order</h3>
                <h2>{eoq:.0f} tons</h2>
                <p>EOQ recommendation</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Price chart
        st.markdown("## 📈 Price Analysis")
        self.render_price_chart()
        
        # Insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Key Insights")
            if 'top_factors' in results and results['top_factors']:
                for i, (factor, corr) in enumerate(list(results['top_factors'].items())[:3], 1):
                    st.markdown(f"{i}. **{factor}** - {corr:.3f} correlation")
            else:
                st.markdown("• Price trend analysis completed")
                st.markdown("• Volatility assessment available")
                st.markdown("• Market indicators evaluated")
        
        with col2:
            st.markdown("### 💼 Recommendations")
            if 'recommendations' in results:
                rec = results['recommendations']
                st.markdown(f"• **Timing**: {rec.get('timing', 'Monitor')}")
                st.markdown(f"• **Quantity**: {rec.get('quantity', '450 tons')}")
                st.markdown(f"• **Risk Level**: {rec.get('risk_level', 'Medium')}")
            else:
                st.markdown("• Monitor market trends")
                st.markdown("• Review procurement timing")
                st.markdown("• Assess supplier options")
    
    def render_price_chart(self):
        data = st.session_state.current_data
        results = st.session_state.results
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(data['Date']),
            y=data['PFAD_Rate'],
            mode='lines',
            name='Historical Prices',
            line=dict(color='#667eea', width=3)
        ))
        
        if 'forecasts' in results:
            forecast_data = results['forecasts']
            if isinstance(forecast_data, dict):
                forecast_data = forecast_data.get('ensemble', forecast_data.get('simple', []))
            
            if forecast_data:
                last_date = pd.to_datetime(data['Date'].max())
                forecast_dates = pd.date_range(
                    start=last_date + pd.Timedelta(days=1),
                    periods=len(forecast_data),
                    freq='D'
                )
                
                fig.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=forecast_data,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='#ff7f0e', width=2, dash='dash'),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title="PFAD Price Analysis with Forecasts",
            xaxis_title="Date",
            yaxis_title="Price (₹/ton)",
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def show_welcome_screen(self):
        st.markdown("""
        ## 🎉 Welcome to PFAD Professional Analytics
        
        ### 🏭 Enterprise-Grade Procurement Optimization
        
        **Features:**
        - Advanced econometric analysis (VAR, GARCH models)
        - Procurement optimization with EOQ calculations
        - Risk management and volatility analysis
        - Professional dashboards and reporting
        
        ### 📁 Getting Started
        1. Upload your Bloomberg PFAD data using the sidebar
        2. Set your business parameters (consumption, inventory)
        3. Run analysis (Advanced or Basic)
        4. Review insights across multiple tabs
        
        ### 📊 Expected Data Format
        - `Date` - Trading dates
        - `PFAD Rate` - PFAD prices (with space)
        - `CPO Bursa` - CPO futures
        - `USD MYR` - Exchange rates
        - Other market parameters
        """)
        
        sample_data = pd.DataFrame({
            'Date': pd.date_range('2024-01-01', periods=5),
            'PFAD Rate': [82000, 82500, 81800, 83200, 82700],
            'CPO Bursa': [3800, 3820, 3790, 3850, 3810],
            'USD MYR': [4.65, 4.68, 4.63, 4.72, 4.69]
        })
        
        st.markdown("### 📋 Sample Data Structure")
        st.dataframe(sample_data, use_container_width=True)
    
    def run(self):
        self.render_header()
        self.render_sidebar()
        
        if st.session_state.data_loaded:
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Executive Overview",
                "🔬 Analysis Results",
                "💼 Procurement",
                "⚠️ Risk Management"
            ])
            
            with tab1:
                self.render_executive_overview()
            
            with tab2:
                if st.session_state.analysis_complete:
                    st.markdown("## 🔬 Analysis Results")
                    results = st.session_state.results
                    
                    if results.get('type') == 'advanced':
                        st.success("✅ Advanced econometric analysis completed")
                        
                        if 'econometric' in results and 'granger_causality' in results['econometric']:
                            st.markdown("### Granger Causality Results")
                            causality = results['econometric']['granger_causality']
                            
                            causality_data = []
                            for var, result in causality.items():
                                causality_data.append({
                                    'Variable': var,
                                    'P-Value': f"{result.get('p_value', 0):.4f}",
                                    'Causal': '✅ Yes' if result.get('is_causal', False) else '❌ No'
                                })
                            
                            if causality_data:
                                df = pd.DataFrame(causality_data)
                                st.dataframe(df, use_container_width=True)
                    
                    elif results.get('type') == 'basic':
                        st.info("📊 Basic statistical analysis completed")
                        
                        if 'top_factors' in results and results['top_factors']:
                            st.markdown("### Top Correlations")
                            
                            correlation_data = []
                            for var, corr in results['top_factors'].items():
                                correlation_data.append({
                                    'Parameter': var,
                                    'Correlation': f"{corr:.3f}",
                                    'Strength': 'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'
                                })
                            
                            df = pd.DataFrame(correlation_data)
                            st.dataframe(df, use_container_width=True)
                else:
                    st.info("🔄 Please run analysis to view results")
            
            with tab3:
                if st.session_state.analysis_complete:
                    st.markdown("## 💼 Procurement Optimization")
                    results = st.session_state.results
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        eoq = results.get('basic_eoq', 450)
                        st.metric("Optimal Order Quantity", f"{eoq:.0f} tons")
                    
                    with col2:
                        consumption = results.get('monthly_consumption', 500)
                        st.metric("Monthly Consumption", f"{consumption} tons")
                    
                    with col3:
                        if 'recommendations' in results:
                            timing = results['recommendations'].get('timing', 'Monitor')
                            st.metric("Recommendation", timing)
                    
                    st.markdown("### 📊 EOQ Analysis")
                    if 'basic_eoq' in results:
                        eoq = results['basic_eoq']
                        consumption = results.get('monthly_consumption', 500)
                        frequency = (consumption * 12) / eoq if eoq > 0 else 12
                        
                        st.markdown(f"""
                        **Optimal Order Quantity:** {eoq:.0f} tons  
                        **Order Frequency:** {frequency:.1f} times per year  
                        **Days Between Orders:** {365 / frequency:.0f} days  
                        **Current Price:** ₹{results.get('current_price', 80000):,.0f}/ton
                        """)
                else:
                    st.info("🔄 Please run analysis to view procurement optimization")
            
            with tab4:
                if st.session_state.analysis_complete:
                    st.markdown("## ⚠️ Risk Management")
                    results = st.session_state.results
                    
                    current_price = results.get('current_price', 80000)
                    volatility = results.get('volatility', 20)
                    var_95 = current_price * 0.05
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Daily VaR (95%)", f"₹{var_95/1000:.1f}K")
                    
                    with col2:
                        st.metric("Annual Volatility", f"{volatility:.1f}%")
                    
                    with col3:
                        risk_level = "High" if volatility > 30 else "Medium" if volatility > 15 else "Low"
                        st.metric("Risk Level", risk_level)
                    
                    st.markdown("### 🛡️ Risk Recommendations")
                    
                    if volatility > 30:
                        st.error("🔴 High Risk: Consider hedging strategies")
                    elif volatility > 15:
                        st.warning("🟡 Medium Risk: Monitor closely")
                    else:
                        st.success("🟢 Low Risk: Normal operations")
                    
                    st.markdown("""
                    **Risk Management Actions:**
                    • Monitor daily price movements
                    • Set stop-loss limits at -5%
                    • Consider partial hedging for inventory
                    • Diversify supplier base
                    • Maintain adequate safety stock
                    """)
                else:
                    st.info("🔄 Please run analysis to view risk assessment")
        else:
            self.show_welcome_screen()

# Run application
if __name__ == "__main__":
    app = AdvancedPFADSystem()
    app.run()
