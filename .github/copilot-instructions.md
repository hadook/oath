# Project Blueprint: Web-Based "Oath" Implementation

## Core Tech Stack & Tools
* **Backend:** Python (FastAPI), managed via `uv`, with linting/formatting via `ruff`.
* **Database:** SQLite (persisting lightweight instance state only).
* **Frontend:** TypeScript UI communicating via REST API and WebSockets.
* **Assets:** Static card images stored in `client/public/images/cards/`.

## Architecture & Design Patterns
1. **Separation of Concerns:**
   - `server/core/`: Pure game rules engine and domain models (no DB/HTTP dependencies).
   - `server/db/`: Persistence layer (SQLite repository logic).
   - `server/api/`: Routing, WebSockets, user authentication, and table management.
2. **Static Definition vs. Dynamic State Pattern:**
   - Master definitions live in `cards.json`.
   - SQLite only stores lightweight keys and mutable properties (e.g., `card_id`, `favor_tokens`).
3. **The Self-Hydrating Model Pattern:**
   - A global `CardRegistry` is loaded once at FastAPI startup from `cards.json`.
   - `Card` objects automatically fetch their static attributes (name, suit, etc.) during instantiation, allowing clean, object-oriented domain logic.
4. **Networking & Sync Strategy:**
   - **WebSockets** push incremental updates chronologically for active sessions to preserve move order and single-step animations.
   - **Tab-Sleep Guard:** If a client goes inactive or experiences a multi-step sequence gap, the UI halts, hides the board elements, and prompts the user to refresh to load a clean state snapshot.

## Development Milestones
- [ ] **Milestone 1:** Initialize server structure, `uv` environment, and `server/core/models.py` with the self-hydrating `Card` and `GameState` architecture.
- [ ] **Milestone 2:** Set up `cards.json` parsing and the global `CardRegistry`.
- [ ] **Milestone 3:** Build the SQLite database layer and repository handlers (`server/db/`).
- [ ] **Milestone 4:** Implement FastAPI routes, WebSocket sync handler, and basic rule evaluation (`server/api/` & `server/core/engine.py`).
- [ ] **Milestone 5:** Scaffold the TypeScript frontend client, establish WebSocket hooks, and implement the out-of-sync refresh guard pattern.
