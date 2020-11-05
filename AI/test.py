cans_hash = "01203040"
cans = list()
for i in range(0,len(cans_hash),4):
    cans.append((int(cans_hash[i:i+2]), int(cans_hash[i+2:i+4])))

print(cans)

hash_val = "0120022010203040"
robot_hash = hash_val[:4]
print((int(robot_hash[0:2]), int(robot_hash[2:4])))