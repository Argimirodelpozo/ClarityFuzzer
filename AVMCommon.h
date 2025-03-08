#include <vector>
#include <map>
#include <string>

#define STACK_MAX_SIZE 1000

using namespace std;


//A value in the stack
struct StackValue
{
    vector<uint8_t> byteslice;
    uint64_t value;

    StackValue(){}
    StackValue(uint64_t i):value(i){}
    //que hacia esto en terminos de memoria? es un buen caso para move semantics?
    StackValue(vector<uint8_t> b):byteslice(b){}
};


//General blockchain state to provide a fuzzing context
struct BlockchainState
{
    //accounts (balances, ASA, local storage, global storage)
    //global storage (std::map)

    std::map<string, StackValue> app_global;
    
};


struct Stack
{
    uint32_t currentTop = 0;
    StackValue stack[1000];

    inline StackValue& pop(){return stack[currentTop--];}
    inline StackValue& get(int i){return stack[currentTop+i];}
    inline StackValue& top(){return get(0);} 
    inline void push(StackValue& v){stack[currentTop++] = v;}
    inline void push(uint64_t i){stack[currentTop++] = StackValue(i);}
};


struct EvalContext
{
    Stack s; 
    StackValue sp[256];  //scratchspace

    //Este se toca una sola vez y no cambia por ejecucion (en tamanio maximo)
    //Se puede directamente saber cual es el maximo que va a ocupar
    //  y metagenerarlo como optimizacion.
    vector<StackValue> ApplicationArgs;

    //Por ahora. TODO: ver si lo podemos predecir con tamanio estatico
    vector<int> CallsubStack;

    //replace intcblock and bytecblock here

    // struct st_txn{

    //     //Array properties
    //     StackValue applicationArgs[10];
    // }txn;
};


struct txn
{
    
};