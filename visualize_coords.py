import sys
import matplotlib.pyplot as plt

def read_coords(filename):
    xs, ys = [], []
    with open(filename) as f:
        for idx, line in enumerate(f, 1):
            # Skip lines 1-22 and 26-28
            if 1 <= idx <= 22 or 26 <= idx <= 28:
                continue
            line = line.strip()
            if not line or ',' not in line:
                continue
            try:
                parts = line.split(',')
                if len(parts) == 5:
                    # Use only the second and third items as x, y
                    x = float(parts[1])
                    y = float(parts[2])
                else:
                    x, y = map(float, parts[:2])
                xs.append(x)
                ys.append(y)
            except ValueError:
                continue
    return xs, ys

# Read both files
x1, y1 = read_coords(sys.argv[1])

plt.figure(figsize=(10, 8))

# Plot first 3 points in red
plt.scatter(x1[:3], y1[:3], color='red', label='reference points', s=10, zorder=5)

# Plot only the second and third items in blue
plt.scatter(x1[3:], y1[3:], color='blue', label='smd', s=10)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Pinball Top Coordinates Comparison')
plt.legend()
plt.grid(True)

# if we have more than 1 argument, save the figure to the second argument
if len(sys.argv) > 2:
    plt.savefig(sys.argv[2])
else:
    plt.show()
