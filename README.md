# Python Cinema 4D SDK

This repository is the new community powered Plugin SDK for the Cinema
4D Python API and replaces the old one delivered with the Python API
documentation. Download and try the plugins in this repository and
browse their well document source code. \*

_\* that is our goal, we are just starting out with this project._

The structure of Python plugins is slightly different than the
structure of C++ plugins. While C++ source files will be compiled into
one plugin file that resides in the root folder of the plugin where
the `res/` (plugin resource folder) can be found by Cinema 4D, this
is not so easy in Python. That is why each plugin in this SDK is able
to *stand completely on its own*.

__Minimum Requirements__

The plugins in the repository will always run with the newest version
of Cinema 4D if it is not otherwise noted. Older versions are supported
as far as the required components of the Python API are available.

__License__

The source code in this repository, if not otherwise noted, is licensed
under the MIT License.

## New to the Cinema 4D plugin development?

Take a look at the [`starters/`][starters/] folder, it contains plugin examples
that are suited for very beginners. Knowing the Python language however
is of advantage.

