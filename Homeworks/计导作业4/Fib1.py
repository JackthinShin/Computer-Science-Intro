import time
def fibonacci(n):
    if n<=1:
        return n
    return fibonacci(n-1)+fibonacci(n-2)
start=time.time()
for i in range(1, 51):
    result=fibonacci(i)
    print(f"F({i:d})={result}\n", end="")
end=time.time()
print(f"F(50)={fibonacci(50)}")
print(f"Time:{(end-start):.4f}\n")
