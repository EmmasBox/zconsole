import os
import sys

from setuptools import Extension, setup
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

# This script needs    export _C89_CCMODE=1
# Otherwise you get FSUM3008  messages
os.environ['_C89_CCMODE'] = '1'

class bdist_wheel(_bdist_wheel): # noqa: N801
    def finalize_options(self):
        super().finalize_options()

        self.root_is_pure = True
        self.python_tag = f"py{sys.version_info.major}{sys.version_info.minor}"

def main():
    """Python extension build entrypoint."""
    if "_C89_CCMODE=1" not in os.environ:
        msg = "_C89_CCMODE=1 not set"
        raise RuntimeError(msg)

    setup_args = {
        "ext_modules": [
            Extension('console.zconsole',['src/zconsole/console.c'],
            include_dirs=[
                "/src/zconsole",
                ],
            extra_compile_args=[
                "-Wc,ASM,SHOWINC,ASMLIB(//'SYS1.MACLIB'),LIST(c.lst),SOURCE,WARN64,XREF",
                "-Wa,LIST,RENT",
                ],
            extra_link_args=[
                "-Wl,LIST,MAP,DLL","/u/tmp/console/cpwto.o","/u/tmp/console/qedit.o",
                "/u/tmp/console/qeditw.o",
                ],
        )],
        "cmdclass": {
            "bdist_wheel": bdist_wheel,
        },
    }
    setup(**setup_args)

if __name__ == "__main__":
    main()