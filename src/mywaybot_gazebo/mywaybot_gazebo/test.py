from ament_index_python.packages import get_package_share_directory
import os

try:
    package_path = get_package_share_directory('mywaybot_gazebo')
    dae_path = os.path.join(package_path, 'models/dae/base_link.dae')
    print(f"Resolved path: {dae_path}")
    if os.path.exists(dae_path):
        print("File exists and is accessible!")
    else:
        print("File not found at resolved path.")
except Exception as e:
    print(f"Error: {e}")
