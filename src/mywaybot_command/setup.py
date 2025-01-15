from setuptools import find_packages, setup

package_name = 'mywaybot_command'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='helloworld',
    maintainer_email='kimhyuninnnn@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'omni_teleop_keyboard = mywaybot_command.omni_teleop_keyboard:main'
        ],
    },
)
