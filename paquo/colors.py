from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Union

from paquo.java import ColorTools, Integer

ColorTypeRGB = Tuple[int, int, int]
ColorTypeRGBA = Tuple[int, int, int, int]
ColorType = Union[ColorTypeRGB, ColorTypeRGBA, 'QuPathColor']


@dataclass
class QuPathColor:
    """color representation in paquo

    >>> c = QuPathColor(128, 128, 160, alpha=240)
    """
    red: int
    green: int
    blue: int
    alpha: int = 255

    def is_valid(self) -> bool:
        """tests if a QuPathColor is valid

        (there are currently no validation checks performed on __init__)
        """
        for value in self.to_rgba():
            if not (0 <= value <= 255):
                # raise ValueError("val not an integer 0 <= val <= 255")
                return False
        return True

    def to_rgb(self) -> ColorTypeRGB:
        """convert to 3 * uint8 rgb tuple"""
        return self.red, self.green, self.blue

    def to_rgba(self) -> ColorTypeRGBA:
        """convert to 4 * uint8 rgba tuple"""
        return self.red, self.green, self.blue, self.alpha

    def to_mpl_rgba(self) -> Tuple[float, float, float, float]:
        """convert to 4 * float rgba tuple (mpl compatible)"""
        r, g, b, a = self.to_rgba()
        return r / 255.0, g / 255.0, b / 255.0, a / 255.0

    def to_java_rgb(self) -> Integer:
        """"convert to the java rgb integer representation used by qupath"""
        return ColorTools.makeRGB(*self.to_rgb())

    @classmethod
    def from_java_rgb(cls, java_rgb: int) -> QuPathColor:
        """convert from java but ignore the alpha value in java_rgb"""
        r = int(ColorTools.red(java_rgb))
        g = int(ColorTools.green(java_rgb))
        b = int(ColorTools.blue(java_rgb))
        return cls(r, g, b)

    def to_java_rgba(self) -> Integer:
        """"convert to the java argb integer representation used by qupath"""
        return ColorTools.makeRGBA(*self.to_rgba())

    @classmethod
    def from_java_rgba(cls, java_rgba: int) -> QuPathColor:
        """converts a java integer color into a QuPathColor instance"""
        r = int(ColorTools.red(java_rgba))
        g = int(ColorTools.green(java_rgba))
        b = int(ColorTools.blue(java_rgba))
        a = int(ColorTools.alpha(java_rgba))
        return cls(r, g, b, a)

    def __repr__(self) -> str:
        if self.alpha != 255:
            return f"<Color rgba{self.to_rgba()}>"
        return f"<Color rgb{self.to_rgb()}>"

    @classmethod
    def from_any(cls, value: ColorType) -> QuPathColor:
        """try creating a QuPathColor from all supported types"""
        if isinstance(value, (tuple, list)):
            return cls(*value)
        elif isinstance(value, QuPathColor):
            return cls(*value.to_rgba())
        else:
            raise TypeError("can't convert to QuPathColor")