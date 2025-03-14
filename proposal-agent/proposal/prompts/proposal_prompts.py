"""Proposal analysis related prompt templates"""

ANALYSIS_TEMPLATE = """
Please analyze and evaluate the following proposal:

Proposal Title: {proposal_title}
Proposal Content: {proposal_content}

Please analyze the following aspects and return in JSON format:
1. Dimension scores (1-10 points):
   - feasibility
   - relevance
   - cost_benefit
   - impact
   - risk
2. overall_score
3. strengths and weaknesses
4. risks

Return JSON format only, no other text.
"""

VOTE_TEMPLATE = """
Based on the following proposal analysis results, decide whether to support or oppose the proposal:

{analysis_result}

Please return your decision in JSON format, including the following fields:
1. vote_type: "support" or "oppose"
2. reason: detailed reasoning for the decision
3. confidence: decision confidence level (0-1)

Return JSON format only, no other text.
"""

COMMENT_TEMPLATE = """
Generate a comment based on the following proposal analysis results:

{analysis_result}

Comment sentiment: {sentiment} (positive/negative/neutral)

Please return the comment in JSON format, including the following fields:
1. content: comment body
2. highlights: proposal highlights
3. suggestions: improvement suggestions

Return JSON format only, no other text.
"""