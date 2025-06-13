from .classifier import classify_ticket
from .agents import get_agent
from .database import SessionLocal, init_db
from .models import Ticket
from .sentiment import analyze_sentiment
from .translate import detect, translate_text
from .proactive import suggest_next_action
from .voice import text_to_speech

def main():
    print("==== Multi-Agent Support CLI ====")
    db = SessionLocal()
    init_db()
    while True:
        user_input = input("\nDescribe your issue (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        lang = detect(user_input)
        body_en = translate_text(user_input, src_lang=lang, tgt_lang="en") if lang != "en" else user_input
        category = classify_ticket(body_en)
        sentiment = analyze_sentiment(body_en)
        suggestion = suggest_next_action(body_en)
        agent = get_agent(category)
        agent_response_en = agent.respond(body_en)
        response = translate_text(agent_response_en, src_lang="en", tgt_lang=lang) if lang != "en" else agent_response_en
        status = "resolved" if category != "escalation" else "escalated"
        ticket = Ticket(
            body=user_input,
            category=category,
            status=status,
            response=response,
            agent=agent.name,
            sentiment=sentiment,
            language=lang,
            suggestion=suggestion
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        print(f"\nTicket ID: {ticket.id}\nCategory: {category}\nAgent: {agent.name}\nStatus: {status}")
        print(f"Sentiment: {sentiment}")
        print(f"Detected Language: {lang}")
        print(f"Agent Response: {response}")
        print(f"Proactive Suggestion: {suggestion}")
        want_voice = input("Read this response aloud? (y/N): ").strip().lower()
        if want_voice == "y":
            text_to_speech(response, lang=lang)
    db.close()

if __name__ == "__main__":
    main()