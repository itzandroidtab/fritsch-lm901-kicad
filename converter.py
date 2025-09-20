import sys

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
    x = str(int(round((position.x * 10) - (reference.x * 10), 0)))
    y = str(int(round((position.y * 10) + (reference.y * 10), 0)))

    if rotate:
        return (y, x)

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

    # first reference point is always 0,0
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

        part = line.split()

        if (len(part) < 7):
            continue

        # check if we already have the feeder info
        if (part[2], part[1]) in pair_data:
            feeder = pair_data[(part[2], part[1])]

            print(f"{Fore.GREEN}<{Style.RESET_ALL} Using feeder id {feeder} for: {part[0]} - {part[1]}")
        else:
            # get the user input for the feeder
            user_data = input(f"{Fore.RED}>{Style.RESET_ALL} Enter feeder id for {part[0]} - {part[1]}: ")
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
            pair_data[(part[2], part[1])] = feeder

        pos = coordinate(float(part[3]), float(part[4]))
        x, y = position_to_board(pos, reference_points[0], rotate)
        r = str(to_rotation(round(float(part[5]), 0)))

        # add to the list
        res = (feeder, x, y, r, part[0])
        parts.append(res)

        if feeder == ignore_value:
            print(f"{Fore.CYAN}\tSkipping part {part[0]}, {x}, {y}, {r}, {Style.RESET_ALL}")
            continue

        # print the data
        print(f"{Fore.YELLOW}\t{feeder}, {x}, {y}, {r}, {part[0]}{Style.RESET_ALL}")
        part_count += 1

    # set the amount of parts
    out.write(str(part_count) + "\n")

    parts.sort(key=lambda p : p[0])

    # write the parts
    for part in parts:
        if part[0] == ignore_value:
            continue

        for i in range(len(part)):
            out.write(str(part[i]))

            if i + 1 < len(part):
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
    parser.add_argument("-r", "--rotate", help="Rotate the part by 90 degrees", action="store_true", required=False)
    parser.add_argument("-ref1", type=str, help="Reference 1 \"X,Y\" coordinate", required=False)
    parser.add_argument("-ref2", type=str, help="Reference 2 \"X,Y\" coordinate", required=False)

    # parse the arguments
    args = parser.parse_args()

    # split the reference into x and y
    ref = args.ref.split(",")
    
    error = False

    references = [args.ref, args.ref1, args.ref2]
    reference_points = []

    for ref in references:
        if ref is None:
            break

        ref_split = ref.split(",")
        if len(ref_split) != 2:
            print(f"{Fore.RED}Invalid reference point. Use \"X,Y\" for the reference{Style.RESET_ALL}")
            error = True
            break

        try:
            reference_points.append(coordinate(float(ref_split[0]), float(ref_split[1])))
        except ValueError:
            print(f"{Fore.RED}Invalid reference point. Use \"X,Y\" for the reference{Style.RESET_ALL}")
            error = True
            break

    if len(reference_points) == 0:
        print(f"{Fore.RED}No reference points found. Use \"X,Y\" for the reference{Style.RESET_ALL}")
    elif error:
        print(f"{Fore.RED}Exiting due to errors{Style.RESET_ALL}")
    else:
        generate(reference_points, args.input_file, args.output_file, args.rotate)


