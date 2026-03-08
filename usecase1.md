# Cas d'Usage #1 : La remontée d'information terrain "Friction Zéro" (Projet PUSH >>)

## 🏢 Contexte : L'industrie de la construction métallique
Dans une PME de construction métallique et serrurerie, le décalage temporel entre le terrain (les chantiers) et le bureau central est un point de friction majeur. 
Les équipes sur place manipulent des matériaux lourds, gèrent des urgences logistiques (rupture de consommables, problèmes de cotes, blocages matériels) et n'ont ni le temps ni l'environnement adéquat pour rédiger des rapports papier complexes.

**Le problème :**
- Perte d'informations critiques (matériel manquant signalé trop tard).
- Retard dans la facturation (les jalons terminés ne sont pas communiqués en temps réel).
- Déconnexion entre la réalité du chantier et le tableau de bord du dirigeant.

---

## 💡 La Solution : Le concept "PUSH >>"
L'objectif est de remplacer la contrainte administrative par un geste mécanique simple, universel et immédiat : un **PUSH**.

L'application agit comme une "avance rapide" (`>>`) sur la bureaucratie : 
1. L'ouvrier sort son smartphone.
2. Il presse le bouton **PUSH**.
3. Il dicte son message vocalement (*"Il manque des IPN de 200 sur le chantier Alpha"*).
4. L'information est instantanément transcrite et envoyée au bureau.

---

## ⚙️ Architecture Technique (V1 - MVP)
Ce premier cas d'usage repose sur une architecture légère, robuste et 100% Cloud :

* **Front-End Terrain (Mobile) :** Une WebApp minimaliste en HTML/JS, pensée pour l'extérieur. Un seul gros bouton d'action. Utilisation de l'API de reconnaissance vocale du smartphone.
* **Base de données (Transit) :** Google Sheets. Il sert de "hub" d'échange gratuit et ultra-rapide pour horodater et stocker les messages entrants.
* **Dashboard Bureau (Écran de contrôle) :** Une application développée en **Python (Streamlit)**. 
  - Connectée en direct à Google Sheets.
  - Dispose d'un système de rafraîchissement manuel/automatique pour garantir la stabilité de l'affichage ("Mode Tour de Contrôle").
  - Affiche des métriques clés : Nombre de messages, heure de la dernière transmission, historique inversé (plus récent en haut).

---

## 📈 Bénéfices Immédiats pour le Dirigeant
* **Visibilité en Temps Réel :** Le tableau de bord Streamlit permet de savoir à la seconde près ce qui se passe sur les différents sites.
* **Réactivité Logistique (La Zone Orange) :** Les commandes de réassort (gaz, boulonnerie spécifique) peuvent être déclenchées avant même que l'équipe ne rentre au dépôt le soir.
* **Déblocage des Chantiers (La Zone Rouge) :** Une anomalie signalée via PUSH permet au conducteur de travaux de réagir instantanément.
* **Acceptation par les équipes :** L'outil demande 0% de formation. S'ils savent envoyer un message vocal sur WhatsApp, ils savent utiliser PUSH.

---

## 🚀 Prochaine Étape (V2) : Le Cerveau IA
La remontée de texte brut n'est que la première étape. La V2 transformera **PUSH** en un véritable assistant logistique :
- **Analyse sémantique (Gemini / n8n) :** L'IA lira les messages PUSH entrant et les classera automatiquement (Urgence 🔴, Achat 🟠, Avancement 🟢).
- **Extraction de données :** L'IA isolera les quantités et les références matérielles dictées par l'ouvrier pour pré-remplir les bons de commande.
