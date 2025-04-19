# FRONTEND /STREAMLIT APP

import streamlit as st
import requests
import pandas as pd

# Configuring page
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")
st.title("SHL Assessment Recommendation System")

# Input area
input_type = st.radio("Input type:", ["Natural Language Query", "Job Description Text", "Job Description URL"])

if input_type == "Natural Language Query":
    query = st.text_input("Enter your query:")
elif input_type == "Job Description Text":
    query = st.text_area("Paste job description:")
else:
    query = st.text_input("Enter job description URL:")

duration_filter = st.slider("Maximum assessment duration (minutes):", 5, 120, 60)

# Recommendation button
if st.button("Get Recommendations") and query:
    with st.spinner("Finding the best assessments..."):
        # Call API
        response = requests.post(
            "http://localhost:8000/recommend",
            json={"query": query}
        )
        
        if response.status_code == 200:
            recommendations = response.json()["recommended_assessments"]
            
            # Applying duration filter
            filtered_recommendations = [r for r in recommendations if r["duration"] <= duration_filter]
            
            # Displaying results
            st.subheader(f"Top {len(filtered_recommendations)} Recommended Assessments")
            
            for i, rec in enumerate(filtered_recommendations, 1):
                with st.expander(f"{i}. {rec['description'][:100]}..."):
                    st.markdown(f"**Test type:** {', '.join(rec['test_type'])}")
                    st.markdown(f"**Duration:** {rec['duration']} minutes")
                    st.markdown(f"**Remote Testing Support:** {rec['remote_support']}")
                    st.markdown(f"**Adaptive/IRT Support:** {rec['adaptive_support']}")
                    st.markdown(f"**URL:** [{rec['url']}]({rec['url']})")
        else:
            st.error("Error getting recommendations. Please try again.")
