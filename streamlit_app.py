import streamlit as st
import requests

DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"
HEADERS = {"User-Agent": "PressingValueChecker/1.0"}

# Get top 3 Discogs matches
def get_discogs_matches(artist, title, format_type):
    url = "https://api.discogs.com/database/search"
    params = {
        "artist": artist,
        "release_title": title,
        "format": format_type,
        "type": "release",
        "token": DISCOGS_TOKEN
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])[:3]

        return [
            {
                "title": r.get("title", ""),
                "year": r.get("year", "Unknown"),
                "thumb": r.get("thumb"),
                "resource_url": r.get("resource_url"),
                "id": r.get("id")
            } for r in results
        ]
    except Exception as e:
        st.error(f"Discogs search error: {e}")
        return []

# Get pressing metadata
def get_pressing_details(resource_url):
    try:
        response = requests.get(resource_url, headers=HEADERS)
        data = response.json()
        labels = ", ".join([label.get("name", "N/A") for label in data.get("labels", [])])
        catnos = ", ".join([label.get("catno", "—") for label in data.get("labels", [])])
        return {
            "country": data.get("country", "N/A"),
            "released": data.get("released_formatted", "N/A"),
            "labels": labels or "N/A",
            "catalog_numbers": catnos or "—"
        }
    except Exception as e:
        st.error(f"Error fetching pressing details: {e}")
        return None

# Get pricing stats
def get_discogs_price_stats(release_id):
    try:
        stats_url = f"https://api.discogs.com/marketplace/stats/{release_id}"
        response = requests.get(stats_url, headers=HEADERS)
        stats = response.json()
        return {
            "lowest_price": stats["lowest_price"].get("value") if stats.get("lowest_price") else None,
            "median_price": stats["median_price"].get("value") if stats.get("median_price") else None,
            "highest_price": stats["highest_price"].get("value") if stats.get("highest_price") else None,
            "num_for_sale": stats.get("num_for_sale", 0),
            "sales": stats.get("sales", 0)
        }
    except Exception as e:
        st.error(f"Discogs pricing error: {e}")
        return None

# UI
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
sleeve_condition = st.selectbox("Sleeve/Case Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
runout_matrix = st.text_input("Runout Matrix / Etchings (for vinyl only)")
notes = st.text_area("Additional Notes (e.g. colored vinyl, promo stamp, misprint)", placeholder="Optional...")

# Run Search
if st.button("🔍 Search Pressings"):
    if name and email and record_title and artist_name:
        matches = get_discogs_matches(artist_name, record_title, format_type)

        if matches:
            st.markdown("## 📦 Top Matching Pressings")
            for i, match in enumerate(matches):
                st.markdown(f"---\n### 🔹 {match['title']} ({match['year']})")
                st.caption(f"Discogs ID: {match['id']}")  # Debug line

                if match.get("thumb"):
                    st.image(match["thumb"], width=200)
                else:
                    st.info("🖼 No cover image available.")

                st.markdown(f"[🔗 View on Discogs]({match['resource_url']})")

                # Pressing info
                details = get_pressing_details(match["resource_url"])
                if details:
                    st.markdown("#### 🏷️ Pressing Details")
                    st.write(f"**Country:** {details['country']}")
                    st.write(f"**Label:** {details['labels']}")
                    st.write(f"**Catalog #:** {details['catalog_numbers']}")
                    st.write(f"**Released:** {details['released']}")

                # Pricing
                stats = get_discogs_price_stats(match["id"])
                if stats and (
                    stats.get("lowest_price") or stats.get("median_price") or stats.get("highest_price")
                ):
                    st.markdown("#### 💰 Estimated Value")
                    if stats.get("lowest_price"):
                        st.write(f"🔻 **Lowest Sale Price:** ${stats['lowest_price']:.2f}")
                    if stats.get("median_price"):
                        st.write(f"⚖️ **Median Sale Price:** ${stats['median_price']:.2f}")
                    if stats.get("highest_price"):
                        st.write(f"🔺 **Highest Sale Price:** ${stats['highest_price']:.2f}")
                    st.write(f"📈 **Sales Recorded:** {stats['sales']}")
                    if stats['num_for_sale'] > 0:
                        st.write(f"🛒 **Currently For Sale:** {stats['num_for_sale']} listings")
                    else:
                        st.warning("❗ This pressing is not currently for sale.")
                else:
                    st.info("💡 No recent pricing data available. This pressing may be rare or hasn’t sold recently.")
        else:
            st.warning("No matching pressings found. Try adjusting your artist or title.")
    else:
        st.warning("Please complete all required fields.")

# Disclaimer
st.markdown("---")
st.markdown(
    "#### ℹ️ Disclaimer\n"
    "_This tool uses the open Discogs API to provide estimated market values based on past sales and listings. "
    "Actual value can vary due to subjective grading, rare features, or collector demand._"
)
