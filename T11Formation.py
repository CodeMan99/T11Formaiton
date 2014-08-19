#!/usr/bin/env python3

__all__ = ["Formation", "InvalidContextError"]
__author__ = "Cody A. Taylor"
__version__ = "0.2a"

class Formation:
    @classmethod
    def parse(cls, title):
        return cls(*(cls.Row(int(r[0]), r[1:], n) for r, n in zip(title.split("-"), ("D", "DM", "M", "AM", "S"))))

    def __init__(self, *rows):
        self._rows = list(rows) # want a list so we can use the __setitem__ for rows

    def __getitem__(self, lookup):
        if isinstance(lookup, int):
            return self._rows[lookup]
        elif isinstance(lookup, slice):
            return Formation(*self._rows[lookup])
        elif isinstance(lookup, tuple) and len(lookup) == 2:
            row, column = lookup
            return self._rows[row][column]
        else:
            raise TypeError("'{}' is not a valid Type for __getitem__".format(type(lookup)))

    def __setitem__(self, lookup, value):
        if isinstance(lookup, int):
            self._rows[lookup] = value
        elif isinstance(lookup, slice):
            self._rows[lookup] = value._rows
        elif isinstance(lookup, tuple) and len(lookup) == 2:
            row, column = lookup
            self._rows[row][column] = value
        else:
            raise TypeError("'{}' is not a valid Type for __setitem__".format(type(lookup)))

    def __iter__(self):
        return iter(self._rows)

    def __len__(self):
        return len(self._rows)

    def __repr__(self):
        return "Formation(\n\t{}\n)".format(",\n\t".join(repr(r) for r in self))

    def __str__(self):
        return "\n".join(str(r) for r in self)

    def str_rotated_cclockwise(self):
        rotated = zip(*(reversed(row) for row in self))
        return "\n".join(
            "{:-<2}-{:-<3}-{:-<2}-{:-<3}-{:->2}".format(*column) for column in rotated
        )

    def str_rotated_clockwise(self):
        rotated = zip(*reversed(self))
        return "\n".join(
            "{:-<2}-{:-<3}-{:-<2}-{:-<3}-{:->2}".format(*column) for column in rotated
        )

    def get_html(self):
        lines = ["<table>"]
        for r in self:
            if r._player_count == 0:
                continue

            lines.append("  <tr>")
            for c in r:
                lines.append("    <td>{}</td>".format(c))
            lines.append("  </tr>")
        lines.append("</table>")

        return "\n".join(lines)

    def get_bb(self):
        lines = ["[table]"]
        for r in self:
            if r._player_count == 0:
                continue

            lines.append("  [tr]")
            for c in r:
                lines.append("    [td]{}[/td]".format(c))
            lines.append("  [/tr]")
        lines.append("[/table]")

        return "\n".join(lines)

    def get_title(self):
        return "-".join(r.get_title() for r in self)

    def is_balanced(self):
        return all(r.is_balanced() for r in self)

    def is_legal(self):
        assert len(self) == 5, "Formation.is_legal(self) assumes 5 rows"
        rule_count = 0
        rules_passed = 0
        
        rule_count += 1
        rules_passed += self[0]._player_count >= 3 #defense count
        
        rule_count += 1
        rules_passed += self[4]._player_count >= 1 #striker count
        
        rule_count += 1
        rules_passed += self[1].columns & 0b01110 > 0 or self[2].columns & 0b01110 > 0 #at least one DMC or MC
        
        rule_count += 1
        rules_passed += sum(r._player_count for r in self[1:4]) >= 3 #midfield count
        
        rule_count += 1
        rules_passed += 0 < sum(1 for r in self if r[0]) < 3 #one or two right side players
        
        rule_count += 1
        rules_passed += 0 < sum(1 for r in self if r[4]) < 3 #one or two left side players
        
        rule_count += 1
        rules_passed += sum(r._player_count for r in self[2:]) >= 4 #at least 4 players in opponents half
        
        return rule_count == rules_passed

    class Row:
        def __init__(self, p, w=False, name=""):
            if not 0 <= p <= 5:
                raise ValueError("A row can only contain [0,5] players, {} given".format(p))
            self._player_count = p
            self._wide_specifier = w in ('w', 'W', True)
            self.name = name
            self.columns = 0b00000
            if p == 5:
                self.columns = 0b11111
            elif p == 4:
                self.columns = 0b11011
            elif p == 3:
                self.columns = 0b10101 if self._wide_specifier else 0b01110
            elif p == 2:
                self.columns = 0b10001 if self._wide_specifier else 0b01010
            elif p == 1:
                self.columns = 0b00100

        def __getitem__(self, index):
            if not isinstance(index, int):
                raise TypeError("Argument 'index' may only be of type integer")
            if index < 0:
                index += len(self) #Allow negative -1 and 4 to reference the same column
            if not 0 <= index < len(self):
                raise IndexError("Argument 'index' is out of range, {} given".format(index))
            bit_column = len(self) - index - 1
            column_name = ("RCCCL" if self.name != 'S' else "RTTTL")[index]
            return self.name + column_name if bool(self.columns & (1 << bit_column)) else ''

        def __setitem__(self, index, value):
            if not isinstance(index, int):
                raise TypeError("Argument 'index' may only be of type integer")
            if index < 0:
                index += len(self) #Allow negative -1 and 4 to reference the same column
            if not 0 <= index < len(self):
                raise IndexError("Argument 'index' is out of range, {} given".format(index))
            bit_column = len(self) - index - 1
            changed(self.columns, "columns")
            if bool(value): #Allow for non-bool types like str
                self.columns |= (1 << bit_column)
                if changed(self.columns, "columns"):
                    self._player_count += 1
            else:
                self.columns &= (0b11111 ^ (1 << bit_column)) # could use NOT (~) instead of XOR (^)
                if changed(self.columns, "columns"):
                    self._player_count -= 1
            self._wide_specifier = self.columns & 0b10001 == 0b10001 and 2 <= self._player_count <= 3

        def __iter__(self):
            for i in range(len(self)):
                yield self[i]

        def __len__(self):
            return 5 # Game constant

        def __repr__(self):
            return "Row(p={!r}, w={!r}, name={!r})".format(self._player_count, self._wide_specifier, self.name)

        def __str__(self):
            return "{:-<3}-{:-<3}-{:-<3}-{:-<3}-{:->3}".format(*iter(self))

        def get_title(self):
            return "{}{}".format(self._player_count, 'W' if self._wide_specifier else '')

        def is_balanced(self):
            w = self.columns & 0b10001
            n = self.columns & 0b01010
            return (w == 0b10001 or w == 0b00000) and (n == 0b01010 or n == 0b00000)

        def flip_wide(self):
            if not 2 <= self._player_count <= 3:
                raise InvalidContextError("Wide/Narrow specification is not valid for {} players".format(self._player_count))
            self.columns ^= 0b11011
            self._wide_specifier = not self._wide_specifier

def changed(value, name="store"):
    """Return True if the value has changed since the previous call
    
    This function will only store the value, not copy
    @see setattr

    >>> changed(0)
    True
    >>> changed(0)
    False
    >>> changed(1)
    True
    """
    r = True if not hasattr(changed, name) else getattr(changed, name) != value
    if r:
        setattr(changed, name, value)
    return r
    #if not hasattr(changed, name) or getattr(changed, name) != value:
    #    setattr(changed, name, value)
    #    return True
    #return False

class InvalidContextError(RuntimeError): pass

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        title = sys.argv[1] if len(sys.argv) == 2 else "-".join(sys.argv[1:])
        f = Formation.parse(title)
        try:
            print(f.str_rotated_cclockwise())
        except:
            print(f)
        # is_balanced will always be True currently
        #print("This formation is {}balanced".format("" if f.is_balanced() else "not "))
    else:
        print("Usage: {} [FORMATION TITLE]".format(sys.argv[0]))

    sys.exit(0)