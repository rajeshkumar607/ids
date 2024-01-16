import subprocess
import os
import string
import secrets
import paramiko
# Generate Password For user
def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

random_string = generate_random_string(12)
user_password = random_string
def create_database(db_name, db_user, db_password):
    subprocess.run(['mysql', '-e', f'CREATE DATABASE {db_name};'])
    subprocess.run(['mysql', '-e', f'CREATE USER \'{db_user}\'@\'localhost\' IDENTIFIED BY \'{db_password}\';'])
    subprocess.run(['mysql', '-e', f'GRANT ALL PRIVILEGES ON {db_name}.* TO \'{db_user}\'@\'localhost\';'])
    subprocess.run(['mysql', '-e', 'FLUSH PRIVILEGES;'])
def create_user(username, homepath, password):
    
    subprocess.run(["useradd", "-m", "-d", homepath, "--shell", "/bin/bash", "-g",  "www-data", username], )
    command = f'echo "{username}:{password}" | chpasswd'
    subprocess.run(command, shell=True)
def install_wordpress(wordpress, installpath):
#     # Define Wordpress download URL
     wordpress_download_url = f"https://wordpress.org/latest.zip"

#     # Create the installation directory
     os.makedirs(install_path, exist_ok=True)

#     # Download Wordpress
     subprocess.run(["wget", wordpress_download_url, "-O", "wordpress.zip"], cwd=install_path)

#     # Extract Magento
     subprocess.run(["unzip",  "wordpress.zip"], cwd=install_path)

#     # Clean up the downloaded archive
     os.remove(os.path.join(install_path, "wordpress.zip"))
def ngninx_config(input_file, output_file, old_word, new_word):
    try:
        # Read the content from the input file
        with open(input_file, 'r') as file:
            content = file.read()

        # Replace the old word with the new word
        modified_content = content.replace(old_word, new_word)

        # Write the modified content to the output file
        with open(output_file, 'w') as file:
            file.write(modified_content)

        print(f"Word '{old_word}' replaced with '{new_word}'.")
        print(f"Modified content written to {output_file}")
        command = f'cd /etc/nginx/sites-enabled && ln -sf ../sites-available/{site_name}.conf && nginx -t'
        subprocess.run(command, shell=True)
        command = f'cp /etc/php/8.0/fpm/pool.d/www.conf /etc/php/8.0/fpm/pool.d/{site_name}.conf'
        subprocess.run(command, shell=True)
        command = f"sed -e '4s/www/{site_name}/' -i -e '23s/www-data/{site_name}/' -e '36s/php8.0-fpm/php8.0-fpm_{site_name}/' /etc/php/8.0/fpm/pool.d/{site_name}.conf "
        subprocess.run(command, shell=True)
        # testing php-fpm and restart 
        subprocess.run(["service", "php8.0-fpm", "restart"]) 
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

import paramiko

def proxy_nginx_config(hostname, port, username, password, command1, command2, output_file_path):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()

        # Automatically add the server's host key
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        ssh_client.connect(hostname, port=port, username=username, password=password)

        # Run the specified command
        stdin1, stdout1, stderr1 = ssh_client.exec_command(command1)
        stdin2, stdout2, stderr2 = ssh_client.exec_command(command2)

        # Print the command output
        print("Command Output For 1st command:")
        for line in stdout1:
            print(line.strip())
        for line in stdout2:
            command_output = line.strip()
            if command_output:
                return command_output
        with open(output_file_path, 'w') as local_file:
            local_file.write(command_output)

        print(f"Command output saved to: {output_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the SSH connection
        ssh_client.close()


if __name__ == "__main__":
     domain = input("Please Enter The Domain Name")
     parts = domain.split('.')
     site_name = parts[0]
     print(site_name)
     
     home_path = f"/var/www/html/{domain}"
     print(home_path)
     install_path = home_path
     wordpress_version = 1
     input_file_path = 'nginx.txt'
     output_file_path = f'/etc/nginx/sites-available/{site_name}.conf'
     print(output_file_path)
     old_word_to_replace = 'domain'
     new_word = f"{site_name}"
     hostname = "192.168.0.252"
     port = "15126"
     username = "root"
     password = "R@mR@jinIDS"
     commandtorun1 = f" bash /root/ids-scripts/nginx-config.bash {domain} 192.168.0.229 "
     commandtorun2 = "cat /root/ids-scripts/certbot.conf"
     output_file_path_certbot = 'certbot.conf'
     

#    Run the installation
     create_user(site_name, home_path, user_password)
     install_wordpress(wordpress_version, install_path)
     create_database(site_name, site_name, user_password)
     ngninx_config(input_file_path, output_file_path, old_word_to_replace, new_word)
     proxy_nginx_config(hostname, port, username, password, commandtorun1, commandtorun2, output_file_path_certbot)
     print (user_password)
     print("Wordpress installation completed.")
