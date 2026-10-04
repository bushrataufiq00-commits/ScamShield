def check_message(message):

    score = 0
    reasons = []

    text = message.lower()

    # Urgency
    if "urgent" in text or "immediately" in text:
        score += 20
        reasons.append("Urgency detected")

    # Account threats
    if "account" in text and (
        "blocked" in text
        or "suspended" in text
        or "closed" in text
    ):
        score += 25
        reasons.append("Account threat detected")

    # Sensitive information
    if "otp" in text:
        score += 30
        reasons.append("OTP request detected")

    if "password" in text:
        score += 30
        reasons.append("Password request detected")

    if "pin" in text:
        score += 25
        reasons.append("PIN request detected")

    # Verification
    if "verify" in text or "verification" in text:
        score += 20
        reasons.append("Verification request detected")

    # Money / rewards
    if "prize" in text or "winner" in text:
        score += 20
        reasons.append("Prize or reward claim detected")

    if "payment" in text or "transfer money" in text:
        score += 25
        reasons.append("Payment request detected")

    # Keep score between 0 and 100
    if score > 100:
        score = 100

    # Decide result
    if score >= 60:
        result = "Likely Scam"
    elif score >= 30:
        result = "Suspicious"
    else:
        result = "Safe"

    return score, result, reasons


def check_url(url):

    score = 0
    reasons = []

    url_lower = url.lower()

    # HTTP instead of HTTPS
    if url_lower.startswith("http://"):
        score += 15
        reasons.append("URL does not use HTTPS")

    # URL shorteners
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "is.gd"
    ]

    for shortener in shorteners:
        if shortener in url_lower:
            score += 20
            reasons.append("URL shortener detected")
            break

    # @ symbol
    if "@" in url:
        score += 20
        reasons.append("Suspicious @ symbol detected")

    # Suspicious domain extensions
    suspicious_tlds = [
        ".xyz",
        ".top",
        ".click",
        ".shop"
    ]

    for tld in suspicious_tlds:
        if tld in url_lower:
            score += 15
            reasons.append("Suspicious domain extension detected")
            break

    # Keep score between 0 and 100
    if score > 100:
        score = 100

    # Decide result
    if score >= 60:
        result = "Likely Scam"
    elif score >= 30:
        result = "Suspicious"
    else:
        result = "Safe"

    return score, result, reasons
