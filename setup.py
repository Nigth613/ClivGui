from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cliv-gui",
    version="1.0.1",
    author="Night613",
    author_email="clivguicontact@gmail.com",
    description="Cliv is a GUI library inspired by ImGui, featuring various classes and released under the MIT license. It’s a great choice for people who want a useful and easy-to-use library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nigth613/ClivGui",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
        "pygame>=2.0.0",
        "keyboard>=0.13.5",
        "pywin32>=304",
        "psutil>=5.9.0",
        "pystray>=0.19.4",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cliv-demo=cliv_extreme:main",
        ],
    },
    keywords=[
        "gui",
        "menu",
        "overlay",
        "tkinter",
        "gaming",
        "esp",
        "notifications",
        "modern-ui",
        "windows",
        "process-overlay",
    ],
    project_urls={
        "Bug Reports": "https://github.com/Nigth613/ClivGui/issues",
        "Source": "https://github.com/Nigth613/ClivGui",
        "Documentation": "https://github.com/Nigth613/ClivGui/wiki",
    },
    include_package_data=True,
    zip_safe=False,
)
