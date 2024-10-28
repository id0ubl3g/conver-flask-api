import subprocess
import shutil

def check_and_install_libreoffice():
        if shutil.which('libreoffice') is not None:
            print("LibreOffice is already installed.\n")
            return True

        print("LibreOffice is not installed. Installing...\n")
        
        try:
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'libreoffice'], check=True)
            print("LibreOffice has been successfully installed.\n")
            return True

        except KeyboardInterrupt:
            print("\nInstallation cancelled.")
            return False

        except subprocess.CalledProcessError:
            print("\nInstallation failed.")
            print("To install LibreOffice manually, run the following commands in your terminal:")
            print("sudo apt update")
            print("sudo apt install -y libreoffice")
            return False
