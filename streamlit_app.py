import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import io
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Fadhu Perodua Financing Calculator", layout="centered")

# Define car data
car_data = {
    "Axia": {
        "E": 23100,
        "G": 40190,
        "X": 41630,
        "SE": 45740,
        "AV": 51390
    },
    "Bezza": {
        "G": 38170,
        "X": 45820,
        "AV": 51920
    },
    "Myvi": {
        "G": 50360,
        "X": 52860,
        "H": 56970,
        "AV": 62110
    },
    "Ativa": {
        "X": 64800,
        "H": 70220,
        "AV": 75720
    },
    "Alza": {
        "X": 64710,
        "H": 70380,
        "AV": 78070
    },
    "Aruz": {
        "X": 75600,
        "AV": 80700
    }
}

# Define interest rates and loan tenures
interest_rates_dict = {
    "Axia": [3.3],
    "Bezza": [3.3],
    "Myvi": [3.3],
    "Ativa": [2.7],
    "Alza": [2.7],
    "Aruz": [2.7]
}
loan_tenures = [5, 7, 9]

# Title
st.title("🚗 Fadhu Perodua Financing Calculator")

# Sidebar selections
st.sidebar.header("Select Car Details")
selected_car = st.sidebar.selectbox("Car Type", list(car_data.keys()))
selected_model = st.sidebar.selectbox("Model", list(car_data[selected_car].keys()))
selected_interest = st.sidebar.selectbox("Interest Rate (%)", interest_rates_dict[selected_car])
selected_tenure = st.sidebar.selectbox("Loan Tenure (Years)", loan_tenures)

# Rebate options for Ativa and Aruz
rebate = 0
if selected_car in ["Ativa", "Aruz"]:
    rebate_option = st.sidebar.selectbox("Rebate Option", ["None", "RM 1,000", "RM 3,500"])
    if rebate_option == "RM 1,000":
        rebate = 1000
    elif rebate_option == "RM 3,500":
        rebate = 3500

# Retrieve OTR price and apply rebate
otr_price = car_data[selected_car][selected_model] - rebate

# Calculate deposits
deposit_10_percent = otr_price * 0.10
deposit_10k = 10000
deposit_5k = 5000

# Function to calculate monthly payment
def calculate_monthly_payment(loan_amount, interest_rate, tenure_years):
    monthly_interest_rate = interest_rate / 100 / 12
    number_of_payments = tenure_years * 12
    if monthly_interest_rate == 0:
        return loan_amount / number_of_payments
    return loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments / ((1 + monthly_interest_rate) ** number_of_payments - 1)

# Calculate monthly payments
loan_full = otr_price
loan_10_percent = otr_price - deposit_10_percent
loan_10k = otr_price - deposit_10k
loan_5k = otr_price - deposit_5k

monthly_full = calculate_monthly_payment(loan_full, selected_interest, selected_tenure)
monthly_10_percent = calculate_monthly_payment(loan_10_percent, selected_interest, selected_tenure)
monthly_10k = calculate_monthly_payment(loan_10k, selected_interest, selected_tenure)
monthly_5k = calculate_monthly_payment(loan_5k, selected_interest, selected_tenure)

# Create DataFrame for display
data = {
    "Description": [
        "OTR Price (After Rebate)",
        "10% Deposit",
        "Monthly Payment (Full Loan)",
        "Monthly Payment (10% Deposit)",
        "Monthly Payment (RM 10k Deposit)",
        "Monthly Payment (RM 5k Deposit)",
        "Loan Tenure (Years)",
        "Interest Rate (%)"
    ],
    "Amount": [
        f"RM {otr_price:,.2f}",
        f"RM {deposit_10_percent:,.2f}",
        f"RM {monthly_full:,.2f}",
        f"RM {monthly_10_percent:,.2f}",
        f"RM {monthly_10k:,.2f}",
        f"RM {monthly_5k:,.2f}",
        f"{selected_tenure}",
        f"{selected_interest}"
    ]
}

df = pd.DataFrame(data)

# Display table without index
st.subheader(f"{selected_car} {selected_model} Financing Details")
st.table(df)

# Create Plotly table
fig = ff.create_table(df)

# Save the figure as a PNG image
img_bytes = fig.to_image(format="png")

# Convert PNG to JPG
img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
buffer = io.BytesIO()
img.save(buffer, format="JPEG")
buffer.seek(0)

# Download button
st.download_button(
    label="📸 Download Table as JPG",
    data=buffer,
    file_name=f"{selected_car}_{selected_model}_financing.jpg",
    mime="image/jpeg"
)

# Add note at the bottom
st.markdown(
    "<
::contentReference[oaicite:14]{index=14}
 
