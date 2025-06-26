# FAQ

**Q: Can I use envlock for files other than .env?**
A: Yes, you can lock/unlock any file by specifying the `-f` option.

**Q: Is the encrypted file safe to store in version control?**
A: Yes, as long as you keep the key secret.

**Q: How do I rotate my encryption key?**
A: Use the `renew` command with `--old-key` and optionally `--new-key`.

**Q: How do I securely delete the original file?**
A: Use the `--shred` option with the `lock` command.
