# app.py
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime
#from scipy import stats
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
df = pd.read_csv("C:/Users/shaya/Downloads/shop/processed_dataset.csv")

class BusinessInsightsAnalyzer:
    def __init__(self, data):
        self.df = data

    # -------------------- SALES & PRODUCT TRENDS --------------------
    def get_top_products_by_revenue(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('item_purchased')['total_revenue'].sum().nlargest(10).to_dict()

    def get_highest_revenue_product(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('item_purchased')['total_revenue'].sum().idxmax()

    def get_sales_by_time_period(self, period='month', filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(period)['total_revenue'].sum().to_dict()

    def get_sales_by_weekday(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('day_of_week')['total_revenue'].sum().to_dict()

    def get_products_by_popularity(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('item_purchased')['popularity_score'].mean().nlargest(10).to_dict()

    def get_revenue_by_season(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('season')['total_revenue'].sum().to_dict()

    def get_sales_distribution_size_color(self, filters=None):
        filtered_df = self._apply_filters(filters)
        size_dist = filtered_df.groupby('product_size')['quantity'].sum().to_dict()
        color_dist = filtered_df.groupby('product_color')['quantity'].sum().to_dict()
        return {'size': size_dist, 'color': color_dist}

    def get_discount_effectiveness(self, filters=None):
        filtered_df = self._apply_filters(filters)
        effectiveness = filtered_df.groupby('promo_code_used')['total_revenue'].mean().to_dict()
        return effectiveness

    # -------------------- HELPER FUNCTION --------------------
    def _apply_filters(self, filters):
        filtered_df = self.df.copy()
        if filters:
            if 'region' in filters and filters['region'] != "All":
                filtered_df = filtered_df[filtered_df['region'] == filters['region']]
            if 'category' in filters and filters['category'] != "All":
                filtered_df = filtered_df[filtered_df['category'] == filters['category']]
        return filtered_df
    
        # -------------------- CUSTOMER DEMOGRAPHICS --------------------
    def get_revenue_by_age_group(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('age')['total_revenue'].sum().to_dict()

    def get_purchases_by_gender(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('gender')['quantity'].sum().to_dict()

    def get_top_regions_by_sales(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('region')['total_revenue'].sum().nlargest(5).to_dict()

    def get_age_category_preferences(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(['age', 'most_purchased_category_by_age'])['quantity'].sum().unstack().to_dict()

    def get_gender_category_preferences(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(['gender', 'most_purchased_category_by_gender'])['quantity'].sum().unstack().to_dict()

    def get_avg_order_value_by_region(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('region')['total_revenue'].mean().to_dict()

    def get_subscribed_vs_non_subscribed(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('is_subscribed')['total_revenue'].sum().to_dict()
    
        # -------------------- CUSTOMER BEHAVIOR --------------------
    def get_avg_purchase_frequency(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df['purchase_frequency'].mean()

    def get_category_repurchase_rate(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(['customer_id', 'category']).size().groupby('category').mean().to_dict()

    def get_customer_lifetime_value(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('customer_id')['total_revenue'].sum().nlargest(10).to_dict()

    def get_discount_response_analysis(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('promo_code_used')['quantity'].sum().to_dict()

    def get_promo_vs_non_promo_spending(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('promo_code_used')['total_revenue'].mean().to_dict()

    def get_rating_purchase_correlation(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df[['review_rating', 'purchase_frequency']].corr().iloc[0,1]

    def get_weekday_vs_weekend_behavior(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('is_weekend')['total_revenue'].sum().to_dict()

    def get_shipping_preference_by_demo(self, demo='gender', filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby([demo, 'shipping_type']).size().unstack().to_dict()
    
        # -------------------- OPERATIONAL INSIGHTS --------------------
    def get_stocking_recommendations(self, filters=None):
        filtered_df = self._apply_filters(filters)
        # Recommend products with high trend_flag and popularity_score
        recommendations = filtered_df[
            (filtered_df['trend_flag'] == 'High') & 
            (filtered_df['popularity_score'] > filtered_df['popularity_score'].quantile(0.75))
        ]['item_purchased'].unique().tolist()
        return recommendations

    def get_seasonal_demand_spikes(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('season')['quantity'].sum().to_dict()

    def get_shipping_preferences_high_value(self, filters=None):
        filtered_df = self._apply_filters(filters)
        high_value = filtered_df[filtered_df['price'] > filtered_df['price'].quantile(0.75)]
        return high_value.groupby('shipping_type').size().to_dict()

    def get_shipping_impact_size_color(self, filters=None):
        filtered_df = self._apply_filters(filters)
        size_impact = filtered_df.groupby(['product_size', 'shipping_type']).size().unstack().to_dict()
        color_impact = filtered_df.groupby(['product_color', 'shipping_type']).size().unstack().to_dict()
        return {'size': size_impact, 'color': color_impact}

    def get_underperforming_categories(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('category')['total_revenue'].sum().nsmallest(5).to_dict()

    def get_payment_method_frequency(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df['payment_method'].value_counts().to_dict()

    def get_revenue_per_payment_method(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('payment_method')['total_revenue'].mean().to_dict()

    def get_multi_category_customers(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('customer_id')['category'].nunique().gt(1).sum()
    
        # -------------------- ADVANCED INSIGHTS --------------------
    def get_size_purchase_freq_correlation(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('product_size')['purchase_frequency'].mean().to_dict()

    def get_revenue_by_rating(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('review_rating')['total_revenue'].sum().to_dict()

    def get_discount_rating_correlation(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df[['discount_effectiveness', 'review_rating']].corr().iloc[0,1]

    def get_promo_usage_trends(self, period='month', filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(period)['promo_code_used'].mean().to_dict()

    def get_young_customer_trends(self, age_threshold=25, filters=None):
        filtered_df = self._apply_filters(filters)
        young_customers = filtered_df[filtered_df['age'] <= age_threshold]
        return young_customers.groupby('item_purchased')['popularity_score'].mean().nlargest(5).to_dict()

    def get_promo_usage_by_region(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('region')['promo_code_used'].mean().to_dict()

    def get_shipping_preferences_by_product(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(['item_purchased', 'shipping_type']).size().unstack().to_dict()

    def get_seasonal_impact(self, filters=None):
        filtered_df = self._apply_filters(filters)
        seasonal_rev = filtered_df.groupby('season')['total_revenue'].sum().to_dict()
        seasonal_cat = filtered_df.groupby(['season', 'category'])['total_revenue'].sum().unstack().to_dict()
        return {'revenue': seasonal_rev, 'category_sales': seasonal_cat}
    
        # -------------------- COMPARATIVE INSIGHTS --------------------
    def get_purchase_freq_by_region(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('region')['purchase_frequency'].mean().to_dict()

    def get_category_popularity_subscribed(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(['is_subscribed', 'category'])['quantity'].sum().unstack().to_dict()

    def get_gender_rating_differences(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('gender')['review_rating'].mean().to_dict()

    def get_avg_spending_subscribed_vs_non(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby('is_subscribed')['average_spending'].mean().to_dict()

    def get_urban_rural_category_preferences(self, filters=None):
        filtered_df = self._apply_filters(filters)
        return filtered_df.groupby(['region_type', 'category'])['quantity'].sum().unstack().to_dict()

analyzer = BusinessInsightsAnalyzer(df)

# -------------------- API ENDPOINTS --------------------
@app.route('/api/questions/sales_trends', methods=['GET'])
@cache.cached(timeout=3600)
def get_sales_questions():
    questions = [
        {"id": 1, "text": "Top 10 products by revenue", "func": "get_top_products_by_revenue", "viz": "bar"},
        {"id": 2, "text": "Product generating the most revenue", "func": "get_highest_revenue_product", "viz": "metric"},
        {"id": 3, "text": "Sales variation by month", "func": "get_sales_by_time_period", "viz": "line"},
        {"id": 4, "text": "Sales by weekday", "func": "get_sales_by_weekday", "viz": "bar"},
        {"id": 5, "text": "Top products by popularity", "func": "get_products_by_popularity", "viz": "bar"},
        {"id": 6, "text": "Revenue by season", "func": "get_revenue_by_season", "viz": "pie"},
        {"id": 7, "text": "Sales distribution by size/color", "func": "get_sales_distribution_size_color", "viz": "dual_bar"},
        {"id": 8, "text": "Discount effectiveness", "func": "get_discount_effectiveness", "viz": "bar"}
    ]
    return jsonify(questions)

@app.route('/api/insights/sales_trends/<int:question_id>', methods=['GET'])
@cache.memoize(timeout=3600)
def get_sales_insights(question_id):
    filters = request.args.to_dict()

    # Create context string based on applied filters
    context = []
    if filters.get('category'):
        context.append(f"Category: {filters['category']}")
    if filters.get('region'):
        context.append(f"Region: {filters['region']}")
    filter_text = f" ({', '.join(context)})" if context else ""

    try:
        if question_id == 1:
            result = analyzer.get_top_products_by_revenue(filters)
            viz = "bar"
        elif question_id == 2:
            result = analyzer.get_highest_revenue_product(filters)
            viz = "metric"
        elif question_id == 3:
            period = filters.get('period', 'month')
            result = analyzer.get_sales_by_time_period(period, filters)
            viz = "line"
        elif question_id == 4:
            result = analyzer.get_sales_by_weekday(filters)
            viz = "bar"
        elif question_id == 5:
            result = analyzer.get_products_by_popularity(filters)
            viz = "bar"
        elif question_id == 6:
            result = analyzer.get_revenue_by_season(filters)
            viz = "pie"
        elif question_id == 7:
            result = analyzer.get_sales_distribution_size_color(filters)
            viz = "dual_bar"
        elif question_id == 8:
            result = analyzer.get_discount_effectiveness(filters)
            viz = "bar"
        else:
            return jsonify({"error": "Question ID not found"}), 404
        
        return jsonify({
            "summary": "Sales & Product Trends Analysis",
            "data": result,
            "visualization": viz,
            "filter_text": filter_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#customer demographic endpoint
# -------------------- API ENDPOINTS --------------------
@app.route('/api/questions/customer_demographics', methods=['GET'])
@cache.cached(timeout=3600)
def get_customer_demo_questions():
    questions = [
        {"id": 1, "text": "Revenue by age group", "func": "get_revenue_by_age_group", "viz": "bar"},
        {"id": 2, "text": "Purchase distribution by gender", "func": "get_purchases_by_gender", "viz": "pie"},
        {"id": 3, "text": "Top regions by sales", "func": "get_top_regions_by_sales", "viz": "bar"},
        {"id": 4, "text": "Age group category preferences", "func": "get_age_category_preferences", "viz": "heatmap"},
        {"id": 5, "text": "Gender category preferences", "func": "get_gender_category_preferences", "viz": "heatmap"},
        {"id": 6, "text": "Average order value by region", "func": "get_avg_order_value_by_region", "viz": "bar"},
        {"id": 7, "text": "Subscribed vs. non-subscribed spending", "func": "get_subscribed_vs_non_subscribed", "viz": "bar"}
    ]
    return jsonify(questions)

@app.route('/api/insights/customer_demographics/<int:question_id>', methods=['GET'])
@cache.memoize(timeout=3600)
def get_customer_demo_insights(question_id):
    filters = request.args.to_dict()
    try:
        if question_id == 1:
            result = analyzer.get_revenue_by_age_group(filters)
            viz = "bar"
        elif question_id == 2:
            result = analyzer.get_purchases_by_gender(filters)
            viz = "pie"
        elif question_id == 3:
            result = analyzer.get_top_regions_by_sales(filters)
            viz = "bar"
        elif question_id == 4:
            result = analyzer.get_age_category_preferences(filters)
            viz = "heatmap"
        elif question_id == 5:
            result = analyzer.get_gender_category_preferences(filters)
            viz = "heatmap"
        elif question_id == 6:
            result = analyzer.get_avg_order_value_by_region(filters)
            viz = "bar"
        elif question_id == 7:
            result = analyzer.get_subscribed_vs_non_subscribed(filters)
            viz = "bar"
        else:
            return jsonify({"error": "Question ID not found"}), 404
        
        return jsonify({
            "summary": "Customer Demographics Analysis",
            "data": result,
            "visualization": viz
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#customer behavior endpoint
# -------------------- API ENDPOINTS --------------------
@app.route('/api/questions/customer_behavior', methods=['GET'])
@cache.cached(timeout=3600)
def get_customer_behavior_questions():
    questions = [
        {"id": 1, "text": "Average purchase frequency", "func": "get_avg_purchase_frequency", "viz": "metric"},
        {"id": 2, "text": "Category repurchase rate", "func": "get_category_repurchase_rate", "viz": "bar"},
        {"id": 3, "text": "Top customers by lifetime value", "func": "get_customer_lifetime_value", "viz": "bar"},
        {"id": 4, "text": "Discount response analysis", "func": "get_discount_response_analysis", "viz": "bar"},
        {"id": 5, "text": "Spending with/without promo codes", "func": "get_promo_vs_non_promo_spending", "viz": "bar"},
        {"id": 6, "text": "Rating vs. purchase frequency correlation", "func": "get_rating_purchase_correlation", "viz": "metric"},
        {"id": 7, "text": "Weekday vs. weekend behavior", "func": "get_weekday_vs_weekend_behavior", "viz": "bar"},
        {"id": 8, "text": "Shipping preferences by gender", "func": "get_shipping_preference_by_demo", "viz": "heatmap"}
    ]
    return jsonify(questions)

@app.route('/api/insights/customer_behavior/<int:question_id>', methods=['GET'])
@cache.memoize(timeout=3600)
def get_customer_behavior_insights(question_id):
    filters = request.args.to_dict()
    try:
        if question_id == 1:
            result = analyzer.get_avg_purchase_frequency(filters)
            viz = "metric"
        elif question_id == 2:
            result = analyzer.get_category_repurchase_rate(filters)
            viz = "bar"
        elif question_id == 3:
            result = analyzer.get_customer_lifetime_value(filters)
            viz = "bar"
        elif question_id == 4:
            result = analyzer.get_discount_response_analysis(filters)
            viz = "bar"
        elif question_id == 5:
            result = analyzer.get_promo_vs_non_promo_spending(filters)
            viz = "bar"
        elif question_id == 6:
            result = analyzer.get_rating_purchase_correlation(filters)
            viz = "metric"
        elif question_id == 7:
            result = analyzer.get_weekday_vs_weekend_behavior(filters)
            viz = "bar"
        elif question_id == 8:
            demo = filters.get('demo', 'gender')
            result = analyzer.get_shipping_preference_by_demo(demo, filters)
            viz = "heatmap"
        else:
            return jsonify({"error": "Question ID not found"}), 404
        
        return jsonify({
            "summary": "Customer Behavior Analysis",
            "data": result,
            "visualization": viz
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#operation insight endpoint
# -------------------- API ENDPOINTS --------------------
@app.route('/api/questions/operational_insights', methods=['GET'])
@cache.cached(timeout=3600)
def get_operational_questions():
    questions = [
        {"id": 1, "text": "Stocking recommendations", "func": "get_stocking_recommendations", "viz": "list"},
        {"id": 2, "text": "Seasonal demand spikes", "func": "get_seasonal_demand_spikes", "viz": "line"},
        {"id": 3, "text": "Shipping preferences for high-value products", "func": "get_shipping_preferences_high_value", "viz": "pie"},
        {"id": 4, "text": "Shipping impact by size/color", "func": "get_shipping_impact_size_color", "viz": "dual_heatmap"},
        {"id": 5, "text": "Underperforming categories", "func": "get_underperforming_categories", "viz": "bar"},
        {"id": 6, "text": "Popular payment methods", "func": "get_payment_method_frequency", "viz": "pie"},
        {"id": 7, "text": "Revenue per payment method", "func": "get_revenue_per_payment_method", "viz": "bar"},
        {"id": 8, "text": "Multi-category customers", "func": "get_multi_category_customers", "viz": "metric"}
    ]
    return jsonify(questions)

@app.route('/api/insights/operational_insights/<int:question_id>', methods=['GET'])
@cache.memoize(timeout=3600)
def get_operational_insights(question_id):
    filters = request.args.to_dict()
    try:
        if question_id == 1:
            result = analyzer.get_stocking_recommendations(filters)
            viz = "list"
        elif question_id == 2:
            result = analyzer.get_seasonal_demand_spikes(filters)
            viz = "line"
        elif question_id == 3:
            result = analyzer.get_shipping_preferences_high_value(filters)
            viz = "pie"
        elif question_id == 4:
            result = analyzer.get_shipping_impact_size_color(filters)
            viz = "dual_heatmap"
        elif question_id == 5:
            result = analyzer.get_underperforming_categories(filters)
            viz = "bar"
        elif question_id == 6:
            result = analyzer.get_payment_method_frequency(filters)
            viz = "pie"
        elif question_id == 7:
            result = analyzer.get_revenue_per_payment_method(filters)
            viz = "bar"
        elif question_id == 8:
            result = analyzer.get_multi_category_customers(filters)
            viz = "metric"
        else:
            return jsonify({"error": "Question ID not found"}), 404
        
        return jsonify({
            "summary": "Operational Insights Analysis",
            "data": result,
            "visualization": viz
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#advanced insight
# -------------------- API ENDPOINTS --------------------
@app.route('/api/questions/advanced_insights', methods=['GET'])
@cache.cached(timeout=3600)
def get_advanced_questions():
    questions = [
        {"id": 1, "text": "Product size vs. purchase frequency", "func": "get_size_purchase_freq_correlation", "viz": "bar"},
        {"id": 2, "text": "Revenue by review rating", "func": "get_revenue_by_rating", "viz": "scatter"},
        {"id": 3, "text": "Discounts vs. ratings correlation", "func": "get_discount_rating_correlation", "viz": "metric"},
        {"id": 4, "text": "Promo code usage trends", "func": "get_promo_usage_trends", "viz": "line"},
        {"id": 5, "text": "Young customers' trendy preferences", "func": "get_young_customer_trends", "viz": "bar"},
        {"id": 6, "text": "Promo usage by region", "func": "get_promo_usage_by_region", "viz": "heatmap"},
        {"id": 7, "text": "Shipping preferences by product", "func": "get_shipping_preferences_by_product", "viz": "heatmap"},
        {"id": 8, "text": "Seasonal revenue & category impact", "func": "get_seasonal_impact", "viz": "dual_line"}
    ]
    return jsonify(questions)

@app.route('/api/insights/advanced_insights/<int:question_id>', methods=['GET'])
@cache.memoize(timeout=3600)
def get_advanced_insights(question_id):
    filters = request.args.to_dict()
    try:
        if question_id == 1:
            result = analyzer.get_size_purchase_freq_correlation(filters)
            viz = "bar"
        elif question_id == 2:
            result = analyzer.get_revenue_by_rating(filters)
            viz = "scatter"
        elif question_id == 3:
            result = analyzer.get_discount_rating_correlation(filters)
            viz = "metric"
        elif question_id == 4:
            period = filters.get('period', 'month')
            result = analyzer.get_promo_usage_trends(period, filters)
            viz = "line"
        elif question_id == 5:
            result = analyzer.get_young_customer_trends(filters=filters)
            viz = "bar"
        elif question_id == 6:
            result = analyzer.get_promo_usage_by_region(filters)
            viz = "heatmap"
        elif question_id == 7:
            result = analyzer.get_shipping_preferences_by_product(filters)
            viz = "heatmap"
        elif question_id == 8:
            result = analyzer.get_seasonal_impact(filters)
            viz = "dual_line"
        else:
            return jsonify({"error": "Question ID not found"}), 404
        
        return jsonify({
            "summary": "Advanced Insights Analysis",
            "data": result,
            "visualization": viz
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#comparative insights
# -------------------- API ENDPOINTS --------------------
@app.route('/api/questions/comparative_insights', methods=['GET'])
@cache.cached(timeout=3600)
def get_comparative_questions():
    questions = [
        {"id": 1, "text": "Purchase frequency by region", "func": "get_purchase_freq_by_region", "viz": "bar"},
        {"id": 2, "text": "Category popularity: Subscribed vs. Non-Subscribed", "func": "get_category_popularity_subscribed", "viz": "heatmap"},
        {"id": 3, "text": "Review ratings by gender", "func": "get_gender_rating_differences", "viz": "bar"},
        {"id": 4, "text": "Average spending: Subscribed vs. Non-Subscribed", "func": "get_avg_spending_subscribed_vs_non", "viz": "bar"},
        {"id": 5, "text": "Urban vs. Rural category preferences", "func": "get_urban_rural_category_preferences", "viz": "heatmap"}
    ]
    return jsonify(questions)

@app.route('/api/insights/comparative_insights/<int:question_id>', methods=['GET'])
@cache.memoize(timeout=3600)
def get_comparative_insights(question_id):
    filters = request.args.to_dict()
    try:
        if question_id == 1:
            result = analyzer.get_purchase_freq_by_region(filters)
            viz = "bar"
        elif question_id == 2:
            result = analyzer.get_category_popularity_subscribed(filters)
            viz = "heatmap"
        elif question_id == 3:
            result = analyzer.get_gender_rating_differences(filters)
            viz = "bar"
        elif question_id == 4:
            result = analyzer.get_avg_spending_subscribed_vs_non(filters)
            viz = "bar"
        elif question_id == 5:
            result = analyzer.get_urban_rural_category_preferences(filters)
            viz = "heatmap"
        else:
            return jsonify({"error": "Question ID not found"}), 404
        
        return jsonify({
            "summary": "Comparative Insights Analysis",
            "data": result,
            "visualization": viz
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)