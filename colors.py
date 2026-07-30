class Colors:
    dark_gray = (26, 31, 40)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (12, 64, 216)
    white = (255, 255, 255)
    dark_blue = (44, 44, 127)
    light_blue = (59, 85, 162)

    # Ghost Colors
    ghost_dark_grey = (40, 40, 40)
    ghost_green  = (30, 120, 30)
    ghost_red    = (150, 40, 40)
    ghost_orange = (180, 100, 20)
    ghost_yellow = (180, 180, 30)
    ghost_purple = (100, 40, 150)
    ghost_cyan   = (30, 150, 150)
    ghost_blue   = (30, 70, 180)

    @classmethod
    def get_cell_colors(cls):
        return [
            cls.dark_gray, 
            cls.green, 
            cls.red, 
            cls.orange, 
            cls.yellow, 
            cls.purple, 
            cls.cyan, 
            cls.blue
        ]

    @classmethod
    def get_ghost_colors(cls):
        return [
            cls.ghost_dark_grey,
            cls.ghost_green,
            cls.ghost_red,
            cls.ghost_orange,
            cls.ghost_yellow,
            cls.ghost_purple,
            cls.ghost_cyan,
            cls.ghost_blue,
    ]