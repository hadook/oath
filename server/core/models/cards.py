from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TypedDict

from .enums import Suit


class CardRegistry:
    """Registry of static card definitions."""

    def __init__(self) -> None:
        self.cards: dict[str, Card] = {}

    def load_from_json(self, file_path: Path) -> None:
        with file_path.open(encoding="utf-8") as file:
            card_set = json.load(file)

        card_type = card_set["type"]

        if card_type == "denizen":
            for card_data in card_set["cards"]:
                card = DenizenCard.from_definition(card_data)
                self.cards[card.id] = card

        else:
            raise ValueError(f"Unsupported card type: {card_type!r}")

    def get(self, card_id: str) -> Card:
        try:
            return self.cards[card_id]
        except KeyError as error:
            raise KeyError(f"Card {card_id!r} not found in registry.") from error


@dataclass
class Card:
    """A base class for all cards in the game."""

    id: str
    type: str
    name: str


class RevealPrompt(TypedDict):
    """Resources to reveal when the site is flipped faceup and during setup."""

    favor: int
    secrets: int
    relics: int


class BurnCost(TypedDict):
    """Resources to burn as part of the cost to Recover a relic at a site."""

    favor: int
    secrets: int


class PayCost(TypedDict):
    """Favor to pay as part of the cost to Recover a relic at a site."""

    favor: int
    bank: Suit


class RecoverCost(TypedDict):
    """The cost to take a relic at the site with Recover."""

    burn: BurnCost | None
    pay: PayCost | None


@dataclass
class SiteCard(Card):
    """A card representing a site in the game."""

    capacity: int
    revealed: bool = False
    reveal_prompt: RevealPrompt | None = None
    recover_cost: RecoverCost | None = None


class Restriction(StrEnum):
    SITE = "site"
    ADVISER = "adviser"


@dataclass
class DenizenCard(Card):
    """A card representing a denizen in the game."""

    suit: Suit
    restriction: Restriction | None = None
    locked: bool = False
    revealed: bool = False
    favor: int = 0
    secrets: int = 0

    def __post_init__(self) -> None:
        """Validate game state data on initialization."""

        if self.locked and self.restriction is None:
            raise ValueError(f"Locked card {self.id!r} has no specified restriction.")

    @classmethod
    def from_definition(cls, data: dict[str, object]) -> DenizenCard:
        """Construct a card from static JSON data."""

        return cls(
            id=data["id"],
            type="denizen",
            name=data["name"],
            suit=Suit(data["suit"]),
            restriction=(
                Restriction(data["restriction"]) if data.get("restriction") else None
            ),
            locked=data.get("locked", False),
        )

    @classmethod
    def from_state(cls, data: dict[str, object], registry: CardRegistry) -> DenizenCard:
        """Construct a card from mutable game state data."""

        template = registry.get(data["id"])
        if not isinstance(template, DenizenCard):
            raise TypeError(f"Card {template.id!r} is not a denizen.")

        return cls(
            id=template.id,
            type=template.type,
            name=template.name,
            suit=template.suit,
            restriction=template.restriction,
            locked=template.locked,
            revealed=data.get("revealed", False),
            favor=data.get("favor", 0),
            secrets=data.get("secrets", 0),
        )

    def to_state(self) -> dict[str, object]:
        """Return a dictionary representation of the card: its id and mutable attributes."""

        return {
            "id": self.id,
            "revealed": self.revealed,
            "favor": self.favor,
            "secrets": self.secrets,
        }
