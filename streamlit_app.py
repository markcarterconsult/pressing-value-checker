# (Top of file stays the same — skipping to bottom for brevity)

# Record Info
st.markdown("### 💿 Item Info")
record_title = st.text_input("Record Title")
artist_name = st.text_input("Artist Name")
format_type = st.selectbox("Format", ["Vinyl", "CD", "Cassette"])
vinyl_condition = st.selectbox("Media Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
sleeve_condition = st.selectbox("Sleeve/Case Condition", ["Mint (M)", "Near Mint (NM or M-)", "Very Good Plus (VG+)", "Very Good (VG)", "Good (G)", "Poor (P)"])
runout_matrix = st.text_input("Runout Matrix / Etchings (for vinyl only)")
notes = st.text_area("Additional Notes (e.g. colored vinyl, promo stamp, misprint)", placeholder="Optional...")

# Submit Button
if st.button("🔍 Check Value"):
    if name and email and record_title and artist_name:
        st.markdown("---")
        st.markdown("🔎 Searching Discogs...")

        result = search_discogs(artist_name, record_title, format_type)

        if result:
            st.success(f"🎉 Found: **{result['title']} ({result['year']})**")
            st.markdown(f"[🔗 View on Discogs]({result['discogs_url']})")

            if result.get("thumb"):
                st.image(result["thumb"], width=200)

            # Pressing Details
            pressing = get_pressing_details(result["discogs_url"])
            if pressing:
                st.markdown("### 📇 Pressing Details")
                st.write(f"**Country:** {pressing['country']}")
                st.write(f"**Label:** {pressing['labels']}")
                st.write(f"**Catalog #:** {pressing['catalog_numbers']}")
                st.write(f"**Released:** {pressing['released']}")

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

# Disclaimer at bottom of the app
st.markdown("---")
st.markdown(
    "#### ℹ️ Disclaimer\n"
    "_This tool uses the open Discogs API to provide estimated market values based on past sales and listings. "
    "Actual value can vary due to subjective grading, rare features, or collector demand. "
    "Always consult a professional appraiser or buyer for official valuations._"
)
