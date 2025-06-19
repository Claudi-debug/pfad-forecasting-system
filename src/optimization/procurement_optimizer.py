"""
PFAD Procurement Optimization System
Advanced algorithms for optimal PFAD procurement strategy

Features:
- Inventory cost minimization
- Optimal order timing
- Supplier contract optimization
- Hedging strategy recommendations
- Risk-adjusted procurement planning
- Real-time decision support
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class PFADProcurementOptimizer:
    """
    Advanced procurement optimization system for PFAD purchasing
    
    Integrates:
    - Economic Order Quantity (EOQ) optimization
    - Dynamic pricing models
    - Risk management
    - Supply chain constraints
    - Working capital optimization
    """
    
    def __init__(self):
        self.optimization_results = {}
        self.constraints = {}
        self.cost_structure = {}
        self.supplier_data = {}
        
        # Default cost parameters (can be customized)
        self.default_costs = {
            'holding_cost_rate': 0.02,  # 2% per month
            'ordering_cost': 25000,     # ₹25,000 per order
            'shortage_cost_rate': 0.05, # 5% penalty for stockouts
            'working_capital_rate': 0.12, # 12% annual cost of capital
            'transportation_cost_per_ton': 2000,  # ₹2,000 per ton
            'storage_cost_per_ton': 500,  # ₹500 per ton per month
            'insurance_rate': 0.005,    # 0.5% of inventory value
            'quality_deterioration_rate': 0.001  # 0.1% monthly
        }
        
        # Supplier parameters
        self.supplier_profiles = {
            'Supplier_A': {
                'reliability': 0.95,
                'lead_time_days': 15,
                'minimum_order': 100,  # tons
                'price_premium': 0.0,  # base price
                'payment_terms': 30,   # days
                'quality_score': 0.98
            },
            'Supplier_B': {
                'reliability': 0.92,
                'lead_time_days': 20,
                'minimum_order': 150,
                'price_premium': -0.02,  # 2% discount
                'payment_terms': 45,
                'quality_score': 0.96
            },
            'Supplier_C': {
                'reliability': 0.98,
                'lead_time_days': 10,
                'minimum_order': 50,
                'price_premium': 0.03,  # 3% premium
                'payment_terms': 15,
                'quality_score': 0.99
            }
        }
    
    def set_business_parameters(self, monthly_consumption, current_inventory, 
                               safety_stock_days=15, max_storage_capacity=2000):
        """
        Set business-specific parameters for optimization
        
        Args:
            monthly_consumption: Average monthly PFAD consumption (tons)
            current_inventory: Current inventory level (tons)
            safety_stock_days: Safety stock in days of consumption
            max_storage_capacity: Maximum storage capacity (tons)
        """
        self.business_params = {
            'monthly_consumption': monthly_consumption,
            'daily_consumption': monthly_consumption / 30,
            'current_inventory': current_inventory,
            'safety_stock': (monthly_consumption / 30) * safety_stock_days,
            'max_storage_capacity': max_storage_capacity,
            'reorder_point': (monthly_consumption / 30) * (safety_stock_days + 15)  # Safety + lead time
        }
        
        print(f"✅ Business parameters set:")
        print(f"   Monthly consumption: {monthly_consumption} tons")
        print(f"   Current inventory: {current_inventory} tons")
        print(f"   Safety stock: {self.business_params['safety_stock']:.1f} tons")
        print(f"   Reorder point: {self.business_params['reorder_point']:.1f} tons")
    
    def calculate_economic_order_quantity(self, current_price, demand_forecast):
        """
        Calculate optimal Economic Order Quantity (EOQ) with dynamic pricing
        
        Args:
            current_price: Current PFAD price per ton
            demand_forecast: Forecasted demand (tons per month)
        """
        print("🔄 Calculating Economic Order Quantity (EOQ)...")
        
        # Standard EOQ formula with modifications for price volatility
        D = demand_forecast * 12  # Annual demand
        S = self.default_costs['ordering_cost']  # Setup/ordering cost
        H = current_price * self.default_costs['holding_cost_rate'] * 12  # Annual holding cost
        
        # Basic EOQ
        basic_eoq = np.sqrt((2 * D * S) / H)
        
        # Adjusted EOQ considering price volatility and storage constraints
        max_order = min(basic_eoq, self.business_params['max_storage_capacity'] - self.business_params['current_inventory'])
        min_order = max(50, self.business_params['safety_stock'])  # Minimum practical order
        
        optimal_eoq = np.clip(basic_eoq, min_order, max_order)
        
        # Calculate total costs for different order quantities
        order_quantities = np.linspace(min_order, max_order, 20)
        costs = []
        
        for q in order_quantities:
            # Ordering cost
            ordering_cost = (D / q) * S
            
            # Holding cost
            holding_cost = (q / 2) * H
            
            # Storage cost
            storage_cost = q * self.default_costs['storage_cost_per_ton'] * 12
            
            # Insurance cost
            insurance_cost = (q * current_price) * self.default_costs['insurance_rate'] * 12
            
            # Total cost
            total_cost = ordering_cost + holding_cost + storage_cost + insurance_cost
            costs.append(total_cost)
        
        # Find optimal quantity
        optimal_index = np.argmin(costs)
        optimal_quantity = order_quantities[optimal_index]
        optimal_cost = costs[optimal_index]
        
        eoq_results = {
            'basic_eoq': basic_eoq,
            'optimal_quantity': optimal_quantity,
            'optimal_cost': optimal_cost,
            'cost_breakdown': {
                'ordering_cost': (D / optimal_quantity) * S,
                'holding_cost': (optimal_quantity / 2) * H,
                'storage_cost': optimal_quantity * self.default_costs['storage_cost_per_ton'] * 12,
                'insurance_cost': (optimal_quantity * current_price) * self.default_costs['insurance_rate'] * 12
            },
            'order_frequency': D / optimal_quantity,  # Orders per year
            'days_between_orders': 365 / (D / optimal_quantity)
        }
        
        print(f"✅ EOQ Analysis Complete:")
        print(f"   Optimal order quantity: {optimal_quantity:.1f} tons")
        print(f"   Order frequency: {eoq_results['order_frequency']:.1f} times per year")
        print(f"   Days between orders: {eoq_results['days_between_orders']:.1f} days")
        
        return eoq_results
    
    def optimize_procurement_timing(self, price_forecasts, forecast_dates, current_price):
        """
        Optimize procurement timing based on price forecasts
        
        Args:
            price_forecasts: Array of forecasted prices
            forecast_dates: Corresponding dates
            current_price: Current market price
        """
        print("🔄 Optimizing procurement timing...")
        
        # Convert to numpy arrays for easier manipulation
        prices = np.array(price_forecasts)
        dates = pd.to_datetime(forecast_dates)
        
        # Calculate potential savings for each day
        savings_per_ton = current_price - prices
        
        # Consider holding costs for delayed purchases
        days_delay = np.arange(len(prices))
        daily_holding_cost = (current_price * self.default_costs['holding_cost_rate']) / 30
        
        # Net benefit = savings - holding costs
        net_benefits = savings_per_ton - (days_delay * daily_holding_cost)
        
        # Find optimal timing
        optimal_day_index = np.argmax(net_benefits)
        optimal_date = dates[optimal_day_index]
        optimal_price = prices[optimal_day_index]
        optimal_savings = net_benefits[optimal_day_index]
        
        # Calculate different scenarios
        scenarios = {
            'buy_immediately': {
                'price': current_price,
                'total_cost': current_price * self.business_params['monthly_consumption'],
                'savings': 0,
                'risk': 'Low'
            },
            'buy_at_optimal_time': {
                'date': optimal_date,
                'price': optimal_price,
                'total_cost': optimal_price * self.business_params['monthly_consumption'],
                'savings': optimal_savings * self.business_params['monthly_consumption'],
                'days_wait': optimal_day_index,
                'risk': 'Medium' if optimal_day_index < 15 else 'High'
            },
            'buy_at_lowest_price': {
                'price': np.min(prices),
                'date': dates[np.argmin(prices)],
                'savings': (current_price - np.min(prices)) * self.business_params['monthly_consumption'],
                'days_wait': np.argmin(prices),
                'risk': 'High' if np.argmin(prices) > 20 else 'Medium'
            }
        }
        
        timing_results = {
            'scenarios': scenarios,
            'recommendation': self._get_timing_recommendation(scenarios),
            'price_trend': 'Declining' if np.mean(prices[:7]) < current_price else 'Rising',
            'volatility': np.std(prices) / np.mean(prices),
            'confidence_level': 'High' if len(prices) > 20 else 'Medium'
        }
        
        print(f"✅ Timing optimization complete:")
        print(f"   Recommended action: {timing_results['recommendation']['action']}")
        print(f"   Potential savings: ₹{timing_results['recommendation']['savings']:,.0f}")
        
        return timing_results
    
    def _get_timing_recommendation(self, scenarios):
        """Generate timing recommendation based on scenarios"""
        
        immediate = scenarios['buy_immediately']
        optimal = scenarios['buy_at_optimal_time']
        lowest = scenarios['buy_at_lowest_price']
        
        # Decision logic
        if optimal['savings'] > immediate['total_cost'] * 0.05:  # 5% savings threshold
            if optimal['days_wait'] <= 15:  # Acceptable wait time
                return {
                    'action': 'Wait for optimal timing',
                    'date': optimal['date'],
                    'savings': optimal['savings'],
                    'rationale': f"Wait {optimal['days_wait']} days for {optimal['savings']:,.0f} savings"
                }
        
        if lowest['savings'] > immediate['total_cost'] * 0.08:  # 8% savings threshold
            if lowest['days_wait'] <= 30:
                return {
                    'action': 'Wait for lowest price',
                    'date': lowest['date'],
                    'savings': lowest['savings'],
                    'rationale': f"Maximum savings opportunity in {lowest['days_wait']} days"
                }
        
        return {
            'action': 'Buy immediately',
            'savings': 0,
            'rationale': 'Current price is optimal or waiting costs exceed potential savings'
        }
    
    def optimize_supplier_selection(self, price_forecasts, quantity_needed):
        """
        Optimize supplier selection based on total cost of ownership
        
        Args:
            price_forecasts: Forecasted prices
            quantity_needed: Required quantity (tons)
        """
        print("🔄 Optimizing supplier selection...")
        
        base_price = np.mean(price_forecasts)
        supplier_analysis = {}
        
        for supplier_name, profile in self.supplier_profiles.items():
            # Calculate adjusted price
            adjusted_price = base_price * (1 + profile['price_premium'])
            
            # Total procurement cost
            procurement_cost = adjusted_price * quantity_needed
            
            # Transportation cost (estimated based on lead time)
            transport_cost = self.default_costs['transportation_cost_per_ton'] * quantity_needed
            
            # Working capital cost (based on payment terms)
            working_capital_cost = (procurement_cost * self.default_costs['working_capital_rate'] * 
                                  profile['payment_terms']) / 365
            
            # Risk premium (based on reliability)
            risk_premium = procurement_cost * (1 - profile['reliability']) * 0.1
            
            # Quality adjustment
            quality_adjustment = procurement_cost * (1 - profile['quality_score']) * 0.05
            
            # Total cost
            total_cost = (procurement_cost + transport_cost + working_capital_cost + 
                         risk_premium + quality_adjustment)
            
            # Delivery reliability score
            delivery_score = profile['reliability'] * (1 - profile['lead_time_days'] / 30)
            
            supplier_analysis[supplier_name] = {
                'base_price': adjusted_price,
                'procurement_cost': procurement_cost,
                'transport_cost': transport_cost,
                'working_capital_cost': working_capital_cost,
                'risk_premium': risk_premium,
                'quality_adjustment': quality_adjustment,
                'total_cost': total_cost,
                'cost_per_ton': total_cost / quantity_needed,
                'delivery_score': delivery_score,
                'overall_score': (1 / total_cost) * delivery_score * 1000000  # Normalized score
            }
        
        # Rank suppliers
        ranked_suppliers = sorted(supplier_analysis.items(), 
                                key=lambda x: x[1]['overall_score'], reverse=True)
        
        supplier_results = {
            'analysis': supplier_analysis,
            'ranking': [name for name, _ in ranked_suppliers],
            'recommended_supplier': ranked_suppliers[0][0],
            'cost_savings': (min(s['total_cost'] for s in supplier_analysis.values()) - 
                           max(s['total_cost'] for s in supplier_analysis.values())),
            'summary': self._generate_supplier_summary(ranked_suppliers)
        }
        
        print(f"✅ Supplier optimization complete:")
        print(f"   Recommended supplier: {supplier_results['recommended_supplier']}")
        print(f"   Potential cost savings: ₹{supplier_results['cost_savings']:,.0f}")
        
        return supplier_results
    
    def _generate_supplier_summary(self, ranked_suppliers):
        """Generate supplier selection summary"""
        
        best = ranked_suppliers[0]
        summary = {
            'best_supplier': {
                'name': best[0],
                'total_cost': best[1]['total_cost'],
                'cost_per_ton': best[1]['cost_per_ton'],
                'delivery_score': best[1]['delivery_score']
            },
            'comparison': []
        }
        
        for name, data in ranked_suppliers:
            summary['comparison'].append({
                'supplier': name,
                'cost_per_ton': data['cost_per_ton'],
                'ranking': ranked_suppliers.index((name, data)) + 1
            })
        
        return summary
    
    def calculate_hedging_strategy(self, price_forecasts, volatility_forecast, quantity_needed):
        """
        Calculate optimal hedging strategy for price risk management
        
        Args:
            price_forecasts: Forecasted prices
            volatility_forecast: Forecasted volatility
            quantity_needed: Quantity to hedge (tons)
        """
        print("🔄 Calculating hedging strategy...")
        
        current_price = price_forecasts[0] if len(price_forecasts) > 0 else 80000
        expected_price = np.mean(price_forecasts)
        price_volatility = np.std(price_forecasts) / np.mean(price_forecasts)
        
        # Value at Risk calculation (95% confidence)
        var_95 = current_price * quantity_needed * price_volatility * 1.645
        
        # Expected shortfall (99% confidence)
        es_99 = current_price * quantity_needed * price_volatility * 2.33
        
        # Hedging scenarios
        hedging_scenarios = {
            'no_hedge': {
                'description': 'No hedging - full market exposure',
                'cost': 0,
                'risk_reduction': 0,
                'max_loss': var_95,
                'recommendation': 'Only if very confident about price direction'
            },
            'partial_hedge_50': {
                'description': '50% quantity hedged',
                'hedge_quantity': quantity_needed * 0.5,
                'hedging_cost': quantity_needed * 0.5 * current_price * 0.02,  # 2% hedging cost
                'risk_reduction': 0.5,
                'max_loss': var_95 * 0.5,
                'recommendation': 'Balanced approach - moderate cost and risk'
            },
            'full_hedge': {
                'description': '100% quantity hedged',
                'hedge_quantity': quantity_needed,
                'hedging_cost': quantity_needed * current_price * 0.035,  # 3.5% hedging cost
                'risk_reduction': 0.9,  # Some basis risk remains
                'max_loss': var_95 * 0.1,
                'recommendation': 'Conservative approach for risk-averse operations'
            },
            'dynamic_hedge': {
                'description': 'Dynamic hedging based on volatility',
                'hedge_ratio': min(0.8, price_volatility / 0.05),  # Adjust based on volatility
                'hedge_quantity': quantity_needed * min(0.8, price_volatility / 0.05),
                'hedging_cost': quantity_needed * min(0.8, price_volatility / 0.05) * current_price * 0.025,
                'risk_reduction': min(0.8, price_volatility / 0.05),
                'recommendation': 'Sophisticated approach - adjust hedge ratio based on market conditions'
            }
        }
        
        # Add max loss calculations
        for scenario in hedging_scenarios.values():
            if 'hedge_quantity' in scenario:
                scenario['max_loss'] = var_95 * (1 - scenario['risk_reduction'])
                scenario['net_cost'] = scenario['hedging_cost']
                scenario['cost_benefit_ratio'] = scenario['hedging_cost'] / (var_95 - scenario['max_loss']) if var_95 != scenario['max_loss'] else float('inf')
        
        # Recommendation logic
        recommended_strategy = self._select_hedging_strategy(hedging_scenarios, price_volatility)
        
        hedging_results = {
            'market_analysis': {
                'current_price': current_price,
                'expected_price': expected_price,
                'volatility': price_volatility,
                'var_95': var_95,
                'expected_shortfall_99': es_99
            },
            'scenarios': hedging_scenarios,
            'recommended_strategy': recommended_strategy,
            'risk_metrics': {
                'unhedged_var': var_95,
                'hedged_var': hedging_scenarios[recommended_strategy]['max_loss'],
                'risk_reduction': hedging_scenarios[recommended_strategy]['risk_reduction']
            }
        }
        
        print(f"✅ Hedging strategy calculated:")
        print(f"   Recommended strategy: {recommended_strategy}")
        print(f"   Risk reduction: {hedging_scenarios[recommended_strategy]['risk_reduction']*100:.1f}%")
        print(f"   Hedging cost: ₹{hedging_scenarios[recommended_strategy].get('hedging_cost', 0):,.0f}")
        
        return hedging_results
    
    def _select_hedging_strategy(self, scenarios, volatility):
        """Select optimal hedging strategy based on market conditions"""
        
        if volatility > 0.06:  # High volatility
            return 'full_hedge'
        elif volatility > 0.03:  # Medium volatility
            return 'partial_hedge_50'
        elif volatility > 0.015:  # Low-medium volatility
            return 'dynamic_hedge'
        else:  # Low volatility
            return 'no_hedge'
    
    def generate_procurement_dashboard(self, price_forecasts, forecast_dates):
        """
        Generate comprehensive procurement dashboard with all optimization results
        """
        print("📊 Generating procurement optimization dashboard...")
        
        current_price = price_forecasts[0] if len(price_forecasts) > 0 else 80000
        monthly_consumption = self.business_params['monthly_consumption']
        
        # Run all optimizations
        eoq_results = self.calculate_economic_order_quantity(current_price, monthly_consumption)
        timing_results = self.optimize_procurement_timing(price_forecasts, forecast_dates, current_price)
        supplier_results = self.optimize_supplier_selection(price_forecasts, eoq_results['optimal_quantity'])
        hedging_results = self.calculate_hedging_strategy(price_forecasts, 0.03, eoq_results['optimal_quantity'])
        
        # Compile dashboard
        dashboard = {
            'executive_summary': {
                'current_inventory_days': (self.business_params['current_inventory'] / self.business_params['daily_consumption']),
                'recommended_order_quantity': eoq_results['optimal_quantity'],
                'optimal_timing': timing_results['recommendation']['action'],
                'best_supplier': supplier_results['recommended_supplier'],
                'hedging_recommendation': hedging_results['recommended_strategy'],
                'total_monthly_procurement_cost': current_price * monthly_consumption,
                'potential_monthly_savings': (timing_results['scenarios']['buy_at_optimal_time']['savings'] + 
                                            supplier_results['cost_savings']) / 12
            },
            'detailed_analysis': {
                'eoq': eoq_results,
                'timing': timing_results,
                'suppliers': supplier_results,
                'hedging': hedging_results
            },
            'key_metrics': {
                'inventory_turnover': (monthly_consumption * 12) / self.business_params['current_inventory'],
                'days_inventory_outstanding': (self.business_params['current_inventory'] / self.business_params['daily_consumption']),
                'procurement_cost_percentage': (current_price * monthly_consumption) / (current_price * monthly_consumption * 1.15) * 100,  # Assuming 15% other costs
                'working_capital_tied': current_price * self.business_params['current_inventory']
            },
            'action_items': self._generate_action_items(eoq_results, timing_results, supplier_results, hedging_results)
        }
        
        print("✅ Procurement dashboard generated")
        print(f"📊 Key recommendations:")
        for item in dashboard['action_items']['immediate']:
            print(f"   • {item}")
        
        return dashboard
    
    def _generate_action_items(self, eoq, timing, suppliers, hedging):
        """Generate actionable recommendations"""
        
        immediate_actions = []
        strategic_actions = []
        
        # Immediate actions
        if timing['recommendation']['action'] != 'Buy immediately':
            immediate_actions.append(f"TIMING: {timing['recommendation']['rationale']}")
        
        immediate_actions.append(f"QUANTITY: Order {eoq['optimal_quantity']:.0f} tons (optimal EOQ)")
        immediate_actions.append(f"SUPPLIER: Use {suppliers['recommended_supplier']} for best total cost")
        
        if hedging['recommended_strategy'] != 'no_hedge':
            immediate_actions.append(f"HEDGING: Implement {hedging['recommended_strategy']} strategy")
        
        # Strategic actions
        strategic_actions.extend([
            "Review supplier contracts quarterly",
            "Monitor market volatility for hedging adjustments",
            "Optimize storage capacity utilization",
            "Implement automated reorder point system",
            "Develop supplier diversification strategy"
        ])
        
        return {
            'immediate': immediate_actions,
            'strategic': strategic_actions
        }

# Example usage
if __name__ == "__main__":
    print("PFAD Procurement Optimization System - Ready")
    print("=" * 50)
    
    # Initialize optimizer
    optimizer = PFADProcurementOptimizer()
    
    # Set business parameters
    optimizer.set_business_parameters(
        monthly_consumption=500,  # tons
        current_inventory=800,    # tons
        safety_stock_days=15,     # days
        max_storage_capacity=2000 # tons
    )
    
    print("\nTo use this optimizer:")
    print("1. Set your business parameters")
    print("2. Provide price forecasts")
    print("3. Run dashboard generation")
    print("4. Get actionable procurement recommendations")
