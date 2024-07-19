from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="payarc",
    version="0.0.1",
    description="Payarc Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Payarc/payarc-sdk-python",
    author="Payarc",
    packages=find_packages(where="src"),
)