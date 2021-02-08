from time import sleep
unsorted_list = [20, 15, 24, 74, 35, 100, 19, 21, 4]

print(f"The current unsorted list is {unsorted_list}")
input()
swapped = True
passes = 0

while swapped:
    swapped = False 
    passes += 1
    for i in range(len(unsorted_list) - passes):
        print(f"Checking if {unsorted_list[i]} is smaller than {unsorted_list[i+1]}\n")
        if unsorted_list[i] > unsorted_list[i + 1]:
            print(f"Switching {unsorted_list[i]} and {unsorted_list[i+1]}\n")
            unsorted_list[i], unsorted_list[i+1] = unsorted_list[i+1], unsorted_list[i]
            swapped = True

        print()
        print(unsorted_list)
        input()

print(f"The final sorted list is {unsorted_list}")