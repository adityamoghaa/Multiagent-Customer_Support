class BillingAgent:
    role = "billing"
    name = "Billing Agent"
    def respond(self, ticket_body):
        if "refund" in ticket_body.lower():
            return "Your refund is being processed. Expect funds in 5-7 days."
        if "invoice" in ticket_body.lower():
            return "You can download invoices from your dashboard under 'Billing'."
        return "Your billing issue has been recorded. We'll get back to you shortly."

class TechnicalSupportAgent:
    role = "technical"
    name = "Technical Support Agent"
    def respond(self, ticket_body):
        if "crash" in ticket_body.lower():
            return "Please try reinstalling the app. If the issue persists, contact support."
        if "error" in ticket_body.lower():
            return "Please provide the error code for further assistance."
        return "Our technical team will review your issue and respond soon."

class ProductInfoAgent:
    role = "product"
    name = "Product Information Agent"
    def respond(self, ticket_body):
        if "feature" in ticket_body.lower():
            return "You can view all features on our website under the 'Features' section."
        if "plan" in ticket_body.lower() or "pricing" in ticket_body.lower():
            return "Our pricing and plans are listed at /pricing."
        return "Our product team will get back to you with more information."

class EscalationManager:
    role = "escalation"
    name = "Escalation Manager"
    def respond(self, ticket_body):
        return "Your issue has been escalated to a manager. We will contact you soon."

def get_agent(category):
    if category == "billing":
        return BillingAgent()
    elif category == "technical":
        return TechnicalSupportAgent()
    elif category == "product":
        return ProductInfoAgent()
    else:
        return EscalationManager()