import sys
import math

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from datetime import datetime
import argparse

ignore_value = 99999

# Format is as following for 1 reference point
# ;
# ;
# ;
# ;
# ;
# 01.01.1985
# 0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
# 0,0
# 239,363
# 256,359
# 0
# 0,0
# 3
# 8,-257,-58,1,U2
# 1,0,10,0,U7777
# 2,0,0,2,TEST

class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class kicad_part:
    def __init__(self, ref, value, package, pos, rot, side):
        self.ref = ref
        self.value = value
        self.package = package
        self.pos = pos
        self.rot = rot
        self.side = side


def to_rotation(value):
    if value != 0 and value != 90 and value != 180 and value != 270:
        return 0
    
    if value == 0:
        return 2
    if value == 90:
        return 3
    if value == 180:
        return 4

    return 1


def position_to_board(position, reference, rotate):
    # translate the position to the reference
    pos = coordinate((position.x - reference.x) * 10, (position.y - reference.y) * 10)

    # rotate the position if needed
    if rotate > 0:
        angle = math.radians(rotate)

        temp = pos.x * math.cos(angle) - pos.y * math.sin(angle)
        pos.y = pos.x * math.sin(angle) + pos.y * math.cos(angle)
        pos.x = temp

    # round the position to the nearest integer
    x = str(int(round(pos.x)))
    y = str(int(round(pos.y)))

    return (x, y)

def generate(reference_points, input_file, output_file, rotate):
    print("Using reference")
    print("\tX: " + str(reference_points[0].x) + ", Y: " + str(reference_points[0].y))

    file = open(input_file, 'r')
    data = file.readlines()

    # get the current date
    date = datetime.now().strftime("%d.%m.%Y")

    out = open(output_file, 'w')
    out.write(";\n")
    out.write(";\n")
    out.write(";\n")
    out.write(";\n")
    out.write(";\n")
    out.write(f"{date}\n")
    out.write(f"0,0,{len(reference_points)},0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")
    out.write("0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0\n")

    # first reference point is always 0,0 (always relative to itself)
    out.write("0,0\n")

    if len(reference_points) == 3:
        # calculate the distance from the first reference point
        for i in range(1, len(reference_points)):
            # convert the reference point to a relative point of the first reference
            x, y = position_to_board(reference_points[i], reference_points[0], rotate)
            out.write(f"{x},{y}\n")
    else:
        # write two empty reference points
        out.write("0,0\n")
        out.write("0,0\n")
    out.write("0\n")
    out.write("0,0\n")

    pair_data = dict()
    parts = list()

    found = False
    part_count = 0

    for line in data:
        if not found:
            # search for the "# Ref"
            if line.startswith("# Ref"):
                found = True

            continue

        # check if we are at the end of the file
        if line.startswith("## End"):
            break

        split_line = line.split()

        # skip the line if it has not enough data
        if (len(split_line) < 7):
            continue

        # convert the split part to a kicad_part
        part = kicad_part(split_line[0], split_line[1], split_line[2], coordinate(float(split_line[3]), float(split_line[4])), float(split_line[5]), split_line[6])

        # check if we already have the feeder info
        if (part.package, part.value) in pair_data:
            feeder = pair_data[(part.package, part.value)]

            print(f"{Fore.GREEN}<{Style.RESET_ALL} Using feeder id {feeder} for: {part.ref} - {part.value}")
        else:
            # get the user input for the feeder
            user_data = input(f"{Fore.RED}>{Style.RESET_ALL} Enter feeder id for {part.ref} - {part.value}: ")
            feeder = None

            # check if we have a number
            if user_data.isdigit():
                feeder = int(user_data)
            else:
                # we have no number, check if we should skip the part 
                # or ignore all the parts of this type
                if user_data == "skip" or user_data == "ignore" or user_data == "s" or user_data == "i":
                    feeder = ignore_value
                else:
                    print(f"{Fore.RED}Invalid input{Style.RESET_ALL}")
                    sys.exit(1)

            # store the feeder info
            pair_data[(part.package, part.value)] = feeder

        x, y = position_to_board(part.pos, reference_points[0], rotate)
        r = str(to_rotation(round(part.rot, 0)))

        # skip the part if needed
        if feeder == ignore_value:
            print(f"{Fore.CYAN}\tSkipping part {part.ref}, {x}, {y}, {r}, {Style.RESET_ALL}")
            continue

        # add to the list
        res = (feeder, x, y, r, part.ref)
        parts.append(res)

        # print the data
        print(f"{Fore.YELLOW}\t{feeder}, {x}, {y}, {r}, {part.ref}{Style.RESET_ALL}")
        part_count += 1

    # set the amount of parts
    out.write(str(part_count) + "\n")

    # sort based on the feeder. This groups all the parts together
    parts.sort(key=lambda p : p[0])

    # write the parts
    for p in parts:
        for i in range(len(p)):
            out.write(str(p[i]))

            if (i + 1) < len(p):
                out.write(",")

        out.write("\n")

    out.close()
    file.close()

    print(f"{Fore.GREEN}File written to disk{Style.RESET_ALL}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert KiCad POS file to Frittish SMD format.")
    parser.add_argument("-ref", type=str, help="Reference 0 \"X,Y\" coordinate", required=True)
    parser.add_argument("-i", "--input_file", type=str, help="Input .pos file", required=True)
    parser.add_argument("-o", "--output_file", type=str, help="Output .smd file", required=True)
    parser.add_argument("-r", "--rotate", help="Rotate the part by 90 degrees", type=int, required=False)
    parser.add_argument("-ref1", type=str, help="Reference 1 \"X,Y\" coordinate", required=False)
    parser.add_argument("-ref2", type=str, help="Reference 2 \"X,Y\" coordinate", required=False)

    # parse the arguments
    args = parser.parse_args()

    # split the reference into x and y
    ref = args.ref.split(",")
    
    error = False

    references = [args.ref, args.ref1, args.ref2]
    reference_points = []

    # add all the reference points from the arguments
    for ref in references:
        if ref is None:
            break

        # split the reference into x and y
        ref_split = ref.split(",")
        if len(ref_split) != 2:
            print(f"{Fore.RED}Invalid reference point. Use \"X,Y\" for the reference{Style.RESET_ALL}")
            error = True
            break

        # try to convert the reference to a float
        try:
            reference_points.append(coordinate(float(ref_split[0]), -1 * float(ref_split[1])))
        except ValueError:
            print(f"{Fore.RED}Invalid reference point. Use \"X,Y\" for the reference{Style.RESET_ALL}")
            error = True
            break

    # check if we have at least one reference point
    if len(reference_points) == 0:
        print(f"{Fore.RED}No reference points found. Use \"X,Y\" for the reference{Style.RESET_ALL}")
    elif error:
        print(f"{Fore.RED}Exiting due to errors{Style.RESET_ALL}")
    else:
        generate(reference_points, args.input_file, args.output_file, args.rotate if args.rotate else 0)


