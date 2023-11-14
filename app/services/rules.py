# chat.py
import spacy
from spacy.tokens import Token
from spacy.pipeline import EntityRuler

# Load spaCy English model
nlp = spacy.load("en_core_web_sm", disable = ['ner'])

# Example: Add custom spaCy entities for DB names and actions
Token.set_extension("entities", default=[], force=True)

# Create an EntityRuler for DB names
db_ruler = nlp.add_pipe("entity_ruler")
db_patterns = [{"label": "DB_NAME", "pattern": "hive"},
               {"label": "DB_NAME", "pattern": "oracle"}
               ]
action_patterns = [{"label": "ACTION", "pattern": "load"}]

table_type_patterns = [{"label": "TYPE", "pattern": "new"},
                       {"label": "TYPE", "pattern": "exist"}]

db_ruler.add_patterns(db_patterns)
db_ruler.add_patterns(action_patterns)
print(db_ruler.name)
# db_ruler.name = 'rulerDB'
# print(db_ruler.name)


# # Create an EntityRuler for actions
# action_ruler = EntityRuler(nlp, overwrite_ents=True)
# action_ruler.add_patterns([{"label": "ACTION", "pattern": "load"}])
# print(action_ruler.name)
# nlp.add_pipe(action_ruler.name, before="ner")

print(nlp.pipe_names)


# Additional functions for step-wise processing
def process_step_1(user_input: str) -> str:
    # Process user response based on the step
    return "What would you like to name the table?"


def process_step_2(user_input: str) -> str:
    # Process user response based on the step
    return "What action would you like to perform? (e.g., 'infer' or 'provide SQL')"


def process_step_3(user_input: str) -> str:
    # Process user response based on the step
    return f"Great! You selected: {user_input}. Now, please upload the CSV file."


def infer_data_types(file_content: bytes) -> str:
    # Assuming user wants to infer column data types
    # Here, you would typically implement logic to read the CSV and infer data types
    # For simplicity, I'm just returning a placeholder message
    return "Do you want to infer column data types from the CSV? (yes/no)"
