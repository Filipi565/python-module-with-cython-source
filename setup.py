from setuptools import setup
from setuptools import find_packages
from setuptools import Extension

import os

from Cython.Build import cythonize

package_separator = "." 
# if you use find_packages functions, set as "."
# but if you set it manually, ex:
# packages = [
# "module/example"
# ] in this case the package_separator will be "/"

#region Functions

ListOfExtesions = list

def get_c_files(packages):
    values = ListOfExtesions()

    for package in packages:
        path = package.replace(package_separator, os.sep)
        package = package.replace("/", os.extsep).replace("\\", os.extsep)
        with os.scandir(path) as scandir:
            for item in scandir:
                if item.is_dir():
                    continue

                if item.name.endswith(".c"):
                    name = package + os.extsep + item.name[0:-2]
                    values.append(Extension(name, [item.path]))
    
    return values

def get_pyx_files(packages):
    values = ListOfExtesions()

    for package in packages:
        path = package.replace(package_separator, os.sep)
        package = package.replace("/", os.extsep).replace("\\", os.extsep)
        with os.scandir(path) as scandir:
            for item in scandir:
                if item.is_dir():
                    continue

                if item.name.endswith(".pyx"):
                    name = package + os.extsep + item.name[0:-4]
                    values.append(Extension(name, [item.path]))
    
    return values

def package_data_generator(packages, *types):
    values = {}

    for package in packages:
        package = package.replace("/", os.extsep).replace("\\", os.extsep)
        values[package] = []
        for type in types:
            values[package].append(f"*.{type}")
    
    return values
#endregion

packages = find_packages()
ext_modules = get_c_files(packages)
cython_modules = get_pyx_files(packages)
package_data = package_data_generator(packages, "py", "pyi")

setup(
    ext_modules=[*ext_modules, *cythonize(cython_modules)],
    packages=packages,
    package_data=package_data,
)
