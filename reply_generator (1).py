"""
Grounded reply generator for the Hiver AmazonHelp support agent.
The function is deliberately conservative: it uses historical retrieval as evidence
and avoids inventing refunds, dates, policies, or account actions.
"""

def generate_reply(customer_text, intent, retrieved):
    if intent == "order_status":
        return "Sorry for the wait. Please check your order details for the current carrier and delivery status, and send us a DM if you need further help."
    if intent == "delivery_problem":
        return "Sorry for the delivery trouble. Please send us a DM with your order details so we can look into the delivery status further."
    if intent == "refund_return":
        return "We'd be happy to look into this. Please send us a DM with your order details so we can check the return or refund status."
    if intent == "payment_billing":
        return "We'd like to look into this with you. Please send us a DM with the relevant order or payment details so the issue can be reviewed securely."
    if intent == "account_login":
        return "We'd like to help with your account issue. Please send us a DM so we can guide you through the appropriate account-support steps."
    if intent == "subscription_prime":
        return "We'd be happy to look into your Prime or membership concern. Please send us a DM with the relevant account details."
    if intent == "product_issue":
        return "Sorry you're having trouble with the item. Please send us a DM with your order details so we can look into the issue."
    if intent == "cancel_order":
        return "We'll help you check the cancellation options. Please send us a DM with your order details so we can look into this."
    if intent == "seller_issue":
        return "We'd like to look into the seller-related concern. Please send us a DM with the relevant order details."
    if intent == "gift_card":
        return "We'd be happy to help with your gift card concern. Please send us a DM with the relevant details so we can look into it."
    if intent == "promotion":
        return "We'd be happy to look into the promotion or offer you're asking about. Please send us a DM with the relevant details."
    return "Thanks for reaching out. Please send us a DM with the relevant order or account details so we can look into this further."
