from typing import Optional


class ChatState:
    def __init__(self, step: int, completed: bool, data: Optional[dict] = None):
        self.step = step
        self.completed = completed
        self.data = data or {}

    def __repr__(self):
        chat_steps = {
            "Step 0": "Greet the user and ask for data load",
            "Step 1": "Initiate the data load process by providing the type of database (e.g., Hive, Oracle, Teradata, etc.).",
            "Step 2": "Specify the name of the database where you want to load the data.",
            "Step 3": "Enter the name of the table where the data should be loaded.",
            "Step 4": "Choose the action you want to perform (e.g., load data into an existing table or create a new table).",
            "Step 5": "Upload the CSV file containing the data you want to load.",
            "Step 6": "Review and confirm the inferred column data types from the CSV file.",
            "Step 7": "Preview the SQL query that will be executed to create the table based on the inferred column data types.",
            "Step 8": "Execute the data load process. If creating a new table, the table will be created, and the data will be loaded.",
            "Step 9": "Review the results of the data load process and handle any errors or issues if they occur.",
            "Step 10": "Complete the data load process, and the system will provide a summary of the operation.",
        }

        return chat_steps
