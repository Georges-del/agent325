# MEMORY.md — Mémoire persistante d'Agent 325

Ce fichier est mis à jour par l'agent (ou par Delano) après chaque mission importante. Il permet à Agent 325 de garder le fil d'une session à l'autre, même sans mémoire native.

## Format d'une entrée

```
## [AAAA-MM-JJ] Titre court de la mission
- Client / projet : (interne Digitalforges ou nom du client tiers)
- Décision prise :
- Résultat / statut :
- À suivre :
```

## Historique

*(la plus récente en haut)*

## [2026-09-22] AgriPass 360 — lancement marketing
- Client / projet : **interne** (Digitalforges) — application propre à Delano Georges
- Produit : AgriPass 360 — passeport agricole panafricain. Identité officielle par producteur, traçabilité parcelle → cycle → récolte → lot, fonctionne hors connexion, saisie vocale assistée (le producteur dicte, l'IA propose un brouillon, rien n'est enregistré sans confirmation), 54 pays référencés, données hébergées en Europe (Paris). URL : https://agripass360-portail.vercel.app
- Angle stratégique retenu : **EUDR**. Depuis le 01/09/2026 la carte du producteur est obligatoire pour vendre du cacao en Côte d'Ivoire ; au 30/12/2026 l'Union européenne exigera une traçabilité **parcelle par parcelle** (6 décimales, art. 2(28)). L'UE absorbe ~66 % des exportations ivoiriennes de cacao. Erreur de rejet fréquente : soumettre les coordonnées de la coopérative au lieu du parcellaire.
- Livrables produits : affiche Facebook 1080×1080, affiche WhatsApp 1080×1920, vidéo verticale 1080×1920 de 52 s (6 plans, voix off française, sous-titres incrustés), texte de publication Facebook + message WhatsApp.
- Résultat / statut : livrables remis. **Publication NON effectuée** — Delano doit la faire lui-même, ou fournir un jeton d'accès Page Meta.
- À suivre : publication des contenus ; recharge du crédit OpenRouter (quota atteint en fin de session) ; musique de fond à ajouter dans CapCut ; envisager une version anglaise de la vidéo.

## [2026-09-22] Les Voyages de Perle & Services — stratégie marketing complète
- Client / projet : **mode conseil** (client tiers confié par Delano Georges)
- Client : Les Voyages de Perle & Services — gérante PerlerareGyna Andoh Aka. Agence de voyage, Palmeraie quartier pharmacie Enica, Abidjan. Tél. 07 08 94 96 21 / 01 60 12 05 05. Facebook : profil personnel « perlerarea andoh » (3 900 amis, 3 500 publications).
- Services : billetterie aérienne, réservation d'hôtels, organisation de séjours, voyages en famille, voyages en couple, épargne voyage, assistance visa (Schengen, Chine, Dubaï, Turquie).
- Diagnostic : 5 freins identifiés — (1) activité menée sur un profil personnel et non une Page pro ; (2) contenu de politesse qui ne vend rien ; (3) sept services empilés sur un même visuel ; (4) aucune offre concrète ni appel à l'action mesurable ; (5) rendu visuel amateur.
- Positionnement retenu : **« Votre voyage, sans arnaque et sans stress. »** — le premier frein du marché ivoirien n'est pas le prix mais la peur de l'arnaque (affaires médiatisées : Arsenal Voyage 28,25 M FCFA, cinq agences poursuivies pour 21 milliards FCFA).
- Décision structurante : faire de **l'ÉPARGNE VOYAGE le produit phare** (aujourd'hui sixième icône d'un flyer) et de **WhatsApp Business le canal de vente principal**.
- Livrables produits : document PDF de 8 pages (13 sections : fiche de mission, diagnostic, positionnement, personas, 4 piliers de contenu, calendrier 30 jours, 5 scripts vidéo, WhatsApp Business, 2 plans publicitaires 50 000 F et 300 000 F, KPI, plan 7 jours) ; visuel de démonstration « Épargne Voyage » avec logo réel intégré ; logo détouré ; vidéo verticale 1080×1920 de 36 s (script « les 3 signes d'une arnaque »).
- Résultat / statut : livrés. En attente de confirmation des tarifs réels par destination avant tournage des scripts.
- À suivre : remplir les prix réels ; créer la Page professionnelle ; faire relire la vidéo par la cliente avant publication.

### Enseignements techniques de la session

- **Génération d'images** : `google/gemini-3-pro-image` respecte les ratios et écrit correctement le français accentué. `google/gemini-2.5-flash-image` sort toujours en 1024×1024 et **casse les accents** dans les gros titres. Toujours vérifier un visuel avant livraison — un faux logo inventé par le modèle (« Ivoire Évasion ») a été détecté et rejeté.
- **Vidéo** : pipeline ffmpeg + edge-tts + Pillow opérationnel (Ken Burns, texte incrusté au pixel, voix off française, sous-titres). Aucune génération de prise de vue réelle possible sans clé fal.ai / Runway / Kling.
- **Coût / quota** : le crédit OpenRouter a été épuisé en fin de session. Prévoir une recharge avant les missions visuelles lourdes.
- **Voix** : la voix TTS par défaut était anglaise (`en-US-EmmaMultilingualNeural`). Réglage corrigé vers le français.

---

## Règles de tenue de cette mémoire

1. Une entrée par mission ou décision stratégique significative (pas les échanges mineurs).
2. Jamais de données sensibles d'un client dans une entrée liée à un autre (voir cloisonnement dans AGENTS.md).
3. Purge annuelle recommandée des entrées obsolètes (> 12 mois) sauf décisions structurantes encore actives.