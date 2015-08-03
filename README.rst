fuzzyhashlib
============

.. contents:: Table of Contents


Introduction
============

What if fuzzy hashing algorithms were usable through a common API,
the same way that Python's hashlib exposes secure hash and message digest
algorithms? This is the question fuzzyhashlib attempts to answer by providing
a hashlib-like interface to:

- ssdeep (via a Python ctypes wrapper)
- sdbf (via sdhash's Python swig interface)

Currently supported for Python 2.7 on 32- and 64-bit linux (Ubuntu 14.04). 


Usage
=====

Example usage in iPython is provided below.

::

  In [1]: import fuzzyhashlib
  
  In [2]: fuzzyhashlib.ssdeep("a" * 1024).hexdigest()
  Out[2]: '3:tj1:n'
  
  In [3]: fuzzyhashlib.sdhash("a" * 1024).hexdigest()
  Out[3]: 'sdbf:03:0::1024:sha1:256:5:7ff:160:1:0:AAAAAAAAAAAAAAAAAAAAAAAAAAA
  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
  AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
  AAAAAAAAAAAAAAA==\n'


Change Log
==========

Version 0.0.5 - Imporoved packaging:

-  (and the versions in-between) fix packaging so libs install correctly

Version 0.0.2 - 32-bit libraries for linux:

-  libraries installed for x86-32 linux too

Version 0.0.1 - Initial version:

- ssdeep and sdhash wrapped with hashlib-like interfaces
- libraries installed for x86-64 linux only


License and Source Availability
===============================

The fuzzyhashlib library and package is licensed under APLv2.

The information in this section is also provided under fuzzyhashlib's source
tree under 'NOTICES'.


ssdeep
------
ssdeep was written by Jesse Kornblum of the ManTech International
Corporation, with acknowledged contributions by Jason Sherman and
testing by the Computer Science Department at the University of
Iowa. Compiled libraries built from unmodified ssdeep source,
version 2.13, are installed as part of this package. The original
source code for this version of ssdeep available from:
   http://downloads.sourceforge.net/project/ssdeep/ssdeep-2.13/ssdeep-2.13.tar.gz

ssdeep is open source software and is licensed under GPLv2.


sdhash
------
sdhash was written by Vassil Roussev and Candice Quates. Compiled
libraries built from unmodified sdhash source, version 3.4, are
installed are installed as part of this package. The original
source code for this version of sdhash is available from:
   http://github.com/sdhash/sdhash

sdhash is open source software and is licensed under APLv2.


Other Thanks
============
Thanks to Michael Dorman whose excellent 'yara-ctypes' provided logical layout
for a Python ctypes-based project. Several concepts and functions here have
been borrowed accordingly :-)
