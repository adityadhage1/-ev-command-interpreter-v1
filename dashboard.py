import matplotlib.pyplot as plt

vehicles = ["Tesla", "Tata", "MG"]
range_km = [500, 312, 461]

plt.style.use("dark_background")

plt.bar(vehicles, range_km)

plt.title("EV Range Comparison")
plt.xlabel("Vehicle")
plt.ylabel("Range (km)")

plt.show()