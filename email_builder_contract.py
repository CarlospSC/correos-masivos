"""Contract for campaign builders used by the sender script.

Builders return static campaign metadata plus recipient data and content payloads.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Optional, Protocol, Sequence, Union


@dataclass(frozen=True)
class EmailRecipient:
    email: str
    name: Optional[str] = None
    rut: Optional[str] = None
    company: Optional[str] = None


@dataclass(frozen=True)
class EmailContent:
    subject: str
    sender: str
    reply_to: str
    html_body: str
    text_body: str
    inline_images: Mapping[str, Union[Path, bytes]]
    attachments: Sequence[Path] = ()


@dataclass(frozen=True)
class EmailCampaign:
    segment: str
    recipients: Sequence[EmailRecipient]
    content: EmailContent


class EmailBuilder(Protocol):
    def build_campaign(self) -> EmailCampaign:
        """Return a fully populated campaign payload for the sender script."""
        raise NotImplementedError
