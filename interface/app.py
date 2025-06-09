import streamlit as st
from transformers import pipeline
from huggingface_hub import login
import hashlib

# Connexion Hugging Face (facultatif si le modèle est public)
login(token="YOUR_TOKEN_HERE")

# Fonction : générer une couleur hex unique pour une entité
def generate_color(label_base):
    hash_object = hashlib.md5(label_base.encode())
    return "#" + hash_object.hexdigest()[:6]

# Interface : choix du modèle
st.title("🔍 BioNER-Highlight: Named Entity Recognition for Biological Texts")
model_choice = st.selectbox("📦 Choose a model:", [
    "mkouka/ner_roberta_v3",
    "mkouka/ner_roberta_v10"
])

# Chargement du modèle (avec cache)
@st.cache_resource
def load_model(model_name):
    return pipeline("ner", model=model_name, grouped_entities=True)

ner_pipeline = load_model(model_choice)

# Exemple
if st.button("Insert an example"):
    st.session_state["text"] = (
        "The Carcharhinus macloti is a species of requiem shark, in the family Carcharhinidae. Distinguishing characteristics include dusky-colored fins without prominent markings, a short free rear tip on the second dorsal fin, and tooth shape and number. A heavy-bodied shark with a "typical" streamlined shape, the Caribbean reef shark is difficult to distinguish from other large requiem shark species. It usually measures 2–2.5 m  long; the maximum recorded length is 3 m and the maximum reported weight is 70 kg . The coloration is dark gray or gray-brown above and white or white-yellow below, with an inconspicuous white band on the flanks"
    )

text = st.text_area("📝 Enter a text to analyze:", height=200, key="text")

# Analyse
if st.button("Analyze"):
    if not text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        results = ner_pipeline(text)

        # Couleur unique par base de label (ex: SPECIE, FAMILY...)
        label_colors = {}
        for entity in results:
            label_full = entity["entity_group"]
            label_base = label_full.split("-")[-1] if "-" in label_full else label_full
            if label_base not in label_colors:
                label_colors[label_base] = generate_color(label_base)

        # Texte annoté
        annotated_text = ""
        last_idx = 0
        for entity in results:
            start, end = entity["start"], entity["end"]
            word = text[start:end]
            label_full = entity["entity_group"]
            label_base = label_full.split("-")[-1] if "-" in label_full else label_full
            color = label_colors[label_base]

            annotated_text += text[last_idx:start]
            annotated_text += (
                f"<span style='background-color:{color}; padding:3px 5px; border-radius:4px;'>"
                f"{word} <sub><i>{label_full}</i></sub></span>"
            )
            last_idx = end

        annotated_text += text[last_idx:]
        st.markdown(annotated_text, unsafe_allow_html=True)

        # Afficher les probabilités
        st.subheader("📈 Probabilities of detected entities")
        for entity in results:
            word = text[entity["start"]:entity["end"]]
            label = entity["entity_group"]
            score = entity.get("score", 0.0)
            st.markdown(f"- **{word}** ({label}) : `{score:.4f}`")
