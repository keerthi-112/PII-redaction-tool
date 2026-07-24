# Evaluation Report

## Evaluation Approach

The evaluation was performed on the provided sample document by comparing the detected PII entities with the expected PII present in the document. Each detected entity was manually verified to determine whether it was correctly identified and classified.

The evaluation considered the following PII types:

- Person Name
- Email Address
- Phone Number
- Company Name
- Physical Address
- SSN
- Credit Card Number
- Date of Birth
- IP Address

## Results

Ground truth entities : 10

Entities detected : 10

True positives : 10

False positives : 0

False negatives : 0

Precision : 100%

Recall : 100%

Accuracy : 100%

## Observations

The combination of Regex, spaCy, and Presidio successfully detected all expected PII entities in the sample document. Regex performed well for structured data such as email addresses, phone numbers, SSNs, credit card numbers, IP addresses, and dates of birth. spaCy and Presidio improved the detection of contextual entities such as person names and organizations.

A limitation observed during testing is that named entity recognition models may occasionally identify parts of an address as separate entities. This was reduced through duplicate removal and overlap resolution.