import matplotlib.pyplot as plt

# credit: https://vectorlinux.com/de-casteljau-algorithm-python/
def de_casteljau(control_points, t):
    if len(control_points) == 1:
        return control_points[0]
    else:
        new_points = []
        for i in range(len(control_points) - 1):
            new_point = (1 - t) * control_points[i] + t * control_points[i + 1]
            new_points.append(new_point)
    return de_casteljau(new_points, t)

def bezier(points_x, points_y, depth):
    calculated_points = []
    for t in [i / (depth - 1) for i in range(depth)]:
        x = de_casteljau(points_x, t)
        y = de_casteljau(points_y, t)
        calculated_points.append((x, y))
    return calculated_points

res = (bezier([0, 1, 2, 3], [0, -2, 2, 0], 100))


def plot_points(points, title="Punkte im Koordinatensystem"):
    """
    Zeichnet Punkte in ein Koordinatensystem.

    :param points: Liste von Punkten [(x1, y1), (x2, y2), ...].
    :param title: Titel der Grafik.
    """
    x, y = zip(*points)  # Punkte in x- und y-Koordinaten zerlegen
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, color='blue', label='Punkte')
    plt.axhline(0, color='black', linewidth=0.8)  # x-Achse
    plt.axvline(0, color='black', linewidth=0.8)  # y-Achse
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    plt.title(title)
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.legend()
    plt.show()

plot_points(res, "test_plot")