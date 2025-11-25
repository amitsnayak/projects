import json
import random

class Flashcard:
    def __init__(self, question, answer, correct_count=0, wrong_count=0):
        self.question = question
        self.answer = answer
        self.correct_count = correct_count
        self.wrong_count = wrong_count

    def mark_correct(self):
        self.correct_count += 1

    def mark_wrong(self):
        self.wrong_count += 1

    def to_dict(self):
        return {
            "question": self.question,
            "answer": self.answer,
            "correct_count": self.correct_count,
            "wrong_count": self.wrong_count
        }

    @staticmethod
    def from_dict(data):
        return Flashcard(
            data["question"],
            data["answer"],
            data.get("correct_count", 0),
            data.get("wrong_count", 0)
        )

class FlashcardApp:
    def __init__(self, filename="flashcards.json"):
        self.filename = filename
        self.flashcards = []
        self.load_flashcards()

    def add_flashcard(self, question, answer):
        flashcard = Flashcard(question, answer)
        self.flashcards.append(flashcard)
        print(f" Flashcard '{question}' added successfully!")

    def view_flashcards(self):
        if not self.flashcards:
            print(" No flashcards available.")
            return
        print("\n Flashcards:")
        for i, card in enumerate(self.flashcards, start=1):
            print(f"{i}. Q: {card.question} | A: {card.answer} | Correct: {card.correct_count} | Wrong: {card.wrong_count}")
        print("")

    def start_quiz(self):
        if not self.flashcards:
            print(" No flashcards to quiz. Add some first!")
            return
        print("\n Starting Quiz! Type 'exit' to quit.\n")
        cards = self.flashcards.copy()
        random.shuffle(cards)
        for card in cards:
            print(f"Q: {card.question}")
            user_answer = input("Your Answer: ").strip()
            if user_answer.lower() == "exit":
                break
            elif user_answer.lower() == card.answer.lower():
                print(" Correct!\n")
                card.mark_correct()
            else:
                print(f" Wrong! Correct answer: {card.answer}\n")
                card.mark_wrong()

    def save_flashcards(self):
        with open(self.filename, "w") as f:
            json.dump([card.to_dict() for card in self.flashcards], f, indent=4)
        print(" Flashcards saved successfully!")

    def load_flashcards(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.flashcards = [Flashcard.from_dict(card) for card in data]
        except FileNotFoundError:
            self.flashcards = []

    def run_cli(self):
        while True:
            print("\n=== Flashcard Learning App ===")
            print("1. Add Flashcard")
            print("2. View Flashcards")
            print("3. Start Quiz")
            print("4. Save & Exit")
            choice = input("Select an option (1-4): ")

            if choice == "1":
                question = input("Enter question: ").strip()
                answer = input("Enter answer: ").strip()
                self.add_flashcard(question, answer)
            elif choice == "2":
                self.view_flashcards()
            elif choice == "3":
                self.start_quiz()
            elif choice == "4":
                self.save_flashcards()
                print(" Goodbye!")
                break
            else:
                print(" Invalid option. Try again.")

if __name__ == "__main__":
    app = FlashcardApp()
    app.run_cli()
