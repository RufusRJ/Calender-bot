from langchain.tools import Tool
from calendar_utils import suggest_slots, create_booking

def suggest_time_slots(_input: str = ""):
    """
    This dummy input parameter allows compatibility with LangChain.
    """
    slots = suggest_slots()
    return [f"{s[0]} to {s[1]}" for s in slots]

def book_slot(input: str):
    """
    Expects a stringified dict like: '{"summary": "...", "start": "...", "end": "..."}'
    """
    import json
    try:
        data = json.loads(input)
        summary = data.get("summary")
        start = data.get("start")
        end = data.get("end")
        return create_booking(summary, start, end)
    except Exception as e:
        return f"Failed to book slot: {str(e)}"

tools = [
    Tool.from_function(
        func=suggest_time_slots,
        name="SuggestAvailableSlots",
        description="Suggest available time slots for booking. Takes no input."
    ),
    Tool.from_function(
        func=book_slot,
        name="BookAppointment",
        description="Book an appointment given a summary and time range in JSON format."
    )
]
