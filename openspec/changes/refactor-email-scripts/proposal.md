# Change: Refactor email scripts into standalone sender/builders

## Why
The current email flow mixes sending, status updates, and campaign-specific content in a single script, which makes it harder to scale new campaigns and reuse behaviors.

## What Changes
- Split email responsibilities into standalone scripts: sender, status updater, and bounced re-sender.
- Create separate campaign builder scripts for Habitat and Alexia email content.
- Make the sender script import and use the desired campaign builder.

## Impact
- Affected specs: email-campaign-scripts (new)
- Affected code: envios_de_email.py, actualizar_envios.py, new campaign scripts at repo root
