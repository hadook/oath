oath/
│
├── server/                       # Python Backend (FastAPI + Game Engine)
│   ├── pyproject.toml            # uv dependencies & ruff configuration
│   ├── main.py                   # FastAPI entry point & WebSocket hub
│   ├── core/                     # Pure domain logic (no DB/HTTP knowledge)
│   │   ├── models.py             # GameState, Cards, Sites (to_dict / from_dict)
│   │   └── engine.py             # Rules engine & action validation
│   ├── db/                       # Persistence layer
│   │   └── repository.py         # SQLite CRUD for users & game sessions
│   └── data/
│       └── cards.json            # Master static definitions
│
└── client/                       # TypeScript Frontend (UI + WebSocket client)
    ├── src/
    └── package.json