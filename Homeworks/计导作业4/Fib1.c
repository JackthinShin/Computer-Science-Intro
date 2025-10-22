#include <stdio.h>
#include <time.h>

long fibonacci(int n){
    if(n<=1) return 1;
    else return fibonacci(n-2)+fibonacci(n-1);
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