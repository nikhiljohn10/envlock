[![codecov](https://codecov.io/gh/nikhiljohn10/envlock/branch/main/graph/badge.svg)](https://codecov.io/gh/nikhiljohn10/envlock)

# ENVLock

A secure CLI tool for encrypting, decrypting, shredding, and rotating secrets files (e.g., `.env`) using strong symmetric encryption (Fernet/AES).

## Features
- Encrypt (`lock`) and decrypt (`unlock`) files with a 256-bit key
- Key can be provided as hex, base64, or via the `ENVLOCK_ENCRYPTION_KEY` environment variable
- Secure file shredding (overwriting and deleting original file)
- Key rotation (`renew`) for re-encrypting with a new key
- Short and long CLI options for all commands

## Installation

Requires Python 3.8+ and the `cryptography` and `click` packages:

```sh
pip install cryptography click
```

## Usage

### Lock a file (encrypt)

```sh
python main.py lock [-f FILE] [-k KEY] [-h] [-s]
```
- `-f, --file`   : File to lock (default: `.env`)
- `-k, --key`    : Encryption key (hex or base64). If omitted, uses `ENVLOCK_ENCRYPTION_KEY` or generates a new key.
- `-h, --hide-key` : Hide generated key output (default: show)
- `-s, --shred`  : Securely delete original file after locking

**Example:**
```sh
python main.py lock -f .env -s
```

### Unlock a file (decrypt)

```sh
python main.py unlock [-f FILE] -k KEY
```
- `-f, --file`   : File to unlock (default: `.env.locked`)
- `-k, --key`    : Encryption key (hex or base64, required)

**Example:**
```sh
python main.py unlock -f .env.locked -k <key>
```

### Renew (rotate) encryption key

```sh
python main.py renew [-f FILE] --old-key OLDKEY [--new-key NEWKEY] [-h]
```
- `-f, --file`   : File to renew (default: `.env.locked`)
- `--old-key`    : Current encryption key (hex or base64, required)
- `--new-key`    : New encryption key (hex or base64, optional; if omitted, a new key is generated)
- `-h, --hide-key` : Hide generated new key output (default: show)

**Example:**
```sh
python main.py renew --old-key <oldkey>
```

## Key Management
- Keys are 32 bytes (64 hex chars or 32 bytes base64)
- Store keys securely (never in your repo)
- You can use the `ENVLOCK_ENCRYPTION_KEY` environment variable for automation

## Security Notes
- The encrypted file can be public; only the key must remain secret
- Never print or log the key in CI/CD logs
- Use secure deletion (`--shred`) for sensitive files
- Rotate keys regularly and after any suspected compromise

## License
MIT
