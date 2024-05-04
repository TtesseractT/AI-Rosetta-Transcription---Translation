import shutil
import subprocess
import requests
import platform
import os
from zipfile import ZipFile
from pathlib import Path

# This code will install all dependancies based on the current needs of the user:
def create_and_activate_conda_env_w(env_name="Batch_Env", python_version="3.10"):
    """Installs conda, creates a new conda environment with the specified Python version,
       activates it, and changes the working directory to the environment's root."""
    try:
        subprocess.run(["conda", "create", "-n", env_name, f"python={python_version}", "-y"], check=True)
        subprocess.run(["conda", "activate", env_name], check=True, shell=True)
        os.chdir(os.environ["CONDA_PREFIX"])
        print(f"Conda environment '{env_name}' created and activated!")
        print(f"Current working directory: {os.getcwd()}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def download_and_install_cuda_w(url: str, filename: str, download_dir: str) -> None:
    """Downloads CUDA installer from the specified URL to the given directory,
    and then executes a silent installation."""
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    # Download the file
    print("Downloading CUDA installer...")
    response = requests.get(url)
    installer_path = os.path.join(download_dir, filename)
    with open(installer_path, 'wb') as file:
        file.write(response.content)
    print("Download complete.")

    # Execute the installer silently
    print("Installing CUDA...")
    subprocess.Popen([installer_path, '/S', f'/D={download_dir}'], shell=True)
    print("Installation started. Please wait for it to complete.")
    
def get_os_variable():
    system, node, release, version, machine, processor = platform.uname()
    os_name = platform.system()
    
    if os_name == "Windows":
        # Extracting major version number for Windows
        major_version = version.split('.')[2]
        return f'w_{major_version}'
    elif os_name == "Darwin":
        # MacOS version can be found directly in `release`
        return f'm_{release}'
    elif os_name == "Linux":
        # Optionally handle Linux differently; here we use the kernel release
        return f'l_{release}'
    else:
        return f'other_{release}'

if __name__ == "__main__":

    # Example usage
    os_variable = get_os_variable()
    print(os_variable)


    if os_variable == 'w':
        print("\nRunning Blanket Install for Windows 10\n")

        try:
            print("Testing Cuda Availability")
            subprocess.run(['nvidia-smi'])
        except:
            print("Cuda Not Installed")
        
        """Cuda 11.8 Installation"""
        print("\nAttempting to install Cuda 11.8")
        download_dir = os.getcwd()  # Use the current working directory or specify another
        filename = "cuda_11.8.0_522.06_windows.exe"
        url = "https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_522.06_windows.exe"
        download_and_install_cuda_w(url, filename, download_dir)

        try:
            print("Conda Version:\n")
            subprocess.run(["conda", "--version"])
        except:
            print("Conda Not Installed\n Run windows_setup.bat as Admin")
        
        print("Testing for git")
        try:
            subprocess.run(['conda', '--version'])
        except:
            subprocess.run(['conda', 'install', 'git', '-y'])

        print("\nInstalling Whisper from OpenAI\n")
        subprocess.run(['pip', 'install', 'git+https://github.com/openai/whisper.git'])
        subprocess.run(['pip', 'install', '--upgrade', '--no-deps', '--force-reinstall', 'git+https://github.com/openai/whisper.git'])

        print("\nUpgrading PyTorch...")
        subprocess.run(['pip', 'install', 'torch', 'torchvision', 'torchaudio', '--index-url', 'https://download.pytorch.org/whl/cu118'])
        
        print("\nSetup Complete, Creating Directory")
        # Create the directories if they don't exist
        if not os.path.exists('Input-Videos'):
            os.mkdir('Input-Videos')

        print("\nDownload Complete: Follow Instructions with CUDA for your system.")
        print("\nPlease 'Restart' computer for changes to be saved once CUDA has finished installing.")
    
    else:
        print("Mac Selection")