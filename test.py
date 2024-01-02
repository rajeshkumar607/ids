import subprocess
import os

def create_database(db_name, db_user, db_password):
    subprocess.run(['mysql', '-e', f'CREATE DATABASE {db_name};'])
    subprocess.run(['mysql', '-e', f'CREATE USER \'{db_user}\'@\'localhost\' IDENTIFIED BY \'{db_password}\';'])
    subprocess.run(['mysql', '-e', f'GRANT ALL PRIVILEGES ON {db_name}.* TO \'{db_user}\'@\'localhost\';'])
    subprocess.run(['mysql', '-e', 'FLUSH PRIVILEGES;'])

def install_magento(magento_version, install_path, db_name, db_user, db_password):
    # Define Magento download URL
    magento_download_url = f"https://github.com/magento/magento2/archive/{magento_version}.zip"

    # Create the installation directory
    os.makedirs(install_path, exist_ok=True)

    # Download Magento
    subprocess.run(["wget", magento_download_url, "-O", f"magento-{magento_version}.zip"], cwd=install_path)

    # Extract Magento
    subprocess.run(["unzip", f"magento-{magento_version}.zip", "-d", install_path])

    # Clean up the downloaded archive
    os.remove(os.path.join(install_path, f"magento-{magento_version}.zip"))

    # Configure Magento
    subprocess.run(["composer", "install", "--working-dir", os.path.join(install_path, f"magento2-{magento_version}")])
    subprocess.run(["php", os.path.join(install_path, f"magento2-{magento_version}", "bin", "magento"), "setup:install",
                    "--base-url=http://localhost/",
                    "--db-host=localhost",
                    "--db-name=" + db_name,
                    "--db-user=" + db_user,
                    "--db-password=" + db_password,
                    "--admin-firstname=Admin",
                    "--admin-lastname=User",
                    "--admin-email=admin@example.com",
                    "--admin-user=admin",
                    "--admin-password=admin123",
                    "--language=en_US",
                    "--currency=USD",
                    "--timezone=America/New_York",
                    "--use-rewrites=1"])

if __name__ == "__main__":
    db_name = input("Enter Magento Database Name: ")
    db_user = input("Enter Magento Database User: ")
    db_password = input("Enter Magento Database Password: ")
    magento_version = input("Enter Magento Version (e.g., 2.4.3): ")
    install_path = input("Enter Installation Path: ")

    create_database(db_name, db_user, db_password)
    install_magento(magento_version, install_path, db_name, db_user, db_password)

    print("Magento installation completed.")
