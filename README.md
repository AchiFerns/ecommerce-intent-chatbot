🛒 Intent-Based E-Commerce Chatbot
This project is a semantic, intent-driven e-commerce chatbot that understands natural language queries and intelligently routes them to the correct logic using an LLM (Groq API + semantic-router). It supports:

❓ Product FAQs

🛍️ SQL-based product search

💬 General small talk

📌 Features
✨ Semantic Intent Routing using semantic-router

📄 FAQ Answering with context-aware LLM responses

🔍 Product Search using natural language → SQL query

🤖 Small Talk powered by a friendly LLM persona

💬 Streamlit Chat Interface

🧠 LLM used: GROQ_MODEL via API

🧠 Architecture Overview
css
Copy
Edit
User Query ➝ Semantic Router ➝ [faq_chain | sql_chain | talk]
                                   ➝ LLM ➝ Response
🗂️ Folder Structure
bash
Copy
Edit
e-commerce/
├── app/
│   ├── main.py              # Streamlit app
│   ├── faq.py               # FAQ logic
│   ├── sql.py               # SQL query + LLM generation
│   ├── smalltalk.py         # General conversation logic
│   ├── router.py            # Semantic router logic
│   └── resources/
│       ├── faq_data.csv     # FAQ knowledge base
│       └── db.sqlite        # Product database
├── web_scrapping/           # (Optional: product scraper)
├── requirements.txt
├── .env                     # Store GROQ_MODEL key
✅ Setup Instructions
Clone the repo

bash
Copy
Edit
git clone https://github.com/yourusername/ecommerce-chatbot.git
cd ecommerce-chatbot
Create virtual environment

bash
Copy
Edit
pip install pipenv
pipenv install
pipenv shell
Add your .env file

env
Copy
Edit
GROQ_MODEL=llama3-8b-...  # Replace with your model ID
Run the app

bash
Copy
Edit
cd app
streamlit run main.py
📊 Example Queries
“What is the return policy of the products?” → routed to faq_chain

“Show top 3 shoes with 50% discount” → routed to sql_chain

“Hey, how are you?” → routed to talk()

🧪 Technologies Used
Streamlit

semantic-router

Groq LLM API

HuggingFace Sentence Transformers

SQLite

Pandas

📜 License
This project is licensed under the MIT License.

