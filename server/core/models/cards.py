from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .enums import Suit

# ---


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

        elif card_type == "site":
            for card_data in card_set["cards"]:
                card = SiteCard.from_definition(card_data)
                self.cards[card.id] = card

        else:
            raise ValueError(f"Unsupported card type: {card_type!r}")

    def get(self, card_id: str) -> Card:
        try:
            return self.cards[card_id]
        except KeyError as error:
            raise KeyError(f"Card {card_id!r} not found in registry.") from error


# ---


@dataclass
class Card:
    """A base class for all cards in the game."""

    id: str
    type: str
    name: str


# ---


class Restriction(StrEnum):
    SITE = "site"
    ADVISER = "adviser"


@dataclass
class DenizenCard(Card):
    """A card representing a denizen in the game."""

    # static attributes
    suit: Suit
    restriction: Restriction | None = None
    locked: bool = False

    # mutable attributes
    faceup: bool = False
    favor: int = 0
    secrets: int = 0

    def __post_init__(self) -> None:
        """Validate game state data on initialization."""

        if self.locked and self.restriction is None:
            raise ValueError(f"Locked card {self.id!r} has no specified restriction.")

    @classmethod
    def from_definition(cls, data: dict[str, Any]) -> DenizenCard:
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
    def from_state(cls, data: dict[str, Any], registry: CardRegistry) -> DenizenCard:
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
            faceup=data["faceup"],
            favor=data["favor"],
            secrets=data["secrets"],
        )

    def to_state(self) -> dict[str, Any]:
        """Return a dictionary representation of the card: its id and mutable attributes."""

        return {
            "id": self.id,
            "faceup": self.faceup,
            "favor": self.favor,
            "secrets": self.secrets,
        }


# ---


@dataclass
class RevealPrompt:
    """Resources to reveal when the site is flipped faceup and during setup."""

    favor: int = 0
    secrets: int = 0
    relics: int = 0

    @classmethod
    def from_definition(cls, data: dict[str, Any]) -> RevealPrompt:
        return cls(
            favor=data.get("favor", 0),
            secrets=data.get("secrets", 0),
            relics=data.get("relics", 0),
        )


@dataclass
class BurnCost:
    """Resources to burn as part of the cost to Recover a relic at a site."""

    favor: int = 0
    secrets: int = 0

    @classmethod
    def from_definition(cls, data: dict[str, Any]) -> BurnCost:
        return cls(
            favor=data.get("favor", 0),
            secrets=data.get("secrets", 0),
        )


@dataclass
class PayCost:
    """Favor to pay as part of the cost to Recover a relic at a site."""

    favor: int
    bank: Suit

    @classmethod
    def from_definition(cls, data: dict[str, Any]) -> PayCost:
        return cls(
            favor=data["favor"],
            bank=Suit(data["bank"]),
        )


@dataclass
class RecoverCost:
    """The cost to take a relic at the site with Recover."""

    burn: BurnCost | None = None
    pay: PayCost | None = None

    @classmethod
    def from_definition(cls, data: dict[str, Any]) -> RecoverCost:
        burn_data = data.get("burn")
        pay_data = data.get("pay")

        return cls(
            burn=BurnCost.from_definition(burn_data) if burn_data else None,
            pay=PayCost.from_definition(pay_data) if pay_data else None,
        )


@dataclass
class SiteCard(Card):
    """A card representing a site in the game."""

    # static attributes
    capacity: int
    defense: int = 1
    reveal_prompt: RevealPrompt | None = None
    recover_cost: RecoverCost | None = None

    # mutable attributes
    faceup: bool = False

    @classmethod
    def from_definition(cls, data: dict[str, Any]) -> SiteCard:
        """Construct a card from static JSON data."""

        reveal_prompt_data = data.get("reveal_prompt")
        recover_cost_data = data.get("recover_cost")

        return cls(
            id=data["id"],
            type="site",
            name=data["name"],
            capacity=data["capacity"],
            defense=data.get("defense", 1),
            reveal_prompt=(
                RevealPrompt.from_definition(reveal_prompt_data)
                if reveal_prompt_data
                else None
            ),
            recover_cost=(
                RecoverCost.from_definition(recover_cost_data)
                if recover_cost_data
                else None
            ),
        )

    # TODO: Implement from_state and to_state methods for SiteCard
