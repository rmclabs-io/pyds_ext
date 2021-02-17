#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup
from setuptools import Extension as BaseExtension
import shlex
import shutil
import subprocess as sp
import sys
import warnings


# ALERT: Do not modify VERSION below by hand! commitizen does this
VERSION = "1.2.1"

try:
    # Available at setup time due to pyproject.toml (PEP 517, 518)
    from pybind11.setup_helpers import Pybind11Extension
    from pybind11.setup_helpers import build_ext
except ImportError as exc:
    warnings.warn(repr(exc))
    warnings.warn(f"Maybe you forgot to upgrade pip?")
    sys.exit(42)


INCLUDE_DIRS = [
    f"/opt/nvidia/deepstream/deepstream/sources/includes/",
    *[
        inc.lstrip("-I")
        for inc in shlex.split(
            sp.check_output(
                shlex.split("pkg-config --cflags gstreamer-1.0 gstreamer-video-1.0")
            ).decode("utf8")
        )
        if inc.startswith("-I")
    ],
]


class CustomExtBuilder(build_ext):
    def build_extension(self, ext):
        if isinstance(ext, Precompiled):
            return ext.copy_precompiled(self)
        return super().build_extension(ext)


class Precompiled(BaseExtension):
    def __init__(self, name, precompiled, *args, **kwargs):
        super().__init__(name, [], *args, **kwargs)
        self.precompiled = Path(precompiled)

    def copy_precompiled(self, builder):
        if self.precompiled.exists():
            path = Path(builder.get_ext_fullpath(self.name))
            path.parent.mkdir(parents=True)
            shutil.copyfile(str(self.precompiled), builder.get_ext_fullpath(self.name))
        else:
            print(
                f"Error: specified file {self.precompiled} not found!", file=sys.stderr
            )


EXT_MODULES = [
    Precompiled("pyds", precompiled="/opt/nvidia/deepstream/deepstream/lib/pyds.so"),
    *[
        Pybind11Extension(
            module.stem,
            sources=[str(module)],
            include_pybind11=True,
            include_dirs=INCLUDE_DIRS,
        )
        for module in Path("src").glob("*.cpp")
    ],
]


def main():

    setup(
        name="pyds_ext",
        version=VERSION,
        description="DeepStream bindings and extra metadata for tracker and bbox",
        ext_modules=EXT_MODULES,
        cmdclass={"build_ext": CustomExtBuilder},
    )


if __name__ == "__main__":
    main()
