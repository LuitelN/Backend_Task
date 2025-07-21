def find_pair(nums, target):
    seen = set()
    for num in nums:
        complement = target - num 
        if complement in seen: 
            print(f"Pair found ({complement}, {num})")
            return 
        seen.add(num)
    print("Pair not found.")

find_pair([8,7,2,5,3,1], 10)
find_pair([5,2,6,8,1,9], 12)
