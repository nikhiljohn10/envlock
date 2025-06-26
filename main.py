import os
import click
import base64
import secrets
from cryptography.fernet import Fernet

def to_base64(data):
    return base64.urlsafe_b64encode(data).decode()

def from_hex(hex_str):
    return bytes.fromhex(hex_str)

def shred_file(file_path, passes=3):
    try:
        if not os.path.isfile(file_path):
            return
        length = os.path.getsize(file_path)
        with open(file_path, 'ba+', buffering=0) as f:
            for _ in range(passes):
                f.seek(0)
                f.write(secrets.token_bytes(length))
        os.remove(file_path)
    except Exception:
        pass

def get_binary_key(key):
    if key is None:
        key = os.environ.get("ENVLOCK_ENCRYPTION_KEY")
    if key is None:
        return secrets.token_bytes(32), True  # True: generated
    if len(key) == 64:
        try:
            return from_hex(key), False
        except Exception:
            print("Invalid hex key.")
            return None, False
    try:
        return base64.urlsafe_b64decode(key.encode()), False
    except Exception:
        print("Invalid key format.")
        return None, False

def lock_file(input_file, key=None, show_key=True, shred=False):
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist.")
        return
    with open(input_file, 'rb') as f:
        data = f.read()
    binary_key, generated = get_binary_key(key)
    if binary_key is None:
        return
    if generated and show_key:
        print(f"Encryption key (hex): {binary_key.hex()}")
    fernet_key = base64.urlsafe_b64encode(binary_key)
    if len(binary_key) != 32:
        print("Key must be 32 bytes (64 hex chars or 32 bytes base64).")
        return
    fernet = Fernet(fernet_key)
    encrypted = fernet.encrypt(data)
    output_file = input_file + '.locked'
    with open(output_file, 'wb') as f:
        f.write(encrypted)
    try:
        os.chmod(output_file, 0o600)
    except Exception:
        pass
    print(f"Locked file created: {output_file}")
    if shred:
        shred_file(input_file)
        print(f"Original file {input_file} securely deleted.")
    del data, encrypted, fernet

def unlock_file(input_file, key):
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist.")
        return
    with open(input_file, 'rb') as f:
        encrypted = f.read()
    binary_key, _ = get_binary_key(key)
    if binary_key is None:
        return
    fernet_key = base64.urlsafe_b64encode(binary_key)
    if len(binary_key) != 32:
        print("Key must be 32 bytes (64 hex chars or 32 bytes base64).")
        return
    fernet = Fernet(fernet_key)
    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        print("Decryption failed. Invalid key or corrupted file.")
        return
    output_file = input_file[:-7] if input_file.endswith('.locked') else input_file + '.unlocked'
    with open(output_file, 'wb') as f:
        f.write(decrypted)
    try:
        os.chmod(output_file, 0o600)
    except Exception:
        pass
    print(f"Unlocked file created: {output_file}")
    del decrypted, encrypted, fernet

@click.group()
def cli():
    """env file locker/unlocker"""
    pass

@cli.command()
@click.option('-f', '--file', 'file_', type=click.Path(exists=True), help='File to lock (default: .env)')
@click.option('-k', '--key', help='Encryption key (32-byte urlsafe base64 string)')
@click.option('-h', '--hide-key/--show-key', default=False, help='Hide generated key (default: show)')
@click.option('-s', '--shred/--no-shred', default=False, help='Securely delete original file after locking')
def lock(file_, key, hide_key, shred):
    """Lock a file (default: .env)"""
    input_file = file_ if file_ else '.env'
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist. Use --file to specify a file.")
        return
    lock_file(input_file, key, not hide_key, shred)

@cli.command()
@click.option('-f', '--file', 'file_', type=click.Path(exists=True), help='File to unlock (default: .env.locked)')
@click.option('-k', '--key', required=True, help='Encryption key (32-byte urlsafe base64 string)')
def unlock(file_, key):
    """Unlock a file (default: .env.locked)"""
    input_file = file_ if file_ else '.env.locked'
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist. Use --file to specify a file.")
        return
    unlock_file(input_file, key)

@cli.command()
@click.option('-f', '--file', 'file_', type=click.Path(exists=True), help='File to renew (default: .env.locked)')
@click.option('--old-key', required=True, help='Current encryption key (hex or base64)')
@click.option('--new-key', help='New encryption key (hex or base64, optional)')
@click.option('-h', '--hide-key/--show-key', default=False, help='Hide generated new key (default: show)')
def renew(file_, old_key, new_key, hide_key):
    """Re-encrypt a locked file with a new key (key renewal)"""
    input_file = file_ if file_ else '.env.locked'
    if not os.path.exists(input_file):
        print(f"File {input_file} does not exist. Use --file to specify a file.")
        return
    # Decrypt with old key
    with open(input_file, 'rb') as f:
        encrypted = f.read()
    old_binary_key, _ = get_binary_key(old_key)
    if old_binary_key is None:
        return
    old_fernet_key = base64.urlsafe_b64encode(old_binary_key)
    if len(old_binary_key) != 32:
        print("Old key must be 32 bytes (64 hex chars or 32 bytes base64).")
        return
    fernet = Fernet(old_fernet_key)
    try:
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        print("Decryption failed. Invalid old key or corrupted file.")
        return
    # Encrypt with new key
    new_binary_key, generated = get_binary_key(new_key)
    if new_binary_key is None:
        return
    new_fernet_key = base64.urlsafe_b64encode(new_binary_key)
    if len(new_binary_key) != 32:
        print("New key must be 32 bytes (64 hex chars or 32 bytes base64).")
        return
    new_fernet = Fernet(new_fernet_key)
    new_encrypted = new_fernet.encrypt(decrypted)
    with open(input_file, 'wb') as f:
        f.write(new_encrypted)
    print(f"File re-encrypted with new key: {input_file}")
    if generated and not hide_key:
        print(f"New encryption key (hex): {new_binary_key.hex()}")
    del decrypted, encrypted, fernet, new_fernet, new_encrypted

if __name__ == '__main__':
    cli()
