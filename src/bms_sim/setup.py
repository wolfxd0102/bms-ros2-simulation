from setuptools import find_packages, setup

package_name = 'bms_sim'

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
    maintainer='wolfxd',
    maintainer_email='wolfxd@example.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'battery_sim_node = bms_sim.battery_sim_node:main',
        'bms_controller_node = bms_sim.bms_controller_node:main',
    ],
 },

)
