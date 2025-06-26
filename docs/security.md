# Security

- The encrypted file can be public; only the key must remain secret.
- Never print or log the key in CI/CD logs.
- Use secure deletion (`--shred`) for sensitive files.
- Rotate keys regularly and after any suspected compromise.
- See [SECURITY.md](../SECURITY.md) for responsible disclosure.
