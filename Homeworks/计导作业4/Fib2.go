package main
import "fmt"
import "time"
func fibonacci(n int)int{
    if n<=1{
        return n
    }
    prev,curr:=0,1
    for i:=2;i<=n;i++{
        prev,curr=curr,prev+curr
    }
    return curr
}

func main(){
    start:=time.Now()
    for i:=1;i<=50;i++{
        result:=fibonacci(i)
        fmt.Printf("F(%d)=%d\n",i,result)
    }
    fmt.Printf("F(50)=%d\n",fibonacci(50))
    t:=time.Since(start)
    fmt.Printf("Time: %v\n",t)
}