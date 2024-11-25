from openai import OpenAI
from config import JUDGE_PROMPT, SYSTEM_PROMPT, MODEL, JUDGE_MODEL
import json
import os
from dotenv import load_dotenv
import logging
from file_handler import FileHandler

class ResponseBenchmarker:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.judge_prompt = JUDGE_PROMPT
        self.model = MODEL
        self.judge_model = JUDGE_MODEL

    def _create_chat_completion(self, messages, model=None):
        return self.client.chat.completions.create(
            model=model or self.model,
            messages=messages
        )

    def _create_message(self, role: str, content: str) -> dict:
        return {"role": role, "content": content}

    def _parse_json_response(self, evaluation_text: str) -> dict:
        if "```" in evaluation_text:
            parts = evaluation_text.split("```")
            evaluation_text = parts[1] if len(parts) >= 2 else parts[0]
            evaluation_text = evaluation_text.replace("json", "", 1).strip()
        
        return json.loads(evaluation_text.strip())

    def get_llm_response(self, question: str) -> str:
        messages = [
            self._create_message("system", SYSTEM_PROMPT),
            self._create_message("user", question)
        ]
        response = self._create_chat_completion(messages)
        return response.choices[0].message.content

    def evaluate_response(self, question: str, correct_answer: str, ai_response: str, question_number: int) -> dict:
        evaluation_prompt = self.judge_prompt.format(
            question_number=question_number,
            question=question,
            correct_answer=correct_answer,
            ai_response=ai_response
        )
        
        messages = [
            self._create_message("system", "You are an impartial judge. You must respond with valid JSON only."),
            self._create_message("user", evaluation_prompt)
        ]
        
        evaluation = self._create_chat_completion(messages, model=self.judge_model)
        evaluation_text = evaluation.choices[0].message.content
        
        return {
            "question_number": question_number,
            "question": question,
            "correct_answer": correct_answer,
            "ai_response": ai_response,
            "evaluation": self._parse_json_response(evaluation_text)
        }

    def evaluate_multiple_questions(self, questions_data: list) -> dict:
        print(f"Evaluating {len(questions_data)} questions...")
        results = []
        for i, item in enumerate(questions_data, 1):
            print(f"Question {i}/{len(questions_data)}")
            ai_response = self.get_llm_response(item['question'])
            result = self.evaluate_response(
                item['question'], 
                item['correct_answer'], 
                ai_response, 
                i
            )
            results.append(result)
        print("Evaluation complete!")
        return {"evaluations": results}

def main():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    print("Loading questions...")
    file_handler = FileHandler()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    questions_data = file_handler.load_questions(os.path.join(script_dir, 'questions.json'))
    
    print("Starting benchmarking process...")
    benchmarker = ResponseBenchmarker(api_key)
    results = benchmarker.evaluate_multiple_questions(questions_data)
    
    print("Saving results...")
    file_handler.save_results(results, "evaluation_report.json")
    print("Process complete!")

if __name__ == "__main__":
    main()
