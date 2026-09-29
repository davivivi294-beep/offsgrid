from setuptools import setup, find_packages

setup(
    name="offsgrid",
    version="1.0.0",
    author="offsgrid",
    description="Painel educacional de cyber security",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "qrcode[pil]>=7.4.2",
    ],
    entry_points={
        "console_scripts": [
            "offsgrid=offsgrid.painel:main",
        ],
    },
)
