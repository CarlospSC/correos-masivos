## ADDED Requirements
### Requirement: Send Emails Script
The system SHALL provide a standalone sender script that imports a selected campaign builder and sends emails using SES.

#### Scenario: Send a campaign via a builder
- **WHEN** the sender script is executed with the Alexia campaign builder
- **THEN** it builds the email content and sends messages to the campaign recipients

### Requirement: Update Email Status Script
The system SHALL provide a standalone script to update delivery, open, and bounce events in the tracking database based on SES insights.

#### Scenario: Update delivery and open events
- **WHEN** the status updater script runs for existing sent emails
- **THEN** it updates received/opened timestamps and status values

### Requirement: Bounced Email Re-sender Script
The system SHALL provide a standalone script that re-sends emails that previously bounced.

#### Scenario: Re-send bounced emails
- **WHEN** the re-sender script runs against emails marked as bounced
- **THEN** it attempts to re-send and updates the tracking record

### Requirement: Alexia Campaign Builder
The system SHALL provide a standalone builder script that creates the Alexia campaign email content for the sender script.

#### Scenario: Build Alexia email content
- **WHEN** the Alexia builder is invoked by the sender
- **THEN** it returns the subject, sender metadata, recipients, and body payloads

### Requirement: Habitat Campaign Builder
The system SHALL provide a standalone builder script that creates the Habitat campaign email content for the sender script.

#### Scenario: Build Habitat email content
- **WHEN** the Habitat builder is invoked by the sender
- **THEN** it returns the subject, sender metadata, recipients, and body payloads
