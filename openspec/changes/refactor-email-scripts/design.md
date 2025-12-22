## Context
Email sending, status updates, and campaign-specific content are currently co-located. The desired change is to split concerns while keeping the workflow as simple standalone scripts.

## Goals / Non-Goals
- Goals: isolate email sending, status updates, and campaign content; make campaigns pluggable from the sender script.
- Non-Goals: introduce new frameworks, restructure the database, or change SES credentials handling.

## Decisions
- Decision: Use standalone scripts at repo root for sender, status updater, bounced re-sender, and campaign builders.
- Decision: Define a minimal builder contract (e.g., a function that returns subject, from, reply-to, recipients, and MIME payload inputs) so the sender can import builders by name.
- Alternatives considered: consolidate into a package under app/; rejected to match the user's preference for standalone scripts.

## Risks / Trade-offs
- Duplicated utilities across scripts if the shared interface is too minimal. Mitigation: keep a small shared helper module if needed.

## Migration Plan
1. Extract campaign-specific content into builder scripts.
2. Update sender script to import builders.
3. Keep old scripts until new workflow is validated, then remove or archive as needed.

## Open Questions
- None.
