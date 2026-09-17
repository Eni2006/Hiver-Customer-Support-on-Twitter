# Decision Log — AmazonHelp AI Support Agent

1. **Selected AmazonHelp as the target brand**
   - Chosen because the dataset contains customer conversations linked to AmazonHelp responses, giving us both customer messages and historical support replies.

2. **Defined 12 support intents**
   - Used a compact taxonomy: order_status, delivery_problem, refund_return, payment_billing, account_login, subscription_prime, product_issue, cancel_order, seller_issue, gift_card, promotion, and general_support.
   - The goal is to keep classification small enough to evaluate clearly.

3. **Created a 200-example Golden Evaluation Set**
   - Chosen because Hiver requires 150–250 hand-labelled examples.
   - The current labels are an initial automated pass and should be manually reviewed before submission.

4. **Used TF-IDF + Logistic Regression for the initial intent model**
   - This provides a fast, explainable baseline and can run locally without an external API.

5. **Used TF-IDF retrieval for historical conversations**
   - This makes the first retrieval implementation lightweight and reproducible.
   - It retrieves the top 5 similar customer messages and their actual AmazonHelp responses.

6. **Kept reply generation conservative**
   - The system should not invent refunds, compensation, delivery dates, policies, or account actions.
   - When account/order-specific information is needed, the reply asks the customer to continue through a DM/support channel.

7. **Separated classification, retrieval, generation, and escalation**
   - A modular pipeline makes each component independently testable and makes failure analysis easier.

8. **Added a confidence threshold for escalation**
   - Predictions below 0.55 confidence are escalated rather than automatically answered.
   - This is a safety-oriented starting point and must be calibrated using validation data.

9. **Escalated sensitive payment/account-security cases**
   - Payment/account issues and terms indicating possible fraud or unauthorized activity are routed to a human.
   - The goal is to avoid unsafe automated handling of sensitive cases.

10. **Compared against a majority-class baseline**
    - This establishes a trivial lower-bound reference for intent classification.

11. **Added a keyword-rule baseline**
    - Included as a simple baseline, but its current 100% result is not treated as valid evidence because the initial labels were created using related keyword rules.

12. **Included an LLM-as-judge rubric**
    - Reply quality is evaluated on relevance, groundedness, helpfulness, tone, and safety.

13. **Did not claim human/LLM judge agreement without human labels**
    - Hiver requires evidence that the judge agrees with a human, so a human-rated subset is required before reporting agreement.

14. **Included failure analysis as a first-class evaluation artifact**
    - The project records ambiguity, retrieval mismatch, conservative escalation, partial grounding, and evaluation leakage as areas requiring improvement.

15. **Prioritized reproducibility over full-dataset processing**
    - The assignment explicitly says a subsample is expected and encouraged, so the implementation uses manageable local subsets while keeping the pipeline reproducible.
