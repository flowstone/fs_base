from setuptools import setup, find_packages

setup(
    name="fs_base",
    version="0.1",
    packages=find_packages(include=["fs_base", "fs_base.*"]),  # 包含子包
    install_requires=[
        "PySide6",  # Qt bindings
        "loguru",  # 添加依赖
    ],
    package_data={
        "fs_base": ["resources/*.qss", "fonts/*.ttf"]
    },
    description="A shared utility library for PySide6 projects", # 项目简短描述
    author="Your Name",
    author_email="your.email@example.com",
    url="https://example.com/shared_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
