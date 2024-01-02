import subprocess

def create_user(username, password):
    try:
        # Create user
        subprocess.run(['sudo', 'useradd', '-m', '-p', password, username], check=True)

        print(f"User '{username}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating user: {e}")

if __name__ == "__main__":
    # Replace 'newuser' and 'password123' with your desired username and password
    new_username = 'newuser'
    new_password = 'password123'

    create_user(new_username, new_password)
