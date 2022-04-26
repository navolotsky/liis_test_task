# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name="liis_test_task",
    version="0.0.0",
    author="Oleg Navolotsky",
    author_email="oleg.navolotsky@gmail.com",
    packages=find_packages(),
    namespace_packages=["liis_test_task"],
    install_requires=[
        "Django~=4.0.4",
        "djangorestframework~=3.13.1",
        "psycopg2~=2.9.3",
        "pyxdg~=0.27"
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": ["liistt-admin=liis_test_task.core.manage:main"],
    },
)
