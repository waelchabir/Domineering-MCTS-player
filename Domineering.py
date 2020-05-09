from Move import Move
import numpy as np

def main():
    m = Move(1, 2)
    l = [0, 0, 0]
    m.changeX(l)
    print(l)

if __name__ == "__main__":
    main()