from typing import NamedTuple

class SizeSquare(NamedTuple):
    width: int
    height: int

class SizeCircle(NamedTuple):
    radius: float

class Point(NamedTuple):
    x: int
    y: int