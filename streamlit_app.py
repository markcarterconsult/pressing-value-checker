import streamlit as st
import requests

# Discogs API Token
DISCOGS_TOKEN = "ebpdNwknvWEvijLOpBRFWeIRVGOOJRrAJstkCYPr"

# Function to search Discogs
def search_discogs(artist, title):
    base_url = "https://api.discogs.com/database/search"
    headers = {"User-Agent": "PressingValueChecker/1.0"}
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
                "discogs_url": first_result.get("resource_url"),
                "id": first_result.get("id")
            }
        else:
            return None
    except Exception as e:
        print("Discogs API error:", e)
        return None

# Function to get historical pricing stats from Discogs
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
        print("Price API error:", e)
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
        st.markdown("🔎 Searching Discogs...")

        result = search_discogs(artist_name, record_title)

        if result:
            st.success(f"🎉 Found: **{result['title']} ({result['year']})**")
            st.markdown(f"[🔗 View on Discogs]({result['discogs_url']})")

            if result.get("thumb"):
                st.image(result["thumb"], width=200)

            # Pricing stats
            price_data = get_discogs_price_stats(result["id"])
            if price_data:
                st.markdown("### 💵 Estimated Value Range")
                if price_data.get("lowest_price"):
                    st.write(f"🔻 **Lowest Sale Price:** ${price_data['lowest_price']:.2f}")
                if price_data.get("median_price"):
                    st.write(f"⚖️ **Median Sale Price:** ${price_data['median_price']:.2f}")
                if price_data.get("highest_price"):
                    st.write(f"🔺 **Highest Sale Price:** ${price_data['highest_price']:.2f}")
                if price_data.get("sales") is not None:
                    st.write(f"📈 **Total Sales Recorded:** {price_data['sales']}")
                if price_data.get("num_for_sale") is not None:
                    st.write(f"🛒 **Currently For Sale:** {price_data['num_for_sale']} listings")
            else:
                st.warning("⚠️ No price stats available for this release.")
        else:
            st.warning("⚠️ No matching release found on Discogs. Try adjusting the title or artist.")
    else:
        st.warning("Please complete all required fields.")
