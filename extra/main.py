import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import spacy
import re
# import en_core_web_sm
#
# nlp = en_core_web_sm.load()

chatdpt_api = FastAPI()

# Load the English language model from spaCy
nlp = spacy.load('en_core_web_sm')

# CORS Configuration
origins = ["http://localhost:3000"]

# Add CORS Middleware
chatdpt_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# def detect_information(text):
#     # Simple pattern matching to detect source database type
#     source_database_match = re.search(r"\b(hive|oracle|teradata)\b", text, re.I)
#     source_database = source_database_match.group(1) if source_database_match else None
#
#     # Simple pattern matching to detect database name
#     database_name_match = re.search(r"\b(?:from|to)\s+([\w\d_]+)\s+", text, re.I)
#     database_name = database_name_match.group(1) if database_name_match else None
#
#     # Simple pattern matching to detect table name
#     table_name_match = re.search(r"\binto\s+([\w\d_]+)\s+", text, re.I)
#     table_name = table_name_match.group(1) if table_name_match else None
#
#     print(source_database, database_name, table_name)
#
#     return source_database, database_name, table_name


def detect_information(text):
    # Process the text using spaCy NLP
    doc = nlp(text)

    print(doc)

    sentences = list(doc.sents)
    print(sentences)
    print(len(sentences))

    # Initialize variables for storing detected information
    source_database = None
    database_name = None
    table_name = None

    print(
        f"{'Text with Whitespace':22}"
        f"{'Is Alphanumeric?':20}"
        f"{'Is Punctuation?':18}"
        f"{'Is Stop Word?'}"
    )

    for token in doc:
        print(
         f"{str(token.text_with_ws):22}"
         f"{str(token.is_alpha):15}"
         f"{str(token.is_punct):18}"
         f"{str(token.is_stop)}"
        )

    # # Iterate through entities and extract relevant information
    # for ent in doc.ents:
    #     # print(ent.text, ent.start_char, ent.end_char, ent.label_)
    #     if ent.label_ == "database":
    #         source_database = ent.text
    #     elif ent.label_ == "DB_NAME":
    #         database_name = ent.text
    #     elif ent.label_ == "TABLE_NAME":
    #         table_name = ent.text

    print(source_database, database_name, table_name)

    return source_database, database_name, table_name


@chatdpt_api.post("/process_chat/")
async def process_chat(
        text: str = Form(...),
        file: UploadFile = File(..., raise_exception=True)
):
    # Extract information using the simple pattern matching approach
    source_database, database_name, table_name = detect_information(text)

    if not (source_database and database_name and table_name):
        return JSONResponse(content={"message": "Please provide source database, database name, and table name."},
                            status_code=400)

    # Process file if provided
    if file:
        # Handle file processing (e.g., upload to database, process CSV)
        pass

    # Construct SQL statement based on the detected information
    sql_statement = f"LOAD DATA FROM '{file.filename}' INTO {source_database}.{database_name}.{table_name};"

    return {"sql_statement": sql_statement}


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:chatdpt_api",
        host='localhost',
        port=5000,
        reload=True
    )
