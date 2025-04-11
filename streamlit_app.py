import streamlit as st
import requests

# Discogs API Token
DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"

# Search Discogs for matching release
def search_discogs(artist, title):
    base_url = "https://api.discogs.com/database/search"
    headers = {
        "User-Agent": "PressingValueChecker/1.0"
    }
    params = {
        "artist": artist,
        "release_title": title,
        "type": "release",
        "token": DISCOGS_TOKEN
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        if results.get("results"):
            first_result = results["results"][0]
            return {
                "title": first_result.get("title"),
                "year": first_result.get("year"),
                "thumb": first_result.get("thumb"),
                "discogs_url": first_result.get("resource_url")
            }
        else:
            return None
    except Exception as e:
        print("Discogs API error:", e)
        return None


# Streamlit UI
st.set_page_config(page_title="Is This Pressing Valuable?", layout="centered")
st.title("🎶 Is This Pressing Valuable?")
st.subheader("Get a quick estimate based on your vinyl pressing details.")

# Lead Info
st.markdown("### 👤 Your Info")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# Record Info
st.markdown("### 💿 Record Info")
record_title = st.text_input("Record Title")
artist_name = st.text_input("Artist Name")
vinyl_condition = st.selectbox("Vinyl Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
sleeve_condition = st.selectbox("Sleeve Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
runout_matrix = st.text_input("Runout Matrix / Etchings (dead wax)")

# Submit Button
if st.button("🔍 Check Value"):
    if name and email and record_title and artist_name:
        st.markdown("---")
        st.markdown("Searching Discogs...")

        result = search_discogs(artist_name, record_title)

        if result:
            st.success(f"🎉 Found: **{result['title']} ({result['year']})**")
            st.markdown(f"[🔗 View on Discogs]({result['discogs_url']})")

            if result.get("thumb"):
                st.image(result["thumb"], width=200)

            st.info("💰 This pressing may be worth between **$25–$100**, depending on condition. (Simulated for now.)")
        else:
            st.warning("⚠️ No matching release found on Discogs. Try adjusting the title or artist.")
    else:
        st.warning("Please complete all required fields.")
