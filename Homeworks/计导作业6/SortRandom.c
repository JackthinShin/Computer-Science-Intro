#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void bubble_sort(int a[], int n) {
    int i, j, temp;
    for (i = 0; i < n-1; i++) {
        for (j = 0; j < n-i-1; j++) {
            if (a[j] > a[j+1]) {
                temp = a[j];
                a[j] = a[j+1];
                a[j+1] = temp;
            }
        }
    }
}

void quick_sort(int a[], int low, int high) {
    if (low < high) {
        int pivot = a[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (a[j] < pivot) {
                i++;
                int temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }
        int temp = a[i + 1];
        a[i + 1] = a[high];
        a[high] = temp;
        int pi = i + 1;
        quick_sort(a, low, pi - 1);
        quick_sort(a, pi + 1, high);
    }
}

int main() {
    int a[100001] = {0};
    srand(time(NULL));
    for (int i = 0; i < 100000; i++) {
        a[i] = rand() % 1000000;
    }
    clock_t start, end;
    start = clock();
    bubble_sort(a, 100000);

    end = clock();
    double T = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Bubble Sort Time: %f seconds\n", T);

    for (int i = 0; i < 100001; i++) {
        a[i] = rand() % 1000000;
    }

    start = clock();
    quick_sort(a, 0, 99999);
    end = clock();
    T = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Quick Sort Time: %f seconds\n", T);

    return 0;
}