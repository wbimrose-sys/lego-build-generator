"""
LEGO Build Idea Generator - Streamlit Web App
==============================================
Run this with:
  streamlit run lego_app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# ==============================================================
# Page configuration
# ==============================================================

st.set_page_config(
    page_title="LEGO Build Idea Generator",
    page_icon="🧱",
    layout="centered"
)

# ==============================================================
# App title and description
# ==============================================================

st.title("🧱 LEGO Build Idea Generator")
st.write("Enter your available LEGO pieces and a theme — the AI will come up with a creative build idea just for you!")

st.divider()

# ==============================================================
# User input section
# ==============================================================

# Text area for pieces
pieces_input = st.text_area(
    "📦 Your available LEGO pieces",
    placeholder="e.g.\n10 red bricks\n4 wheels\n6 black plates",
    height=150,
    help="Type one piece per line"
)

# Theme input
theme = st.text_input(
    "🎨 Build theme",
    placeholder="e.g. spaceship, castle, cyberpunk city, jungle base..."
)

# Two columns for difficulty and style
col1, col2 = st.columns(2)

with col1:
    difficulty = st.selectbox(
        "⚙️ Difficulty",
        ["Any", "Easy", "Medium", "Hard"]
    )

with col2:
    style = st.selectbox(
        "✨ Style",
        ["Creative", "Realistic"]
    )

st.divider()

# ==============================================================
# Generate button
# ==============================================================

generate = st.button("🚀 Generate my LEGO idea!", use_container_width=True)

# ==============================================================
# Generate prompt function
# ==============================================================

def generate_prompt(pieces, theme, difficulty, style):
    """Builds the AI prompt from user inputs."""
    pieces_list = "\n".join(f"- {p.strip()}" for p in pieces.strip().split("\n") if p.strip())

    prompt = f"""
You are a fun and creative LEGO building assistant for beginners.

A user has the following LEGO pieces:
{pieces_list}

They want to build something with the theme: {theme}
Preferred difficulty: {difficulty}
Style preference: {style}

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
# Call AI function
# ==============================================================

def call_ai(prompt):
    """Sends the prompt to Claude and returns the response."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Error: {e}"
    else:
        # Mock response if no API key
        return """NAME: Neon Street Patrol Bike

DESCRIPTION: A small futuristic police bike built for high-speed chases through glowing city streets. Its red accents light up the dark roads ahead.

STEPS:
1. Lay out your black plates flat to create a long, narrow base for the bike body.
2. Stack two red bricks on top at the front to form the nose of the bike.
3. Attach one wheel on each side near the front and one on each side near the back.
4. Add a single red brick upright at the front as the headlight tower.
5. Place one black plate across the middle to create a low seat/cockpit area.
6. Add remaining red bricks along the sides as glowing stripe details.

DIFFICULTY: Easy

STORY: This sleek patrol bike belongs to Officer Nova, the fastest cop in Neon District. She zooms between skyscrapers at midnight, keeping the streets safe from rogue delivery drones."""


# ==============================================================
# Display result
# ==============================================================

def display_result(response):
    """Parses and displays the AI response nicely."""

    # Split response into sections
    lines = response.strip().split("\n")

    name = ""
    description = ""
    steps = []
    difficulty_out = ""
    story = ""
    current_section = ""

    for line in lines:
        line = line.strip()
        if line.startswith("NAME:"):
            name = line.replace("NAME:", "").strip()
        elif line.startswith("DESCRIPTION:"):
            description = line.replace("DESCRIPTION:", "").strip()
            current_section = "description"
        elif line.startswith("STEPS:"):
            current_section = "steps"
        elif line.startswith("DIFFICULTY:"):
            difficulty_out = line.replace("DIFFICULTY:", "").strip()
            current_section = ""
        elif line.startswith("STORY:"):
            story = line.replace("STORY:", "").strip()
            current_section = "story"
        elif current_section == "steps" and line and line[0].isdigit():
            steps.append(line)
        elif current_section == "description" and line:
            description += " " + line
        elif current_section == "story" and line:
            story += " " + line

    # Display the result nicely
    st.success("✅ Your LEGO build idea is ready!")

    st.subheader(f"🏗️ {name}")

    if difficulty_out:
        st.badge(f"Difficulty: {difficulty_out}")

    if description:
        st.write(description)

    if steps:
        st.subheader("📋 Building Steps")
        for step in steps:
            st.write(step)

    if story:
        st.info(f"📖 **The story:** {story}")


# ==============================================================
# Run on button click
# ==============================================================

if generate:
    # Validate inputs
    if not pieces_input.strip():
        st.error("Please enter your LEGO pieces!")
    elif not theme.strip():
        st.error("Please enter a build theme!")
    else:
        # Show a spinner while generating
        with st.spinner("Generating your LEGO build idea..."):
            prompt = generate_prompt(pieces_input, theme, difficulty, style)
            response = call_ai(prompt)

        # Display the result
        display_result(response)

        st.divider()

        # Regenerate button
        st.write("Not happy with this idea?")
        if st.button("🔄 Generate another idea!", use_container_width=True):
            with st.spinner("Generating a new idea..."):
                prompt = generate_prompt(pieces_input, theme, difficulty, style)
                response = call_ai(prompt)
            display_result(response)
