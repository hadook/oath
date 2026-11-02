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