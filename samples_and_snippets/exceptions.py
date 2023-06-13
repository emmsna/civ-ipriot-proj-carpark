total_spaces = 125
car_count = -1
car_tracking = total_spaces - sum(car_count)

parking_spaces = total_spaces - car_count
if parking_spaces < 0:
    parking_spaces = 0
elif parking_spaces > total_spaces:
    parking_spaces = total_spaces

print(parking_spaces)