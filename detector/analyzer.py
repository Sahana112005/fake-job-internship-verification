
from detector.ml_model import predict_suspicion
import re


def analyze_offer(
    company, title, description,
    website, email, payment, salary
):
    warnings = []
    rule_score = 0

    text = (
        company + " " + title + " " + description
    ).lower()

    # Check payment requests
    payment_words = [
        "registration fee",
        "security deposit",
        "processing fee",
        "job confirmation fee",
        "pay immediately",
        "pay for the interview",
        "refundable deposit"
    ]

    if any(word in text for word in payment_words):
        warnings.append(
            "The offer mentions a recruitment fee or deposit."
        )
        rule_score += 35

    # Check urgency
    urgency_words = [
        "act now", "immediately",
        "limited vacancies", "urgent hiring",
        "last chance", "today only"
    ]

    if any(word in text for word in urgency_words):
        warnings.append(
            "The message pressures you to act quickly."
        )
        rule_score += 15

    # Check sensitive information requests
    sensitive_words = [
        "share your otp",
        "bank password",
        "send your password",
        "share your pin"
    ]

    if any(word in text for word in sensitive_words):
        warnings.append(
            "The message requests sensitive credentials."
        )
        rule_score += 40

    # Check website
    if not website.strip():
        warnings.append(
            "No company website was provided."
        )
        rule_score += 10

    # Check email
    if email.strip():
        email = email.strip().lower()

        if not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", email
        ):
            warnings.append(
                "The email address format is invalid."
            )
            rule_score += 15

        elif re.search(
            r"@(gmail|yahoo|outlook|hotmail)\.com$", email
        ):
            warnings.append(
                "The recruiter uses a generic email provider. "
                "Verify the recruiter independently."
            )
            rule_score += 10

    # Check payment answer
    if payment == "Yes":
        warnings.append(
            "You confirmed that the recruiter asks for money."
        )
        rule_score += 15

    elif payment == "Not sure":
        warnings.append(
            "Clarify whether any payment is required."
        )
        rule_score += 5

    # Check unusually high salary
    if salary >= 200000:
        warnings.append(
            "Verify the unusually high monthly salary independently."
        )
        rule_score += 10

    rule_score = min(rule_score, 100)

    ml_score = predict_suspicion(description)

    final_score = round(
        (ml_score * 0.5) + (rule_score * 0.5)
    )

    if final_score >= 60:
        verdict = "HIGH RISK"
    elif final_score >= 30:
        verdict = "NEEDS REVIEW"
    else:
        verdict = "LOWER RISK"

    if not warnings:
        warnings.append(
            "No configured rule-based warning signs were found."
        )

    recommendations = [
        "Check the official company careers website.",
        "Verify the recruiter using independent contact details.",
        "Check the email domain and offer letter.",
        "Never share OTPs, passwords or banking credentials.",
        "Avoid suspicious recruitment fees and deposits."
    ]

    return {
        "risk_score": final_score,
        "ml_score": ml_score,
        "rule_score": rule_score,
        "verdict": verdict,
        "warnings": warnings,
        "recommendations": recommendations
    }
