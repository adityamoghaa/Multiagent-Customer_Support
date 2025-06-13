def classify_ticket(text: str) -> str:
    text = text.lower()
    if any(w in text for w in ["refund", "invoice", "billing", "charge"]):
        return "billing"
    elif any(w in text for w in ["crash", "error", "technical", "bug", "issue", "not working"]):
        return "technical"
    elif any(w in text for w in ["feature", "plan", "product", "info", "pricing", "details"]):
        return "product"
    elif any(w in text for w in ["escalate", "supervisor", "manager"]):
        return "escalation"
    return "product"