import streamlit as st
import requests

DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"
HEADERS = {"User-Agent": "PressingValueChecker/1.0"}

def smart_discogs_match(artist, title, format_type, runout_matrix):
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

        for result in results[:20]:
            resource_url = result.get("resource_url")
            if resource_url:
                detail = requests.get(resource_url, headers=HEADERS).json()
                for identifier in detail.get("identifiers", []):
                    if identifier.get("type", "").lower() == "matrix / runout" and runout_matrix.lower() in identifier.get("value", "").lower():
                        return {
                            "title": detail.get("title"),
                            "year": detail.get("year"),
                            "thumb": result.get("thumb"),
                            "resource_url": detail.get("resource_url"),
                            "id": detail.get("id")
                        }

        # fallback to first match if no matrix match
        if results:
            fallback = results[0]
            return {
                "title": fallback.get("title"),
                "year": fallback.get("year"),
                "thumb": fallback.get("thumb"),
                "resource_url": fallback.get("resource_url"),
                "id": fallback.get("id")
            }

    except Exception as e:
        st.error(f"Discogs error: {e}")
        return None

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
if st.button("🔍 Search Pressing"):
    if name and email and record_title and artist_name:
        match = smart_discogs_match(artist_name, record_title, format_type, runout_matrix)

        if match:
            st.markdown("## 🎯 Best Match Found")
            st.markdown(f"**{match['title']} ({match['year']})**")
            st.caption(f"Discogs ID: {match['id']}")
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
            if stats and (stats.get("lowest_price") or stats.get("median_price") or stats.get("highest_price")):
                st.markdown("### 💰 Estimated Value")
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
            st.warning("⚠️ No matching pressing found based on your input.")
    else:
        st.warning("Please complete all required fields.")

# Disclaimer
st.markdown("---")
st.markdown(
    "#### ℹ️ Disclaimer\n"
    "_This tool uses the open Discogs API to provide estimated market values based on past sales and listings. "
    "Actual value can vary due to subjective grading, rare features, or collector demand._"
)
