from setuptools import find_packages, setup

package_name = 'webcam_publish'

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
    maintainer='pradheep',
    maintainer_email='mantissa6789@gmail.com',
    description='ROS 2 package to publish images from a webcam',
    license='Apache License 2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'webcam_publisher = webcam_publish.webcam_publish:main',
        ],
    },
)