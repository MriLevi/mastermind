import time
program_start = time.time()
for i in range(10000):
    exec(open("./mastermind.py").read())
program_end = time.time()

with open('results.txt', 'r+') as f:
    lines = [int(x) for x in f.read().split()]
    avg = sum(lines) / len(lines)
    f.close()
print(f'10000 tests of Algorithm 3')
print(f'Average tries was {avg}. Program took {program_end - program_start} seconds to run. We took {round(int(program_end - program_start), 4) / len(lines)} seconds per try.')