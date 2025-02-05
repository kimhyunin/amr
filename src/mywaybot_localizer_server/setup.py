from setuptools import find_packages, setup

package_name = 'mywaybot_localizer_server'

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
            'initial_pose = mywaybot_localizer_server.initial_pose:main',
            'global_localization = mywaybot_localizer_server.global_localization:main',
        ],
    },
)
