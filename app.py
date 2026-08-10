import streamlit as st
import pickle
import numpy as np

# Load the Random Forest Regressor model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Configure the Streamlit page
st.set_page_config(page_title="IPL Score Predictor", page_icon="🏏", layout="centered")

# Custom CSS for a beautiful modern design
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .title-text {
        font-family: 'Outfit', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4, #FFE66D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        text-align: center;
        color: #a0aab2;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 30px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4ECDC4 0%, #556270 100%);
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #556270 0%, #4ECDC4 100%);
        color: white;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='title-text'>IPL First Innings Score Predictor 🏏</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Predict the first innings total using machine learning</p>", unsafe_allow_html=True)

# Define consistent teams
teams = [
    'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
]

# Create columns for user input layout
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('🏏 Batting Team', teams, index=0)
with col2:
    bowling_team = st.selectbox('🎯 Bowling Team', teams, index=1)

st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)

with col3:
    overs = st.number_input('📊 Current Overs', min_value=5.0, max_value=19.5, value=5.1, step=0.1)
    runs = st.number_input('🏃 Current Runs', min_value=0, max_value=300, value=50, step=1)
with col4:
    wickets = st.number_input('🏏 Wickets Out', min_value=0, max_value=9, value=0, step=1)
    runs_in_prev_5 = st.number_input('🔥 Runs in last 5 overs', min_value=0, max_value=100, value=50, step=1)
with col5:
    wickets_in_prev_5 = st.number_input('⚾ Wickets in last 5 overs', min_value=0, max_value=9, value=0, step=1)

# Prediction Logic
if st.button('Predict Final Score ✨'):
    if batting_team == bowling_team:
        st.error("Batting and Bowling teams cannot be the same!")
    else:
        temp_array = list()
        
        # Batting Team One-Hot Encode
        for team in teams:
            if team == batting_team:
                temp_array.append(1)
            else:
                temp_array.append(0)
                
        # Bowling Team One-Hot Encode
        for team in teams:
            if team == bowling_team:
                temp_array.append(1)
            else:
                temp_array.append(0)
                
        # Append numerical features
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
        # Convert to numpy array
        data = np.array([temp_array])
        
        # Make Prediction
        my_prediction = int(model.predict(data)[0])
        
        lower_limit = my_prediction - 10
        upper_limit = my_prediction + 5
        
        # Display Result nicely
        st.markdown(f"""
            <div class='prediction-card'>
                <h3 style='color: #4ECDC4; margin-bottom: 10px;'>Predicted Score Range</h3>
                <h1 style='font-size: 3.5rem; margin: 0; padding: 0;'>{lower_limit} - {upper_limit}</h1>
            </div>
        """, unsafe_allow_html=True)
