
import streamlit as st

from detector.analyzer import analyze_offer
from detector.database import (
    create_database,
    save_result,
    get_history,
    clear_history
)


# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="VerifyAI - Job Verification",
    page_icon="🛡️",
    layout="wide"
)

create_database()


# ---------------------------------
# CUSTOM CSS DESIGN
# ---------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #dbe3ef;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------

st.sidebar.title("🛡️ VerifyAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Verify Job",
        "History",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "AI-Based Fake Job & Internship Verification"
)


# ---------------------------------
# DASHBOARD PAGE
# ---------------------------------

if page == "Dashboard":

    st.title("🛡️ Job & Internship Verification")

    st.write(
        "Check job offers for suspicious recruitment "
        "patterns before accepting them."
    )

    history = get_history()

    total = len(history)

    high_risk = (
        int((history["verdict"] == "HIGH RISK").sum())
        if total else 0
    )

    needs_review = (
        int((history["verdict"] == "NEEDS REVIEW").sum())
        if total else 0
    )

    lower_risk = (
        int((history["verdict"] == "LOWER RISK").sum())
        if total else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Offers Checked", total)
    c2.metric("High Risk", high_risk)
    c3.metric("Needs Review", needs_review)
    c4.metric("Lower Risk", lower_risk)

    st.divider()

    st.subheader("How to use VerifyAI")

    st.write("1. Open the Verify Job page.")
    st.write("2. Enter the company and job details.")
    st.write("3. Paste the offer message.")
    st.write("4. Click Analyze Offer.")
    st.write("5. Read the risk score and warnings.")

    st.info(
        "The result is a risk estimate, not proof that a "
        "company is genuine or fraudulent."
    )

    if total > 0:
        st.subheader("Recent Verification Activity")

        st.dataframe(
            history.head(5),
            use_container_width=True,
            hide_index=True
        )


# ---------------------------------
# VERIFY JOB PAGE
# ---------------------------------

elif page == "Verify Job":

    st.title("🔍 Verify a Job or Internship")

    st.write(
        "Enter the details of the job offer you received."
    )

    with st.form("verification_form"):

        company = st.text_input("Company Name")

        title = st.text_input(
            "Job or Internship Title"
        )

        website = st.text_input(
            "Company Website (optional)",
            placeholder="https://example.com"
        )

        email = st.text_input(
            "Recruiter Email (optional)"
        )

        salary = st.number_input(
            "Monthly Salary (INR)",
            min_value=0,
            max_value=10000000,
            value=0,
            step=1000
        )

        payment = st.radio(
            "Does the recruiter ask for money?",
            ["No", "Yes", "Not sure"],
            horizontal=True
        )

        description = st.text_area(
            "Job Description or Offer Message",
            height=220,
            placeholder=(
                "Paste the complete job description or "
                "internship offer message here..."
            )
        )

        submitted = st.form_submit_button(
            "Analyze Offer",
            use_container_width=True
        )

    if submitted:

        if not company.strip() or not title.strip():

            st.error(
                "Please enter the company name and job title."
            )

        elif not description.strip():

            st.error(
                "Please paste the job description or offer message."
            )

        else:

            result = analyze_offer(
                company.strip(),
                title.strip(),
                description.strip(),
                website.strip(),
                email.strip(),
                payment,
                salary
            )

            save_result(
                company.strip(),
                title.strip(),
                result
            )

            st.divider()

            st.subheader("Verification Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Risk Score",
                f'{result["risk_score"]}/100'
            )

            col2.metric(
                "ML Suspicion Score",
                f'{result["ml_score"]}/100'
            )

            col3.metric(
                "Rule-Based Score",
                f'{result["rule_score"]}/100'
            )

            st.progress(
                result["risk_score"] / 100
            )

            if result["verdict"] == "HIGH RISK":

                st.error(
                    "🚨 HIGH RISK — Investigate carefully."
                )

            elif result["verdict"] == "NEEDS REVIEW":

                st.warning(
                    "⚠️ NEEDS REVIEW — Verify independently."
                )

            else:

                st.success(
                    "🟢 LOWER RISK — No strong configured "
                    "warning pattern was detected."
                )

            st.subheader("⚠️ Warning Signs")

            for warning in result["warnings"]:
                st.write(f"- {warning}")

            st.subheader("✅ Recommended Actions")

            for recommendation in result["recommendations"]:
                st.write(f"- {recommendation}")

            st.caption(
                "This is an educational prototype. Its score "
                "is not a validated fraud probability."
            )

            st.success(
                "Analysis saved to verification history."
            )


# ---------------------------------
# HISTORY PAGE
# ---------------------------------

elif page == "History":

    st.title("📋 Verification History")

    history = get_history()

    if history.empty:

        st.info(
            "No verification records yet. Analyze your "
            "first job offer to see it here."
        )

    else:

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

        csv_data = history.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download History as CSV",
            data=csv_data,
            file_name="job_verification_history.csv",
            mime="text/csv"
        )

        if st.button("Clear All History"):

            clear_history()

            st.success(
                "Verification history cleared."
            )

            st.rerun()


# ---------------------------------
# ABOUT PAGE
# ---------------------------------

else:

    st.title("About VerifyAI")

    st.write("""
    VerifyAI is a Python-based project that helps students
    analyze job and internship offers for potential warning signs.

    Technologies:
    - Python
    - Streamlit
    - Scikit-learn
    - TF-IDF
    - Logistic Regression
    - SQLite
    - Pandas

    Features:
    - Job description analysis
    - Suspicious-pattern detection
    - Machine-learning text classification
    - Risk scoring
    - Verification history
    - CSV export
    - Safety recommendations
    """)

    st.warning(
        "The current model uses a small illustrative dataset. "
        "Further training, evaluation, and independent company "
        "verification are required for reliable real-world use."
    )
