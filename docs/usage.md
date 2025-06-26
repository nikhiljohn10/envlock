# Usage

## Basic Commands

### Lock a file
```sh
envlock lock -f .env -s
```

### Unlock a file
```sh
envlock unlock -f .env.locked -k <key>
```

### Renew (rotate) encryption key
```sh
envlock renew --old-key <oldkey>
```

## Advanced Usage
- Use stdin/stdout for piping secrets.
- Use the `--shred` option to securely delete the original file.
- Use environment variable `ENVLOCK_ENCRYPTION_KEY` for automation.
