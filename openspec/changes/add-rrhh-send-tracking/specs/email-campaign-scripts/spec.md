## ADDED Requirements
### Requirement: RRHH send tracking record
The system SHALL persist a tracking record for each RRHH email sent, including a fixed campaign segment, recipient identifiers, send status, message ID, and timestamps.

#### Scenario: Persist RRHH send record
- **WHEN** the RRHH sender delivers an email via SES
- **THEN** a tracking record is stored with segment, recipient email, status SENT, message ID, and sent timestamp

### Requirement: RRHH duplicate send prevention
The system SHALL avoid re-sending an RRHH email when a SENT tracking record already exists for the same segment and recipient email.

#### Scenario: Skip already-sent recipient
- **WHEN** the RRHH sender processes a recipient with an existing SENT record in the same segment
- **THEN** it skips the send and leaves the existing record unchanged

### Requirement: RRHH status updater scoping
The system SHALL scope status updates to the RRHH segment and mark records missing a message ID as ERROR.

#### Scenario: Mark missing message ID as error
- **WHEN** the RRHH status updater encounters a tracking record without a message ID
- **THEN** it sets the status to ERROR and records the update error
