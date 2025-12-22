## 1. Implementation
- [ ] 1.1 Define a minimal email builder contract (inputs/outputs) for sender integration.
- [ ] 1.2 Create a standalone sender script that imports a selected builder and sends emails.
- [ ] 1.3 Split status update logic into a standalone script that updates delivery/open/bounce events.
- [ ] 1.4 Create a bounced re-sender script that re-sends bounced emails using the same builder contract.
- [ ] 1.5 Extract Alexia campaign content into its own builder script.
- [ ] 1.6 Add a Habitat campaign builder script (or extract existing logic if already present).

## 2. Validation
- [ ] 2.1 Manually run the sender script for Alexia and confirm send flow completes.
- [ ] 2.2 Manually run the status updater and confirm statuses update in tracking DB.
- [ ] 2.3 Manually run the bounced re-sender against a bounced record set.
