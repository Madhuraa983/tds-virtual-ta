from fastapi import FastAPI, Query
from typing import Optional
import json

app = FastAPI()

# --- Load Discourse Posts ---
def load_discourse_posts():
    try:
        with open("tds_discourse_posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️ Discourse posts file not found.")
        return []

# --- Load Course Content ---
def load_course_content():
    try:
        with open("tds_course_content.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            chunks = []
            for week in data.get("outline", []):
                for lesson in week.get("lessons", []):
                    chunks.append({
                        "title": lesson["title"],
                        "text": f"Week {week['week']}: {lesson['title']} - {lesson['content']}",
                        "url": f"https://ds.study.iitm.ac.in/courses/ns_25t2_se2002/unit?week={week['week']}"
                    })
            return chunks
    except FileNotFoundError:
        print("⚠️ Course content file not found.")
        return []

# --- Combine All Docs ---
course_content = load_course_content()
discourse_posts = load_discourse_posts()
all_docs = discourse_posts + course_content

# --- Dummy Answering Logic ---
def find_best_match(question: str):
    question = question.lower()
    for doc in all_docs:
        if question in doc["text"].lower():
            return {
                "answer": doc["text"],
                "source": doc.get("url", "No URL available")
            }
    return {
        "answer": "❓ Sorry, I couldn't find an answer to your question.",
        "source": None
    }

# --- API Endpoint ---
@app.get("/ask")
def ask_question(q: str = Query(..., description="Your question about the TDS course")):
    result = find_best_match(q)
    return result


