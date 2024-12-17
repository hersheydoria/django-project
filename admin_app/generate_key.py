from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key somewhere safe (e.g., in a file or an environment variable)
print("Generated Fernet key:", key)
