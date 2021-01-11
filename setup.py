from setuptools import setup, Extension
import pybind11
from distutils.core import setup

ext_modules = [
       Extension(
       'pyds_tracker_meta',
       sources = ['pyds_tracker_meta.cpp'],
       include_dirs=[pybind11.get_include(), '/opt/nvidia/deepstream/deepstream-5.0/sources/includes/', '/usr/include/gstreamer-1.0', '/usr/include/orc-0.4', '/usr/include/gstreamer-1.0', '/usr/include/glib-2.0', '/usr/lib/aarch64-linux-gnu/glib-2.0/include'],
       language='c++'
       ),
       Extension(
       'pyds_bbox_meta',
       sources = ['pyds_bbox_meta.cpp'],
       include_dirs=[pybind11.get_include(), '/opt/nvidia/deepstream/deepstream-5.0/sources/includes/', '/usr/include/gstreamer-1.0', '/usr/include/orc-0.4', '/usr/include/gstreamer-1.0', '/usr/include/glib-2.0', '/usr/lib/aarch64-linux-gnu/glib-2.0/include'],
       language='c++'
       ),
]

setup(
       name = 'pyds_metadata_patch',
       version = '1.0',
       description = """Install precompiled DeepStream Python bindings for tracker metadata extension""",
       packages=[''],
       package_data={'': ['pyds_tracker_meta.so', 'pyds_bbox_meta.so']},
       ext_modules=ext_modules
       )