# Hiver AmazonHelp AI Support Agent

Pipeline:
Customer Tweet -> Intent Classification -> Historical Retrieval -> Grounded Reply -> Auto-handle/Escalate

Selected brand: AmazonHelp

## Run
1. Install: `pip install -r requirements.txt`
2. Run: `python pipeline.py "Where is my order? It was supposed to arrive yesterday."`

## Output
The pipeline returns intent, confidence, top historical customer/reply examples, a conservative reply, action, and escalation reason.

## Important evaluation note
The current intent labels are an initial automated labeling pass over a Golden Set. Before submission, the 200 examples should be manually reviewed because Hiver explicitly asks for a hand-labelled Golden Evaluation Set.
