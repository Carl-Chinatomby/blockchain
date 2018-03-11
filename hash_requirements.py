from hashlib import sha256


x = 5
y = 0 # we don't know what y should be yet...


still_processing = True
while still_processing:
    product = float(x*y)
    current_hash = sha256('{}'.format(product).encode()).hexdigest()
    if current_hash[-1] != '0':
        print(current_hash, y)
        y += 1
    else:
        print(current_hash, y)
        still_processing = False

print('The solution to y = {}'.format(y))
