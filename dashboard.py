import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:5000/api"  # Flask backend URL

# -------------------- HELPER FUNCTIONS --------------------
def get_filter_text(filters):
    """Create context string based on applied filters"""
    context = []
    if filters.get('category'):
        context.append(f"Category: {filters['category']}")
    if filters.get('region'):
        context.append(f"Region: {filters['region']}")
    return f" ({', '.join(context)})" if context else ""

def fetch_questions(category):
    """Fetch questions for a category from the backend"""
    try:
        response = requests.get(f"{API_URL}/questions/{category}")
        return response.json() if response.status_code == 200 else []
    except:
        return []

def fetch_insights(category, question_id, filters=None):
    """Fetch insights for a specific question"""
    try:
        params = {k:v for k,v in (filters or {}).items() if v != "All"}
        response = requests.get(
            f"{API_URL}/insights/{category}/{question_id}",
            params=params
        )
        return response.json() if response.status_code == 200 else {"error": "API Failed"}
    except:
        return {"error": "API Failed"}

def render_visualization(data, viz_type):
    """Render Plotly chart based on visualization type"""
    if viz_type == "bar":
        fig = px.bar(x=list(data.keys()), y=list(data.values()))
    elif viz_type == "line":
        fig = px.line(x=list(data.keys()), y=list(data.values()))
    elif viz_type == "pie":
        fig = px.pie(names=list(data.keys()), values=list(data.values()))
    elif viz_type == "metric":
        fig = None
        st.metric("Result", data)
    elif viz_type == "dual_bar":
        fig1 = px.bar(x=list(data['size'].keys()), y=list(data['size'].values()), title="By Size")
        fig2 = px.bar(x=list(data['color'].keys()), y=list(data['color'].values()), title="By Color")
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)
        return
    st.plotly_chart(fig)

# -------------------- DASHBOARD LAYOUT --------------------
st.set_page_config(layout="wide")
st.title("TrendLens Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox("Region", ["All"] + list(pd.read_csv("C:/Users/shaya/Downloads/shop/processed_dataset.csv")['region'].unique()))
selected_category = st.sidebar.selectbox("Category", ["All"] + list(pd.read_csv("C:/Users/shaya/Downloads/shop/processed_dataset.csv")['category'].unique()))

# Initialize tabs
tabs = st.tabs(["Sales Trends", "Customer Demographics", "Customer Behavior", 
               "Operational Insights", "Advanced Insights", "Comparative Insights"])

# -------------------- SALES TRENDS TAB --------------------
with tabs[0]:
    st.subheader("Sales & Product Trends Analysis")
    
    # Fetch questions from backend
    questions = fetch_questions("sales_trends")
    
    if not questions:
        st.warning("No questions found for this category.")
    else:
        # Question selection
        selected_question = st.selectbox(
            "Select a Question", 
            questions, 
            format_func=lambda x: x['text'],
            key="sales_question"
        )
        
        if st.button("Analyze", key="sales_analyze"):
            # Prepare filters
            filters = {
                "region": selected_region,
                "category": selected_category
            }
            # if selected_region != "All":
                # filters["region"] = selected_region
            # if selected_category != "All":
                # filters["category"] = selected_category
            
            # Fetch insights
            insights = fetch_insights("sales_trends", selected_question['id'], filters)
            
            if "error" in insights:
                st.error(insights["error"])
            else:
                # Display results
                filter_text = get_filter_text(filters)
                st.subheader(insights["summary"])
                render_visualization(insights["data"], insights["visualization"])
                
                # Show raw data
                with st.expander("View Raw Data"):
                    if isinstance(insights["data"], dict):
                        st.write(pd.DataFrame(insights["data"].items(), columns=["Key", "Value"]))
                    else:
                        st.write(insights["data"])

