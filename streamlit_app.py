import streamlit as st
import requests

# Discogs API Token
DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"

# Function to search Discogs
def search_discogs(artist, title, format_type):
    base_url = "https://api.discogs.com/database/search"
    headers = {"User-Agent": "PressingValueChecker/1.0"}
    params = {
        "artist": artist,
        "release_title": title,
        "format": format_type,
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
                "discogs_url": first_result.get("resource_url"),
                "id": first_result.get("id")
            }
        else:
            return None
    except Exception as e:
        st.error(f"Discogs API search error: {e}")
        return None

# Function to get historical pricing stats
def get_discogs_price_stats(release_id):
    try:
        headers = {"User-Agent": "PressingValueChecker/1.0"}
        stats_url = f"https://api.discogs.com/marketplace/stats/{release_id}"
        response = requests.get(stats_url, headers=headers)
        response.raise_for_status()
        stats = response.json()

        return {
            "lowest_price": stats["lowest_price"].get("value") if stats.get("lowest_price") else None,
            "median_price": stats["median_price"].get("value") if stats.get("median_price") else None,
            "highest_price": stats["highest_price"].get("value") if stats.get("highest_price") else None,
            "num_for_sale": stats.get("num_for_sale"),
            "sales": stats.get("sales")
        }
    except Exception as e:
        st.error(f"Discogs pricing error: {e}")
        return None

# Function to get pressing metadata
def get_pressing_details(resource_url):
    try:
        headers = {"User-Agent": "PressingValueChecker/1.0"}
        response = requests.get(resource_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        labels = ", ".join([label.get("name", "N/A") for label in data.get("labels", [])])
        catnos = ", ".join([label.get("catno", "N/A") for label in data.get("labels", [])])
        return {
            "country": data.get("country", "N/A"),
            "released": data.get("released_formatted", "N/A"),
            "labels": labels or "N/A",
            "catalog_numbers": catnos or "N/A"
        }
    except Exception as e:
        st.error(f"Error fetching pressing details: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Is This Pressing Valuable?", layout="centered")
st.title("🎶 Is This Pressing Valuable?")
st.subheader("Get a quick estimate based on your physical media pressing.")

# Lead Info
st.markdown("### 👤 Your Info")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

# Record Info
st.markdown("### 💿 Item Info")
record_title = st.text_input("Record Title")
artist_name = st.text_input("Artist Name")
format_type = st.selectbox("Format", ["Vinyl", "CD", "Cassette"])
vinyl_condition = st.selectbox("Media Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
sleeve_condition = st.selectbox("Sleeve/Case_
