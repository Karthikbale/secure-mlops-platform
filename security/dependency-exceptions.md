# Dependency Vulnerability Exception

## Package
- starlette 0.49.3
- click 8.1.8

## Scanner
pip-audit

## Reason
Available fixed versions require Python 3.10+.
Current Jenkins build environment uses Python 3.9.

## Risk Decision
Temporary acceptance.

## Remediation Plan
Migrate Jenkins build environment to Python 3.11 in a future platform upgrade.

## Owner
DevSecOps Team