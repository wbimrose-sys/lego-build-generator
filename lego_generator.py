"""
LEGO Build Idea Generator - Version 3
======================================
A beginner-friendly Python app that uses AI to generate
creative LEGO build ideas based on your available pieces and theme.

How to run:
  pip install anthropic python-dotenv
  python lego_generator.py

Put your API key in a .env file next to this script:
  ANTHROPIC_API_KEY=sk-ant-...

If you don't have an API key, the app will use a built-in mock
response so you can still try it out!
"""

import os  # Used to read environment variables (like your API key)
from dotenv import load_dotenv  # Loads variables from a .env file

# Load variables from .env into os.environ (no-op if the file is missing)
load_dotenv()


# ==============================================================
# STEP 1: Get input from the user
# ==============================================================

def get_user_input():
    """
    Ask the user for their LEGO pieces and build theme.
    Returns a dictionary with 'pieces', 'theme', 'difficulty', and 'style'.
    """
    print("\n" + "=" * 50)
    print("🧱  LEGO Build Idea Generator  🧱")
    print("=" * 50)
    print("Tell me what LEGO pieces you have and what")
    print("you'd like to build — I'll come up with a fun idea!\n")

    # --- Collect LEGO pieces ---
    print("📦 Enter your available LEGO pieces.")
    print("   (Type one piece per line. Press Enter twice when done.)\n")

    pieces = []
    while True:
        piece = input("   Piece: ").strip()
        if piece == "":
            if len(pieces) == 0:
                print("   ⚠️  Please enter at least one piece!\n")
            else:
                break  # Empty line = done entering pieces
        else:
            pieces.append(piece)

    # --- Collect build theme ---
    print("\n🎨 What theme would you like? ")
    print("   Examples: spaceship, castle, cyberpunk city, race car\n")
    theme = input("   Theme: ").strip()
    while theme == "":
        print("   ⚠️  Please enter a theme!")
        theme = input("   Theme: ").strip()

    # --- Optional: difficulty preference ---
    print("\n⚙️  Preferred difficulty? (or press Enter to skip)")
    print("   Options: Easy / Medium / Hard\n")
    difficulty = input("   Difficulty: ").strip().capitalize()
    if difficulty not in ["Easy", "Medium", "Hard"]:
        difficulty = "Any"  # Default if nothing valid entered

    # --- Optional: style preference ---
    print("\n✨ Style preference? (or press Enter to skip)")
    print("   Options: Creative / Realistic\n")
    style = input("   Style: ").strip().capitalize()
    if style not in ["Creative", "Realistic"]:
        style = "Creative"  # Default style

    # Package everything into a dictionary
    user_input = {
        "pieces": pieces,
        "theme": theme,
        "difficulty": difficulty,
        "style": style
    }

    return user_input


# ==============================================================
# STEP 2: Turn user input into an AI prompt
# ==============================================================

def generate_prompt(user_input):
    """
    Takes the user's input dictionary and builds a clear,
    detailed prompt to send to the AI.
    """

    # Format the list of pieces as a neat bullet list
    pieces_text = "\n".join(f"- {piece}" for piece in user_input["pieces"])

    # Build the full prompt string
    prompt = f"""
You are a fun and creative LEGO building assistant for beginners.

A user has the following LEGO pieces:
{pieces_text}

They want to build something with the theme: {user_input["theme"]}
Preferred difficulty: {user_input["difficulty"]}
Style preference: {user_input["style"]}

IMPORTANT RULES:
- ONLY use the pieces listed above. Do not add any extra pieces.
- Keep instructions simple and beginner-friendly (no complex language).
- Make the idea creative but realistic to actually build.

Please respond in EXACTLY this format (use these section headers):

NAME: [Creative name for the build]

DESCRIPTION: [1-2 sentence description of what it looks like]

STEPS:
1. [First building step]
2. [Second building step]
3. [Keep going — aim for 4-6 clear steps]

DIFFICULTY: [Easy / Medium / Hard]

STORY: [A fun 1-2 sentence backstory or theme for the build]
"""
    return prompt


# ==============================================================
# STEP 3: Call the AI (real API or mock fallback)
# ==============================================================

def call_ai_model(prompt):
    """
    Sends the prompt to Claude (the AI) and returns the response text.
    If no API key is found, it falls back to a built-in mock response.
    """

    api_key = os.environ.get("ANTHROPIC_API_KEY")  # Look for your API key

    if api_key:
        # --- REAL AI call using the Anthropic Python library ---
        try:
            import anthropic  # You need to install this: pip install anthropic

            client = anthropic.Anthropic(api_key=api_key)

            message = client.messages.create(
                model="claude-sonnet-4-6",  # Use the latest Claude model
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the text from the AI's response
            return message.content[0].text

        except ImportError:
            print("\n⚠️  The 'anthropic' library isn't installed.")
            print("   Run: pip install anthropic")
            print("   Falling back to mock response...\n")
            return mock_ai_response()

        except Exception as e:
            print(f"\n⚠️  API error: {e}")
            print("   Falling back to mock response...\n")
            return mock_ai_response()

    else:
        # --- No API key found — use the mock response ---
        print("\n💡 No API key found. Using a built-in demo response.")
        print("   (Set ANTHROPIC_API_KEY in your environment to use real AI)\n")
        return mock_ai_response()


def mock_ai_response():
    """
    A hardcoded example response — used when no API key is set.
    This lets you test the app without needing an account.
    """
    return """NAME: Neon Street Patrol Bike

DESCRIPTION: A small but fierce futuristic police bike built for high-speed chases through glowing city streets. Its red accents light up the dark roads ahead.

STEPS:
1. Lay out your black plates flat to create a long, narrow base for the bike body.
2. Stack two red bricks on top of each other at the front to form the nose of the bike.
3. Attach one wheel on each side near the front and one on each side near the back.
4. Add a single red brick upright at the very front as the headlight tower.
5. Place one black plate across the middle to create a low seat/cockpit area.
6. Finish by adding any remaining red bricks along the sides as glowing stripe details.

DIFFICULTY: Easy

STORY: This sleek patrol bike belongs to Officer Nova, the fastest cop in Neon District. She zooms between skyscrapers at midnight, keeping the streets safe from rogue delivery drones."""


# ==============================================================
# STEP 4: Display the final output nicely
# ==============================================================

def display_output(ai_response):
    """
    Takes the raw AI text and prints it in a clean, readable format.
    """
    print("\n" + "=" * 50)
    print("🏗️  YOUR LEGO BUILD IDEA")
    print("=" * 50)
    print(ai_response.strip())
    print("=" * 50)


# ==============================================================
# STEP 5: Main loop — ties everything together
# ==============================================================

def main():
    """
    The main function that runs the whole app.
    Keeps looping so the user can generate new ideas.
    """
    while True:
        # 1. Get input from the user
        user_input = get_user_input()

        # 2. Build the AI prompt
        prompt = generate_prompt(user_input)

        # 3. Call the AI (or mock)
        print("\n⏳ Generating your LEGO build idea...")
        ai_response = call_ai_model(prompt)

        # 4. Show the result
        display_output(ai_response)

        # 5. Ask if they want to try again
        print("\nWould you like to generate another idea?")
        again = input("Type 'yes' to try again, or press Enter to quit: ").strip().lower()

        if again != "yes":
            print("\n👋 Happy building! Have fun with your LEGO creations!\n")
            break  # Exit the loop and end the program


# ==============================================================
# Entry point — this runs when you do: python lego_generator.py
# ==============================================================

if __name__ == "__main__":
    main()
