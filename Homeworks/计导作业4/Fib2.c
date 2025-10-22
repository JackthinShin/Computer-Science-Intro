#include <stdio.h>
#include <time.h>

long fibonacci(int n){
    long a=1,b=1;
    for(int i=1;i<n;i++){
        long c=a+b;
        a=b;
        b=c;
    }
    return b;
}
int main(){
    clock_t start,end; 
    start=clock();
    for(int i=0;i<50;i++){
        printf("F(%d)=%ld\n",i+1,fibonacci(i));
    }
    printf("F(50)=%ld\n",fibonacci(49));
    end=clock();
    printf("Time:%f\n",(double)(end-start)/CLOCKS_PER_SEC);
    return 0;
}