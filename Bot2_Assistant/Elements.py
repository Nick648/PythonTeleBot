# Token's List
el_expression = [  # \b - граница слова(с одной стороны буква, а с другой — нет)
    (r'[ \t]+', None),

    # [commands]
    (r'\bsudo\b', "SUDO"),
    (r'\bls\b', "LS"),
    (r'\bcd\b', "CD"),
    (r'\bhelp\b', "HELP"),
    (r'\bcmd\b', "CMD"),
    (r'\bselect\b', "SELECT"),
    (r'\binfo\b', "INFO"),
    (r'\bsize\b', "SIZE"),
    (r'\btree\b', "TREE"),
    (r'\bwalk\b', "WALK"),
    (r'\bcount\b', "COUNT"),
    (r'\binsert\b', "INSERT"),
    (r'\bsend\b', "SEND"),
    (r'\bfrom\b', "FROM"),
    (r'\binto\b', "INTO"),
    (r'\bphoto\b', "PHOTO"),
    (r'\bvideo\b', "VIDEO"),

    # [path]
    (r'[/|\\]?[A-Za-z0-9_]+\.[A-Za-z0-9]+', "FILE"),  # CHECK WILL COMMENT!!!
    (r'[/|\\]?([A-Za-z0-9_]+[/|\\])+[A-Za-z0-9_]+\.[A-Za-z0-9]+', "PATH_FILE"),  # REPLACE ()+ -> ()* JUST FILE
    (r'[/|\\]?([A-Za-z0-9_]+[/|\\]?)+', "PATH"),

    # (r'/([A-Za-z0-9_]+/)+[A-Za-z0-9_]+\.[A-Za-z0-9]+', "PATH_FILE_1"),
    # (r'([A-Za-z0-9_]+/)+[A-Za-z0-9_]+\.[A-Za-z0-9]+', "PATH_FILE"),
    # (r'/([A-Za-z0-9_]+/)+[A-Za-z0-9_]+', "PATH_1"),
    # (r'/([A-Za-z0-9_]+/)+', "PATH_1"),
    # (r'([A-Za-z0-9_]+/)+[A-Za-z0-9_]+', "PATH"),
    # (r'([A-Za-z0-9_]+/)+', "PATH"),
    #
    # (r'\\([A-Za-z0-9_]+\\)+[A-Za-z0-9_]+\.[A-Za-z0-9]+', "PATH_FILE_1"),
    # (r'([A-Za-z0-9_]+\\)+[A-Za-z0-9_]+\.[A-Za-z0-9]+', "PATH_FILE"),
    # (r'\\([A-Za-z0-9_]+\\)+[A-Za-z0-9_]+', "PATH_1"),
    # (r'\\([A-Za-z0-9_]+\\)+', "PATH_1"),
    # (r'([A-Za-z0-9_]+\\)+[A-Za-z0-9_]+', "PATH"),
    # (r'([A-Za-z0-9_]+\\)+', "PATH"),
    #
    # (r'[A-Za-z0-9_]+\.[A-Za-z0-9]+', "FILE"),
    # (r'/[A-Za-z0-9_]+\.[A-Za-z0-9]+', "FILE_1"),
    # (r'\\[A-Za-z0-9_]+\.[A-Za-z0-9]+', "FILE_1"),
    #
    # (r'/[A-Za-z0-9_]+/', "FOLDER_1"),
    # (r'/[A-Za-z0-9_]+', "FOLDER_1"),
    # (r'[A-Za-z0-9_]+/', "FOLDER"),
    #
    # (r'\\[A-Za-z0-9_]+\\', "FOLDER_1"),
    # (r'\\[A-Za-z0-9_]+', "FOLDER_1"),
    # (r'[A-Za-z0-9_]+\\', "FOLDER"),
    #
    # (r'[A-Za-z0-9_]+', "FOLDER"),

    # [symbols]
    (r'\;', 'SEMICOLON'),
    (r'\:', 'COLON'),
    (r'\..', '2_POINT'),
    (r'\.', 'POINT'),
    (r'\,', 'COMMA'),
    # (r'/', "SLASH"),
    # (r'\\', "BACKSLASH"),
    (r'[/|\\]', "SLASH"),

    # [option]
    (r'\*\.[A-Za-z0-9]+', "ALL_TYPES"),
    (r'[\^]?[A-Za-z0-9_]*\*?[A-Za-z0-9_]*\.\*?[A-Za-z0-9_]*\*?', "RE_OPTION"),
    (r'[\^]?[A-Za-z0-9_]+\*?[A-Za-z0-9_]*', "RE_OPTION"),
    (r'[\^]?[A-Za-z0-9_]*\*?[A-Za-z0-9_]+', "RE_OPTION"),
    (r'\*', "ALL_FILES"),

]


class Element:

    def __init__(self, type_token: str, value: str, position: int):
        if "PATH" in type_token or "FILE" in type_token:
            if value[0] == "/" or value[0] == "\\":
                value = value[1:]
            if value[-1] == "/" or value[-1] == "\\":
                value = value[:-1]
        self.type_token = type_token
        self.value = value
        self.position = position

    def getTypeToken(self) -> str:
        return self.type_token

    def getValue(self) -> str:
        return self.value

    def getPosition(self) -> int:
        return self.position

    def __repr__(self):
        description = f"Element >>> [type: '{self.type_token}'; " \
                      f"value: '{self.value}'; " \
                      f"position: {self.position}]"
        return description

    def toString(self) -> None:  # Output
        text = f"Element >>> [type: '{self.type_token}'; " \
               f"value: '{self.value}'; " \
               f"position: {self.position}]"
        print(text)

# import os
# main_directory = r"N:\NewDir" # Not start with \
#
# while True:
#     s = input(">>> ")
#     if s == "":
#         break
#     new_dir = os.path.join(main_directory, s)
#     print(new_dir, os.path.exists(new_dir))
