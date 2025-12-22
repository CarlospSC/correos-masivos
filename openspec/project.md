# Project Context

## Purpose
Automate HR and benefits communications by generating documents and sending batch emails via AWS SES. The project also tracks delivery/open/bounce status in a local SQLite database.

## Tech Stack
- Python 3
- AWS SES / SESv2 via boto3
- pandas + openpyxl for Excel inputs
- Jinja2 + WeasyPrint for HTML/PDF generation
- SQLAlchemy + SQLite for tracking
- BeautifulSoup for HTML-to-text fallback
- tqdm for batch progress
- python-dotenv for local credentials

## Project Conventions

### Code Style
- Python scripts run from repo root; app/ holds shared modules.
- snake_case for variables/functions; class names in PascalCase.
- Format with Black (listed in requirements).
- Use .env for SES credentials; do not hardcode secrets.

### Architecture Patterns
- Batch scripts that read Excel lists, build templates, and send via SES.
- Email content assembled with MIME multipart (HTML + plain text, inline images).
- Tracking stored in tracking-alexia.db via SQLAlchemy models.
- Optional PDF generation from template.html for per-recipient documents.

### Testing Strategy
- No automated tests; manual verification using test Excel lists (e.g., rrhh_listado_correos_prueba.xlsx) and SES sandbox where applicable.

### Git Workflow
- TBD (please confirm branching/commit conventions).

## Domain Context
- HR/RRHH communications and benefits/reimbursement notices.
- Inputs arrive as Excel files with recipient data.
- Templates are HTML and static images embedded in emails.

## Important Constraints
- Requires valid SES credentials and verified sender identity.
- Excel inputs must include expected columns (e.g., Nombre, Correo).
- Locale dependency for PDF generation (e.g., es_ES.UTF-8).
- Handle PII carefully (emails, names, RUT).

## External Dependencies
- AWS SES / SESv2
- Local SQLite file tracking-alexia.db
- Excel input files and HTML templates
- Static images used in email bodies
