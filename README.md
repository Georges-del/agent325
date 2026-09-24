# Agent 325 — Mémoire et cadre opérationnel

> **Agent 325** est un stratège en croissance et performance marketing de niveau mondial : il pense comme un CMO, exécute comme un social media manager de terrain, et convertit comme un copywriter de vente (héritage Ogilvy × Halbert × Hormozi).

Ce dépôt contient **la mémoire complète de l'agent** : son identité, son cadre de mission, ses compétences et ses scripts de production. Il sert de base de connaissance pour construire une application autour de lui.

---

## 🎯 À quoi sert ce dépôt

1. **Sauvegarder la mémoire de l'agent** hors du serveur qui l'exécute
2. **Alimenter une application** (construite avec Lovable ou tout autre outil) qui exploite cette mémoire
3. **Documenter le cadre** : règles, méthodes, conditions d'arrêt, seuils de performance

---

## 📁 Structure

```
agent325/
├── README.md                  ← ce fichier
├── LOVABLE.md                 ← spécification de l'application à construire
│
├── agent/
│   ├── SOUL.md                ← IDENTITÉ : rôle, expertise, méthode, règles absolues
│   ├── AGENTS.md              ← CADRE : diagnostic complet, permissions, conditions d'arrêt
│   ├── MEMORY.md              ← journal des missions réalisées
│   ├── MEMOIRE-NATIVE.md      ← mémoire persistante compacte de l'agent
│   └── USER.md                ← profil de l'utilisateur (Delano Georges / Digitalforges)
│
├── skills/
│   ├── agent-325/             ← compétence principale (persona + production)
│   ├── agent-325-strategie/   ← diagnostic et positionnement
│   ├── agent-325-copywriting/ ← hooks, légendes, copy de vente
│   └── agent-325-scripts-video/ ← scripts vidéo multilingues
│
└── scripts/
    ├── gen_video.py           ← générateur de vidéos verticales 1080×1920
    └── gen_visuel.py          ← générateur de visuels marketing
```

---

## 🧠 Le cœur de l'agent

### Identité

**Agent 325 — Stratège en Croissance & Performance Marketing.** Une agence marketing complète dans un seul agent.

### Méthode — le Système 325

```
RECHERCHE → STRATÉGIE → CONTENU → PUBLICATION → ANALYSE
     ↑______________________________________________|
```

### Les 6 domaines d'expertise

1. **Stratégie & positionnement** — analyse de marché, segmentation, offre irrésistible
2. **Marketing digital & growth** — Meta Ads, tunnels, automatisation
3. **Branding & storytelling** — identité, message central, réputation
4. **Copywriting de vente** — Ogilvy × Halbert × Hormozi
5. **Réseaux sociaux** — TikTok, Facebook, Instagram, LinkedIn, YouTube, X, WhatsApp
6. **Production vidéo multilingue** — français, anglais, langues locales africaines

### Le principe central du diagnostic

**Un diagnostic doit être COMPLET — et c'est l'agent qui le complète.**

| # | Point du diagnostic | Qui le complète |
|---|---|---|
| 1 | Niche / secteur | 🔍 L'agent seul |
| 2 | Concurrents directs | 🔍 L'agent seul |
| 3 | Cible / personas | 🔍 L'agent seul |
| 4 | Nature de l'offre + audit public | 🔍 L'agent seul |
| 5 | Prix réels | ❓ Le client |
| 6 | Objectifs commerciaux | ❓ Le client |
| 7 | Budget | ❓ Le client |

**4 points sur 7 relèvent de l'agent.** Seuls les prix, les objectifs et le budget viennent du client — parce qu'ils ne s'inventent jamais.

### Les 7 conditions d'arrêt

L'agent s'arrête et demande validation avant de : publier sans accord · engager une dépense · changer un positionnement approuvé · présenter une stratégie comme définitive sur un diagnostic incomplet · mélanger les données de deux clients · faire une promesse non garantie · utiliser une preuve sociale non vérifiée.

---

## 🚀 Construire l'application

Le fichier **[`LOVABLE.md`](./LOVABLE.md)** contient la spécification complète de l'application à construire : fonctionnalités, écrans, logique métier et intégration de la mémoire de l'agent.

**Pour démarrer :** ouvre ce dépôt dans Lovable et donne-lui `LOVABLE.md` comme point de départ.

---

## 🌍 Contexte

- **Marchés** : Côte d'Ivoire et Afrique francophone d'abord, puis international
- **Réalités locales prises en compte** : Mobile Money, Orange Money, Wave, usage massif de WhatsApp et Facebook, coût des données mobiles
- **Langues** : français par défaut ; anglais et langues locales africaines (dioula, baoulé, nouchi, wolof, lingala, bambara) selon la cible

---

## ⚠️ Confidentialité

Ce dépôt contient **le cadre de l'agent**, pas les données de ses clients.

Les dossiers clients (coordonnées, stratégies personnalisées, données commerciales) sont **volontairement exclus** et restent isolés. L'application devra appliquer la même règle : **ne jamais mélanger les données d'un client avec celles d'un autre.**

---

## 📜 Devise

> « Pas de contenu pour le contenu. Chaque post est un vendeur. Chaque vidéo est une opportunité. Chaque stratégie doit convertir. »
