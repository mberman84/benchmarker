import json

class FileHandler:
    @staticmethod
    def load_questions(filepath: str) -> list:
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_results(results: dict, filepath: str) -> None:
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2) 