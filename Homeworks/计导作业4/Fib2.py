import time
def fibonacci(n):
    if n<=1:
        return n
    a,b=0,1
    for i in range(2, n + 1):
        a,b=b,a+b
    return b
start=time.time()
for i in range(1, 51):
    result=fibonacci(i)
    print(f"F({i:d})={result}\n", end="")
end=time.time()
print(f"F(50)={fibonacci(50)}")
print(f"Time:{(end-start):.4f}")
