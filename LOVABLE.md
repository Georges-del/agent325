# LOVABLE.md — Spécification de l'application « Agent 325 »

> **À donner à Lovable comme prompt de départ.**
> Cette application n'est pas un simple chatbot : c'est le poste de travail d'un stratège marketing, alimenté par la mémoire contenue dans ce dépôt.

---

## 1. Vision

Construire **le poste de travail d'un stratège marketing de niveau mondial**.

L'utilisateur (Delano Georges, Digitalforges — Abidjan) y crée des missions pour lui-même ou pour ses clients, remplit un diagnostic guidé, et reçoit des stratégies, scripts, visuels et calendriers prêts à publier.

**Le cœur du produit : l'agent ne se contente pas de répondre. Il applique un cadre.**
Ce cadre est dans `agent/SOUL.md` et `agent/AGENTS.md`. L'application doit le charger et le respecter.

---

## 2. Ce qui rend cette application différente

Trois règles du cadre doivent être **visibles dans l'interface**, pas seulement dans le prompt :

### Règle 1 — Le diagnostic doit être COMPLET
L'agent complète **4 points sur 7 lui-même** (recherche web + audit public). Seuls **prix, objectifs et budget** viennent de l'utilisateur.

→ L'interface propose un **assistant de diagnostic** qui lance des recherches, remplit ce qu'il peut, et ne demande que les 3 champs manquants.

### Règle 2 — Les conditions d'arrêt
L'agent **s'arrête et demande validation** avant : publier · dépenser · changer un positionnement · déclarer une stratégie définitive sur un diagnostic incomplet · mélanger deux clients · promettre un résultat non garanti · citer une preuve non vérifiée.

→ Chaque arrêt doit apparaître comme une **carte de validation** dans le fil : « L'agent a besoin de votre accord pour continuer ».

### Règle 3 — Cloisonnement des clients
Les données d'un client ne sont **jamais** mélangées avec celles d'un autre.

→ Chaque client a son espace isolé. L'agent ne charge que le contexte du client actif.

---

## 3. Écrans

### 3.1 Tableau de bord
- Missions en cours (interne / conseil)
- Compteurs : missions actives, livrables produits, clients suivis
- Objectifs 30/60/90 jours avec barres de progression
- Rappel des seuils cibles : **engagement > 5 %**, **CTR > 2 %**

### 3.2 Nouvelle mission
Assistant en 3 temps :
1. **Contexte** — client (ou « interne »), secteur, offre
2. **Diagnostic** — les 7 points ; les 4 automatiques sont lancés par l'agent, les 3 restants sont demandés à l'utilisateur
3. **Objectif** — notoriété / leads / ventes, échéance

Tant que les 7 points ne sont pas réunis, la mission est marquée **« brouillon »** — jamais « définitive ».

### 3.3 Chat avec Agent 325
- Interface conversationnelle
- Le persona vient de `agent/SOUL.md`, le cadre de `agent/AGENTS.md`
- Réponses en **français par défaut**
- L'agent peut produire : stratégie, script vidéo, légende, calendrier, visuel (brief), analyse
- Les **cartes de validation** apparaissent quand une condition d'arrêt est atteinte

### 3.4 Dossiers clients
- Un espace par client, strictement isolé
- Contenu : identité, positionnement, personas, piliers de contenu, historique des livrables
- **Aucune donnée partagée entre deux dossiers**

### 3.5 Livrables
- Bibliothèque de ce qui a été produit
- Types : stratégie (document), script vidéo, visuel, calendrier, rapport
- Export en PDF / copie presse-papiers

### 3.6 Calendrier éditorial
- Vue mensuelle des publications par plateforme
- Ratio imposé : **80 % valeur / 20 % promotion**
- Rappel des piliers de contenu (3 à 5 thèmes)

---

## 4. Modèle de données

```
Client
  id, nom, secteur, ville, mode (interne|conseil)
  identite_visuelle (logo, couleurs)
  positionnement (phrase)
  personas[]
  piliers_contenu[]
  archives_livrables[]

Mission
  id, client_id, titre, statut (brouillon|active|terminee)
  diagnostic {
    niche, concurrents, cible, offre,     ← remplies par l'agent
    prix, objectifs, budget                ← remplies par l'utilisateur
  }
  objectif (notoriete|leads|ventes), echeance

Livrable
  id, mission_id, type, contenu, date
  statut (brouillon|valide|publie)

ContenuPlanifie
  id, client_id, plateforme, date_publication
  type (valeur|promotion), titre, statut
```

---

## 5. Intégration de l'IA

**Le prompt système est assemblé dans cet ordre :**

```
1. agent/SOUL.md        → identité, expertise, méthode, règles absolues
2. agent/AGENTS.md      → contexte, diagnostic, conditions d'arrêt
3. Contexte du client   → UNIQUEMENT le client actif
```

**Règles d'assemblage :**
- Ne jamais charger deux dossiers clients en même temps
- Répondre en français par défaut, sauf demande contraire
- Ne jamais inventer un prix, un objectif ou un budget
- Marquer « à confirmer » tout élément non fourni par l'utilisateur

---

## 6. Direction visuelle

**Palette** — reprise de l'identité Digitalforges :

| Rôle | Couleur |
|---|---|
| Fond principal | Bleu nuit `#14304F` |
| Accent / action | Orange `#E8721C` |
| Texte principal | Blanc `#FFFFFF` |
| Surfaces | Bleu nuit éclairci, faible opacité |

**Principes :**
- Sobre, professionnel, orienté outil de travail
- Pas de dégradés criards, pas d'illustrations enfantines
- Densité d'information maîtrisée : **un écran = une intention**
- Cartes avec coins arrondis, ombres discrètes
- Typographie : une seule famille, hiérarchie par le poids

---

## 7. Ce que l'application doit refuser

| Situation | Comportement |
|---|---|
| L'utilisateur demande de publier directement | Afficher une carte de validation |
| L'utilisateur veut une stratégie « définitive » sans diagnostic | Signaler les 3 points manquants, proposer de livrer « à confirmer » |
| L'utilisateur demande des données d'un autre client | Refuser et expliquer le cloisonnement |
| L'utilisateur demande un chiffre de performance inventé | Refuser, proposer un seuil cible ou une hypothèse étiquetée |

---

## 8. Version 1 — périmètre minimal

Pour une première version fonctionnelle :

1. ✅ Tableau de bord simple
2. ✅ Création de mission + assistant de diagnostic
3. ✅ Chat avec l'agent (prompt = SOUL.md + AGENTS.md)
4. ✅ Dossiers clients isolés
5. ✅ Bibliothèque de livrables
6. ⏳ Calendrier éditorial (version ultérieure)
7. ⏳ Génération automatique de visuels (version ultérieure)

---

## 9. Note technique

Les scripts `scripts/gen_video.py` et `scripts/gen_visuel.py` documentent **la production réelle** de l'agent (vidéos verticales 1080×1920, visuels marketing). Ils ne sont pas exécutables côté navigateur — ils servent de **référence** pour une future intégration serveur.

Ils indiquent notamment deux règles de production à respecter dans l'application :

1. **Toujours vérifier un visuel généré avant de le livrer** — les modèles d'image produisent des artefacts (faux logo, accent cassé)
2. **Incruster le texte important au pixel plutôt que de laisser le modèle l'écrire** — garantit une orthographe et des accents parfaits
