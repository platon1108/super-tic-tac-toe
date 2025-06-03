from setuptools import setup

setup(
    name='Super Tic-Tac-Toe',
    version='1.0.0',
    description='Супер крестики-нолики',
    packages=['package'],
    package_dir={'': '.'}, 
    install_requires=[
        'pygame>=2.0' # Требуемые зависимости
    ],
    entry_points={
        'console_scripts': [
            'tic-tac-toe=package.game:main' # Точка входа
        ]
    },
    include_package_data=True,
)
