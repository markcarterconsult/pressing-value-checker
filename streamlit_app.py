import streamlit as st

st.set_page_config(page_title="Is This Pressing Valuable?", layout="centered")

st.title("🎶 Is This Pressing Valuable?")
st.subheader("Get a quick estimate based on your vinyl pressing details.")

# Lead info first
st.markdown("### 👤 Your Info")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# Record details
st.markdown("### 💿 Record Info")
record_title = st.text_input("Record Title")
artist_name = st.text_input("Artist Name")
vinyl_condition = st.selectbox("Vinyl Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
sleeve_condition = st.selectbox("Sleeve Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
runout_matrix = st.text_input("Runout Matrix / Etchings (dead wax)")

# Submit button
if st.button("🔍 Check Value"):
    if name and email and record_title and artist_name:
        st.success(f"🎉 Based on your info, your pressing of **{record_title}** might be worth **$45–$85** in {vinyl_condition} condition.")
        st.info("We'll send you more detailed info by email soon.")
    else:
        st.warning("Please complete all required fields.")

