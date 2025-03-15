#include "ClarityCommon.h"
#include "opcodeDefinitions.cpp"
#include <stdio.h>
#include <stdlib.h>
// #include <unistd.h>
#include <signal.h>
#include <string.h>
#include <limits.h>

/* this lets the source compile without afl-clang-fast/lto */
#ifndef __AFL_FUZZ_TESTCASE_LEN
  ssize_t       fuzz_len;
  unsigned char fuzz_buf[1024000];

  #define __AFL_FUZZ_TESTCASE_LEN fuzz_len
  #define __AFL_FUZZ_TESTCASE_BUF fuzz_buf
  #define __AFL_FUZZ_INIT() void sync(void);
  #define __AFL_LOOP(x) \
    ((fuzz_len = read(0, fuzz_buf, sizeof(fuzz_buf))) > 0 ? 1 : 0)
  #define __AFL_INIT() sync()
#endif


__AFL_FUZZ_INIT();


/* To ensure checks are not optimized out it is recommended to disable
   code optimization for the fuzzer harness main() */
#pragma clang optimize off
#pragma GCC optimize("O0")




void contract_call()
{
  //Prepare state
  BlockchainState St;
  //fuzz blockchain state here (when applicable)
  //fuzz context here (when applicable)

  //prepare arguments
  //execute contract
}




int main(int argc, char **argv) 
{
  ssize_t        len;                        /* how much input did we read? */
  unsigned char *buf;                        /* test case buffer pointer    */

#ifdef __AFL_HAVE_MANUAL_CONTROL
  __AFL_INIT();
#endif
  buf = __AFL_FUZZ_TESTCASE_BUF;  // this must be assigned before __AFL_LOOP!


  while (__AFL_LOOP(UINT_MAX)) 
  {
    len = __AFL_FUZZ_TESTCASE_LEN;  // do not use the macro directly in a call!

    /*** PLACEHOLDER CODE ***/

    /* STEP 1: Fully re-initialize all critical variables. In our example, this
               involves zeroing buf[], our input buffer. */

    memset(buf, 0, 100);


    /* STEP 2: Read input data. When reading from stdin, no special preparation
               is required. When reading from a named file, you need to close
               the old descriptor and reopen the file first!

               Beware of reading from buffered FILE* objects such as stdin. Use
               raw file descriptors or call fopen() / fdopen() in every pass. */

    len = read(0, buf, 100);

    //TODO: special function to prepare input goes here
    contract_call();
  }

  return 0;
}




// TO COMPILE RUN 
//    afl-clang-fast -o fuzz_target ClarityFuzzer.cpp -lstdc++
// in WSL

// TO RUN
//    afl-fuzz -i seeds -o out -- ./fuzz_target
// in WSL