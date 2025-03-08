#include "AVMCommon.h"

inline void pushint(Stack& s, uint64_t value)
{
    s.push(value);
}

inline void bool_and(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic

    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    s.push(bool(v1.value) == bool(v2.value));
}

inline void bool_or(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic

    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    s.push(bool(v1.value) || bool(v2.value));
}

inline void bool_eq(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic

    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    if(v1.value == v2.value) s.push(1);
    else s.push(0);
}

inline void bool_neq(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic

    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    if(v1.value != v2.value) s.push(1);
    else s.push(0);
}

inline void bool_lt(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic

    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    if(v1.value < v2.value) s.push(1);
    else s.push(0);
}

inline void bool_gt(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic
    
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    if(v1.value < v2.value) s.push(1);
    else s.push(0);
}

inline void bool_leq(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic
    
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    if(v1.value <= v2.value) s.push(1);
    else s.push(0);
}

inline void bool_geq(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic
    
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    if(v1.value >= v2.value) s.push(1);
    else s.push(0);
}

inline void add(Stack& s)
{
    if (s.get(0).byteslice.size() || s.get(1).byteslice.size()) 
        return; //HERE we need to panic
    
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();
    s.push(v1.value+v2.value);
}

inline void sub(Stack& s)
{
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();

    if (v1.byteslice.size() || v2.byteslice.size()) 
        return; //HERE we need to panic

    if (v1.value > v2.value) 
        return; //HERE we need to panic (underflow)
    
    s.push(v1.value-v2.value);
}

inline void mul(Stack& s)
{
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();

    if (v1.byteslice.size() || v2.byteslice.size()) 
        return; //HERE we need to panic
    
    s.push(v1.value*v2.value);
}

inline void mod(Stack& s)
{
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();

    if (v1.byteslice.size() || v2.byteslice.size()) 
        return; //HERE we need to panic
    
    s.push(v1.value%v2.value);
}

inline void div(Stack& s)
{
    StackValue v1 = s.pop();
    StackValue v2 = s.pop();

    if (v2.byteslice.size() || v2.byteslice.size()) 
        return; //HERE we need to panic

    if (v2.value == 0)
        return; //HERE we need to panic
    
    s.push(v1.value/v2.value);
}

inline void btoi(Stack& s)
{
    StackValue v1 = s.pop();
    uint64_t value =  (uint64_t)(v1.byteslice[0]) |
   (uint64_t)(v1.byteslice[1]) << 8  |
   (uint64_t)(v1.byteslice[2]) << 16 |
   (uint64_t)(v1.byteslice[3]) << 24 |
   (uint64_t)(v1.byteslice[4]) << 32 |
   (uint64_t)(v1.byteslice[5]) << 40 |
   (uint64_t)(v1.byteslice[6]) << 48 |
   (uint64_t)(v1.byteslice[7]) << 56;

   s.push(value);
}

inline void load(Stack& s, uint64_t val)
{   
    s.push(ctx.sp[val]);
}

inline void store(Stack& s, uint64_t val)
{   
    StackValue v1 = s.pop();
    ctx.sp[val] = v1;
}

inline void avm_assert(Stack& s)
{
    StackValue v1 = s.pop();
    if (v1.value == 0)
        return; //HERE we need to panic (explicit assert violation)
}

inline void avm_log(Stack& s)
{
    StackValue v1 = s.pop();
    //TODO: save log as an additional output. Conditionally discard.
    // (for cases when it is completely irrelevant for the fuzzing targets)
}

inline void dup(Stack& s)
{
    s.push(s.get(0))
}

inline void err()
{
    return; //HERE we need to panic (explicit error call)
}

inline void pushbytes(Stack& s, string bytes)
{
    //TODO: convert string to byte array
    //TODO: alternative version that takes explicit bytearray

    StackValue v1;
    v1.bytes = bytes;
    s.push(v1);
}

inline void txna_ApplicationArgs(Stack& s, int n)
{
    s.push(txn.ApplicationArgs[n]);
}

inline void app_global_put(Stack& s)
{
    //TODO impl
}

inline void app_global_get(Stack& s)
{
    //TODO impl
}

inline void len(Stack& s)
{
    
}