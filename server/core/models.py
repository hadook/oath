from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class CardRegistry:
    _definitions: dict[str, dict[str, Any]] = {}  # noqa: RUF012

    @classmethod
    def load_definitions(cls, definitions: dict[str, dict[str, Any]]) -> None:
        cls._definitions = definitions

    @classmethod
    def get(cls, card_id: str) -> dict[str, Any]:
        if card_id not in cls._definitions:
            raise ValueError(f"Card ID '{card_id}' not found in registry.")
        return cls._definitions[card_id]


@dataclass
class Card:
    card_id: str
    favor: int = 0

    name: str = field(init=False)
    suit: str = field(init=False)

    def __post_init__(self) -> None:
        static_data = CardRegistry.get(self.card_id)
        self.name = static_data["name"]
        self.suit = static_data["suit"]
