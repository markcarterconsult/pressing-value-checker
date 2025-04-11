import streamlit as st
import requests

# Discogs API Token
DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"

# Function to search Discogs
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
    response = requests.get(base_url, headers=headers, params=params)
    results = response.json()

    if results.get("results"):
        first_result = results["results"][0]
        return {
            "title": first_result.get("title"),
            "year": first_result.get("year"),
            "thumb": first_result.get("thumb"),
            "discogs_url": first_result.get("resource_url")
        }
    return None


# Streamlit UI
st.set_page_config(page_title="Is This Pressing Valuable?", layout="centered")
