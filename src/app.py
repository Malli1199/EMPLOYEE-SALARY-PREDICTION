import streamlit as st
import pandas as pd
import joblib
import os

# Page Configurations & Setup
st.set_page_config(
    page_title='Salary Predictor Pro', 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Render Global Injectable Custom Styling
st.markdown("""
    <style>
    .main-header { font-size: 2.6rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; }
    div.stButton > button:first-child { background-color: #1E3A8A; color: white; border-radius: 6px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>Employee Salary Prediction Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>A clean corporate analytical system powered by automated CI/CD DevOps workflows.</div>", unsafe_allow_html=True)

# Path Resolution for Saved Pipeline Binary File
model_path = 'best_model_pipeline.pkl'

if not os.path.exists(model_path):
    st.error(f"🚨 Core engine binary mapping missing at `{model_path}`! Run the model training pipeline stage (`train.py`) first to generate it.")
    st.stop()

# Thread-safe cached loading of the model
@st.cache_resource
def load_pipeline():
    return joblib.load(model_path)

model = load_pipeline()

# Create Distinct Work Navigation Frames
tab1, tab2 = st.tabs(["🎯 Single Individual Evaluation", "📁 Bulk Batch Data Processing"])

with tab1:
    st.markdown("### Profile Demographics & Professional Structural Inputs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.slider("Age Range Allocation", 17, 75, 30)
        workclass = st.selectbox("Employment Structure Class", ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Notlisted"])
        education = st.selectbox("Highest Educational Achievement Level", ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th", "7th-8th", "12th", "Masters", "Doctorate", "10th"])

    with col2:
        marital_status = st.selectbox("Social Civil Matrix Status", ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"])
        occupation = st.selectbox("Designated Technical Job Role", ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty", "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving", "Priv-house-serv", "Protective-serv", "Armed-Forces", "Others"])
        relationship = st.selectbox("Household Structural Relationship Status", ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"])

    with col3:
        race = st.selectbox("Identified Demographic Race Group", ["White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"])
        gender = st.radio("Biological Gender", ["Male", "Female"], horizontal=True)
        hours_per_week = st.slider("Active Operations Labor Hours (Weekly)", 1, 99, 40)
        
    with st.expander("Advanced Core Financial Metrics (Optional Assets Entry)"):
        c1, c2 = st.columns(2)
        with c1: capital_gain = st.number_input("Capital Asset Investment Gains ($)", min_value=0, value=0, step=100)
        with c2: capital_loss = st.number_input("Capital Asset Investment Losses ($)", min_value=0, value=0, step=100)

    # Base Reference Constant Default String Setting 
    native_country = "United-States"

    # Match the exact schema layout expected by the Scikit-Learn Pipeline
    input_df = pd.DataFrame([{
        'age': age, 'workclass': workclass, 'education': education,
        'marital-status': marital_status, 'occupation': occupation,
        'relationship': relationship, 'race': race, 'gender': gender,
        'capital-gain': capital_gain, 'capital-loss': capital_loss,
        'hours-per-week': hours_per_week, 'native-country': native_country
    }])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Evaluate Target Income Bracket", type="primary"):
        # Inference running transparently through scaler, encoder, and model
        prediction = model.predict(input_df)[0]
        
        st.markdown("---")
        if prediction in [">50K", 1]:
            st.balloons()
            st.success("### 💎 Target Prediction: **High-Value Earner (> $50,000 / Year)**")
        else:
            st.info("### 💼 Target Prediction: **Standard Value Base Earner (≤ $50,000 / Year)**")

with tab2:
    st.markdown("### Upload Target Enterprise Records Dataset")
    uploaded_file = st.file_uploader("Drop standardized evaluation dataset CSV frames here", type="csv")
    
    if uploaded_file is not None:
        batch_data = pd.read_csv(uploaded_file)
        
        st.subheader("Data Input Inspection Matrix Preview")
        st.dataframe(batch_data.head(5), use_container_width=True)
        
        if st.button("Run Batch Inference Operations", type="primary"):
            try:
                # Direct prediction calculation
                batch_preds = model.predict(batch_data)
                
                # Format response presentation column
                batch_data['Predicted_Income_Class'] = batch_preds
                
                st.subheader("Annotated Inference Output Log View")
                st.dataframe(batch_data, use_container_width=True)
                
                # Prep payload for download
                csv_download_payload = batch_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Classified Predictions Sheet",
                    data=csv_download_payload,
                    file_name='batch_salary_classifications.csv',
                    mime='text/csv'
                )
            except Exception as error:
                st.error(f"Pipeline Analysis Execution Refused: Ensure structural columns line up precisely. Internal Details: {error}")