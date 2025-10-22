import time
def fib1(n):
    if n<=1:
        return n
    return fib1(n-1)+fib1(n-2)
def fib2(n):
    if n<=1:
        return n
    a,b=0,1
    for i in range(2,n+1):
        a,b=b,a+b
    return b
print("方法1:")
start1=time.time()
for i in range(1,51):
    r1=fib1(i)
    print(f"F({i:d})={r1}")
t1=time.time()-start1
print(f"递归时间: {t1:.4f}秒")
print("方法2:")
start2=time.time()
for i in range(1,51):
    r2=fib2(i)
    print(f"F({i:d})={r2}")
t2=time.time()-start2
print(f"迭代时间: {t2:.4f}秒")
