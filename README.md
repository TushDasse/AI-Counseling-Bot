# 🎓 Student Support Chatbot (Rasa)

An AI chatbot that answers common questions from **BSc IT students at the Open University of Sri Lanka (OUSL)**: fees, courses, admissions, registration, exams and student support.

This was my **final year project** for the BSc (Hons) in Information Technology. It's built with the open-source **Rasa** framework.

---

## ✨ Features

- **Natural language understanding.** Students can ask in their own words, e.g. *"how much is one credit?"* or *"what do I pay at registration?"*
- **Course lookup by level.** A custom action returns the course list for Levels 3–6, and buttons help users pick a level.
- **Fees and payments.** Explains tuition per credit and the first/second installment breakdown.
- **Admissions and registration.** Covers entry requirements, degree duration, exemptions and the registration process.
- **Two-stage fallback.** When the bot isn't sure, it suggests the two most likely topics (*"Did you mean Course Fees or First Payment?"*). If it still can't help, it hands the student over to the help desk.
- **Sentiment-aware reply.** If a student sounds unhappy, it points them to the student counsellor.
- **Web chat UI.** A custom HTML/CSS/JS chat interface connected to Rasa's REST API.

## 🧠 How it works

| Component | Details |
|---|---|
| NLU pipeline | WhitespaceTokenizer → Regex & Lexical-Syntactic featurizers → CountVectors (word + char n-grams) → **DIETClassifier** (intents & entities) → ResponseSelector |
| Dialogue policies | MemoizationPolicy, RulePolicy, **TEDPolicy** |
| Fallback | FallbackClassifier (confidence < 0.6 or ambiguity < 0.1) → custom `action_two_stage_fallback` |
| Training data | 17 intents with 155 example questions, plus entities for course code, level, student ID and module |
| Custom actions | `actions/actions.py` (Rasa SDK): course details, exam date lookup, registration status (mock), smart fallback |

## 📁 Project structure

```
├── actions/actions.py      # Custom Python actions (Rasa SDK)
├── data/
│   ├── nlu.yml             # Training examples for each intent
│   ├── rules.yml           # Fixed question → answer rules
│   └── stories.yml         # Example multi-turn conversations
├── ui/
│   ├── chatbot_final_ui.html  # Custom chat interface (REST API)
│   └── webchat_test.html      # Quick test page using rasa-webchat
├── config.yml              # NLU pipeline & policies
├── domain.yml              # Intents, entities, slots, responses
├── credentials.yml
└── endpoints.yml
```

## 🚀 Run it locally

Requires **Python 3.10**.

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model
rasa train

# 4. Start the action server (terminal 1)
rasa run actions

# 5. Start the Rasa server with the API enabled (terminal 2)
rasa run --enable-api --cors "*"

# 6. Open ui/chatbot_final_ui.html in your browser and start chatting
```

To chat in the terminal instead, run `rasa shell`.

## 💬 Example questions

- "Hi" / "Ayubowan"
- "How much are the fees?"
- "What do I pay at registration?"
- "Show me the level 4 courses"
- "What are the admission requirements?"
- "How long is the degree?"
- "I'm feeling stressed about my studies"

## 🛠️ Tech stack

Python · Rasa 3.6 · Rasa SDK · DIET & TED (transformer-based models) · HTML / CSS / JavaScript

## 📌 Notes

- Fee amounts, dates and contact details were correct for the 2025/26 intake when I built the project. Check the official OUSL website for current information.
- The registration status action is a mock. It isn't connected to a real student database.

---

👤 **Tushara Dassanayake** · [LinkedIn](https://www.linkedin.com/in/tushara-dassanayake-4b428530a) · tusharadassanayake99@gmail.com
