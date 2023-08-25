#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>

#define PAGE_SIZE 4096
#define MEM_SIZE (1ul << 30)     //1GB
#define STEP_SIZE (100ul << 20)  //100MB

int main() {
    char *mem = mmap(NULL, MEM_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0); // 가상 메모리 공간 할당
    if (mem == MAP_FAILED) {
        perror("mmap failed");
        exit(EXIT_FAILURE);
    }
    size_t step_offset = 0;
    size_t touched_size = 0;

    while (touched_size < MEM_SIZE) {
        memset(mem + step_offset, 0, STEP_SIZE); // 메모리 초기화
        touched_size += STEP_SIZE; //  터치 사이즈 업데이트 , 현재까지 터치한 메모리 출력

        printf("Touched %lu MB\n", touched_size >> 20); // 20비트만큼 시프트 : MB로 표현

        if (touched_size < MEM_SIZE) {
            printf("Press enter to continue to next step...");
            getchar();
        } // 전체 할당이 이루어지지 않으면 계속 할당

        step_offset += STEP_SIZE;
    }

    if (munmap(mem, MEM_SIZE) == -1) {
        perror("munmap failed");
        exit(EXIT_FAILURE); // 할당한 메모리 해제
    }
    return 0;
}
