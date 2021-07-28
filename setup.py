from setuptools import setup

package_name = 'barcode_scanner_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alphonsustay',
    maintainer_email='alphonsus_tay@cgh.com.sg',
    description='ROS2 Adapter for driverless USB Barcode Scanner',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'barcode_scanner_script = barcode_scanner_ros2.barcode_scanner_script:main'
        ],
    },
)
