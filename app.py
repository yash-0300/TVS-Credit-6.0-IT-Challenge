import streamlit as st
import requests
from streamlit_lottie import st_lottie
import time
import pickle

# Lottie animation function
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function to calculate EMI, total payable, interest, and principal
def calculate_emi(loan_amount, annual_interest_rate, tenure_months):
    monthly_interest_rate = (annual_interest_rate / 12) / 100
    emi = loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**tenure_months / ((1 + monthly_interest_rate)**tenure_months - 1)
    total_payable = emi * tenure_months
    interest_amount = total_payable - loan_amount
    return emi, total_payable, interest_amount


# Load a Lottie animation for loan approval (verified URL)
lottie_animation_code = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_t9gkkhz4.json")

# Page configuration
st.set_page_config(page_title="TVS CredAssist", page_icon="💼", layout="wide")

# Set custom CSS for Google-themed colors
st.markdown("""
    <style>
    .reportview-container {
        background: #ffffff;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #4285F4, #34A853, #FBBC05, #EA4335);
    }
    .stTextInput > div > input {
        border: 2px solid #4285F4;
        padding: 10px;
        border-radius: 8px;
    }
    .stNumberInput > div > input {
        border: 2px solid #FBBC05;
        padding: 10px;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #34A853;
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stDateInput > div {
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #EA4335;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Lottie animation
st.title("💼 TVS Credit Loan Application")
if lottie_animation_code:
    st_lottie(lottie_animation_code, height=250, key="loan_approval")
else:
    st.error("Failed to load animation. Please check the URL.")

# Headline with catchy message
st.markdown("""
    <div style="text-align: center;">
    <h2 style="color: #4285F4; font-size: 40px;">Your Dream, Our Loan! Quick & Easy Application</h2>
    <p style="font-size: 20px;">Complete the form to apply for a loan in minutes.</p>
    </div>
    """, unsafe_allow_html=True)

# Loan Application Form
st.markdown("## 📋 Loan Details")

loan_type = st.selectbox("Select Loan Type", ["Two Wheeler Loan", "Used Car Loan", "Consumer Durable Loans", "Mobile Loans", "Online Personal Loans", "Gold Loans", "Tractor Loans", "Three Wheeler Loans"])
loan_amount = st.number_input("Loan Amount (in ₹)", min_value=10000, max_value=1000000000, value=None)
#  loan_rate = st.slider("Rate of Interest (p.a)", min_value=5, max_value=35)
loan_tenure = st.slider("Loan Tenure (in months)", min_value=6, max_value=36)
# cibil_score = st.number_input("Enter your Cibil Score", min_value=0, max_value=900, value=None)


# Personal Information
st.markdown("## 🧑 Personal Information")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
dob = st.date_input("Date of Birth", value=None)
contact_number = st.text_input("Contact Number")
address = st.text_area("Residential Address")

# Income Information
st.markdown("## 💵 Income Information")
monthly_income = st.number_input("Monthly Income (in ₹)", value=None)
employment_type = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Business", "Retired"])
existing_loan = st.radio("Do you have any existing loans?", ("Yes", "No"))


# Submit Button with action
if st.button("Submit Loan Application"):
    # Prediction Using Machine Learning Model
    with open('interest_rate_model.pkl', 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    test_data = [[loan_amount, loan_tenure, monthly_income]]
    loan_rate = loaded_model.predict(test_data)[0]
    
    with st.spinner("Submitting your application..."):
        time.sleep(2)
        st.success(f"Thank you {name}! Your {loan_type} application for ₹{loan_amount} is submitted!")
        st.success(f"Your Predicted Rate of Interest: {loan_rate}")

    
    if loan_amount and loan_rate and loan_tenure:
        emi, total_payable, interest_amount = calculate_emi(loan_amount, loan_rate, loan_tenure)
        
        # Display the results in a clean format
        st.markdown("## 💵 Loan EMI Breakdown")
        st.write(f"**Loan Amount (Principal)**: ₹{loan_amount:,.2f}")
        st.write(f"**Monthly EMI**: ₹{emi:,.2f}")
        st.write(f"**Total Interest Payable**: ₹{interest_amount:,.2f}")
        st.write(f"**Total Amount Payable (Principal + Interest)**: ₹{total_payable:,.2f}")

        # Styling the output in a nice table-like UI
        st.markdown("""
        <style>
        .result {
            font-size: 18px;
            font-weight: bold;
            color: #4285F4;
            padding: 10px;
        }
        .emi-box {
            background-color: #black;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="emi-box">
            <div class="result">💰 Monthly EMI: <span style="color: #34A853;">₹{emi:,.2f}</span></div>
            <div class="result">📈 Total Interest Payable: <span style="color: #EA4335;">₹{interest_amount:,.2f}</span></div>
            <div class="result">🏦 Total Amount Payable: <span style="color: #FBBC05;">₹{total_payable:,.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)



# Footer with branding
st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <h4 style="color: #FBBC05;"> Powered by TVS Credit Services 🚀</h4>
        <p>© TVS CredAssist | Ensuring your financial success</p>
    </div>
    """, unsafe_allow_html=True)
