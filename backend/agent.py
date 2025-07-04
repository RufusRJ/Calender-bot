from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

from langchain_community.llms import Together
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from calendar_utils import suggest_slots, create_booking

def suggest_time_slots(_: str = ""):
    slots = suggest_slots()
    return [f"{s[0]} to {s[1]}" for s in slots]

def book_slot(input_str: str):
    try:
        # Expecting input like: "Meeting | 2025-07-05 10:00:00 | 2025-07-05 11:00:00"
        parts = input_str.strip().split("|")
        if len(parts) != 3:
            return "Input format invalid. Use: Summary | Start Time | End Time"

        summary = parts[0].strip()
        start = datetime.strptime(parts[1].strip(), "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(parts[2].strip(), "%Y-%m-%d %H:%M:%S")

        return create_booking(summary, start, end)
    except Exception as e:
        return f"Failed to book slot: {e}"

tools = [
    Tool.from_function(
        func=suggest_time_slots,
        name="SuggestAvailableSlots",
        description="Suggest available time slots for booking."
    ),
    Tool.from_function(
        func=book_slot,
        name="BookAppointment",
        description="Book an appointment. Input should be in the format: Summary | Start Time | End Time (e.g., Doctor Appointment | 2025-07-05 10:00:00 | 2025-07-05 11:00:00)"
    )
]

llm = Together(
    model="meta-llama/Llama-3-70b-chat-hf",
    temperature=0,
    together_api_key=os.getenv("TOGETHER_API_KEY")
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=1000,
    max_execution_time=None
)

def run_agent(input_text):
    return agent.run(input_text)
