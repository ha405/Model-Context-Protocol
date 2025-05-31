import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from context_manager import ContextManager

cm = ContextManager("context.json")
cm.update_context("if statements", "completed")

print(cm.get_context())
