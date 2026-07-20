import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_commentary(player_gesture, computer_gesture, result):
    if result == "You Win!":
        prompt = (
            f"Generate a comment for a Rock-Paper-Scissors game where the player won. "
            f"Player chose: {player_gesture}. Computer chose: {computer_gesture}. "
            "Requirements:\n"
            "- Appreciate the player.\n"
            "- Sound energetic.\n"
            "- One sentence only.\n"
            "- Maximum 8 words.\n"
            "- Mention both gestures naturally.\n"
            "- No emojis.\n"
            "- No quotation marks.\n"
            "- Output only the sentence."
        )
    elif result == "Computer Wins!":
        prompt = (
            f"Generate a comment for a Rock-Paper-Scissors game where the computer won. "
            f"Player chose: {player_gesture}. Computer chose: {computer_gesture}. "
            "Requirements:\n"
            "- Generate a playful sarcastic ragebait message.\n"
            "- Not offensive.\n"
            "- One sentence only.\n"
            "- Maximum 8 words.\n"
            "- Mention both gestures naturally.\n"
            "- No emojis.\n"
            "- Output only the sentence."
        )
    elif result == "It is a Tie!":
        prompt = (
            f"Generate a comment for a Rock-Paper-Scissors game where it was a tie. "
            f"Both chose: {player_gesture}. "
            "Requirements:\n"
            "- Generate a funny tie message.\n"
            "- One sentence only.\n"
            "- Maximum 8 words.\n"
            "- Mention the gesture.\n"
            "- No emojis.\n"
            "- Output only the sentence."
        )
    else:
        return "Good game!"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Good game!"
