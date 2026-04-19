import streamlit as st

# App title and header
st.title("📞 Distributor to Vendor Call Intelligence")
st.subheader("Analyze your call and generate actionable insights for the vendor")

# Input: Distributor transcript
st.markdown("### 📝 Enter Distributor Transcript")
transcript = st.text_area("Paste your 10–14 line mock transcript here", height=300)

# Simulated AI output
if transcript:
    st.markdown("### 🔍 AI-Generated Insights")

    # Problems raised by distributor
    st.markdown("#### 🧩 Problems Raised")
    problems = [
        "Lack of onboarding support for new sales reps",
        "Confusion around tiered pricing",
        "No access to technical documentation for new product line"
    ]
    for prob in problems:
        st.write(f"🔴 {prob}")

    # Suggested solutions from vendor resources
    st.markdown("#### 🛠️ Suggested Vendor Solutions")
    solutions = [
        "Provide Sales Rep Onboarding Kit",
        "Share Pricing Tier Explainer PDF",
        "Invite distributor to Technical Workshop (Oct 3)"
    ]
    for sol in solutions:
        st.write(f"🟢 {sol}")

    # Action items for vendor
    st.markdown("#### ✅ Vendor Follow-up Tasks")
    st.table([
        {"Task": "Send onboarding kit", "Owner": "Vendor AE", "Deadline": "Sep 28"},
        {"Task": "Clarify pricing tiers", "Owner": "Partner Manager", "Deadline": "Sep 27"},
        {"Task": "Schedule tech workshop", "Owner": "Solutions Engineer", "Deadline": "Sep 30"}
    ])

    # Sentiment analysis
    st.markdown("#### 😊 Sentiment Tags")
    sentiment_data = [
        {"Line": "We're excited to grow together", "Sentiment": "Positive"},
        {"Line": "Still unclear on pricing", "Sentiment": "Negative"},
        {"Line": "Thanks for the support", "Sentiment": "Positive"},
        {"Line": "Technical issues are slowing us down", "Sentiment": "Negative"}
    ]
    for item in sentiment_data:
        emoji = "🟢" if item["Sentiment"] == "Positive" else "🔴"
        st.write(f"{emoji} **{item['Sentiment']}** — {item['Line']}")

    st.success("Insights generated for vendor follow-up!")
