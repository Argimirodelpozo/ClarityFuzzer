#include <vector>
#include <unordered_map>
#include <map>
#include <string>

using namespace std;

// TYPE DEFINITIONS
enum types{INT, UINT, BOOL, PRINCIPAL, BUFFER, STRING_ASCII, STRING_UTF8, LIST, };

struct principal
{
    string address;
};

struct clarity_type
{
    types type;

    int clar_int = 0;
    uint64_t clar_uint = 0;
    bool clar_bool = false;
    principal clar_principal;
    string clar_string_ascii;
    string clar_string_utf8;
    vector<clarity_type> clar_list;
    std::map<string, clarity_type> clar_tuple;
};


// hold user account data (deployed contracts, balance in different tokens)
struct account_data
{
    //deployed contracts (as a list of function pointers?)
    //token-balance pairs
};

//General blockchain state to provide a fuzzing context
struct BlockchainState
{
    unordered_map<principal, account_data> accountData;

    //que mas hay en estado que nos sirva?
    //por ejemplo last timestamp, block height, etc.
};


struct ContractEvaluationContext
{
    //TODO: how does the context of a contract work?
    //delta
};


struct txn
{
    //TODO: what are fields of a transaction?
};