# app.py
import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models.state import ChatState
from app.services import chat
from app import utils

chatdpt_api = FastAPI()

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

# Store chat states in memory (for simplicity, you might want to use a database in a real-world scenario)
chat_states = {}


@chatdpt_api.post("/process_chat/")
async def process_chat(
        input: str = Form(...),
        file: UploadFile = File(..., raise_exception=True)
):
    # Get or initialize chat state
    chat_state = chat_states.get(input,
                                 ChatState(step=0, completed=False, data={})
                                 )
    response_message = "NULL"
    # Initiate chat or process based on the step
    if chat_state.step == 0:
        print(chat_state)
        # Initiate chat by asking for the database type
        response_message = chat.initiate(input)
        chat_state.step += 1
        chat_state.completed = True
        chat_states[input] = chat_state
    elif chat_state.step == 1:
        print(chat_state)
        # Process user response based on the step
        response_message = chat.process_step_1(input)
        chat_state.data["database_name"] = input  # Save user response
        chat_state.step += 1
        chat_state.completed = True
        chat_states[input] = chat_state
    elif chat_state.step == 2:
        print(chat_state)
        # Process user response based on the step
        response_message = chat.process_step_2(input)
        chat_state.data["table_name"] = input  # Save user response
        chat_state.step += 1  # Move to the next step
        chat_state.completed = True
        chat_states[input] = chat_state
    elif chat_state.step == 3:
        print(chat_state)
        # Process user response based on the step
        response_message = chat.process_step_3(input)
        chat_state.data["action"] = input  # Save user response

        # Infer column data types
        response_message = chat.infer_data_types(file.file.read())
        print(response_message)

        # Read CSV and infer column data types
        column_datatypes = utils.read_csv_and_infer_types(file.file.read())
        response_message = utils.create_table_sql(
            chat_state.data["database_name"],
            chat_state.data["table_name"],
            column_datatypes
        )
        print(response_message)

        # Reset chat state after completion
        del chat_states[input]

    print(chat_state)
    print(response_message)
    return JSONResponse(content={"message": response_message,
                                 "state": chat_state.__dict__
                                 },
                        status_code=200
                        )


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:chatdpt_api",
        host='localhost',
        port=5000,
        reload=True
    )
