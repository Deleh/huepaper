from setuptools import setup
import os
import shutil

if not os.path.exists("bin"):
    os.makedirs("bin")
shutil.copyfile("huepaper.py", "bin/huepaper")

setup(
    name="huepaper",
    version="0.0.1",
    author="Denis Lehmann",
    author_email="denis@opaque.tech",
    scripts=["bin/huepaper"],
    packages=["huepaper"],
    url="https://git.opaque.tech/denis/huepaper",
    license="LICENSE",
    description="A colorful wallpaper generator",
    long_description=open("README.org").read(),
    install_requires=["colour", "pillow"],
)
