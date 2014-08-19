T11Formaiton
============

A python tool to help be social about your [Top Eleven] Formation.

Installing
----------

 1. Install [python] 3.x on your machine.
 2. Download the T11Formation.py script from this directory.

Usage
-----

You may run `python T11Formation.py [FORMATION]` to get a basic string
representation of your formation. Here's an example:

    $ python T11Formation.py 4-1-2-2w-1
    DL--------AML---
    DC-----MC-------
    ---DMC--------ST
    DC-----MC-------
    DR--------AMR---

You may do more complex things by using the script as a module. This
currently includes:

 * Get a string (like above) rotated counter-clockwise from top-to-bottom view
 * Get a string rotated clockwise from top-to-bottem view
 * Get a html table
 * Get a bb code table
 * Determine if the formation is balance (left-right)
 * Determine if the formation is legal according to Top Eleven [rules]
 * Modify the formation
     * Set or unset a role
     * Flip a row from wide to narrow (or vise-versa)

License
-------

Released under the GNU General Public License version 3.


[Top Eleven]: http://www.topeleven.com "Top Eleven Website"
[python]: https://www.python.org/downloads "Python Downloads"
[rules]: http://wiki.topeleven.com/Squad#Formations
