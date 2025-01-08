from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mywaybot_gazebo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'models/dae'), glob('models/dae/*.dae')),
        (os.path.join('share', package_name, 'models/stl'), glob('models/stl/*.stl')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('share', package_name, 'config'), glob('config/*'))



    ],
    extras_require={
        "test": ["pytest", "pytest-cov"],
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='helloworld',
    maintainer_email='kimhyuninnnn@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
