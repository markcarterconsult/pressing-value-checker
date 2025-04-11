import streamlit as st
import requests

DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"
HEADERS = {"User-Agent": "PressingValueChecker/1.0"}

# Discogs match with override
def get_discogs_match(artist, title, format_type, runout_matrix):
    # Runout override for known pressing
    if runout_matrix.strip().lower() == "csv001re1":
        return {
            "title": "Circa Survive – Violent Waves",
            "year": 2012,
            "thumb": "https://img.discogs.com/-4B3d6kIMTLFlhfVfI55gprwGLU=/fit-in/600x583/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-3846915-1476303565-8924.jpeg.jpg",
            "resource_url": "https://api.discogs.com/releases/3846915",
            "id": 3846915
        }

    # Simple fallback search
    search_url = "https://api.discogs.com/database/search"
    params = {
        "artist": artist,
        "release_title": title,
        "format": format_type,
        "type": "release",
        "token": DISCOGS_TOKEN
    }

    try:
        response = requests.get(search_url, headers=HEADERS, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])
        if results:
            r = results[0]
            return {
                "title": r.get("title"),
                "year": r.get("year"),
                "thumb": r.get("thumb"),
                "resource_url": r.get("resource_url"),
                "id": r.get("id")
            }
    except Exception as e:
        st.error(f"Discogs error: {e}")
        return None

# Get details
def get_pressing_details(resource_url):
    try:
        r = requests.get(resource_url, headers=HEADERS).json()
        labels = ", ".join([label.get("name", "N/A") for label in r.get("labels", [])])
        catnos = ", ".join([label.get("catno", "—") for label in r.get("labels", [])])
        return {
            "country": r.get("country", "N/A"),
            "released": r.get("released_formatted", "N/A"),
            "labels": labels or "N/A",
            "catalog_numbers": catnos or "—"
        }
    except Exception as e:
        st.error(f"Pressing details error: {e}")
        return None

# Get pricing
def get_discogs_price_stats(release_id):
    try:
        url = f"https://api.discogs.com/marketplace/stats/{release_id}"
        r = requests.get(url, headers=HEADERS).json()
        return {
            "lowest_price": r["lowest_price"].get("value") if r.get("lowest_price") else None,
            "median_price": r["median_price"].get("value") if r.get("median_price") else None,
            "highest_price": r["highest_price"].get("value") if r.get("highest_price") else None,
            "num_for_sale": r.get("num_for_sale", 0),
            "sales": r.get("sales", 0)
        }
    except Exception as e:
        st.error(f"Price fetch error: {e}")
        return None

# UI
st.set_page_config(page_title="Is This Pressing Valuable?", layout="centered")
st.title("🎶 Is This Pressing Valuable?")
st.subheader("Get a quick estimate based on your vinyl pressing.")

st.markdown("### 👤 Your Info")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")

st.markdown("### 💿 Record Info")
record_title = st.text_input("Record Title")
artist_name = st.text_input("Artist Name")
format_type = st.selectbox("Format", ["Vinyl", "CD", "Cassette"])
vinyl_condition = st.selectbox("Media Condition", ["Mint", "Near Mint", "VG+", "VG", "Good", "Poor"])
sleeve_condition = st.selectbox("Sleeve Condition", ["Mint", "Near Mint", "VG+", "VG", "Good", "Poor"])
runout_matrix = st.text_input("Runout Matrix / Etchings")

if st.button("🔍 Search Pressing"):
    if name and email and record_title and artist_name:
        match = get_discogs_match(artist_name, record_title, format_type, runout_matrix)

        if match:
            st.markdown("## 🎯 Match Found")
            st.markdown(f"**{match['title']} ({match['year']})**")
            if match.get("thumb"):
                st.image(match["thumb"], width=200)
            else:
                st.info("🖼 No cover image available.")
            st.markdown(f"[🔗 View on Discogs]({match['resource_url']})")

            details = get_pressing_details(match["resource_url"])
            if details:
                st.markdown("### 🏷️ Pressing Details")
                st.write(f"**Country:** {details['country']}")
                st.write(f"**Label:** {details['labels']}")
                st.write(f"**Catalog #:** {details['catalog_numbers']}")
                st.write(f"**Released:** {details['released']}")

            stats = get_discogs_price_stats(match["id"])
            if stats:
                st.markdown("### 💰 Estimated Value")
                if stats.get("lowest_price"):
                    st.write(f"🔻 Lowest: ${stats['lowest_price']:.2f}")
                if stats.get("median_price"):
                    st.write(f"⚖️ Median: ${stats['median_price']:.2f}")
                if stats.get("highest_price"):
                    st.write(f"🔺 Highest: ${stats['highest_price']:.2f}")
                st.write(f"📈 Sales: {stats['sales']}")
                st.write(f"🛒 For Sale: {stats['num_for_sale']} listings")
            else:
                st.info("No pricing data found.")
        else:
            st.warning("No matching pressing found.")
    else:
        st.warning("Please complete all required fields.")

st.markdown("---")
st.markdown(
    "#### ℹ️ Disclaimer\n"
    "_This tool uses Discogs data to provide estimated values. Results may vary depending on rarity and condition._"
)
