
import os
from pathlib import Path
from setuptools import setup
import shlex
import subprocess as sp
import sys
import warnings

try:
    # Available at setup time due to pyproject.toml
    from pybind11.setup_helpers import Pybind11Extension
    from pybind11.setup_helpers import build_ext
    from pybind11 import get_cmake_dir
except ImportError as exc:
    warnings.warn(repr(exc))
    warnings.warn(f"Maybe you forgot to upgrade pip?")
    sys.exit(42)


INCLUDE_DIRS = [
    f"{os.environ['DS']}/sources/includes/",
    *[
        inc.lstrip('-I')
        for inc in shlex.split(
            sp.check_output(
                shlex.split(
                    "pkg-config --cflags gstreamer-1.0 gstreamer-video-1.0"
                )
            ).decode("utf8")
        )
        if inc.startswith("-I")
    ]
]

EXT_MODULES = [
    Pybind11Extension(
       module.stem,
       sources = [str(module)],
       include_pybind11=True,
       include_dirs=INCLUDE_DIRS,
    ) for module in Path("src").glob("*.cpp")
]

def main():
    install_requires = []
    dep_name = 'pyds'
    setup_py = pathlib.Path("/opt/nvidia/deepstream/deepstream/lib/setup.py")
    parent = setup_py.parent
    if parent.is_dir():
        install_requires.append(f'{dep_name} @ {parent}')

    setup(
        name = 'pyds_metadata_patch',
        version = '1.1.1',
        description = """DeepStream bindings for tracker and bbox metadata""",
        install_requires=install_requires,
        ext_modules=EXT_MODULES,
        # Currently, build_ext only provides an optional "highest supported C++
        # level" feature, but in the future it may provide more features.
        cmdclass={"build_ext": build_ext},
    )

if __name__ == '__main__':
    main()
