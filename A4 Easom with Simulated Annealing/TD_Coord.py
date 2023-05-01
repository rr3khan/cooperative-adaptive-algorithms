# Class definition for a 2D coordinate


class TD_Coord:
    def __init__(self, x1: int, x2: int):
        self.x1 = x1
        self.x2 = x2

    def get_x1(self) -> int:
        return self.x1

    def get_x2(self) -> int:
        return self.x2

    def set_x1(self, new_x1) -> None:
        self.x1 = new_x1

    def set_x2(self, new_x2) -> None:
        self.x2 = new_x2
