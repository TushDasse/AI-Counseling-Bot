from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# --- COURSE DATABASE (From Prospectus Pages 17-21) ---
COURSE_DB_BY_LEVEL = {
    "3": [
        "COU3300: Computer Organisation", "COU3301: Database Mgmt Systems",
        "COU3202: System Analysis", "ADU3330: Discrete Mathematics I",
        "COU3304: Programming Fundamentals", "COU3303: Software Engineering",
        "ITU3201: Web Development", "COU3305: Computer Security"
    ],
    "4": [
        "COU4300: OOP", "COU4201: Logic Programming", "COU4302: Operating Systems",
        "ISU4200: Prof. Ethics", "ADU4230: Discrete Math II",
        "COU4304: Computer Arch", "COU4303: AI", "COU4305: Computer Networks"
    ],
    "5": [
        "ADU5330: Inferential Stats", "ITU5300: HCI", "ITU5301: Quality Assurance",
        "ITU5302: Data Analytics", "ITU5303: Multimedia", "COU5300: Neural Networks"
    ],
    "6": [
        "ITU6621: Research Project", "COU6303: Advanced DBMS", "COU6304: Adv. Algorithms",
        "ITU6302: Distributed Systems", "COU6308: Machine Learning"
    ]
}

class ActionGiveCourseDetails(Action):
    def name(self) -> Text:
        return "action_give_course_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get level from slot
        level_slot = tracker.get_slot("level_number")
        
        # Logic: If user says "Level 3", we just want "3"
        if level_slot:
            # Extract just digits
            level_key = ''.join(filter(str.isdigit, str(level_slot)))
        else:
            level_key = None

        if level_key in COURSE_DB_BY_LEVEL:
            courses = COURSE_DB_BY_LEVEL[level_key]
            # Create a nice list
            formatted_list = "\n".join([f"- {c}" for c in courses])
            dispatcher.utter_message(text=f"Here are the **Level {level_key}** courses:\n{formatted_list}")
        else:
            dispatcher.utter_message(text="I couldn't identify the level. We offer Level 3, 4, 5, and 6.")
        
        return []

class ActionCheckExamDate(Action):
    def name(self) -> Text:
        return "action_check_exam_date"

    def run(self, dispatcher, tracker, domain):
        course_code = next(tracker.get_latest_entity_values("course_code"), None)
        if course_code and course_code.upper() == "EEI3366":
            dispatcher.utter_message(text=f"The exam for **{course_code.upper()}** is on **Oct 12th, 9:00 AM**.")
        else:
            dispatcher.utter_message(text="Exam dates are **Coming Soon**.")
        return []

class ActionCheckRegistrationStatus(Action):
    def name(self) -> Text:
        return "action_check_registration_status"
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="I cannot access the live student database yet. (Mock Action)")
        return []
    
# actions.py

# Map technical intent names to human-readable names for Stage 1
INTENT_MAP = {
    "ask_fees": "Course Fees",
    "ask_first_installment": "First Payment",
    "ask_second_installment": "Second Payment",
    "ask_exam_schedule": "Exams",
    "ask_course_list_by_level": "Course Lists",
    "ask_admission_requirements": "Admissions",
    "ask_registration_status": "Registration Status",
    "ask_drop_policy": "Dropping a Course",
    "ask_contact_info": "Contact Info",
    "mood_unhappy": "Student Support",
    "greet": "Greeting",
    "goodbye": "Ending Chat"
}

# actions.py

# ... (Keep your INTENT_MAP and imports at the top)

class ActionTwoStageFallback(Action):
    def name(self) -> Text:
        return "action_two_stage_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Check History: Did we just do a fallback?
        last_action_was_fallback = False
        for event in reversed(tracker.events):
            if event.get("event") == "action" and event.get("name") == "action_two_stage_fallback":
                last_action_was_fallback = True
                break
            if event.get("event") == "user":
                break

        # --- STAGE 2: HANDOFF (If we already tried once) ---
        if last_action_was_fallback:
            dispatcher.utter_message(text="I am having trouble understanding. Please contact the Help Desk at **helpdesk@ou.ac.lk** for human assistance.")
            return []

        # --- STAGE 1: CLARIFICATION (First failure) ---
        else:
            # Get the intent ranking from the tracker
            intent_ranking = tracker.latest_message.get("intent_ranking", [])
            
            # FILTER: Remove 'nlu_fallback' from the list of suggestions
            valid_intents = [
                i for i in intent_ranking 
                if i['name'] != "nlu_fallback" and i['confidence'] > 0.1 # Optional: skip very low confidence ones too
            ]
            
            if len(valid_intents) >= 2:
                first_guess = valid_intents[0]['name']
                second_guess = valid_intents[1]['name']
                
                # Convert to readable text
                str1 = INTENT_MAP.get(first_guess, first_guess)
                str2 = INTENT_MAP.get(second_guess, second_guess)
                
                dispatcher.utter_message(text=f"I didn't quite catch that. Did you mean **{str1}** or **{str2}**?")
            else:
                # If we don't have enough valid guesses left
                dispatcher.utter_message(text="I didn't quite catch that. Could you please rephrase your question?")
            
            return []