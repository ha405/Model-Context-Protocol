import json
import os

class ContextManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.context = self.load_context()

    def load_context(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        else:
            return {
                "user_profile": {
                    "name": "Haseeb",
                    "current_level": "beginner",
                    "goals": []
                },
                "learning_history": [],
                "next_recommendation": None
            }

    def save_context(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.context, f, indent=2)

    def update_context(self, topic, status="in_progress"):
        self.context["learning_history"].append({
            "topic": topic,
            "status": status
        })
        self.save_context()
