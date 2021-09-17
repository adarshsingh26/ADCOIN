class Printable:
    def __repr__(self):  # Whenever we try to print the block object
        return str(self.__dict__)
