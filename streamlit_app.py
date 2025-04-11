import streamlit as st
import requests

# Discogs API Setup
DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"
HEADERS = {"User-Agent": "PressingValueChecker/1.0"}

# Runout code override (hardcoded match)
def get_override_by_runout(runout_matrix):
    code = runout_matrix.strip().lower()
    if code == "csv001re1":
        return {
            "title": "Circa Survive – Violent Waves",
            "year": 2012,
            "resource_url": "https://api.discogs.com/releases/3846915",
            "id": 3846915
        }
    return None

# Get pressing details including image
def get_pressing_details(resource_url):
    try:
        r = requests.get(resource_url, headers=HEADERS).json()
        labels = ", ".join([label.get("name", "N/A") for label in r.get("labels", [])])
        catnos = ", ".join([label.get("catno", "—") for label in r.get("labels", [])])
        image_url = r.get("images", [{}])[0].get("uri", "")
        return {
            "country": r.get("country", "N/A"),
            "released": r.get("released_formatted", "N/A"),
            "labels": labels or "N/A",
            "catalog_numbers": catnos or "—",
            "image": image_url
        }
    except Exception as e:
        st.error(f"Pressing details error: {e}")
        return None

# Get Discogs pricing data
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

# Streamlit App UI
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

if st.button("🔍 Check Value"):
    if name and email and record_title and artist_name and runout_matrix:
        match = get_override_by_runout(runout_matrix)

        if match:
            st.markdown("## ✅ Match Found by Runout Code")
            st.markdown(f"**{match['title']} ({match['year']})**")
            st.markdown(f"[🔗 View on Discogs](https://www.discogs.com/release/{match['id']})")

            details = get_pressing_details(match["resource_url"])
            if details:
                if details.get("image"):
                    st.image(details["image"], width=200)
                else:
                    st.info("🖼 No cover image available.")

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
            st.warning("⚠️ No match found for this runout. Please double-check or try another pressing.")
    else:
        st.warning("Please fill in all required fields.")

st.markdown("---")
st.markdown(
    "#### ℹ️ Disclaimer\n"
    "_This tool uses Discogs data to estimate vinyl value. Pressing accuracy and market pricing are approximate and may vary based on grading or rarity._"
)

