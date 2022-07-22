with open('test2.log', 'r') as file:
    lines = file.readlines()

avg_fitness = []
best_fitness = []

for line in lines:
    if 'average fitness value' in line:
        avg_fitness.append(float(line.split(' ')[-1]))
    if 'most fit' in line:
        best_fitness.append(float(line.split(' ')[-1]))

print(avg_fitness)
print(best_fitness)

import matplotlib.pyplot as plt

plt.plot(avg_fitness, label='average fitness')
plt.legend()
plt.show()

plt.close()
plt.plot(best_fitness, label='best fitness')
plt.legend()
plt.show()