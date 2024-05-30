# Personal Data Project

## Project Overview

This project focuses on handling personal data securely and efficiently. It involves understanding Personally Identifiable Information (PII), implementing logging mechanisms that obfuscate sensitive data, encrypting passwords, and authenticating database connections using environment variables.

## Project Timeline

- **Start Date:** May 29, 2024, 6:00 AM
- **End Date:** May 31, 2024, 6:00 AM
- **Checker Release:** May 29, 2024, 6:00 PM

## Reviews

- **Manual QA Review:** Must be requested upon project completion.
- **Auto Review:** Will be initiated at the project deadline.

## Learning Objectives

By the end of this project, you should be able to:

1. Identify examples of Personally Identifiable Information (PII).
2. Implement a log filter to obfuscate PII fields.
3. Encrypt passwords and validate input passwords.
4. Authenticate to a database using environment variables.

## Resources

- [What Is PII, non-PII, and Personal Data?](#)
- [Logging Documentation](#)
- [bcrypt Package](#)
- [Logging to Files, Setting Levels, and Formatting](#)

## Requirements

- **Environment:** Ubuntu 18.04 LTS, Python 3.7
- **File Standards:**
  - All files should end with a new line.
  - The first line of all files should be `#!/usr/bin/env python3`.
  - All files must be executable.
  - Compliance with `pycodestyle` (version 2.5).
  - Files' lengths will be tested using `wc`.

- **Documentation:**
  - A `README.md` file is mandatory at the root of the project folder.
  - All modules, classes, and functions must have proper documentation.
  - Documentation should be comprehensive and explain the purpose of the module, class, or method.
  - Functions should be type annotated.

## Implementation Details

### Personally Identifiable Information (PII)

PII includes any data that can be used to identify an individual, such as:
- Full Name
- Social Security Number
- Email Address
- Phone Number

### Log Filtering

Implement a log filter to obfuscate PII fields. This ensures sensitive data is not exposed in logs.

### Password Encryption

Use the `bcrypt` package to:
- Encrypt passwords.
- Validate input passwords against encrypted passwords.

### Database Authentication

Authenticate to a database using environment variables to store sensitive credentials securely.

## Usage

1. **Setup Environment:**
   ```sh
   sudo apt-get update
   sudo apt-get install python3.7
   sudo apt-get install python3-pip
   pip3 install pycodestyle bcrypt
sebsibe solomon
