JUDGE_PROMPT = """
You are an impartial judge evaluating the accuracy and correctness of an AI's response
compared to a known correct answer. Please evaluate on the following criteria and return your response in JSON format:

Question: {question}
Correct Answer: {correct_answer}
AI Response: {ai_response}

Return your evaluation in the following JSON structure:
{{
    "factual_accuracy": {{
        "score": 0-10,
        "explanation": "Brief explanation of score"
    }},
    "completeness": {{
        "score": 0-10,
        "explanation": "Brief explanation of score"
    }},
    "clarity": {{
        "score": 0-10,
        "explanation": "Brief explanation of score"
    }},
    "overall_score": 0-10,
    "result": {{
        "status": "Pass/Fail",
        "explanation": "Brief explanation of pass/fail decision"
    }}
}}"""

SYSTEM_PROMPT = "Please answer the following question in 2-4 sentences:"
MODEL = "gpt-4o"
JUDGE_MODEL = "gpt-4o"