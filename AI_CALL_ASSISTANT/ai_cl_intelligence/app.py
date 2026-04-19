import streamlit as st

# Sidebar role selection
st.sidebar.title("User Role")
role = st.sidebar.radio("Choose your role:", ["Vendor", "Distributor"])

# Header
st.title("🤝 AI Call Intelligence Assistant")
st.subheader(f"Welcome, {role}!")

# Transcript input
st.markdown("### 📝 Enter Call Transcript")
transcript = st.text_area("Paste your 10–14 line transcript here", height=300)

# Simulated NLP outputs
if transcript:
    st.markdown("### 🔍 Extracted Insights")

    if role == "Distributor":
        st.markdown("#### 🧩 Challenges You Raised")
        st.write([
            "Need better onboarding for new sales reps",
            "Confusion around tiered pricing",
            "Lack of technical support for new product line"
        ])

        st.markdown("#### ✅ Vendor Follow-ups")
        st.table([
            {"Task": "Send onboarding guide", "Owner": "Vendor AE", "Deadline": "Sep 28"},
            {"Task": "Clarify pricing tiers", "Owner": "Partner Manager", "Deadline": "Sep 27"},
            {"Task": "Schedule tech workshop", "Owner": "Solutions Engineer", "Deadline": "Sep 30"}
        ])

    elif role == "Vendor":
        st.markdown("#### 🛠️ Matched Solutions")
        st.write([
            "Sales Rep Onboarding Kit (PDF)",
            "Pricing Tier Explainer Video",
            "Technical Workshop Invite (Oct 3)"
        ])

        st.markdown("#### 📌 Action Items to Assign")
        st.table([
            {"Task": "Share onboarding kit", "Owner": "You", "Deadline": "Sep 28"},
            {"Task": "Send pricing video", "Owner": "You", "Deadline": "Sep 27"},
            {"Task": "Confirm workshop invite", "Owner": "You", "Deadline": "Sep 30"}
        ])

    st.markdown("#### 😊 Sentiment Tags")
    sentiment_data = [
        {"Line": "Thanks for the support last quarter", "Sentiment": "Positive"},
        {"Line": "We're still confused about pricing", "Sentiment": "Negative"},
        {"Line": "Looking forward to the bootcamp", "Sentiment": "Positive"},
        {"Line": "Technical issues are slowing us down", "Sentiment": "Negative"}
    ]

    for item in sentiment_data:
        color = "🟢" if item["Sentiment"] == "Positive" else "🔴" if item["Sentiment"] == "Negative" else "🟡"
        st.write(f"{color} **{item['Sentiment']}** — {item['Line']}")

    st.success("Call insights generated successfully!")
