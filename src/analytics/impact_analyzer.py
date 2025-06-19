"""
PFAD Impact Analysis Module

Analyzes how different market parameters have affected PFAD prices historically.
Provides clear business explanations for price movements.
"""

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class PFADImpactAnalyzer:
    """
    Analyzes historical impact of market parameters on PFAD prices
    
    Provides business-ready explanations of:
    - Which factors drove price changes
    - Why these factors affected prices
    - Quantified impact of each parameter
    """
    
    def __init__(self):
        self.impact_results = {}
        self.correlation_matrix = None
        self.regression_results = {}
        self.factor_explanations = {
            'CPO_Bursa': 'CPO Bursa Malaysia futures - Direct palm oil benchmark pricing',
            'Malaysia_FOB': 'Malaysia export prices - International trade pricing reference',
            'USD_MYR': 'Currency exchange rate - Affects import costs for Indian buyers',
            'MCX_Palm_Futures': 'Indian domestic futures - Local market sentiment and demand',
            'Brent_Crude': 'Global energy prices - Affects biodiesel demand and transportation costs',
            'US_10Y_Treasury': 'Global interest rates - Impacts commodity financing and investment flows',
            'India_Repo_Rate': 'Indian interest rates - Affects domestic demand and financing',
            'India_CPI': 'Indian inflation - Consumer purchasing power and demand patterns',
            'Soy_Rate': 'Soybean oil prices - Substitute oil competition',
            'Sunflower_Rate': 'Sunflower oil prices - Alternative oil pricing pressure',
            'Coconut_Rate': 'Coconut oil prices - Regional substitute oil dynamics',
            'CPO_Volume': 'Trading volumes - Market liquidity and price volatility',
            'Indonesia_Palm_Rate': 'Indonesian pricing - Regional competition and arbitrage',
            'Indonesia_Palm_Volume': 'Indonesian trade volumes - Supply availability'
        }
    
    def analyze_historical_impact(self, data):
        """
        Comprehensive analysis of how parameters affected PFAD prices
        
        Returns business-ready insights about price drivers
        """
        print("🔍 Analyzing Historical Impact of Market Parameters...")
        
        # 1. Calculate correlations
        self.correlation_matrix = self._calculate_correlations(data)
        
        # 2. Perform regression analysis
        self.regression_results = self._regression_analysis(data)
        
        # 3. Time period analysis
        period_analysis = self._time_period_analysis(data)
        
        # 4. Volatility impact analysis
        volatility_analysis = self._volatility_impact_analysis(data)
        
        # 5. Generate business insights
        business_insights = self._generate_business_insights()
        
        self.impact_results = {
            'correlations': self.correlation_matrix,
            'regression': self.regression_results,
            'period_analysis': period_analysis,
            'volatility_analysis': volatility_analysis,
            'business_insights': business_insights
        }
        
        print("✅ Impact Analysis Complete!")
        return self.impact_results
    
    def _calculate_correlations(self, data):
        """Calculate correlation between PFAD and all parameters"""
        
        # Select numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove Date if present
        if 'Date' in numeric_cols:
            numeric_cols.remove('Date')
        
        # Calculate correlation matrix
        corr_matrix = data[numeric_cols].corr()
        
        # Focus on PFAD correlations
        if 'PFAD_Rate' in corr_matrix.columns:
            pfad_correlations = corr_matrix['PFAD_Rate'].drop('PFAD_Rate')
            
            # Classify correlation strength
            correlation_analysis = {}
            for param, corr in pfad_correlations.items():
                if abs(corr) > 0.7:
                    strength = "Very Strong"
                elif abs(corr) > 0.5:
                    strength = "Strong"
                elif abs(corr) > 0.3:
                    strength = "Moderate"
                else:
                    strength = "Weak"
                
                correlation_analysis[param] = {
                    'correlation': corr,
                    'strength': strength,
                    'direction': 'Positive' if corr > 0 else 'Negative',
                    'explanation': self.factor_explanations.get(param, 'Market parameter')
                }
            
            return correlation_analysis
        
        return {}
    
    def _regression_analysis(self, data):
        """Quantify impact of each parameter using regression"""
        
        # Prepare data for regression
        feature_cols = [col for col in data.columns 
                       if col not in ['Date', 'PFAD_Rate'] and data[col].dtype in ['float64', 'int64']]
        
        if 'PFAD_Rate' not in data.columns or len(feature_cols) == 0:
            return {}
        
        # Clean data
        clean_data = data[['PFAD_Rate'] + feature_cols].dropna()
        
        if len(clean_data) < 100:  # Need sufficient data
            return {}
        
        X = clean_data[feature_cols]
        y = clean_data['PFAD_Rate']
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Fit regression model
        model = LinearRegression()
        model.fit(X_scaled, y)
        
        # Calculate R-squared
        r_squared = model.score(X_scaled, y)
        
        # Get coefficients and their importance
        coefficients = {}
        for i, feature in enumerate(feature_cols):
            # Calculate percentage impact
            impact_per_std = model.coef_[i] * X[feature].std()
            percentage_impact = (impact_per_std / y.mean()) * 100
            
            coefficients[feature] = {
                'coefficient': model.coef_[i],
                'impact_per_std': impact_per_std,
                'percentage_impact': percentage_impact,
                'explanation': self.factor_explanations.get(feature, 'Market parameter')
            }
        
        return {
            'r_squared': r_squared,
            'coefficients': coefficients,
            'model_explanation': f"This model explains {r_squared*100:.1f}% of PFAD price movements"
        }
    
    def _time_period_analysis(self, data):
        """Analyze how impact changed over different time periods"""
        
        if 'Date' not in data.columns or 'PFAD_Rate' not in data.columns:
            return {}
        
        # Convert Date column
        data['Date'] = pd.to_datetime(data['Date'])
        data['Year'] = data['Date'].dt.year
        
        # Analyze by year
        yearly_analysis = {}
        
        for year in data['Year'].unique():
            if pd.notna(year):
                year_data = data[data['Year'] == year]
                
                if len(year_data) > 50:  # Need sufficient data
                    # Calculate year statistics
                    pfad_change = ((year_data['PFAD_Rate'].iloc[-1] - year_data['PFAD_Rate'].iloc[0]) 
                                  / year_data['PFAD_Rate'].iloc[0] * 100)
                    
                    volatility = year_data['PFAD_Rate'].pct_change().std() * 100
                    
                    yearly_analysis[int(year)] = {
                        'price_change_percent': pfad_change,
                        'volatility': volatility,
                        'avg_price': year_data['PFAD_Rate'].mean(),
                        'min_price': year_data['PFAD_Rate'].min(),
                        'max_price': year_data['PFAD_Rate'].max()
                    }
        
        return yearly_analysis
    
    def _volatility_impact_analysis(self, data):
        """Analyze which factors contributed to price volatility"""
        
        if 'PFAD_Rate' not in data.columns:
            return {}
        
        # Calculate price changes
        data['PFAD_Returns'] = data['PFAD_Rate'].pct_change()
        
        # Calculate volatility (rolling 30-day standard deviation)
        data['PFAD_Volatility'] = data['PFAD_Returns'].rolling(30).std()
        
        # Identify high volatility periods (top 20%)
        volatility_threshold = data['PFAD_Volatility'].quantile(0.8)
        high_vol_periods = data[data['PFAD_Volatility'] > volatility_threshold]
        
        volatility_analysis = {
            'average_volatility': data['PFAD_Volatility'].mean() * 100,
            'high_volatility_threshold': volatility_threshold * 100,
            'high_volatility_days': len(high_vol_periods),
            'total_days': len(data.dropna()),
            'volatility_explanation': "Periods when daily price changes exceeded normal market fluctuations"
        }
        
        return volatility_analysis
    
    def _generate_business_insights(self):
        """Generate clear business explanations of the analysis"""
        
        insights = {
            'executive_summary': [],
            'key_drivers': [],
            'procurement_implications': [],
            'risk_factors': []
        }
        
        # Executive Summary
        if self.correlation_matrix:
            # Find strongest correlations
            strong_factors = [(param, data['correlation']) 
                            for param, data in self.correlation_matrix.items() 
                            if abs(data['correlation']) > 0.5]
            
            strong_factors.sort(key=lambda x: abs(x[1]), reverse=True)
            
            if strong_factors:
                top_factor = strong_factors[0]
                insights['executive_summary'].append(
                    f"Primary Driver: {top_factor[0]} shows {abs(top_factor[1]):.2f} correlation with PFAD prices"
                )
                insights['executive_summary'].append(
                    f"This means when {top_factor[0]} increases by 1%, PFAD typically moves by {abs(top_factor[1])*100:.1f}%"
                )
        
        # Key Drivers
        if self.regression_results and 'coefficients' in self.regression_results:
            # Sort by absolute impact
            impacts = [(param, abs(data['percentage_impact'])) 
                      for param, data in self.regression_results['coefficients'].items()]
            impacts.sort(key=lambda x: x[1], reverse=True)
            
            for i, (param, impact) in enumerate(impacts[:5]):  # Top 5
                insights['key_drivers'].append(
                    f"{i+1}. {param}: {impact:.1f}% impact on PFAD prices"
                )
        
        # Procurement Implications
        insights['procurement_implications'].extend([
            "Monitor CPO Bursa futures for early price signals",
            "Track USD/MYR exchange rates for import cost planning",
            "Watch substitute oil prices for market switching opportunities",
            "Consider hedging during high volatility periods"
        ])
        
        # Risk Factors
        insights['risk_factors'].extend([
            "Currency fluctuations can impact import costs significantly",
            "Energy price changes affect both transportation and biodiesel demand",
            "Substitute oil price movements can trigger demand shifts",
            "Interest rate changes affect commodity financing costs"
        ])
        
        return insights
    
    def get_top_impact_factors(self, n=5):
        """Get the top N factors that impact PFAD prices"""
        
        if not self.correlation_matrix:
            return []
        
        # Sort by absolute correlation
        factors = [(param, abs(data['correlation']), data) 
                  for param, data in self.correlation_matrix.items()]
        factors.sort(key=lambda x: x[1], reverse=True)
        
        return factors[:n]
    
    def explain_factor_impact(self, factor_name):
        """Provide detailed explanation of how a specific factor impacts PFAD"""
        
        if factor_name not in self.correlation_matrix:
            return f"No analysis available for {factor_name}"
        
        factor_data = self.correlation_matrix[factor_name]
        
        explanation = f"""
        IMPACT ANALYSIS: {factor_name}
        
        Correlation Strength: {factor_data['strength']} ({factor_data['correlation']:.3f})
        Direction: {factor_data['direction']} relationship with PFAD prices
        
        Business Explanation: {factor_data['explanation']}
        
        Practical Meaning:
        - When {factor_name} increases, PFAD prices typically {'increase' if factor_data['correlation'] > 0 else 'decrease'}
        - The relationship is {factor_data['strength'].lower()}, meaning it's a {'reliable' if abs(factor_data['correlation']) > 0.5 else 'moderate'} indicator
        
        Procurement Impact:
        - {'Monitor this factor closely for procurement timing' if abs(factor_data['correlation']) > 0.5 else 'Consider this factor alongside other indicators'}
        - {'High priority' if abs(factor_data['correlation']) > 0.7 else 'Medium priority'} for price forecasting
        """
        
        return explanation.strip()
