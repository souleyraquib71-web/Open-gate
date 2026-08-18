import json
import os
import requests
import webbrowser
from dotenv import load_dotenv

# 1. Charger la clé API depuis .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ Erreur : Clé GEMINI_API_KEY introuvable dans le fichier .env !")
    exit()

# 2. Profil de l'étudiant
PROFIL_ETUDIANT = {
    "nom": "Raquib",
    "niveau_actuel": "Licence en Informatique",
    "domaine_interet": ["Intelligence Artificielle", "Machine Learning", "Data Science"],
    "modalite_preferee": "En ligne ou Bourse internationale",
    "pays_origine": "Afrique de l'Ouest",
    "disponibilite": "Immédiate",
    "objectifs": "Obtenir un financement complet pour une formation ou un Master en IA."
}

# 3. Charger la source d'opportunités
chemin_fichier_data = os.path.join("data", "opportunities.json")
try:
    with open(chemin_fichier_data, "r", encoding="utf-8") as f:
        data = json.load(f)
        liste_opportunites = data.get("opportunities", [])
except Exception as e:
    print(f"❌ Erreur lors de la lecture du fichier data : {e}")
    exit()

# 4. Le System Prompt pour une réponse JSON structurée
SYSTEM_PROMPT = """
Tu es Open-Gate, un agent IA autonome de veille académique.
Compare le profil de l'étudiant avec chaque opportunité.
Tu dois répondre STRICTEMENT au format JSON avec cette structure exacte (sans texte autour) :
{
  "meilleure_opportunite": {
    "nom": "nom de l'offre",
    "score": 95,
    "pourquoi": "courte explication percutante",
    "lien_candidature": "url",
    "documents_a_preparer": ["doc 1", "doc 2"]
  },
  "offres_rejetees_count": 2
}
"""

def executer_agent():
    print("\n" + "=" * 60)
    print("🤖 [BACKGROUND] Open-Gate tourne en tâche de fond...")
    print(f"🔍 Scan de {len(liste_opportunites)} opportunités pour {PROFIL_ETUDIANT['nom']}...")
    print("=" * 60 + "\n")

    contenu_prompt = f"""
    {SYSTEM_PROMPT}

    Profil : {json.dumps(PROFIL_ETUDIANT, ensure_ascii=False)}
    Opportunités : {json.dumps(liste_opportunites, ensure_ascii=False)}
    """

    # Utilisation du endpoint Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": contenu_prompt}]}]
    }

    try:
        reponse = requests.post(url, json=payload)
        reponse_json = reponse.json()

        if "candidates" in reponse_json:
            texte_brut = reponse_json["candidates"][0]["content"]["parts"][0]["text"]
            # Nettoyer le format JSON si Gemini a mis des balises markdown ```json
            texte_propre = texte_brut.replace("```json", "").replace("```", "").strip()
            resultat = json.loads(texte_propre)

            top = resultat["meilleure_opportunite"]
            rejetees = resultat.get("offres_rejetees_count", 0)

            # Notification à l'utilisateur (Human-in-the-loop)
            print(f"✅ Analyse terminée : {rejetees} offre(s) rejetée(s) en arrière-plan car non adaptées.")
            print("\n" + "⭐" * 30)
            print(f"🎯 OPPORTUNITÉ RECOMMANDÉE : {top['nom']} (Match : {top['score']}%)")
            print(f"💡 Raison : {top['pourquoi']}")
            print("⭐" * 30 + "\n")

            # Demande de décision à l'étudiant
            choix = input(f"👉 Souhaitez-vous postuler à '{top['nom']}' ?\n[1] Oui, ouvrir la candidature et préparer ma checklist\n[2] Non, ignorer pour l'instant\nVotre choix (1 ou 2) : ")

            if choix.strip() == "1":
                print("\n🚀 Action validée !")
                # 1. Ouvrir le navigateur
                print(f"🌐 Ouverture du lien de candidature : {top['lien_candidature']}")
                webbrowser.open(top["lien_candidature"])

                # 2. Générer la checklist pour l'étudiant
                with open("to_do_candidature.txt", "w", encoding="utf-8") as f_todo:
                    f_todo.write(f"📋 CHECKLIST CANDIDATURE : {top['nom']}\n")
                    f_todo.write(f"Lien : {top['lien_candidature']}\n\n")
                    f_todo.write("Documents à préparer :\n")
                    for doc in top.get("documents_a_preparer", []):
                        f_todo.write(f" [ ] {doc}\n")

                print("📝 Fichier 'to_do_candidature.txt' créé avec succès pour suivre votre dossier !")
            else:
                print("👍 Entendu ! L'opportunité est archivée et l'agent continue sa veille.")

        else:
            print("❌ Erreur API :", reponse_json)
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution : {e}")

if __name__ == "__main__":
    executer_agent()