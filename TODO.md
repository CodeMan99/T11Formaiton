TODO
====

There is still a lot to do to make T11Formation.py more useful, especially in the scipt
scope. This is an active project, so feel free to contribute.

 * Add flexibility to the number of rows to eliminate IndexError. This occurs in:
    * `str_rotated_cclockwise`
    * `str_rotated_clockwise`
    * `is_legal` (as an assertion, this may not need to be changed)
 * Add rule "at least four players in the opponents half (ML/MC/MR or AML/AMC/AMR or ST)" to `is_legel`
 * Add `__doc__` strings to all classes, methods, and functions
 * Add GPLv3 statement to T11Formation.py
 * Create coded test cases
 * Create a setup.py script

There is also a need to improve the front end (non-module) part of T11Formation.py. This
can be done in a number of ways, but for now it need more command line arguments to give
users more control.