#Importing the required libraries
import os 
import time
import collections 

os.system("clear") #clear the console
from datetime import datetime
from collections import Counter
counter = Counter

#Print current time
Currenttime = datetime.now()
print("Current time: ", Currenttime.strftime("%H:%M:%S"))

# record start time
start = time.time()

def MinWindow(s:str, t:str) -> str:
    # Function takes two strings and returns the minimum window substring
    if not s or not t:
        return ""
    #count  characters of t
    t_count = Counter(t)

    required = len(counter(t))
    #slidding window pointers
    left, right = 0, 0
    formed = 0
    window_counts = {}

    #Result tuple: (Window length, left pointer, right pointer)
    ans = float("inf"), None, None

    while right < len(s):
        #add character from right pointer to window
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        #check if the current character is part of t
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1

        #try to contract the window till the point it ceases to be 'desirable'
        while left <= right and formed == required:
            char = s[left]

            #save the smallest window and update the result
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)

            #remove the leftmost character from the window
            window_counts[char] -= 1
            if char in t_count and window_counts[char] < t_count[char]:
                formed -= 1

            #move left pointer ahead
            left += 1

        #keep expanding the right pointer
        right += 1
    #return the smallest window
    return "" if ans[0] == float("inf") else s[ans[1]: ans[2] + 1]
#record end time
end = time.time()

#Example usage
s = "Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Only Reflecting Giants Stand Erect In Orbit, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel, Amidst the silver mist that drapes the rolling meadows at dawn, wind-carved oaks stand sentinel,"
t = "ORGSEI"
print("Minimum window substring is:", MinWindow(s, t))

# print the difference between start in ms
print("Programme executed in:",
    (end-start) * 10**3, "ms")          
