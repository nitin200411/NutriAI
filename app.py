import os
import streamlit as st
import google.generativeai as genai

# ── constants ─────────────────────────────────────────────────────────
PREFERRED = "models/gemini-2.5-flash-latest"
TEMPERATURE   = 1

# ── Gemini client ─────────────────────────────────────────────────────
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def list_models():
    """Return only text-generation models that are still live."""
    return [
        m.name for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
        and "vision" not in m.name
        and not m.name.startswith("models/gemini-1.0")
    ]

def select_llm(model_id: str):
    return genai.GenerativeModel(
        model_name=model_id,
        generation_config={"temperature": TEMPERATURE},
    )

# ── prompt helpers ────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a certified nutritionist. "
    "For each food item in the comma-separated list, return:\n"
    "• Calories (kcal)\n"
    "• Macronutrients (protein, fat, carbohydrates, etc)\n"
    "• Micronutrients (vitamins, minerals, etc)\n"
    "• Any other relevant nutritional information\n"
    "Provide the information as plain Markdown bullet lists — no tables, "
    "no code fences, no extra commentary."
)

def build_prompt(food_list: str) -> str:
    return f"{SYSTEM_PROMPT}\n\nFood list: {food_list.strip()}"

def get_nutrition(food_list: str, model_id: str) -> str:
    llm = select_llm(model_id)
    response = llm.generate_content(build_prompt(food_list))
    return response.text

# ── Streamlit UI ──────────────────────────────────────────────────────
st.set_page_config(page_title="Nutrition Insight Generator", layout="wide")
st.title("NutriAI - Instant Nutritional Information")

with st.sidebar:
    models = list_models()
    st.write("Models your key can access:")
    for m in models:
        st.write("•", m)
    st.markdown("---")
    chosen = st.selectbox(
        "Choose model for this run:",
        models,
        index=models.index(PREFERRED) if PREFERRED in models else 0,
    )

food_input = st.text_area("Enter food items (comma-separated):", height=120)

if st.button("Get Nutritional Information"):
    if not food_input.strip():
        st.warning("Please enter at least one food item.")
        st.stop()

    with st.spinner("Fetching nutritional information…"):
        try:
            raw_text = get_nutrition(food_input, chosen)
        except Exception as e:
            st.error(f"Gemini API error: {e}")
            st.stop()

    st.markdown("### Nutritional Information")
    st.markdown(raw_text)
