# Change: Add RRHH send tracking and duplicate prevention

## Why
RRHH sends need durable tracking for each recipient and a guard against duplicate sends. The status updater must also align with the RRHH campaign segment and handle missing message IDs safely.

## What Changes
- Record RRHH sends in the tracking database with a fixed campaign segment.
- Skip sending when a SENT record already exists for the same segment + recipient.
- Update status refresh to scope by segment and mark missing message IDs as ERROR.

## Impact
- Affected specs: email-campaign-scripts
- Affected code: envios_de_email.py, actualizar_envios.py, app/models.py
