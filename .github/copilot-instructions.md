# GitHub Copilot Instructions: Oath Web App

## Project Overview & Architecture
This project is a web-based implementation of the board game **Oath**, built using a server-authoritative monorepo architecture:
- **Backend:** Python (FastAPI) managing game state, rules, and actions.
- **Frontend:** TypeScript / React handling UI rendering and local predictive calculations.
- **Shared Assets:** A root-level `shared/` directory containing static JSON files (denizens, relics, sites, dice distributions) acting as the single source of truth for both client and server.
- **Persistence:** SQLite database storing the entire `GameState` as a single serialized JSON blob. No internal relational normalization is used for game entities.

---

## Backend Guidelines (Python / FastAPI)
- **State Mutability & Serialization:** The `GameState` is loaded from and saved to SQLite as a single JSON blob. Custom serialization/deserialization methods handle complex nested object trees and hydration. Models should remain pure data containers.
- **Action Handler Pattern:** All player actions (e.g., *Muster*, *Search*, *Campaign*) must live inside `server/core/actions/` inheriting from `BaseAction`. They follow an atomic lifecycle:
  1. Validate base requirements & payload.
  2. Resolve active modifiers (cards/advisors).
  3. Pay costs (supply, favor, tapping cards).
  4. Mutate the `GameState` and return the result.
- **Dice Engine:** Combat rolls must use the `DiceEngine` (`server/core/engine/dice.py`), which evaluates attack and defense dice against weights defined in `shared/dice.json`.

---

## Frontend Guidelines (TypeScript / React)
- **Atomic Action Pattern:** The client performs all predictive UI calculations locally (e.g., checking if a player can afford an action with specific modifiers toggled) to ensure zero-latency responsiveness.
- **Local Lookups:** When rendering components like sites or maps, look up derived data (such as which player pawns are standing at a site) locally using the existing `GameState` tree rather than expecting pre-mutated server DTOs.
- **Shared Types:** Keep client-side TypeScript models in sync with Python backend state models, referencing shared static JSON data directly from `shared/`.

---

## Coding Rules & Conventions
- **Declarative vs. Custom Modifiers:** 
  - Standard card modifiers (costs, numeric bonuses) must be declared in shared JSON files and evaluated via generic engine loops.
  - Complex, bespoke card abilities with multi-step logic or targeting must be isolated in explicit Python/TypeScript custom handlers.
- **Typing & Strictness:** Use strict Python type hints (`mypy`-friendly) and strong TypeScript interfaces. Avoid `any` types where possible.
- **File Structure Adherence:** 
  - State models: `server/core/models/`
  - Action logic & hooks: `server/core/actions/`
  - Dice & math engines: `server/core/engine/`
  - Static definitions: `shared/`


---

## Project structure

my-oath-project/
├── shared/
│   ├── denizens.json               # Static metadata & declarative modifiers
│   ├── relics.json                 # Relic card definitions
│   └── dice.json                   # Attack and defense face weights & distributions
│
├── server/
│   └── core/
│       ├── models/
│       │   ├── game_state.py
│       │   │   └── └── Class: GameState (Root state blob serialized to SQLite)
│       │   ├── player.py
│       │   │   ├── └── Class: Player (Holds current_site_id pawn reference)
│       │   │   └── └── Class: PlayerBoard (Tracks supply warbands, favor, advisors)
│       │   ├── map.py
│       │   │   ├── └── Class: Map
│       │   │   ├── └── Class: Region
│       │   │   └── └── Class: Site (Holds local garrison warbands, tokens, denizens)
│       │   └── cards.py
│       │       ├── └── Class: CardRegistry (Loads and queries shared JSON data)
│       │       ├── └── Class: Card (Base class for Denizens, Visions, Relics)
│       │       └── └── Class: Deck[T] (Generic container for homogeneous/heterogeneous stacks)
│       │
│       ├── engine/
│       │   └── dice.py
│       │       ├── └── Class: DiceEngine (Rolls attack/defense dice against distributions)
│       │       └── └── Class: BattleRollResult (Structured outcome of raw rolls & net hits)
│       │
│       └── actions/
│           ├── base.py
│           │   └── └── Class: BaseAction (Abstract base class defining validate/execute lifecycle)
│           ├── hooks.py
│           │   ├── └── Class: ActionModifiers (Bucket for gathered discounts/bonuses)
│           │   └── └── Class: ModifierOption (Structured toggle metadata for client/server sync)
│           ├── muster.py
│           │   └── └── Class: MusterAction
│           ├── search.py
│           │   └── └── Class: SearchAction
│           └── campaign.py
│               └── └── Class: CampaignAction (Integrates DiceEngine into combat resolution)
│
└── client/
    └── src/
        ├── types/
        │   └── game.ts             # TypeScript mirror interfaces of Python state models
        ├── utils/
        │   ├── dicePredictor.ts    # Client-side predictive pool calculation
        │   └── actionHelpers.ts    # Local validation & modifier selectors
        └── components/
            ├── BoardView.tsx       # React components rendering map, regions, and sites
            └── DiceRoller.tsx      # Dice face visual animations