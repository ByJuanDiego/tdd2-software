from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "example",
        sorted(glob("sensor.cpp")),  # Sort source files for reproducibility
    ),
]

setup(
    name="example",
    version="1.0",
    author="Juan Diego",
    description="Si",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext}
)
