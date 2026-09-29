from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setup(
    name="offsgrid",
    version="1.1.0",
    author="offsgrid",
    description="Painel educacional de cyber security com ferramentas reais e simulações visuais",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # ferramentas base
        "requests>=2.31.0",
        "psutil>=5.9.0",
        "qrcode[pil]>=7.4.2",
        # face scan
        "opencv-python>=4.8.0",
        "opencv-contrib-python>=4.8.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "offsgrid=offsgrid.painel:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Security",
        "Intended Audience :: Education",
    ],
    keywords="cyber security education offsgrid face-scan opencv",
)
