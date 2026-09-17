import pickle, sys, json, re, numpy as np, pandas as pd
from sklearn.metrics.pairwise import linear_kernel

BASE = "."
clf=pickle.load(open(f"{BASE}/intent_model.pkl","rb"))
vec=pickle.load(open(f"{BASE}/intent_vectorizer.pkl","rb"))
rvec=pickle.load(open(f"{BASE}/retrieval_vectorizer.pkl","rb"))
rmatrix=pickle.load(open(f"{BASE}/retrieval_matrix.pkl","rb"))
pairs=pd.read_csv(f"{BASE}/historical_pairs.csv").fillna("")

REPLIES = {'order_status': 'Sorry for the wait. Please check your order details for the current carrier and delivery status, and send us a DM if you need further help.', 'delivery_problem': 'Sorry for the delivery trouble. Please send us a DM with your order details so we can look into the delivery status further.', 'refund_return': "We'd be happy to look into this. Please send us a DM with your order details so we can check the return or refund status.", 'payment_billing': "We'd like to look into this with you. Please send us a DM with the relevant order or payment details so the issue can be reviewed securely.", 'account_login': "We'd like to help with your account issue. Please send us a DM so we can guide you through the appropriate account-support steps.", 'subscription_prime': "We'd be happy to look into your Prime or membership concern. Please send us a DM with the relevant account details.", 'product_issue': "Sorry you're having trouble with the item. Please send us a DM with your order details so we can look into the issue.", 'cancel_order': "We'll help you check the cancellation options. Please send us a DM with your order details so we can look into this.", 'seller_issue': "We'd like to look into the seller-related concern. Please send us a DM with the relevant order details.", 'gift_card': "We'd be happy to help with your gift card concern. Please send us a DM with the relevant details so we can look into it.", 'promotion': "We'd be happy to look into the promotion or offer you're asking about. Please send us a DM with the relevant details.", 'general_support': 'Thanks for reaching out. Please send us a DM with the relevant order or account details so we can look into this further.'}
SENSITIVE = ["fraud","fraudulent","unauthorized","stolen","hacked","hack","scam","identity theft","someone used my card"]
HIGH_RISK = {"payment_billing","account_login"}

def run_agent(customer_text,k=5):
    q=vec.transform([customer_text])
    probs=clf.predict_proba(q)[0]
    idx=probs.argmax()
    intent=clf.classes_[idx]
    confidence=float(probs[idx])

    rq=rvec.transform([customer_text])
    scores=linear_kernel(rq,rmatrix).ravel()
    top=np.argsort(scores)[::-1][:k]
    historical=[{
        "customer":str(pairs.iloc[i]["customer_text"]),
        "historical_reply":str(pairs.iloc[i]["historical_reply"]),
        "similarity":round(float(scores[i]),4)
    } for i in top]

    t=customer_text.lower()
    if any(s in t for s in SENSITIVE):
        action="escalate"; reason="Potential fraud, unauthorized activity, or account-security risk requires human review."
    elif intent in HIGH_RISK:
        action="escalate"; reason="Account or payment issue may require account-specific verification or human intervention."
    elif confidence < .55:
        action="escalate"; reason="Intent-classification confidence is below the safety threshold, so human review is preferred."
    else:
        action="auto_handle"; reason=f"Routine {intent.replace('_',' ')} request with a standard support path; suitable for automated handling."

    return {"customer":customer_text,"intent":intent,"confidence":round(confidence,4),
            "historical_examples":historical,"reply":REPLIES.get(intent,REPLIES["general_support"]),
            "action":action,"reason":reason}

if __name__=="__main__":
    text=" ".join(sys.argv[1:]) if len(sys.argv)>1 else input("Customer message: ")
    print(json.dumps(run_agent(text),ensure_ascii=False,indent=2))
