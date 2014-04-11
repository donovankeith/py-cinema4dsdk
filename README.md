# Python Cinema 4D SDK

This repository is the new community powered Plugin SDK for the Cinema
4D Python API and replaces the old one delivered with the Python API
documentation. Download and try the plugins in this repository and
browse their well document source code. \*

_\* that is our goal, we are just starting out with this project._

__Minimum Requirements__

The plugins in the repository will always run with the newest version
of Cinema 4D if it is not otherwise noted. Older versions are supported
as far as the required components of the Python API are available.

__License__

The source code in this repository, if not otherwise noted, is licensed
under the MIT License.

## Recommended development tools

For string and description resource identifiers (in `c4d_symbols.h` and
description resource headerss), we use the [`c4ddev`][c4ddev] toolbelt
to extract the symbols and load via JSON in the Python plugin.

  [c4ddev]: https://github.com/nr-tools/c4ddev

## New to the Cinema 4D plugin development?

Take a look at the [`starters/`](starters/) folder, it contains plugin
examples that are suited for very beginners. Knowing the Python language
however is of advantage.

## Structure

The structure of Python plugins is slightly different than the
structure of C++ plugins. While C++ source files will be compiled into
one plugin file that resides in the root folder of the plugin where
the `res/` (plugin resource folder) can be found by Cinema 4D, this
is not so easy in Python. That is why each plugin in this SDK is able
to *stand completely on its own*.

You may also want to look at the readme file that is available for many
source files. These have the same name but the Markdown suffix (*.md) and
provide additional information to the example.

## File Headers

Besides the license text, the documentation headers of source files
contain useful information such as a short description, the experience
level required to understand the example, tags and names of files that
should be read and understand before reading that example file.

Take the `src/starters/commands/group-objects.cpp` file for an instance:

```cpp
/**
 * Copyright (c) 2013-2014  Niklas Rosenstein
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * [...]
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * file: src/starters/commands/group-objects.cpp
 * description:
 *    This plugin command groups all selected objects under a
 *    single Null object.
 * tags: command simple muchdoc group object-creation hierarchy-modifications
 * level: beginner
 * read-before: create-cube.cpp
 */
```

__file__: The full path of the file in the Cinema4D SDK project relative
to the projects main directory.

__description__: A short description of the plugin. Some files might have
an `*.md` file in the same directory with the same name which contains a
more detailed description of the example.

__tags__: A list of the tags that match with the example.

__level__: The level someone requires to understand the example.

__read-before__: The name of one or more files that should be read and
understood before reading the current file.

## Contributions are Welcome!

Don't hesitate to fork this repository and add new stuff to it. GitHub allows
you to make a request that we will merge your changes into the main repository,
and so we will do! It would be nice if you'd stick to the File Headers information
for each file as we plan to do something with this information.

We prefer the MIT license, but if, for any special reasons, you want to put your
contributed sources under a different license, we are fine with that as long as
it does not contradict with other contents of the repository! The *copyright* is
granted to the original author of the source file, so don't forget to add it to
the file(s).

